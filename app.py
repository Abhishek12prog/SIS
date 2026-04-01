from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from datetime import datetime
import os
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
        db = get_db_connection()
        cur = db.cursor()

        cur.execute("""
            INSERT INTO students 
            (name, email, branch, username, password, joining_year, course_type)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            request.form['name'],
            request.form['email'],
            request.form['branch'],
            request.form['username'],
            request.form['password'],
            int(request.form['joining_year']),   # ✅ FIX
            request.form['course_type']
        ))

        db.commit()
        cur.close()
        db.close()

        return redirect(url_for('students'))

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

    if request.method == 'POST':

        type1 = request.form['type1']
        year1 = int(request.form['year1'])

        type2 = request.form['type2']
        year2 = int(request.form['year2'])

        rooms = int(request.form['rooms'])
        capacity = int(request.form['capacity'])
        db = get_db_connection()
        cur = db.cursor(dictionary=True)

        # Group 1
        cur.execute("""
            SELECT * FROM students
            WHERE course_type=%s AND year=%s
            ORDER BY student_id
        """, (type1, year1))
        group1 = cur.fetchall()

        # Group 2
        cur.execute("""
            SELECT * FROM students
            WHERE course_type=%s AND year=%s
            ORDER BY student_id
        """, (type2, year2))
        group2 = cur.fetchall()
        db.close()
        cur.close()

        seating = []
        i, j = 0, 0

        for r in range(rooms):
            room = []

            for b in range(capacity // 2):
                if i < len(group1) and j < len(group2):
                    room.append((group1[i], group2[j]))
                    i += 1
                    j += 1

            seating.append(room)

        return render_template(
            'admin_seating.html',
            seating=seating,
            info=f"{type1} Year {year1} + {type2} Year {year2}"
        )

    return render_template('admin_seating.html')

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
    return render_template('student_academics.html')


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
    cur = db.cursor()

    cur.execute("""
        SELECT subject_name, exam_date, exam_time
        FROM exam_subjects
        WHERE student_id=%s
    """, (session['student_id'],))

    exams = cur.fetchall()
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