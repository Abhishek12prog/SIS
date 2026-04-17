from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_file
import mysql.connector
from datetime import datetime, timedelta
import os
import json
import math
import random
from io import BytesIO
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

    cur.execute("""
        CREATE TABLE IF NOT EXISTS faculty_subject_assignments (
            id INT NOT NULL AUTO_INCREMENT,
            faculty_id INT NOT NULL,
            subject_name VARCHAR(150) NOT NULL,
            branch VARCHAR(50) NOT NULL,
            semester INT NOT NULL,
            course_type VARCHAR(20) DEFAULT NULL,
            created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (id),
            KEY faculty_id (faculty_id),
            CONSTRAINT faculty_subject_assignments_ibfk_1
                FOREIGN KEY (faculty_id) REFERENCES admin (admin_id)
                ON DELETE CASCADE
        )
    """)

    db.commit()
    cur.close()
    db.close()


def infer_course_type_for_branch(branch_name):
    branch_value = (branch_name or '').strip().upper()
    if branch_value in ['BCA', 'BSC']:
        return branch_value
    return 'BTECH'


def ensure_sample_faculty_and_assignments():
    db = get_db_connection()
    if db is None:
        return

    cur = db.cursor(dictionary=True)

    cur.execute("""
        SELECT admin_id, username
        FROM admin
        WHERE LOWER(username) != 'admin'
        ORDER BY admin_id
    """)
    faculty_rows = cur.fetchall()

    if not faculty_rows:
        sample_faculty = [
            ('faculty_cse', 'faculty123'),
            ('faculty_ece', 'faculty123'),
            ('faculty_bca', 'faculty123'),
            ('faculty_bsc', 'faculty123')
        ]
        insert_cur = db.cursor()
        for username, password in sample_faculty:
            insert_cur.execute("""
                INSERT INTO admin (username, password)
                SELECT %s, %s
                WHERE NOT EXISTS (
                    SELECT 1 FROM admin WHERE UPPER(username)=UPPER(%s)
                )
            """, (username, password, username))
        db.commit()
        insert_cur.close()

        cur.execute("""
            SELECT admin_id, username
            FROM admin
            WHERE LOWER(username) != 'admin'
            ORDER BY admin_id
        """)
        faculty_rows = cur.fetchall()

    cur.execute("SELECT COUNT(*) AS total FROM faculty_subject_assignments")
    assignment_count = (cur.fetchone() or {}).get('total', 0)

    if assignment_count == 0 and faculty_rows:
        cur.execute("""
            SELECT DISTINCT subject_name, branch, semester
            FROM subjects
            WHERE subject_name IS NOT NULL AND branch IS NOT NULL AND semester IS NOT NULL
            ORDER BY branch, semester, subject_name
        """)
        subjects = cur.fetchall()

        if subjects:
            insert_cur = db.cursor()
            for index, subject in enumerate(subjects):
                faculty = faculty_rows[index % len(faculty_rows)]
                branch_name = (subject.get('branch') or '').strip().upper()
                insert_cur.execute("""
                    INSERT INTO faculty_subject_assignments
                    (faculty_id, subject_name, branch, semester, course_type)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    faculty['admin_id'],
                    subject['subject_name'],
                    branch_name,
                    subject['semester'],
                    infer_course_type_for_branch(branch_name)
                ))
            db.commit()
            insert_cur.close()

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
            exam_end_time VARCHAR(50) DEFAULT NULL,
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
            subject_name VARCHAR(150) NOT NULL,
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

    try:
        cur.execute("""
            SELECT COUNT(*)
            FROM information_schema.COLUMNS
            WHERE TABLE_SCHEMA = DATABASE()
              AND TABLE_NAME = 'exam_seating_plans'
              AND COLUMN_NAME = 'exam_end_time'
        """)
        has_exam_end_time = cur.fetchone()[0] > 0

        if not has_exam_end_time:
            cur.execute("""
                ALTER TABLE exam_seating_plans
                ADD COLUMN exam_end_time VARCHAR(50) DEFAULT NULL
                AFTER exam_time
            """)

        cur.execute("""
            SELECT COUNT(*)
            FROM information_schema.COLUMNS
            WHERE TABLE_SCHEMA = DATABASE()
              AND TABLE_NAME = 'exam_seating_allocations'
              AND COLUMN_NAME = 'subject_name'
        """)
        has_subject_name = cur.fetchone()[0] > 0

        if not has_subject_name:
            cur.execute("""
                ALTER TABLE exam_seating_allocations
                ADD COLUMN subject_name VARCHAR(150) NOT NULL
                AFTER classroom_id
            """)
    except Exception as e:
        print("ALTER exam_seating_allocations skipped:", e)

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
ensure_sample_faculty_and_assignments()
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


def resolve_course_types(course_type, branch):
    course = (course_type or "").upper()
    branch_value = (branch or "ALL").upper()

    if course == "DEGREE":
        if branch_value in ["BCA", "BSC"]:
            return [branch_value]
        return ["BCA", "BSC"]

    return [course]


def resolve_subject_branches(course_type, branch, year):
    course = (course_type or "").upper()
    branch_value = (branch or "ALL").upper()

    if course == "BTECH":
        if year in [1]:
            return ["ALL"]
        if branch_value != "ALL":
            return [branch_value]
        return ["CSE", "CSEAI", "CSEDS", "ECE"]

    if course == "DEGREE":
        if branch_value in ["BCA", "BSC"]:
            return [branch_value]
        return ["BCA", "BSC"]

    if course in ["BCA", "BSC"]:
        return [course]

    return [branch_value]


def build_in_clause(values):
    placeholders = ", ".join(["%s"] * len(values))
    return f"({placeholders})"


def column_exists(cur, table_name, column_name):
    cur.execute("""
        SELECT COUNT(*)
        FROM information_schema.COLUMNS
        WHERE TABLE_SCHEMA = DATABASE()
          AND TABLE_NAME = %s
          AND COLUMN_NAME = %s
    """, (table_name, column_name))
    return cur.fetchone()[0] > 0


def first_value(row):
    if row is None:
        return None
    if isinstance(row, dict):
        return next(iter(row.values()), None)
    return row[0]


def get_group_stats(cur, course_type, year, branch, subject_name=None, exam_date=None, exam_time=None):
    course_types = resolve_course_types(course_type, branch)
    branch_value = (branch or "ALL").upper()

    total_query = f"""
        SELECT COUNT(*)
        FROM students s
        WHERE UPPER(s.course_type) IN {build_in_clause(course_types)}
          AND s.year=%s
    """
    total_params = list(course_types) + [year]
    if branch_value != "ALL" and branch_value not in ["BCA", "BSC"]:
        total_query += " AND UPPER(s.branch)=%s"
        total_params.append(branch_value)

    cur.execute(total_query, tuple(total_params))
    branch_year_total = first_value(cur.fetchone()) or 0

    matched_total = 0
    if subject_name:
        available_subjects = {
            value.upper() for value in get_available_subjects(cur, course_type, year, branch)
        }
        if subject_name.upper() in available_subjects:
            matched_total = branch_year_total

    return {
        "branch_year_total": branch_year_total,
        "matched_total": matched_total
    }


def get_students_for_group(cur, course_type, year, branch, subject_name):
    course_types = resolve_course_types(course_type, branch)
    branch_value = (branch or "ALL").upper()
    available_subjects = {
        value.upper() for value in get_available_subjects(cur, course_type, year, branch)
    }
    if subject_name.upper() not in available_subjects:
        return []

    query = f"""
        SELECT DISTINCT s.student_id, s.name, s.username, s.branch, s.year, s.course_type
        FROM students s
        WHERE UPPER(s.course_type) IN {build_in_clause(course_types)}
          AND s.year=%s
    """
    params = list(course_types) + [year]
    if branch_value != "ALL" and branch_value not in ["BCA", "BSC"]:
        query += " AND UPPER(s.branch)=%s"
        params.append(branch_value)

    cur.execute(query, tuple(params))
    students = cur.fetchall()
    for student in students:
        student['subject_name'] = subject_name
    return students


def ensure_exam_subject_entries(cur, students, subject_name, exam_date, exam_time):
    normalized_subject = (subject_name or "").strip()
    if not normalized_subject or not exam_date or not exam_time:
        return

    for student in students:
        cur.execute("""
            SELECT 1
            FROM exam_subjects
            WHERE student_id=%s
              AND UPPER(subject_name)=%s
              AND exam_date=%s
              AND exam_time=%s
            LIMIT 1
        """, (
            student['student_id'],
            normalized_subject.upper(),
            exam_date,
            exam_time
        ))
        exists = cur.fetchone()
        if exists:
            continue

        cur.execute("""
            INSERT INTO exam_subjects (student_id, subject_name, exam_date, exam_time)
            VALUES (%s, %s, %s, %s)
        """, (
            student['student_id'],
            normalized_subject,
            exam_date,
            exam_time
        ))


def get_available_subjects(cur, course_type, year, branch):
    subject_branches = resolve_subject_branches(course_type, branch, year)
    subject_sets = []

    for subject_branch in subject_branches:
        cur.execute("""
            SELECT DISTINCT subject_name
            FROM subjects
            WHERE UPPER(branch)=%s AND year=%s
            ORDER BY subject_name
        """, (subject_branch.upper(), year))
        subject_sets.append({first_value(row) for row in cur.fetchall() if first_value(row)})

    if not subject_sets:
        return []

    common = set.intersection(*subject_sets) if len(subject_sets) > 1 else subject_sets[0]
    return sorted(common)


def order_students(students, strategy):
    if strategy == 'alphabetical':
        return sorted(students, key=lambda item: ((item.get('name') or '').lower(), item['student_id']))
    if strategy == 'enrollment':
        return sorted(students, key=lambda item: ((item.get('username') or '').lower(), item['student_id']))
    if strategy == 'branch_shuffle':
        return sorted(students, key=lambda item: ((item.get('branch') or '').lower(), (item.get('name') or '').lower(), item['student_id']))
    return sorted(students, key=lambda item: item['student_id'])


def remove_duplicate_students(students, seen_student_ids):
    unique_students = []
    for student in students:
        student_id = student.get('student_id')
        if student_id in seen_student_ids:
            continue
        seen_student_ids.add(student_id)
        unique_students.append(student)
    return unique_students


def dedupe_students_by_identity(students):
    seen_keys = set()
    unique_students = []

    for student in students:
        username = (student.get('username') or '').strip().upper()
        email = (student.get('email') or '').strip().lower()
        key = username or email or f"student_id:{student.get('student_id')}"

        if key in seen_keys:
            continue

        seen_keys.add(key)
        unique_students.append(student)

    return unique_students


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

    return positions


def interleave_grouped_students(grouped_students):
    working = [(key, value[:]) for key, value in grouped_students.items() if value]
    allocation = []

    while working:
        next_working = []
        progressed = False

        for key, students in working:
            if not students:
                continue

            allocation.append(students.pop(0))
            progressed = True

            if students:
                next_working.append((key, students))

        if not progressed:
            break

        working = next_working

    return allocation


def dedupe_allocation_students(students):
    seen_student_ids = set()
    unique_students = []
    for student in students:
        student_id = student.get('student_id')
        if student_id in seen_student_ids:
            continue
        seen_student_ids.add(student_id)
        unique_students.append(student)
    return unique_students


def dedupe_allocations_by_student(allocations):
    seen_student_ids = set()
    unique_allocations = []
    for allocation in allocations:
        student_id = allocation.get('student_id')
        if student_id in seen_student_ids:
            continue
        seen_student_ids.add(student_id)
        unique_allocations.append(allocation)
    return unique_allocations


def sanitize_filename(value):
    cleaned = []
    for char in (value or ""):
        if char.isalnum() or char in ("-", "_"):
            cleaned.append(char)
        elif char in (" ", "/", "\\"):
            cleaned.append("_")
    result = "".join(cleaned).strip("_")
    return result or "seating"


def build_group_pdf(plan, group_label, allocations):
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib.units import mm
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        leftMargin=12 * mm,
        rightMargin=12 * mm,
        topMargin=12 * mm,
        bottomMargin=12 * mm
    )
    styles = getSampleStyleSheet()

    story = [
        Paragraph(f"Seating Plan - {group_label}", styles["Title"]),
        Paragraph(
            f"{plan['exam_name']} | {plan['exam_date']} | {plan['exam_time']}"
            + (f" - {plan['exam_end_time']}" if plan.get('exam_end_time') else ""),
            styles["Normal"]
        ),
        Spacer(1, 8)
    ]

    table_data = [[
        "Seat No",
        "Room No",
        "Student ID",
        "Student Name",
        "Enrollment",
        "Branch",
        "Course",
        "Year",
        "Subject"
    ]]

    for item in allocations:
        table_data.append([
            item.get('seat_label'),
            item.get('room_number'),
            item.get('student_id'),
            item.get('name'),
            item.get('username'),
            item.get('branch'),
            item.get('course_type'),
            item.get('year'),
            item.get('subject_name')
        ])

    table = Table(table_data, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#22313f")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(table)

    doc.build(story)
    buffer.seek(0)
    return buffer


def generate_seating_allocations(classrooms, grouped_students, exam_datetime, room_reveal_hours_before, seat_reveal_minutes_before):
    ordered_students = dedupe_allocation_students(interleave_grouped_students(grouped_students))
    total_capacity = sum(room['total_seats'] for room in classrooms)

    if len(ordered_students) > total_capacity:
        return None, "Not enough rooms available to allocate all students."

    room_visible_at = exam_datetime - timedelta(hours=room_reveal_hours_before)
    seat_visible_at = exam_datetime - timedelta(minutes=seat_reveal_minutes_before)

    allocations = []
    student_index = 0
    allocated_student_ids = set()

    for room in classrooms:
        seat_positions = build_seat_positions(room['total_seats'], room.get('columns_count'))
        for position in seat_positions:
            if student_index >= len(ordered_students):
                break

            student = ordered_students[student_index]
            student_index += 1

            student_id = student.get('student_id')
            if student_id in allocated_student_ids:
                continue

            allocated_student_ids.add(student_id)
            allocations.append({
                'student_id': student_id,
                'classroom_id': room['id'],
                'subject_name': student['subject_name'],
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

        search = request.args.get('search', '').strip()
        selected_course = request.args.get('course_type', '').strip().upper()
        selected_batch = request.args.get('batch', type=int)
        selected_year = request.args.get('year', type=int)
        selected_branch = request.args.get('branch', '').strip().upper()
        cleanup_status = request.args.get('cleanup_status', '').strip().lower()

        cur = db.cursor(dictionary=True)

        filters = []
        params = []

        if search:
            filters.append("(name LIKE %s OR username LIKE %s OR email LIKE %s)")
            value = f"%{search}%"
            params.extend([value, value, value])

        if selected_course:
            filters.append("UPPER(course_type)=%s")
            params.append(selected_course)

        if selected_batch:
            filters.append("joining_year=%s")
            params.append(selected_batch)

        if selected_year:
            filters.append("year=%s")
            params.append(selected_year)

        if selected_branch:
            filters.append("UPPER(branch)=%s")
            params.append(selected_branch)

        where_clause = f"WHERE {' AND '.join(filters)}" if filters else ""

        cur.execute(f"""
            SELECT student_id, name, email, branch, username, year, semester,
                   joining_year, course_type, phone
            FROM students
            {where_clause}
            ORDER BY course_type, joining_year, year, branch, name
        """, tuple(params))

        students = dedupe_students_by_identity(cur.fetchall())

        raw_grouped_students = {}
        for student in students:
            course_key = (student.get('course_type') or 'UNKNOWN').upper()
            batch_key = student.get('joining_year') if student.get('joining_year') is not None else 'Unknown Batch'
            year_key = student.get('year') if student.get('year') is not None else 'Unknown Year'
            branch_key = (student.get('branch') or 'UNKNOWN').upper()

            raw_grouped_students.setdefault(course_key, {})
            raw_grouped_students[course_key].setdefault(batch_key, {})
            raw_grouped_students[course_key][batch_key].setdefault(year_key, {})
            raw_grouped_students[course_key][batch_key][year_key].setdefault(branch_key, [])
            raw_grouped_students[course_key][batch_key][year_key][branch_key].append(student)

        grouped_students = {}
        for course_key in sorted(raw_grouped_students):
            grouped_students[course_key] = {}
            batch_map = raw_grouped_students[course_key]
            batch_keys = sorted(
                batch_map,
                key=lambda value: (isinstance(value, str), -(value if isinstance(value, int) else 0), str(value))
            )

            for batch_key in batch_keys:
                grouped_students[course_key][batch_key] = {}
                year_map = batch_map[batch_key]
                year_keys = sorted(
                    year_map,
                    key=lambda value: (isinstance(value, str), value if isinstance(value, int) else 999, str(value))
                )

                for year_key in year_keys:
                    branch_map = year_map[year_key]
                    grouped_students[course_key][batch_key][year_key] = {}

                    for branch_key in sorted(branch_map):
                        grouped_students[course_key][batch_key][year_key][branch_key] = sorted(
                            branch_map[branch_key],
                            key=lambda item: (
                                (item.get('name') or '').lower(),
                                item.get('student_id', 0)
                            )
                        )

        cur.execute("""
            SELECT DISTINCT UPPER(course_type) AS course_type
            FROM students
            ORDER BY course_type
        """)
        course_options = [row['course_type'] for row in cur.fetchall() if row.get('course_type')]

        cur.execute("""
            SELECT DISTINCT joining_year
            FROM students
            WHERE joining_year IS NOT NULL
            ORDER BY joining_year DESC
        """)
        batch_options = [row['joining_year'] for row in cur.fetchall() if row.get('joining_year')]

        cur.execute("""
            SELECT DISTINCT year
            FROM students
            WHERE year IS NOT NULL
            ORDER BY year
        """)
        year_options = [row['year'] for row in cur.fetchall() if row.get('year')]

        cur.execute("""
            SELECT DISTINCT UPPER(branch) AS branch
            FROM students
            WHERE branch IS NOT NULL AND branch != ''
            ORDER BY branch
        """)
        branch_options = [row['branch'] for row in cur.fetchall() if row.get('branch')]

        cur.close()
        db.close()

        return render_template(
            'students.html',
            students=students,
            grouped_students=grouped_students,
            course_options=course_options,
            batch_options=batch_options,
            year_options=year_options,
            branch_options=branch_options,
            selected_course=selected_course,
            selected_batch=selected_batch,
            selected_year=selected_year,
            selected_branch=selected_branch,
            search=search,
            cleanup_status=cleanup_status
        )

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
            username = request.form['username'].strip()
            email = request.form['email'].strip()

            cur.execute("""
                SELECT student_id
                FROM students
                WHERE UPPER(username)=UPPER(%s) OR LOWER(email)=LOWER(%s)
                LIMIT 1
            """, (username, email))
            existing_student = cur.fetchone()

            if existing_student:
                cur.close()
                db.close()
                return "Student with the same username or email already exists."

            cur.execute("""
                INSERT INTO students 
                (name, email, branch, year, semester, course_type, phone, username, password)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                request.form['name'],
                email,
                request.form['branch'],
                int(request.form['year']),          # ✅ changed
                int(request.form['semester']),      # ✅ added
                request.form['course_type'],
                request.form['phone'],              # ✅ added
                username,
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
    cur = db.cursor(dictionary=True)

    cur.execute("""
        SELECT UPPER(TRIM(branch)) AS branch, year, COUNT(*) AS student_count
        FROM students
        WHERE branch IS NOT NULL
          AND TRIM(branch) != ''
          AND year IS NOT NULL
          AND year BETWEEN 1 AND 8
        GROUP BY branch, year
        ORDER BY branch, year
    """)
    rows = cur.fetchall()

    branch_map = {}
    for row in rows:
        branch_name = (row.get('branch') or 'Unknown Branch').strip()
        year_value = row.get('year') if row.get('year') is not None else 'Unknown Year'
        student_count = row.get('student_count') or 0

        if branch_name not in branch_map:
            branch_map[branch_name] = {
                'name': branch_name,
                'years': [],
                'total_students': 0
            }

        branch_map[branch_name]['years'].append({
            'year': year_value,
            'student_count': student_count
        })
        branch_map[branch_name]['total_students'] += student_count

    ordered_branches = []
    for branch_name in sorted(branch_map):
        branch_item = branch_map[branch_name]
        branch_item['years'] = sorted(
            branch_item['years'],
            key=lambda item: (
                isinstance(item['year'], str),
                item['year'] if isinstance(item['year'], int) else 999,
                str(item['year'])
            )
        )
        ordered_branches.append(branch_item)

    cur.close()
    db.close()

    return render_template('branches.html', branches=ordered_branches)

@app.route('/branch/<branch_name>')
def branch_students(branch_name):
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    db = get_db_connection()
    cur = db.cursor(dictionary=True)
    normalized_branch_name = (branch_name or '').strip().upper()

    cur.execute("""
        SELECT student_id, name, email, branch, username, year, semester,
               joining_year, course_type, phone
        FROM students
        WHERE UPPER(TRIM(branch))=%s
        ORDER BY year, name
    """, (normalized_branch_name,))
    raw_students = cur.fetchall()

    students = []
    for student in raw_students:
        year_value = student.get('year')
        if isinstance(year_value, int) and 1 <= year_value <= 8:
            students.append(student)

    students_by_year = {}
    for student in students:
        year_key = student.get('year')
        students_by_year.setdefault(year_key, []).append(student)

    ordered_students_by_year = {}
    year_keys = sorted(
        students_by_year,
        key=lambda value: (isinstance(value, str), value if isinstance(value, int) else 999, str(value))
    )
    for year_key in year_keys:
        ordered_students_by_year[year_key] = sorted(
            students_by_year[year_key],
            key=lambda item: (
                (item.get('name') or '').lower(),
                item.get('student_id', 0)
            )
        )

    cur.close()
    db.close()

    return render_template(
        'branch_students.html',
        students=students,
        students_by_year=ordered_students_by_year,
        branch=normalized_branch_name
    )
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

        cur.execute("""
            SELECT student_id
            FROM students
            WHERE student_id != %s
              AND (UPPER(username)=UPPER(%s) OR LOWER(email)=LOWER(%s))
            LIMIT 1
        """, (student_id, username, email))
        existing_student = cur.fetchone()

        if existing_student:
            cur.close()
            db.close()
            return "Another student already uses this username or email."

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


@app.route('/cleanup_duplicate_students')
def cleanup_duplicate_students():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    db = get_db_connection()
    if db is None:
        return "Database connection failed"

    cur = db.cursor(dictionary=True)
    student_reference_tables = [
        ('academics', 'student_id'),
        ('exam_subjects', 'student_id'),
        ('feedback', 'student_id'),
        ('fees', 'student_id'),
        ('helpdesk', 'student_id'),
        ('faculty_chat_messages', 'student_id'),
        ('faculty_meeting_requests', 'student_id'),
        ('exam_seating_allocations', 'student_id')
    ]

    try:
        cur.execute("""
            SELECT LOWER(TRIM(username)) AS username_key
            FROM students
            WHERE username IS NOT NULL AND TRIM(username) != ''
            GROUP BY LOWER(TRIM(username))
            HAVING COUNT(*) > 1
        """)
        duplicate_keys = [row['username_key'] for row in cur.fetchall() if row.get('username_key')]

        if not duplicate_keys:
            return redirect(url_for('students', cleanup_status='none'))

        for username_key in duplicate_keys:
            cur.execute("""
                SELECT student_id
                FROM students
                WHERE LOWER(TRIM(username))=%s
                ORDER BY student_id
            """, (username_key,))
            student_ids = [row['student_id'] for row in cur.fetchall()]

            if len(student_ids) <= 1:
                continue

            keep_student_id = student_ids[0]
            duplicate_ids = student_ids[1:]

            for duplicate_id in duplicate_ids:
                for table_name, column_name in student_reference_tables:
                    cur.execute(
                        f"UPDATE `{table_name}` SET `{column_name}`=%s WHERE `{column_name}`=%s",
                        (keep_student_id, duplicate_id)
                    )

                cur.execute("DELETE FROM students WHERE student_id=%s", (duplicate_id,))

        db.commit()
        return redirect(url_for('students', cleanup_status='success'))
    except Exception as e:
        db.rollback()
        print("DUPLICATE CLEANUP ERROR:", e)
        return redirect(url_for('students', cleanup_status='failed'))
    finally:
        cur.close()
        db.close()
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
    try:
        db = get_db_connection()
        if db is None:
            return render_template(
                'admin_seating.html',
                classrooms=[],
                plans=[],
                selected_plan=None,
                selected_plan_groups=[],
                plan_allocations=[],
                room_summary=[],
                error_message="Database connection failed. Please try again in a moment."
            )

        cur = db.cursor(dictionary=True)
        generated_plan_id = None
        error_message = None
        has_exam_end_time = False

        try:
            meta_cur = db.cursor()
            has_exam_end_time = column_exists(meta_cur, 'exam_seating_plans', 'exam_end_time')
            meta_cur.close()
        except Exception:
            has_exam_end_time = False

        if request.method == 'POST':
            action = request.form.get('action')

            if action == 'generate_plan':
                exam_name = request.form.get('exam_name', '').strip()
                exam_date = request.form.get('exam_date')
                exam_time = request.form.get('exam_time', '').strip()
                exam_end_time = request.form.get('exam_end_time', '').strip()
                strategy = request.form.get('strategy', 'alphabetical')
                room_reveal_hours_before = request.form.get('room_reveal_hours_before', type=int) or 12
                seat_reveal_minutes_before = request.form.get('seat_reveal_minutes_before', type=int) or 10
                selected_room_ids = request.form.getlist('room_ids')

                if not exam_name or not exam_date or not exam_time or not exam_end_time:
                    error_message = "Please fill exam name, date, start time, and end time."
                elif not selected_room_ids:
                    error_message = "Please select at least one classroom."
                else:
                    exam_datetime = parse_exam_datetime(exam_date, exam_time)
                    if exam_datetime is None:
                        error_message = "Use exam time in '10:00 AM' or 24-hour format like '14:00'."
                    else:
                        groups = []
                        grouped_students = {}
                        seen_student_ids = set()

                        for index in range(1, 5):
                            course_type = request.form.get(f'course_type_{index}', '').strip()
                            year = request.form.get(f'year_{index}', type=int)
                            branch = request.form.get(f'branch_{index}', 'ALL').strip() or 'ALL'
                            subject_name = request.form.get(f'subject_name_{index}', '').strip()

                            if not course_type or not year:
                                continue

                            if not subject_name:
                                error_message = f"Please select the subject for group {index}."
                                break

                            group_label = build_group_label(course_type, year, branch)
                            stats = get_group_stats(
                                cur,
                                course_type,
                                year,
                                branch,
                                subject_name
                            )
                            students = get_students_for_group(
                                cur,
                                course_type,
                                year,
                                branch,
                                subject_name
                            )
                            ordered = order_students(students, strategy)
                            unique_ordered = remove_duplicate_students(ordered, seen_student_ids)

                            enriched_students = []
                            for student in unique_ordered:
                                item = dict(student)
                                item['group_label'] = group_label
                                item['ordering_value'] = item.get('name') if strategy == 'alphabetical' else item.get('username')
                                item['subject_name'] = subject_name
                                enriched_students.append(item)

                            if enriched_students:
                                groups.append({
                                    'course_type': course_type.upper(),
                                    'year': year,
                                    'branch': branch.upper(),
                                    'subject_name': subject_name,
                                    'group_label': group_label,
                                    'branch_year_total': stats['branch_year_total'],
                                    'student_count': len(enriched_students)
                                })
                                grouped_students[group_label] = enriched_students

                        if error_message:
                            pass
                        elif not groups:
                            error_message = "Please select at least one student group."
                        elif sum(group['student_count'] for group in groups) == 0:
                            details = ", ".join(
                                f"{group['group_label']} ({group['subject_name']}: 0 matched)"
                                for group in groups
                            )
                            error_message = f"No students matched the selected exam details. Check subject/date/time or course mapping. {details}"
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
                                for group_students in grouped_students.values():
                                    ensure_exam_subject_entries(
                                        cur,
                                        group_students,
                                        group_students[0]['subject_name'] if group_students else None,
                                        exam_date,
                                        exam_time
                                    )

                                cur.execute("""
                                    INSERT INTO exam_seating_plans
                                    (exam_name, subject_name, exam_date, exam_time, exam_end_time, strategy,
                                     room_reveal_hours_before, seat_reveal_minutes_before,
                                     selected_groups_json, room_ids_json, created_by)
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                """, (
                                    exam_name,
                                    'Mixed Session',
                                    exam_date,
                                    exam_time,
                                    exam_end_time,
                                    strategy,
                                    room_reveal_hours_before,
                                    seat_reveal_minutes_before,
                                    json.dumps(groups),
                                    json.dumps(selected_room_ids),
                                    session.get('admin_id')
                                ))
                                generated_plan_id = cur.lastrowid

                                inserted_student_ids = set()
                                for allocation in allocations:
                                    if allocation['student_id'] in inserted_student_ids:
                                        continue
                                    inserted_student_ids.add(allocation['student_id'])
                                    cur.execute("""
                                        INSERT INTO exam_seating_allocations
                                        (plan_id, student_id, classroom_id, subject_name, room_number, seat_number, seat_label,
                                         seat_row, seat_column, group_label, ordering_value,
                                         room_visible_at, seat_visible_at)
                                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                    """, (
                                        generated_plan_id,
                                        allocation['student_id'],
                                        allocation['classroom_id'],
                                        allocation['subject_name'],
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

        plans_query = """
            SELECT id, exam_name, subject_name, exam_date, exam_time,
                   {exam_end_time_select}
                   strategy, created_at
            FROM exam_seating_plans
            ORDER BY exam_date DESC, created_at DESC
        """.format(
            exam_end_time_select="exam_end_time, " if has_exam_end_time else "NULL AS exam_end_time, "
        )
        cur.execute(plans_query)
        plans = cur.fetchall()

        plan_id = request.args.get('plan_id', type=int) or generated_plan_id
        selected_plan = None
        selected_plan_groups = []
        plan_allocations = []
        room_summary = []

        if plan_id:
            selected_plan_query = """
                SELECT id, exam_name, subject_name, exam_date, exam_time,
                       {exam_end_time_select}
                       strategy, room_reveal_hours_before, seat_reveal_minutes_before,
                       selected_groups_json, room_ids_json, created_at
                FROM exam_seating_plans
                WHERE id=%s
            """.format(
                exam_end_time_select="exam_end_time, " if has_exam_end_time else "NULL AS exam_end_time, "
            )
            cur.execute(selected_plan_query, (plan_id,))
            selected_plan = cur.fetchone()

            if selected_plan:
                if selected_plan.get('selected_groups_json'):
                    try:
                        selected_plan_groups = json.loads(selected_plan['selected_groups_json'])
                    except Exception:
                        selected_plan_groups = []

                cur.execute("""
                    SELECT a.room_number, a.subject_name, a.seat_label, a.seat_number, a.group_label,
                           s.student_id, s.name, s.username, s.branch, s.course_type, s.year
                    FROM exam_seating_allocations a
                    JOIN students s ON s.student_id = a.student_id
                    WHERE a.plan_id=%s
                    ORDER BY a.room_number, a.seat_number
                """, (plan_id,))
                plan_allocations = dedupe_allocations_by_student(cur.fetchall())

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
            selected_plan_groups=selected_plan_groups,
            plan_allocations=plan_allocations,
            room_summary=room_summary,
            error_message=error_message
        )
    except Exception as e:
        print("SEATING PAGE ERROR:", e)
        return render_template(
            'admin_seating.html',
            classrooms=[],
            plans=[],
            selected_plan=None,
            selected_plan_groups=[],
            plan_allocations=[],
            room_summary=[],
            error_message=f"Seating page error: {e}"
        )


@app.route('/seating_group_counts')
def seating_group_counts():
    if 'admin' not in session:
        return jsonify({"groups": [], "totals": {"branch_year_total": 0, "matched_total": 0}}), 403

    exam_date = request.args.get('exam_date')
    exam_time = request.args.get('exam_time')

    db = get_db_connection()
    if db is None:
        return jsonify({"groups": [], "totals": {"branch_year_total": 0, "matched_total": 0}})

    cur = db.cursor()
    groups = []
    total_branch_year = 0
    total_matched = 0

    for index in range(1, 5):
        course_type = request.args.get(f'course_type_{index}', '').strip()
        year = request.args.get(f'year_{index}', type=int)
        branch = request.args.get(f'branch_{index}', 'ALL').strip() or 'ALL'
        subject_name = request.args.get(f'subject_name_{index}', '').strip()

        if not course_type or not year:
            continue

        stats = get_group_stats(cur, course_type, year, branch, subject_name, exam_date, exam_time)
        group = {
            "index": index,
            "group_label": build_group_label(course_type, year, branch),
            "subject_name": subject_name,
            "branch_year_total": stats["branch_year_total"],
            "matched_total": stats["matched_total"]
        }
        groups.append(group)
        total_branch_year += stats["branch_year_total"]
        total_matched += stats["matched_total"]

    cur.close()
    db.close()

    return jsonify({
        "groups": groups,
        "totals": {
            "branch_year_total": total_branch_year,
            "matched_total": total_matched
        }
    })


@app.route('/seating_subject_options')
def seating_subject_options():
    if 'admin' not in session:
        return jsonify({"subjects": []}), 403

    course_type = request.args.get('course_type', '').strip()
    year = request.args.get('year', type=int)
    branch = request.args.get('branch', 'ALL').strip() or 'ALL'

    if not course_type or not year:
        return jsonify({"subjects": []})

    db = get_db_connection()
    if db is None:
        return jsonify({"subjects": []})

    cur = db.cursor()
    subjects = get_available_subjects(cur, course_type, year, branch)
    cur.close()
    db.close()

    return jsonify({"subjects": subjects})


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


@app.route('/seating_plan/<int:plan_id>/group_pdf')
def seating_group_pdf(plan_id):
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    group_label = request.args.get('group_label', '').strip()
    if not group_label:
        return redirect(url_for('seating', plan_id=plan_id))

    db = get_db_connection()
    if db is None:
        return redirect(url_for('seating', plan_id=plan_id))

    cur = db.cursor(dictionary=True)
    cur.execute("""
        SELECT exam_name, exam_date, exam_time, exam_end_time
        FROM exam_seating_plans
        WHERE id=%s
    """, (plan_id,))
    plan = cur.fetchone()

    cur.execute("""
        SELECT a.room_number, a.seat_label, a.group_label, a.subject_name,
               s.student_id, s.name, s.username, s.branch, s.course_type, s.year
        FROM exam_seating_allocations a
        JOIN students s ON s.student_id = a.student_id
        WHERE a.plan_id=%s AND a.group_label=%s
        ORDER BY a.room_number, a.seat_number
    """, (plan_id, group_label))
    allocations = dedupe_allocations_by_student(cur.fetchall())
    cur.close()
    db.close()

    if not plan or not allocations:
        return redirect(url_for('seating', plan_id=plan_id))

    pdf_buffer = build_group_pdf(plan, group_label, allocations)
    filename = f"{sanitize_filename(plan['exam_name'])}_{sanitize_filename(group_label)}.pdf"
    return send_file(pdf_buffer, mimetype='application/pdf', as_attachment=True, download_name=filename)

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
    if 'student_id' not in session:
        return redirect(url_for('student_login'))

    db = get_db_connection()
    cur = db.cursor(dictionary=True)
    cur.execute("""
        SELECT student_id, name, email, branch, username, year, semester,
               joining_year, course_type, phone
        FROM students
        WHERE student_id=%s
    """, (session['student_id'],))
    student = cur.fetchone()
    cur.close()
    db.close()

    return render_template('student_registration.html', student=student)


@app.route('/courses')
def courses():
    if 'student_id' not in session:
        return redirect(url_for('student_login'))

    db = get_db_connection()
    if db is None:
        return "Database connection failed"

    cur = db.cursor(dictionary=True)

    cur.execute("""
        SELECT branch, joining_year, course_type, year, semester
        FROM students WHERE student_id=%s
    """, (session['student_id'],))

    student = cur.fetchone()
    if not student:
        cur.close()
        db.close()
        return redirect(url_for('student_login'))

    branch = (student.get('branch') or '').strip().upper()
    course_type = (student.get('course_type') or '').strip().upper()
    joining_year = student.get('joining_year')

    if joining_year:
        sem = calculate_semester(joining_year, course_type)
    else:
        sem = student.get('semester') or 1

    subject_branches = []
    if course_type == 'BTECH' and sem in [1, 2]:
        subject_branches = ['ALL']
    elif branch:
        subject_branches = [branch]
    elif course_type:
        subject_branches = [course_type]

    subjects = []
    for subject_branch in subject_branches:
        cur.execute("""
            SELECT subject_name, branch, semester
            FROM subjects
            WHERE UPPER(branch)=%s AND semester=%s
            ORDER BY subject_name
        """, (subject_branch, sem))
        subjects.extend(cur.fetchall())

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

    return redirect(url_for('my_faculty'))


@app.route('/my_faculty')
def my_faculty():
    if 'student_id' not in session:
        return redirect(url_for('student_login'))

    db = get_db_connection()
    if db is None:
        return "Database connection failed"

    cur = db.cursor(dictionary=True)
    cur.execute("""
        SELECT student_id, name, branch, joining_year, course_type, semester
        FROM students
        WHERE student_id=%s
    """, (session['student_id'],))
    student = cur.fetchone()
    if not student:
        cur.close()
        db.close()
        return redirect(url_for('student_login'))

    branch = (student.get('branch') or '').strip().upper()
    course_type = (student.get('course_type') or '').strip().upper()
    joining_year = student.get('joining_year')
    if joining_year:
        current_sem = calculate_semester(joining_year, course_type)
    else:
        current_sem = student.get('semester') or 1

    subject_branch = 'ALL' if course_type == 'BTECH' and current_sem in [1, 2] else branch
    cur.execute("""
        SELECT subject_name, branch, semester
        FROM subjects
        WHERE UPPER(branch)=%s AND semester=%s
        ORDER BY subject_name
    """, (subject_branch, current_sem))
    subject_rows = cur.fetchall()

    subject_faculty_rows = []
    for subject in subject_rows:
        cur.execute("""
            SELECT fsa.subject_name, a.admin_id, a.username
            FROM faculty_subject_assignments fsa
            JOIN admin a ON a.admin_id = fsa.faculty_id
            WHERE UPPER(fsa.branch)=%s
              AND fsa.semester=%s
              AND fsa.subject_name=%s
            LIMIT 1
        """, (
            (subject.get('branch') or '').strip().upper(),
            subject.get('semester'),
            subject.get('subject_name')
        ))
        faculty_row = cur.fetchone()
        subject_faculty_rows.append({
            'subject_name': subject.get('subject_name'),
            'faculty_id': faculty_row['admin_id'] if faculty_row else None,
            'faculty_name': faculty_row['username'] if faculty_row else 'Not Assigned'
        })

    cur.close()
    db.close()

    return render_template(
        'student_my_faculty.html',
        student=student,
        current_sem=current_sem,
        subject_faculty_rows=subject_faculty_rows
    )


@app.route('/attendance')
def attendance():
    if 'student_id' not in session:
        return redirect(url_for('student_login'))

    db = get_db_connection()
    cur = db.cursor(dictionary=True)
    cur.execute("""
        SELECT student_id, name, branch, year, semester, course_type
        FROM students
        WHERE student_id=%s
    """, (session['student_id'],))
    student = cur.fetchone()
    cur.close()
    db.close()

    return render_template('student_attendance.html', student=student)


@app.route('/resources')
def resources():
    if 'student_id' not in session:
        return redirect(url_for('student_login'))

    db = get_db_connection()
    if db is None:
        return render_template('student_resources.html', resources=[])

    cur = db.cursor()
    cur.execute("""
        SELECT id, title, file_name, uploaded_at
        FROM documents
        ORDER BY uploaded_at DESC, id DESC
    """)
    resources = cur.fetchall()
    cur.close()
    db.close()

    return render_template('student_resources.html', resources=resources)


@app.route('/mentor')
def mentor():
    if 'student_id' not in session:
        return redirect(url_for('student_login'))

    db = get_db_connection()
    cur = db.cursor(dictionary=True)
    cur.execute("""
        SELECT student_id, name, branch, year, semester, course_type
        FROM students
        WHERE student_id=%s
    """, (session['student_id'],))
    student = cur.fetchone()

    cur.execute("""
        SELECT admin_id, username
        FROM admin
        ORDER BY username
        LIMIT 1
    """)
    mentor_faculty = cur.fetchone()
    cur.close()
    db.close()

    return render_template('student_mentor.html', student=student, mentor_faculty=mentor_faculty)


@app.route('/marks')
def marks():
    if 'student_id' not in session:
        return redirect(url_for('student_login'))

    db = get_db_connection()
    cur = db.cursor()
    cur.execute("""
        SELECT subject_name, internal_marks, external_marks, total_marks, semester
        FROM academics
        WHERE student_id=%s
        ORDER BY semester, subject_name
    """, (session['student_id'],))
    records = cur.fetchall()
    cur.close()
    db.close()

    return render_template('student_marks.html', records=records)


@app.route('/grades')
def grades():
    if 'student_id' not in session:
        return redirect(url_for('student_login'))

    db = get_db_connection()
    cur = db.cursor()
    cur.execute("""
        SELECT subject_name, total_marks, semester
        FROM academics
        WHERE student_id=%s
        ORDER BY semester, subject_name
    """, (session['student_id'],))
    rows = cur.fetchall()
    cur.close()
    db.close()

    grade_rows = []
    for subject_name, total_marks, semester in rows:
        marks_value = total_marks or 0
        if marks_value >= 90:
            grade = 'O'
        elif marks_value >= 80:
            grade = 'A+'
        elif marks_value >= 70:
            grade = 'A'
        elif marks_value >= 60:
            grade = 'B+'
        elif marks_value >= 50:
            grade = 'B'
        elif marks_value >= 40:
            grade = 'C'
        else:
            grade = 'F'

        grade_rows.append({
            'subject_name': subject_name,
            'total_marks': marks_value,
            'semester': semester,
            'grade': grade
        })

    return render_template('student_grades.html', grade_rows=grade_rows)

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
    meta_cur = db.cursor()
    has_exam_end_time = column_exists(meta_cur, 'exam_seating_plans', 'exam_end_time')
    meta_cur.close()

    exam_query = """
        SELECT e.subject_name, e.exam_date, e.exam_time,
               p.exam_name, {exam_end_time_select}
               a.room_number, a.seat_label, a.room_visible_at, a.seat_visible_at
        FROM exam_subjects e
        LEFT JOIN exam_seating_allocations a
            ON a.student_id = e.student_id
           AND a.subject_name = e.subject_name
        LEFT JOIN exam_seating_plans p
            ON p.id = a.plan_id
           AND p.exam_date = e.exam_date
           AND p.exam_time = e.exam_time
        WHERE e.student_id=%s
        GROUP BY e.subject_name, e.exam_date, e.exam_time, p.exam_name, {exam_end_time_group}
                 a.room_number, a.seat_label, a.room_visible_at, a.seat_visible_at
        ORDER BY e.exam_date, e.exam_time
    """.format(
        exam_end_time_select="p.exam_end_time, " if has_exam_end_time else "NULL AS exam_end_time, ",
        exam_end_time_group="p.exam_end_time, " if has_exam_end_time else ""
    )
    cur.execute(exam_query, (session['student_id'],))

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
