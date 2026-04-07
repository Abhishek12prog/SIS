from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from datetime import datetime, timedelta
import os
import json
import math
import random
from urllib.parse import urlparse

# ================= SEMESTER LOGIC =================
def calculate_semester(joining_year, course_type):
    now = datetime.now()
    current_year = now.year
    month = now.month

    year_diff = current_year - joining_year

    if year_diff < 0:
        return 1

    if month >= 7:
        sem = year_diff * 2 + 1
    else:
        sem = year_diff * 2 + 2

    if course_type == "BTECH":
        return min(max(sem, 1), 8)
    else:
        return min(max(sem, 1), 6)

# ================= FLASK APP =================
app = Flask(__name__, template_folder='templates')
app.secret_key = os.getenv("SECRET_KEY", "fallback_key")

# ================= DATABASE FUNCTION =================
def get_db_connection():
    try:
        mysql_url = os.getenv("MYSQL_URL")

        # 👉 Production (Render + Railway)
        if mysql_url:
            parsed = urlparse(mysql_url)

            return mysql.connector.connect(
                host=parsed.hostname,
                user=parsed.username,
                password=parsed.password,
                database=parsed.path.lstrip('/'),
                port=parsed.port
            )

        # 👉 Local (Laptop)
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="abhishek",
            database="college_db"
        )

    except Exception as e:
        print("DATABASE CONNECTION ERROR:", e)
        return None


def ensure_faculty_feature_tables():
    db = get_db_connection()
    if db is None:
        return

    cur = db.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS faculty_schedule (
            id INT NOT NULL AUTO_INCREMENT,
            faculty_id INT NOT NULL,
            title VARCHAR(120) NOT NULL,
            day_name VARCHAR(20) NOT NULL,
            start_time VARCHAR(20) NOT NULL,
            end_time VARCHAR(20) NOT NULL,
            location VARCHAR(120) DEFAULT NULL,
            availability_note VARCHAR(255) DEFAULT NULL,
            created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (id),
            KEY faculty_id (faculty_id),
            CONSTRAINT faculty_schedule_ibfk_1
                FOREIGN KEY (faculty_id) REFERENCES admin (admin_id)
                ON DELETE CASCADE
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS faculty_meeting_requests (
            id INT NOT NULL AUTO_INCREMENT,
            student_id INT NOT NULL,
            faculty_id INT NOT NULL,
            request_message TEXT NOT NULL,
            preferred_slot VARCHAR(120) DEFAULT NULL,
            status VARCHAR(20) DEFAULT 'Pending',
            faculty_response VARCHAR(255) DEFAULT NULL,
            created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP
                ON UPDATE CURRENT_TIMESTAMP,
            PRIMARY KEY (id),
            KEY student_id (student_id),
            KEY faculty_id (faculty_id),
            CONSTRAINT faculty_meeting_requests_ibfk_1
                FOREIGN KEY (student_id) REFERENCES students (student_id)
                ON DELETE CASCADE,
            CONSTRAINT faculty_meeting_requests_ibfk_2
                FOREIGN KEY (faculty_id) REFERENCES admin (admin_id)
                ON DELETE CASCADE
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS faculty_chat_messages (
            id INT NOT NULL AUTO_INCREMENT,
            student_id INT NOT NULL,
            faculty_id INT NOT NULL,
            sender_role VARCHAR(20) NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (id),
            KEY student_id (student_id),
            KEY faculty_id (faculty_id),
            CONSTRAINT faculty_chat_messages_ibfk_1
                FOREIGN KEY (student_id) REFERENCES students (student_id)
                ON DELETE CASCADE,
            CONSTRAINT faculty_chat_messages_ibfk_2
                FOREIGN KEY (faculty_id) REFERENCES admin (admin_id)
                ON DELETE CASCADE
        )
    """)

    db.commit()
    cur.close()
    db.close()


def ensure_exam_seating_tables():
    db = get_db_connection()
    if db is None:
        return

    cur = db.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS classrooms (
            id INT NOT NULL AUTO_INCREMENT,
            room_number VARCHAR(50) NOT NULL,
            block_name VARCHAR(100) DEFAULT NULL,
            total_seats INT NOT NULL,
            columns_count INT DEFAULT 6,
            is_active TINYINT(1) DEFAULT 1,
            created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (id)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS exam_seating_plans (
            id INT NOT NULL AUTO_INCREMENT,
            exam_name VARCHAR(150) NOT NULL,
            subject_name VARCHAR(150) NOT NULL,
            exam_date DATE NOT NULL,
            exam_time VARCHAR(50) NOT NULL,
            strategy VARCHAR(50) NOT NULL,
            room_reveal_hours_before INT DEFAULT 12,
            seat_reveal_minutes_before INT DEFAULT 10,
            selected_groups_json LONGTEXT,
            room_ids_json LONGTEXT,
            created_by INT DEFAULT NULL,
            created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (id),
            KEY created_by (created_by),
            CONSTRAINT exam_seating_plans_ibfk_1
                FOREIGN KEY (created_by) REFERENCES admin (admin_id)
                ON DELETE SET NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS exam_seating_allocations (
            id INT NOT NULL AUTO_INCREMENT,
            plan_id INT NOT NULL,
            student_id INT NOT NULL,
            classroom_id INT NOT NULL,
            room_number VARCHAR(50) NOT NULL,
            seat_number INT NOT NULL,
            seat_label VARCHAR(20) NOT NULL,
            seat_row INT NOT NULL,
            seat_column INT NOT NULL,
            group_label VARCHAR(100) NOT NULL,
            ordering_value VARCHAR(120) DEFAULT NULL,
            room_visible_at DATETIME NOT NULL,
            seat_visible_at DATETIME NOT NULL,
            created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (id),
            KEY plan_id (plan_id),
            KEY student_id (student_id),
            KEY classroom_id (classroom_id),
            CONSTRAINT exam_seating_allocations_ibfk_1
                FOREIGN KEY (plan_id) REFERENCES exam_seating_plans (id)
                ON DELETE CASCADE,
            CONSTRAINT exam_seating_allocations_ibfk_2
                FOREIGN KEY (student_id) REFERENCES students (student_id)
                ON DELETE CASCADE,
            CONSTRAINT exam_seating_allocations_ibfk_3
                FOREIGN KEY (classroom_id) REFERENCES classrooms (id)
                ON DELETE CASCADE
        )
    """)

    db.commit()
    cur.close()
    db.close()


def get_logged_in_student():
    if 'student_id' not in session:
        return None

    db = get_db_connection()
    cur = db.cursor(dictionary=True)
    cur.execute("""
        SELECT student_id, name, branch, email
        FROM students
        WHERE student_id=%s
    """, (session['student_id'],))
    student = cur.fetchone()
    cur.close()
    db.close()
    return student


ensure_faculty_feature_tables()
ensure_exam_seating_tables()


DAY_ORDER_SQL = "FIELD(day_name, 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')"


def parse_exam_datetime(exam_date, exam_time):
    if exam_date is None or exam_time is None:
        return None

    time_value = str(exam_time).strip()
    date_value = str(exam_date)

    formats = [
        "%Y-%m-%d %I:%M %p",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d %I %p",
        "%Y-%m-%d %H"
    ]

    for fmt in formats:
        try:
            return datetime.strptime(f"{date_value} {time_value}", fmt)
        except ValueError:
            continue

    return None


def build_group_label(course_type, year, branch):
    parts = [course_type.upper(), f"Year {year}"]
    if branch and branch != "ALL":
        parts.append(branch.upper())
    return " - ".join(parts)


def get_students_for_group(cur, course_type, year, branch):
    if branch and branch != "ALL":
        cur.execute("""
            SELECT student_id, name, username, branch, year, course_type
            FROM students
            WHERE UPPER(course_type)=%s AND year=%s AND UPPER(branch)=%s
        """, (course_type.upper(), year, branch.upper()))
    else:
        cur.execute("""
            SELECT student_id, name, username, branch, year, course_type
            FROM students
            WHERE UPPER(course_type)=%s AND year=%s
        """, (course_type.upper(), year))
    return cur.fetchall()


def order_students(students, strategy):
    if strategy == 'alphabetical':
        return sorted(students, key=lambda item: ((item.get('name') or '').lower(), item['student_id']))
    if strategy == 'enrollment':
        return sorted(students, key=lambda item: ((item.get('username') or '').lower(), item['student_id']))
    if strategy == 'branch_shuffle':
        return sorted(students, key=lambda item: ((item.get('branch') or '').lower(), (item.get('name') or '').lower(), item['student_id']))
    return sorted(students, key=lambda item: item['student_id'])


def build_seat_positions(total_seats, columns_count):
    columns = max(columns_count or 6, 1)
    positions = []
    for seat_number in range(1, total_seats + 1):
        seat_row = ((seat_number - 1) // columns) + 1
        seat_column = ((seat_number - 1) % columns) + 1
        seat_label = str(seat_number)
        positions.append({
            'seat_number': seat_number,
            'seat_row': seat_row,
            'seat_column': seat_column,
            'seat_label': seat_label
        })

    alternate_first = [pos for pos in positions if (pos['seat_row'] + pos['seat_column']) % 2 == 0]
    alternate_second = [pos for pos in positions if (pos['seat_row'] + pos['seat_column']) % 2 == 1]
    return alternate_first + alternate_second


def interleave_grouped_students(grouped_students):
    working = {key: value[:] for key, value in grouped_students.items()}
    allocation = []

    while True:
        available = [key for key, value in working.items() if value]
        if not available:
            break

        available.sort(key=lambda key: len(working[key]), reverse=True)
        for key in available:
            if working[key]:
                allocation.append(working[key].pop(0))

    return allocation


def generate_seating_allocations(classrooms, grouped_students, exam_datetime, room_reveal_hours_before, seat_reveal_minutes_before):
    ordered_students = interleave_grouped_students(grouped_students)
    total_capacity = sum(room['total_seats'] for room in classrooms)

    if len(ordered_students) > total_capacity:
        return None, f"Not enough seats. Selected classrooms have {total_capacity} seats but {len(ordered_students)} students were chosen."

    room_visible_at = exam_datetime - timedelta(hours=room_reveal_hours_before)
    seat_visible_at = exam_datetime - timedelta(minutes=seat_reveal_minutes_before)

    allocations = []
    student_index = 0

    for room in classrooms:
        seat_positions = build_seat_positions(room['total_seats'], room.get('columns_count'))
        for position in seat_positions:
            if student_index >= len(ordered_students):
                break

            student = ordered_students[student_index]
            allocations.append({
                'student_id': student['student_id'],
                'classroom_id': room['id'],
                'room_number': room['room_number'],
                'seat_number': position['seat_number'],
                'seat_label': position['seat_label'],
                'seat_row': position['seat_row'],
                'seat_column': position['seat_column'],
                'group_label': student['group_label'],
                'ordering_value': student['ordering_value'],
                'room_visible_at': room_visible_at,
                'seat_visible_at': seat_visible_at
            })
            student_index += 1

    return allocations, None

# ======================================================
# ======================= HOME =========================
# ======================================================

@app.route('/')
def home():
    try:
        return render_template("choose_role.html")
    except Exception as e:
        return f"ERROR: {e}"

# ======================================================
# ======================= ADMIN ========================
# ======================================================

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        db = get_db_connection()
        cur = db.cursor()
        cur.execute(
            "SELECT * FROM admin WHERE username=%s AND password=%s",
            (request.form['username'], request.form['password'])
        )
        admin = cur.fetchone()
        cur.close()
        db.close()

        if admin:
            session['admin_id'] = admin[0]
            session['admin'] = admin[1]
            return redirect(url_for('admin_dashboard'))
        else:
            return "Invalid Admin Login"

    return render_template('admin_login.html')


@app.route('/admin')
def admin_dashboard():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    db = get_db_connection()
    cur = db.cursor()

    cur.execute("SELECT COUNT(*) FROM students")
    total_students = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM announcements")
    total_announcements = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM feedback")
    total_feedback = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM helpdesk")
    total_tickets = cur.fetchone()[0]

    cur.execute("SELECT branch, COUNT(*) FROM students GROUP BY branch")
    branch_data = cur.fetchall()

    cur.close()
    db.close()

    return render_template(
        'admin_dashboard.html',
        total_students=total_students,
        total_announcements=total_announcements,
        total_feedback=total_feedback,
        total_tickets=total_tickets,
        branch_data=branch_data
    )


@app.route('/faculty_portal')
def faculty_portal():
    if 'admin' not in session or 'admin_id' not in session:
        return redirect(url_for('admin_login'))

    db = get_db_connection()
    cur = db.cursor(dictionary=True)
    faculty_id = session['admin_id']
    selected_student_id = request.args.get('student_id', type=int)

    cur.execute("""
        SELECT id, title, day_name, start_time, end_time, location, availability_note
        FROM faculty_schedule
        WHERE faculty_id=%s
        ORDER BY FIELD(day_name, 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'),
                 start_time
    """, (faculty_id,))
    schedules = cur.fetchall()

    cur.execute("""
        SELECT r.id, r.student_id, s.name AS student_name, s.branch,
               r.request_message, r.preferred_slot, r.status,
               r.faculty_response, r.created_at
        FROM faculty_meeting_requests r
        JOIN students s ON s.student_id = r.student_id
        WHERE r.faculty_id=%s
        ORDER BY r.created_at DESC
    """, (faculty_id,))
    meeting_requests = cur.fetchall()

    cur.execute("""
        SELECT DISTINCT s.student_id, s.name, s.branch,
               MAX(m.created_at) AS last_message_at
        FROM faculty_chat_messages m
        JOIN students s ON s.student_id = m.student_id
        WHERE m.faculty_id=%s
        GROUP BY s.student_id, s.name, s.branch
        ORDER BY last_message_at DESC
    """, (faculty_id,))
    chat_students = cur.fetchall()

    if selected_student_id is None and chat_students:
        selected_student_id = chat_students[0]['student_id']

    selected_student = None
    chat_messages = []
    if selected_student_id:
        cur.execute("""
            SELECT student_id, name, branch, email
            FROM students
            WHERE student_id=%s
        """, (selected_student_id,))
        selected_student = cur.fetchone()

        cur.execute("""
            SELECT sender_role, message, created_at
            FROM faculty_chat_messages
            WHERE faculty_id=%s AND student_id=%s
            ORDER BY created_at ASC
        """, (faculty_id, selected_student_id))
        chat_messages = cur.fetchall()

    cur.close()
    db.close()

    return render_template(
        'admin_faculty_portal.html',
        schedules=schedules,
        meeting_requests=meeting_requests,
        chat_students=chat_students,
        selected_student=selected_student,
        chat_messages=chat_messages
    )


@app.route('/faculty_schedule/add', methods=['POST'])
def add_faculty_schedule():
    if 'admin' not in session or 'admin_id' not in session:
        return redirect(url_for('admin_login'))

    db = get_db_connection()
    cur = db.cursor()
    cur.execute("""
        INSERT INTO faculty_schedule
        (faculty_id, title, day_name, start_time, end_time, location, availability_note)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        session['admin_id'],
        request.form.get('title'),
        request.form.get('day_name'),
        request.form.get('start_time'),
        request.form.get('end_time'),
        request.form.get('location'),
        request.form.get('availability_note')
    ))
    db.commit()
    cur.close()
    db.close()

    return redirect(url_for('faculty_portal'))


@app.route('/faculty_schedule/delete/<int:schedule_id>')
def delete_faculty_schedule(schedule_id):
    if 'admin' not in session or 'admin_id' not in session:
        return redirect(url_for('admin_login'))

    db = get_db_connection()
    cur = db.cursor()
    cur.execute("""
        DELETE FROM faculty_schedule
        WHERE id=%s AND faculty_id=%s
    """, (schedule_id, session['admin_id']))
    db.commit()
    cur.close()
    db.close()

    return redirect(url_for('faculty_portal'))


@app.route('/faculty_request/<int:request_id>/<action>')
def update_faculty_request(request_id, action):
    if 'admin' not in session or 'admin_id' not in session:
        return redirect(url_for('admin_login'))

    if action not in ['approve', 'reject']:
        return redirect(url_for('faculty_portal'))

    status = 'Approved' if action == 'approve' else 'Rejected'
    faculty_response = request.args.get(
        'response',
        'Please come to the cabin during the approved slot.' if action == 'approve'
        else 'I am not available in that slot. Please send another request.'
    )

    db = get_db_connection()
    cur = db.cursor()
    cur.execute("""
        UPDATE faculty_meeting_requests
        SET status=%s, faculty_response=%s
        WHERE id=%s AND faculty_id=%s
    """, (status, faculty_response, request_id, session['admin_id']))
    db.commit()
    cur.close()
    db.close()

    return redirect(url_for('faculty_portal'))


@app.route('/faculty_chat/reply', methods=['POST'])
def faculty_chat_reply():
    if 'admin' not in session or 'admin_id' not in session:
        return redirect(url_for('admin_login'))

    student_id = request.form.get('student_id', type=int)
    message = request.form.get('message', '').strip()

    if not student_id or not message:
        return redirect(url_for('faculty_portal', student_id=student_id))

    db = get_db_connection()
    cur = db.cursor()
    cur.execute("""
        INSERT INTO faculty_chat_messages
        (student_id, faculty_id, sender_role, message)
        VALUES (%s, %s, %s, %s)
    """, (student_id, session['admin_id'], 'faculty', message))
    db.commit()
    cur.close()
    db.close()

    return redirect(url_for('faculty_portal', student_id=student_id))


@app.route('/students')
def students():
    try:
        if 'admin' not in session:
            return redirect(url_for('admin_login'))

        db = get_db_connection()

        if db is None:
            return "Database connection failed"

        search = request.args.get('search')

        cur = db.cursor()

        if search:
            query = """
                SELECT * FROM students 
                WHERE name LIKE %s OR username LIKE %s
            """
            value = f"%{search}%"
            cur.execute(query, (value, value))
        else:
            cur.execute("SELECT * FROM students")

        students = cur.fetchall()

        cur.close()
        db.close()

        return render_template('students.html', students=students)

    except Exception as e:
        return f"ERROR: {e}"

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():

    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        try:
            db = get_db_connection()
            cur = db.cursor()

            cur.execute("""
                INSERT INTO students 
                (name, email, branch, year, semester, course_type, phone, username, password)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                request.form['name'],
                request.form['email'],
                request.form['branch'],
                int(request.form['year']),          # ✅ changed
                int(request.form['semester']),      # ✅ added
                request.form['course_type'],
                request.form['phone'],              # ✅ added
                request.form['username'],
                request.form['password']
            ))

            db.commit()
            cur.close()
            db.close()

            return redirect(url_for('students'))

        except Exception as e:
            return f"Error: {e}"

    return render_template('add_student.html')


@app.route('/branches')
def branches():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    db = get_db_connection()
    cur = db.cursor()

    # Get unique branches from students table
    cur.execute("SELECT DISTINCT branch FROM students")
    branches = cur.fetchall()

    cur.close()
    db.close()

    return render_template('branches.html', branches=branches)

@app.route('/branch/<branch_name>')
def branch_students(branch_name):
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    
    db = get_db_connection()
    cur = db.cursor()

    cur.execute("SELECT * FROM students WHERE branch=%s", (branch_name,))
    students = cur.fetchall()

    cur.close()
    db.close()

    return render_template('branch_students.html', students=students, branch=branch_name)
@app.route('/edit_student/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    db = get_db_connection()
    cur = db.cursor()

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        branch = request.form.get('branch')
        username = request.form.get('username')   # ✅ FIX
        year = request.form.get('year')
        semester = request.form.get('semester')   # ✅ FIX
        course_type = request.form.get('course_type')
        phone = request.form.get('phone')

        print(request.form)   # 🔍 DEBUG

        cur.execute("""
            UPDATE students
            SET name=%s, email=%s, branch=%s, username=%s,
                year=%s, semester=%s, course_type=%s, phone=%s
            WHERE student_id=%s
        """, (
            name, email, branch, username,
            year, semester, course_type, phone,
            student_id
        ))

        db.commit()
        cur.close()
        db.close()

        return redirect(url_for('students'))

    # GET request
    cur.execute("SELECT * FROM students WHERE student_id=%s", (student_id,))
    student = cur.fetchone()
    cur.close()

    return render_template('admin_edit_student.html', student=student)

@app.route('/delete_student/<int:student_id>')
def delete_student(student_id):
    if 'admin' not in session:
        return redirect(url_for('admin_login'))
    db = get_db_connection()
    cur = db.cursor()
    cur.execute("DELETE FROM students WHERE student_id=%s", (student_id,))
    db.commit()
    cur.close()
    db.close()

    return redirect(url_for('students'))

@app.route('/view_student/<int:student_id>')
def view_student(student_id):
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    db = get_db_connection()
    cur = db.cursor()
    cur.execute("SELECT * FROM students WHERE student_id=%s", (student_id,))
    student = cur.fetchone()
    cur.close()
    db.close()

    return render_template('admin_view_student.html', student=student)
# ================= DOCUMENTS =================
@app.route('/documents')
def documents():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    db = get_db_connection()
    cur = db.cursor()
    cur.execute("SELECT * FROM documents ORDER BY uploaded_at DESC")
    docs = cur.fetchall()
    cur.close()
    db.close()

    return render_template('admin_documents.html', docs=docs)


# ================= UPLOAD DATA =================
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/upload_data', methods=['GET', 'POST'])
def upload_data():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        title = request.form.get('title')
        file = request.files.get('file')

        if title and file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))


            db = get_db_connection()
            cur = db.cursor()
            cur.execute(
                "INSERT INTO documents (title, file_name) VALUES (%s, %s)",
                (title, filename)
            )
            db.commit()
            cur.close()
            db.close()

            return redirect(url_for('documents'))

        else:
            return "Please provide both title and file"

    return render_template('admin_upload.html')

@app.route('/admin_notice')
def admin_notice():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    db = get_db_connection()
    cur = db.cursor()
    cur.execute("SELECT * FROM notice ORDER BY created_at DESC")
    notices = cur.fetchall()
    cur.close()
    db.close()
    return render_template('admin_notice.html', notices=notices)

@app.route('/add_notice', methods=['GET', 'POST'])
def add_notice():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        file = request.files.get('file')

        filename = None
        if file and file.filename != "":
            filename = file.filename
            file.save("static/uploads/" + filename)

        db = get_db_connection()
        cur = db.cursor()
        cur.execute(
            "INSERT INTO notice (title, description, file_name) VALUES (%s, %s, %s)",
            (title, description, filename)
        )
        db.commit()
        cur.close()
        db.close()

        return redirect(url_for('admin_notice'))

    return render_template('admin_add_notice.html')

# ================= ANNOUNCEMENTS =================
@app.route('/announcements')
def announcements():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    db = get_db_connection()
    cur = db.cursor()
    cur.execute("SELECT * FROM announcements ORDER BY created_at DESC")
    announcements = cur.fetchall()
    cur.close()
    db.close()

    return render_template('admin_announcements.html', announcements=announcements)

# ================= REPORTS =================
@app.route('/reports')
def reports():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    return render_template('admin_reports.html')

@app.route('/admin_exams')
def admin_exams():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    db = get_db_connection()
    cur = db.cursor()
    cur.execute("SELECT * FROM exam_subjects ORDER BY exam_date")
    exams = cur.fetchall()
    cur.close()
    db.close()

    return render_template('admin_exams.html', exams=exams)

@app.route('/add_exam', methods=['GET', 'POST'])
def add_exam():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        student_id = request.form.get('student_id')
        subject = request.form.get('subject')
        date = request.form.get('date')
        time = request.form.get('time')

        db = get_db_connection()
        cur = db.cursor()
        cur.execute("""
            INSERT INTO exam_subjects (student_id, subject_name, exam_date, exam_time)
            VALUES (%s, %s, %s, %s)
        """, (student_id, subject, date, time))

        db.commit()
        cur.close()
        db.close()

        return redirect(url_for('admin_exams'))

    return render_template('admin_add_exam.html')


# ================= ADMIN HELP DESK =================
@app.route('/admin_helpdesk')
def admin_helpdesk():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    db = get_db_connection()
    cur = db.cursor()
    cur.execute("""
        SELECT helpdesk.id, students.name, helpdesk.subject,
               helpdesk.description, helpdesk.status, helpdesk.created_at
        FROM helpdesk
        JOIN students ON helpdesk.student_id = students.student_id
        ORDER BY helpdesk.created_at DESC
    """)
    tickets = cur.fetchall()
    cur.close()
    db.close()
    return render_template('admin_helpdesk.html', tickets=tickets)

# ================= VIEW FEEDBACK =================
@app.route('/view_feedback')
def view_feedback():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    db = get_db_connection()
    cur = db.cursor()
    cur.execute("""
        SELECT students.name, feedback.message, feedback.created_at
        FROM feedback
        JOIN students ON feedback.student_id = students.student_id
        ORDER BY feedback.created_at DESC
    """)
    feedbacks = cur.fetchall()
    cur.close()
    db.close()

    return render_template('admin_view_feedback.html', feedbacks=feedbacks)

# ================= ADD ANNOUNCEMENT =================
@app.route('/add_announcement', methods=['GET', 'POST'])
def add_announcement():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        title = request.form['title']
        message = request.form['message']

        db = get_db_connection()
        cur = db.cursor()
        cur.execute(
            "INSERT INTO announcements (title, message) VALUES (%s, %s)",
            (title, message)
        )
        db.commit()
        cur.close()
        db.close()

        return redirect(url_for('announcements'))

    return render_template('admin_add_announcement.html')
# -------------------SEATING ARRANGEMENT-------------------
@app.route('/seating', methods=['GET', 'POST'])
def seating():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    db = get_db_connection()
    cur = db.cursor(dictionary=True)
    generated_plan_id = None
    error_message = None

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'generate_plan':
            exam_name = request.form.get('exam_name', '').strip()
            subject_name = request.form.get('subject_name', '').strip()
            exam_date = request.form.get('exam_date')
            exam_time = request.form.get('exam_time', '').strip()
            strategy = request.form.get('strategy', 'alphabetical')
            room_reveal_hours_before = request.form.get('room_reveal_hours_before', type=int) or 12
            seat_reveal_minutes_before = request.form.get('seat_reveal_minutes_before', type=int) or 10
            selected_room_ids = request.form.getlist('room_ids')

            if not exam_name or not subject_name or not exam_date or not exam_time:
                error_message = "Please fill exam name, subject, date, and time."
            elif not selected_room_ids:
                error_message = "Please select at least one classroom."
            else:
                exam_datetime = parse_exam_datetime(exam_date, exam_time)
                if exam_datetime is None:
                    error_message = "Use exam time in '10:00 AM' or 24-hour format like '14:00'."
                else:
                    groups = []
                    grouped_students = {}

                    for index in range(1, 5):
                        course_type = request.form.get(f'course_type_{index}', '').strip()
                        year = request.form.get(f'year_{index}', type=int)
                        branch = request.form.get(f'branch_{index}', 'ALL').strip() or 'ALL'

                        if not course_type or not year:
                            continue

                        group_label = build_group_label(course_type, year, branch)
                        students = get_students_for_group(cur, course_type, year, branch)
                        ordered = order_students(students, strategy)

                        enriched_students = []
                        for student in ordered:
                            item = dict(student)
                            item['group_label'] = group_label
                            item['ordering_value'] = item.get('name') if strategy == 'alphabetical' else item.get('username')
                            enriched_students.append(item)

                        groups.append({
                            'course_type': course_type.upper(),
                            'year': year,
                            'branch': branch.upper(),
                            'group_label': group_label,
                            'student_count': len(enriched_students)
                        })
                        grouped_students[group_label] = enriched_students

                    if not groups:
                        error_message = "Please select at least one student group."
                    else:
                        placeholders = ','.join(['%s'] * len(selected_room_ids))
                        cur.execute(f"""
                            SELECT id, room_number, block_name, total_seats, columns_count
                            FROM classrooms
                            WHERE is_active=1 AND id IN ({placeholders})
                            ORDER BY room_number
                        """, tuple(selected_room_ids))
                        selected_rooms = cur.fetchall()

                        allocations, allocation_error = generate_seating_allocations(
                            selected_rooms,
                            grouped_students,
                            exam_datetime,
                            room_reveal_hours_before,
                            seat_reveal_minutes_before
                        )

                        if allocation_error:
                            error_message = allocation_error
                        else:
                            cur.execute("""
                                INSERT INTO exam_seating_plans
                                (exam_name, subject_name, exam_date, exam_time, strategy,
                                 room_reveal_hours_before, seat_reveal_minutes_before,
                                 selected_groups_json, room_ids_json, created_by)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            """, (
                                exam_name,
                                subject_name,
                                exam_date,
                                exam_time,
                                strategy,
                                room_reveal_hours_before,
                                seat_reveal_minutes_before,
                                json.dumps(groups),
                                json.dumps(selected_room_ids),
                                session.get('admin_id')
                            ))
                            generated_plan_id = cur.lastrowid

                            for allocation in allocations:
                                cur.execute("""
                                    INSERT INTO exam_seating_allocations
                                    (plan_id, student_id, classroom_id, room_number, seat_number, seat_label,
                                     seat_row, seat_column, group_label, ordering_value,
                                     room_visible_at, seat_visible_at)
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                """, (
                                    generated_plan_id,
                                    allocation['student_id'],
                                    allocation['classroom_id'],
                                    allocation['room_number'],
                                    allocation['seat_number'],
                                    allocation['seat_label'],
                                    allocation['seat_row'],
                                    allocation['seat_column'],
                                    allocation['group_label'],
                                    allocation['ordering_value'],
                                    allocation['room_visible_at'],
                                    allocation['seat_visible_at']
                                ))

                            db.commit()

    cur.execute("""
        SELECT id, room_number, block_name, total_seats, columns_count, is_active
        FROM classrooms
        ORDER BY room_number
    """)
    classrooms = cur.fetchall()

    cur.execute("""
        SELECT id, exam_name, subject_name, exam_date, exam_time, strategy, created_at
        FROM exam_seating_plans
        ORDER BY exam_date DESC, created_at DESC
    """)
    plans = cur.fetchall()

    plan_id = request.args.get('plan_id', type=int) or generated_plan_id
    selected_plan = None
    plan_allocations = []
    room_summary = []

    if plan_id:
        cur.execute("""
            SELECT id, exam_name, subject_name, exam_date, exam_time, strategy,
                   room_reveal_hours_before, seat_reveal_minutes_before,
                   selected_groups_json, room_ids_json, created_at
            FROM exam_seating_plans
            WHERE id=%s
        """, (plan_id,))
        selected_plan = cur.fetchone()

        if selected_plan:
            cur.execute("""
                SELECT a.room_number, a.seat_label, a.seat_number, a.group_label,
                       s.student_id, s.name, s.username, s.branch, s.course_type, s.year
                FROM exam_seating_allocations a
                JOIN students s ON s.student_id = a.student_id
                WHERE a.plan_id=%s
                ORDER BY a.room_number, a.seat_number
            """, (plan_id,))
            plan_allocations = cur.fetchall()

            cur.execute("""
                SELECT room_number, COUNT(*) AS allocated_students
                FROM exam_seating_allocations
                WHERE plan_id=%s
                GROUP BY room_number
                ORDER BY room_number
            """, (plan_id,))
            room_summary = cur.fetchall()

    cur.close()
    db.close()

    return render_template(
        'admin_seating.html',
        classrooms=classrooms,
        plans=plans,
        selected_plan=selected_plan,
        plan_allocations=plan_allocations,
        room_summary=room_summary,
        error_message=error_message
    )


@app.route('/classrooms/add', methods=['POST'])
def add_classroom():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    room_number = request.form.get('room_number', '').strip()
    block_name = request.form.get('block_name', '').strip()
    total_seats = request.form.get('total_seats', type=int)
    columns_count = request.form.get('columns_count', type=int) or 6

    if room_number and total_seats:
        db = get_db_connection()
        cur = db.cursor()
        cur.execute("""
            INSERT INTO classrooms (room_number, block_name, total_seats, columns_count)
            VALUES (%s, %s, %s, %s)
        """, (room_number, block_name or None, total_seats, columns_count))
        db.commit()
        cur.close()
        db.close()

    return redirect(url_for('seating'))


@app.route('/classrooms/delete/<int:classroom_id>')
def delete_classroom(classroom_id):
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    db = get_db_connection()
    cur = db.cursor()
    cur.execute("DELETE FROM classrooms WHERE id=%s", (classroom_id,))
    db.commit()
    cur.close()
    db.close()
    return redirect(url_for('seating'))


@app.route('/seating_plan/<int:plan_id>')
def seating_plan(plan_id):
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    return redirect(url_for('seating', plan_id=plan_id))

# ================= ADMIN LOGOUT =================
@app.route('/admin_logout')
def admin_logout():
    session.clear()
    return redirect(url_for('admin_login'))


# ======================================================
# ======================= STUDENT ======================
# ======================================================

@app.route('/student_login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        db = get_db_connection()
        cur = db.cursor()
        cur.execute("SELECT * FROM students WHERE username=%s AND password=%s",
                    (request.form['username'], request.form['password']))
        student = cur.fetchone()
        cur.close()
        db.close()

        if student:
            session['student_id'] = student[0]
            return redirect(url_for('student_dashboard'))
        else:
            return "Invalid Student Login"

    return render_template('student_login.html')


@app.route('/student')
def student_dashboard():
    if 'student_id' not in session:
        return redirect(url_for('student_login'))

    return render_template('base_student.html')


@app.route('/faculty_connect')
def faculty_connect():
    student = get_logged_in_student()
    if not student:
        return redirect(url_for('student_login'))

    db = get_db_connection()
    cur = db.cursor(dictionary=True)

    cur.execute("""
        SELECT a.admin_id, a.username,
               COUNT(fs.id) AS schedule_count
        FROM admin a
        LEFT JOIN faculty_schedule fs ON fs.faculty_id = a.admin_id
        GROUP BY a.admin_id, a.username
        ORDER BY a.username
    """)
    faculty_members = cur.fetchall()

    selected_faculty_id = request.args.get('faculty_id', type=int)
    if selected_faculty_id is None and faculty_members:
        selected_faculty_id = faculty_members[0]['admin_id']

    schedules = []
    requests_data = []
    chat_messages = []
    selected_faculty = None

    if selected_faculty_id:
        cur.execute("""
            SELECT admin_id, username
            FROM admin
            WHERE admin_id=%s
        """, (selected_faculty_id,))
        selected_faculty = cur.fetchone()

        cur.execute("""
            SELECT title, day_name, start_time, end_time, location, availability_note
            FROM faculty_schedule
            WHERE faculty_id=%s
            ORDER BY FIELD(day_name, 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'),
                     start_time
        """, (selected_faculty_id,))
        schedules = cur.fetchall()

        cur.execute("""
            SELECT id, request_message, preferred_slot, status,
                   faculty_response, created_at
            FROM faculty_meeting_requests
            WHERE student_id=%s AND faculty_id=%s
            ORDER BY created_at DESC
        """, (student['student_id'], selected_faculty_id))
        requests_data = cur.fetchall()

        cur.execute("""
            SELECT sender_role, message, created_at
            FROM faculty_chat_messages
            WHERE student_id=%s AND faculty_id=%s
            ORDER BY created_at ASC
        """, (student['student_id'], selected_faculty_id))
        chat_messages = cur.fetchall()

    cur.close()
    db.close()

    return render_template(
        'student_faculty_connect.html',
        student=student,
        faculty_members=faculty_members,
        selected_faculty=selected_faculty,
        schedules=schedules,
        meeting_requests=requests_data,
        chat_messages=chat_messages
    )


@app.route('/faculty_request_meeting', methods=['POST'])
def faculty_request_meeting():
    student = get_logged_in_student()
    if not student:
        return redirect(url_for('student_login'))

    faculty_id = request.form.get('faculty_id', type=int)
    request_message = request.form.get('request_message', '').strip()
    preferred_slot = request.form.get('preferred_slot', '').strip()

    if not faculty_id or not request_message:
        return redirect(url_for('faculty_connect', faculty_id=faculty_id))

    db = get_db_connection()
    cur = db.cursor()
    cur.execute("""
        INSERT INTO faculty_meeting_requests
        (student_id, faculty_id, request_message, preferred_slot)
        VALUES (%s, %s, %s, %s)
    """, (student['student_id'], faculty_id, request_message, preferred_slot or None))
    db.commit()
    cur.close()
    db.close()

    return redirect(url_for('faculty_connect', faculty_id=faculty_id))


@app.route('/faculty_chat/send', methods=['POST'])
def faculty_chat_send():
    student = get_logged_in_student()
    if not student:
        return redirect(url_for('student_login'))

    faculty_id = request.form.get('faculty_id', type=int)
    message = request.form.get('message', '').strip()

    if not faculty_id or not message:
        return redirect(url_for('faculty_connect', faculty_id=faculty_id))

    db = get_db_connection()
    cur = db.cursor()
    cur.execute("""
        INSERT INTO faculty_chat_messages
        (student_id, faculty_id, sender_role, message)
        VALUES (%s, %s, %s, %s)
    """, (student['student_id'], faculty_id, 'student', message))
    db.commit()
    cur.close()
    db.close()

    return redirect(url_for('faculty_connect', faculty_id=faculty_id))

@app.route('/notice_board')
def notice_board():
    if 'student_id' not in session:
        return redirect(url_for('student_login'))

    db = get_db_connection()
    cur = db.cursor()
    cur.execute("SELECT * FROM announcements ORDER BY created_at DESC")
    notices = cur.fetchall()
    cur.close()
    db.close()

    return render_template('student_notice.html', notices=notices)

@app.route('/view_notice/<int:id>')
def view_notice(id):
    if 'student_id' not in session:
        return redirect(url_for('student_login'))

    db = get_db_connection()
    cur = db.cursor()

    # Mark as viewed
    cur.execute("UPDATE announcements SET viewed=1 WHERE id=%s", (id,))
    db.commit()

    # Get file name
    cur.execute("SELECT file_name FROM announcements WHERE id=%s", (id,))
    file = cur.fetchone()[0]

    cur.close()
    db.close()

    return redirect(url_for('static', filename='uploads/' + file))

@app.route('/academics')
def academics():
    if 'student_id' not in session:
        return redirect(url_for('student_login'))

    db = get_db_connection()
    cur = db.cursor()
    cur.execute("""
        SELECT subject_name, internal_marks, external_marks, total_marks, semester
        FROM academics WHERE student_id=%s
    """, (session['student_id'],))
    records = cur.fetchall()
    cur.close()
    db.close()

    return render_template('student_academics.html', records=records)

@app.route('/student_announcements')
def student_announcements():
    if 'student_id' not in session:
        return redirect(url_for('student_login'))

    db = get_db_connection()
    cur = db.cursor()
    cur.execute("SELECT * FROM announcements ORDER BY created_at DESC")
    announcements = cur.fetchall()
    cur.close()
    db.close()
    

    return render_template('student_announcements.html', announcements=announcements)


@app.route('/student_notice')
def student_notice():
    if 'student_id' not in session:
        return redirect(url_for('student_login'))

    db = get_db_connection()
    cur = db.cursor()
    cur.execute("SELECT * FROM notice ORDER BY created_at DESC")
    notices = cur.fetchall()
    cur.close()
    db.close()

    return render_template('student_notice.html', notices=notices)


@app.route('/my_info')
def my_info():
    if 'student_id' not in session:
        return redirect(url_for('student_login'))

    db = get_db_connection()
    cur = db.cursor()
    cur.execute("SELECT * FROM students WHERE student_id=%s",
                (session['student_id'],))
    student = cur.fetchone()
    cur.close()
    db.close()

    return render_template('student_myinfo.html', student=student)


# ================= ACADEMICS SUB MODULES =================

@app.route('/registration')
def registration():
    return render_template('student_academics.html')


@app.route('/courses')
def courses():
    if 'student_id' not in session:
        return redirect(url_for('student_login'))

    db = get_db_connection()
    cur = db.cursor(dictionary=True)

    # ✅ Get student details (UPDATED)
    cur.execute("""
        SELECT branch, joining_year, course_type 
        FROM students WHERE student_id=%s
    """, (session['student_id'],))

    student = cur.fetchone()

    branch = student['branch']

    # ✅ Calculate semester (NEW LOGIC)
    sem = calculate_semester(
        student['joining_year'],
        student['course_type']
    )

    print("DEBUG -> Branch:", branch)
    print("DEBUG -> Semester:", sem)

    # ✅ CORE LOGIC (same but cleaner)
    if sem in [1, 2]:
        query_branch = 'ALL'
    else:
        query_branch = branch

    cur.execute("""
        SELECT subject_name 
        FROM subjects 
        WHERE branch=%s AND semester=%s
    """, (query_branch, sem))

    subjects = cur.fetchall()
    cur.close()
    db.close()

    return render_template(
        'student_courses.html',
        subjects=subjects,
        student=student,
        sem=sem   # ✅ pass sem to UI
    )

@app.route('/faculty')
def faculty():
    if 'student_id' not in session:
        return redirect(url_for('student_login'))

    return redirect(url_for('faculty_connect'))


@app.route('/attendance')
def attendance():
    return render_template('student_academics.html')


@app.route('/resources')
def resources():
    return render_template('student_resources.html')


@app.route('/mentor')
def mentor():
    return render_template('student_academics.html')


@app.route('/marks')
def marks():
    return render_template('student_academics.html')


@app.route('/grades')
def grades():
    return render_template('student_academics.html')

@app.route('/student_documents')
def student_documents():
    if 'student_id' not in session:
        return redirect(url_for('student_login'))

    db = get_db_connection()
    cur = db.cursor()
    cur.execute("SELECT * FROM documents ORDER BY uploaded_at DESC")
    docs = cur.fetchall()
    cur.close()
    db.close()

    return render_template('student_documents.html', docs=docs)

@app.route('/student_examinations')
def student_examinations():
    if 'student_id' not in session:
        return redirect(url_for('student_login'))

    db = get_db_connection()
    cur = db.cursor(dictionary=True)

    cur.execute("""
        SELECT e.subject_name, e.exam_date, e.exam_time,
               p.exam_name, a.room_number, a.seat_label,
               a.room_visible_at, a.seat_visible_at
        FROM exam_subjects e
        LEFT JOIN exam_seating_allocations a ON a.student_id = e.student_id
        LEFT JOIN exam_seating_plans p
            ON p.id = a.plan_id
           AND p.subject_name = e.subject_name
           AND p.exam_date = e.exam_date
           AND p.exam_time = e.exam_time
        WHERE e.student_id=%s
        GROUP BY e.subject_name, e.exam_date, e.exam_time, p.exam_name,
                 a.room_number, a.seat_label, a.room_visible_at, a.seat_visible_at
        ORDER BY e.exam_date, e.exam_time
    """, (session['student_id'],))

    exams = cur.fetchall()
    now = datetime.now()

    for exam in exams:
        exam['room_is_visible'] = bool(exam.get('room_visible_at') and now >= exam['room_visible_at'])
        exam['seat_is_visible'] = bool(exam.get('seat_visible_at') and now >= exam['seat_visible_at'])

    cur.close()
    db.close()

    return render_template('student_examinations.html', exams=exams)

# ================= OTHER STUDENT FEATURES =================

@app.route('/fees')
def fees():
    return render_template('student_fees.html')


@app.route('/feedback')
def feedback():
    return render_template('student_feedback.html')


@app.route('/helpdesk')
def helpdesk():
    return render_template('student_helpdesk.html')

@app.route('/hall_ticket')
def hall_ticket():
    if 'student_id' not in session:
        return redirect(url_for('student_login'))

    db = get_db_connection()
    cur = db.cursor()

    # Get student details
    cur.execute("SELECT name, branch FROM students WHERE student_id=%s",
                (session['student_id'],))
    student = cur.fetchone()

    # Get subjects (optional)
    cur.execute("""
        SELECT subject_name, exam_date, exam_time
        FROM exam_subjects WHERE student_id=%s
    """, (session['student_id'],))
    subjects = cur.fetchall()

    cur.close()
    db.close()

    return render_template(
        'student_hall_ticket.html',
        student=student,
        subjects=subjects
    )


@app.route('/change_password')
def change_password():
    return render_template('student_change_password.html')


@app.route('/student_logout')
def student_logout():
    session.clear()
    return redirect(url_for('student_login'))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
