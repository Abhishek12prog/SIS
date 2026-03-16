from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "sis_secret_key"

# ================= DATABASE =================
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="abhishek",
    database="college_db"
)

# ======================================================
# ======================= HOME =========================
# ======================================================

@app.route('/')
def home():
    return render_template('choose_role.html')


# ======================================================
# ======================= ADMIN ========================
# ======================================================

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        cur = db.cursor()
        cur.execute(
            "SELECT * FROM admin WHERE username=%s AND password=%s",
            (request.form['username'], request.form['password'])
        )
        admin = cur.fetchone()
        cur.close()

        if admin:
            session['admin'] = admin[1]
            return redirect(url_for('admin_dashboard'))
        else:
            return "Invalid Admin Login"

    return render_template('admin_login.html')


# ================= DASHBOARD =================
@app.route('/admin')
def admin_dashboard():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

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

    return render_template(
        'admin_dashboard.html',
        total_students=total_students,
        total_announcements=total_announcements,
        total_feedback=total_feedback,
        total_tickets=total_tickets,
        branch_data=branch_data
    )


# ================= STUDENTS =================
@app.route('/students')
def students():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    cur = db.cursor()
    cur.execute("SELECT * FROM students")
    students = cur.fetchall()
    cur.close()

    return render_template('students.html', students=students)


# ================= ADD STUDENT =================
@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        cur = db.cursor()
        cur.execute("""
            INSERT INTO students (name, email, branch, username, password)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            request.form['name'],
            request.form['email'],
            request.form['branch'],
            request.form['username'],
            request.form['password']
        ))
        db.commit()
        cur.close()

        return redirect(url_for('students'))

    return render_template('add_student.html')


# ================= BRANCHES =================
@app.route('/branches')
def branches():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    cur = db.cursor()
    cur.execute("SELECT * FROM branches")
    branches = cur.fetchall()
    cur.close()

    return render_template('branches.html', branches=branches)


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
        title = request.form['title']
        file = request.files['file']

        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            cur = db.cursor()
            cur.execute(
                "INSERT INTO documents (title, file_name) VALUES (%s, %s)",
                (title, filename)
            )
            db.commit()
            cur.close()

            return redirect(url_for('documents'))

    return render_template('admin_upload.html')


# ================= DOCUMENTS =================
@app.route('/documents')
def documents():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    cur = db.cursor()
    cur.execute("SELECT * FROM documents ORDER BY uploaded_at DESC")
    docs = cur.fetchall()
    cur.close()

    return render_template('admin_documents.html', docs=docs)


# ================= ANNOUNCEMENTS =================
@app.route('/announcements')
def announcements():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    cur = db.cursor()
    cur.execute("SELECT * FROM announcements ORDER BY created_at DESC")
    announcements = cur.fetchall()
    cur.close()

    return render_template('admin_announcements.html', announcements=announcements)

# ================= REPORTS =================
@app.route('/reports')
def reports():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    return render_template('admin_reports.html')

# ================= ADMIN HELP DESK =================
@app.route('/admin_helpdesk')
def admin_helpdesk():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

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

    return render_template('admin_helpdesk.html', tickets=tickets)

# ================= VIEW FEEDBACK =================
@app.route('/view_feedback')
def view_feedback():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    cur = db.cursor()
    cur.execute("""
        SELECT students.name, feedback.message, feedback.created_at
        FROM feedback
        JOIN students ON feedback.student_id = students.student_id
        ORDER BY feedback.created_at DESC
    """)
    feedbacks = cur.fetchall()
    cur.close()

    return render_template('admin_view_feedback.html', feedbacks=feedbacks)
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
        cur = db.cursor()
        cur.execute("SELECT * FROM students WHERE username=%s AND password=%s",
                    (request.form['username'], request.form['password']))
        student = cur.fetchone()
        cur.close()

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


@app.route('/my_info')
def my_info():
    if 'student_id' not in session:
        return redirect(url_for('student_login'))

    cur = db.cursor()
    cur.execute("SELECT * FROM students WHERE student_id=%s",
                (session['student_id'],))
    student = cur.fetchone()
    cur.close()

    return render_template('student_myinfo.html', student=student)


@app.route('/student_announcements')
def student_announcements():
    if 'student_id' not in session:
        return redirect(url_for('student_login'))

    cur = db.cursor()
    cur.execute("SELECT * FROM announcements ORDER BY created_at DESC")
    announcements = cur.fetchall()
    cur.close()

    return render_template('student_announcements.html', announcements=announcements)


@app.route('/academics')
def academics():
    if 'student_id' not in session:
        return redirect(url_for('student_login'))

    cur = db.cursor()
    cur.execute("""
        SELECT subject_name, internal_marks, external_marks, total_marks, semester
        FROM academics WHERE student_id=%s
    """, (session['student_id'],))
    records = cur.fetchall()
    cur.close()

    return render_template('student_academics.html', records=records)


@app.route('/fees')
def fees():
    if 'student_id' not in session:
        return redirect(url_for('student_login'))

    cur = db.cursor()
    cur.execute("""
        SELECT semester, total_fee, paid_amount, due_amount, status
        FROM fees WHERE student_id=%s
    """, (session['student_id'],))
    fee_records = cur.fetchall()
    cur.close()

    return render_template('student_fees.html', fee_records=fee_records)


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if 'student_id' not in session:
        return redirect(url_for('student_login'))

    if request.method == 'POST':
        cur = db.cursor()
        cur.execute("INSERT INTO feedback (student_id, message) VALUES (%s, %s)",
                    (session['student_id'], request.form['message']))
        db.commit()
        cur.close()

        return redirect(url_for('student_dashboard'))

    return render_template('student_feedback.html')


@app.route('/helpdesk', methods=['GET', 'POST'])
def helpdesk():
    if 'student_id' not in session:
        return redirect(url_for('student_login'))

    cur = db.cursor()

    if request.method == 'POST':
        cur.execute("""
            INSERT INTO helpdesk (student_id, subject, description)
            VALUES (%s, %s, %s)
        """, (
            session['student_id'],
            request.form['subject'],
            request.form['description']
        ))
        db.commit()

    cur.execute("""
        SELECT subject, description, status, created_at
        FROM helpdesk WHERE student_id=%s
        ORDER BY created_at DESC
    """, (session['student_id'],))
    tickets = cur.fetchall()
    cur.close()

    return render_template('student_helpdesk.html', tickets=tickets)


@app.route('/hall_ticket')
def hall_ticket():
    if 'student_id' not in session:
        return redirect(url_for('student_login'))

    cur = db.cursor()

    cur.execute("SELECT name, branch FROM students WHERE student_id=%s",
                (session['student_id'],))
    student = cur.fetchone()

    cur.execute("""
        SELECT subject_name, exam_date, exam_time
        FROM exam_subjects WHERE student_id=%s
    """, (session['student_id'],))
    subjects = cur.fetchall()

    cur.close()

    return render_template('student_hall_ticket.html',
                           student=student,
                           subjects=subjects)


@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if 'student_id' not in session:
        return redirect(url_for('student_login'))

    if request.method == 'POST':
        cur = db.cursor()
        cur.execute("UPDATE students SET password=%s WHERE student_id=%s",
                    (request.form['new_password'], session['student_id']))
        db.commit()
        cur.close()

        return redirect(url_for('student_dashboard'))

    return render_template('student_change_password.html')


@app.route('/student_logout')
def student_logout():
    session.clear()
    return redirect(url_for('student_login'))


if __name__ == '__main__':
    app.run(debug=True, port=5001)