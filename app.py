from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import hashlib

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL configuration
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'piyush@2004'
app.config['MYSQL_DB'] = 'user_management'
app.config['MYSQL_HOST'] = 'localhost'

mysql = MySQL(app)

@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    return render_template('home.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        raw_password = request.form['password']
        role = request.form['role']

        password_hash = hashlib.md5(raw_password.encode()).hexdigest()

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id, is_admin, password FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user:
            stored_password_hash = user[2]

            if password_hash == stored_password_hash:
                session['username'] = username

                if role == '1' and user[1] == 1:
                    return redirect(url_for('admin_home'))
                elif role == '0' and user[1] == 0:
                    cursor.execute("SELECT Mentor_id FROM MENTOR WHERE User_id = %s", (user[0],))
                    mentor_id = cursor.fetchone()

                    if mentor_id:
                        session['mentor_id'] = mentor_id[0]
                        return redirect(url_for('mentor_home'))
                    else:
                        return "Invalid mentor record. Please contact an administrator."
                else:
                    return "Invalid role selected."
            else:
                return "Invalid password. Please try again."
        else:
            return "Invalid username. Please try again."

    return render_template('login.html')

'''
@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    if 'username' in session and session['username']:
        if request.method == 'POST':
            student_id = request.form['student_id']
            feedback_text = request.form['feedback_text']
            admin_only = 'admin_only' in request.form  # Set to True if checkbox is checked, False otherwise
            mentor_feedback = 'mentor' in request.form  # Set to True if checkbox is checked, False otherwise
            fees_paid = request.form['fees_paid']
            issues = request.form['issues']
            achievements = request.form['achievements']
            backlogs = request.form['backlogs']
            remarks = request.form['remarks']

            cursor = mysql.connection.cursor()

            try:
                # Insert new feedback
                cursor.execute("INSERT INTO feedback (student_id, feedback_text, admin_only, mentor_feedback, "
                               "fees_paid, issues, achievements, backlogs, remarks) "
                               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                               (student_id, feedback_text, admin_only, mentor_feedback, fees_paid, issues,
                                achievements, backlogs, remarks))

                mysql.connection.commit()

                # Fetch the submitted feedback for displaying
                cursor.execute("SELECT * FROM feedback WHERE student_id = %s", (student_id,))
                submitted_feedback = cursor.fetchone()

                flash('Feedback submitted successfully!')

            except Exception as e:
                print(f"SQL Error: {str(e)}")
                flash(f"An error occurred while submitting feedback: {str(e)}")

            finally:
                cursor.close()

    return render_template('submitted_feedback.html', username=session['username'], submitted_feedback=submitted_feedback)
'''
'''
@app.route('/admin_home')
def admin_home():
    if 'username' in session and session['username']:
        cursor = mysql.connection.cursor()

        # Fetch all mentors (excluding those with 'Admin' in their name)
        cursor.execute("SELECT * FROM MENTOR WHERE NOT Mentor_name LIKE '%Admin%'")
        mentors = cursor.fetchall()

        # Create a list to store mentor-student pairs
        mentor_student_pairs = []

        # Iterate through mentors and fetch their students
        for mentor in mentors:
            cursor.execute("SELECT * FROM STUDENT WHERE Mentor_id = %s", (mentor[0],))
            students = cursor.fetchall()
            mentor_student_pairs.append((mentor, students))

        return render_template('admin_home.html', username=session['username'], mentor_student_pairs=mentor_student_pairs)

    return redirect(url_for('home'))
'''

@app.route('/admin_home')
def admin_home():
    if 'username' in session and session['username']:
        cursor = mysql.connection.cursor()

        # Fetch all mentors (excluding those with 'Admin' in their name)
        cursor.execute("SELECT * FROM MENTOR WHERE NOT Mentor_name LIKE '%Admin%'")
        mentors = cursor.fetchall()

        # Create a list to store mentor-student-feedback triples
        mentor_student_feedback_triples = []

        # Iterate through mentors and fetch their students
        for mentor in mentors:
            cursor.execute("SELECT * FROM STUDENT WHERE Mentor_id = %s", (mentor[0],))
            students = cursor.fetchall()

            # Fetch feedback for each student
            feedbacks = {}
            for student in students:
                cursor.execute("SELECT * FROM FEEDBACK WHERE student_id = %s", (student[0],))
                feedbacks[student[0]] = cursor.fetchall()

            mentor_student_feedback_triples.append((mentor, students, feedbacks))

        return render_template('admin_home.html', username=session['username'], mentor_student_feedback_triples=mentor_student_feedback_triples)

    return redirect(url_for('home'))

# Assuming you have a route like this in your Flask application
@app.route('/profile/<int:student_id>')
def profile(student_id):
    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT * FROM PROFILE
        WHERE Std_id = %s
    """, (student_id,))
    profile_data = cursor.fetchone()

    return render_template('profile.html', username=session['username'], profile_data=profile_data)



@app.route('/feedback/<int:student_id>')
def feedback(student_id):
    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT 
            student_id, 
            feedback_text,
            fees_paid,
            issues,
            achievements,
            backlogs,
            remarks,
            submission_date
        FROM FEEDBACK
        WHERE student_id = %s
    """, (student_id,))
    feedback_data = cursor.fetchone()

    return render_template('feedback.html', username=session['username'], feedback_data=feedback_data)


@app.route('/mentor_students/<int:mentor_id>')
def mentor_students(mentor_id):
    if 'username' in session and session['username']:
        cursor = mysql.connection.cursor()

        # Fetch the mentor's details
        cursor.execute("SELECT * FROM MENTOR WHERE Mentor_id = %s", (mentor_id,))
        mentor = cursor.fetchone()

        # Fetch all data for students and their profiles mentored by this mentor
        cursor.execute("""
            SELECT s.Student_id, s.Student_name, s.S_mobile, s.Student_email, s.Student_address, s.Student_dob, s.Student_bloodgp,
            p.Student_program, p.Student_Sem, p.Student_sec, p.Father_name, p.F_mobile, p.F_email, p.Mother_name, p.M_mobile, p.M_email
            FROM STUDENT AS s
            LEFT JOIN profile AS p ON s.Student_id = p.Std_id
            WHERE s.Mentor_id = %s
        """, (mentor_id,))
        students_with_profile = cursor.fetchall()

        fees = {}
        for student in students_with_profile:
            cursor.execute("SELECT Fee_id, Amount, Status, Due_Date FROM fees WHERE Std_id = %s", (student[0],))
            student_fees = cursor.fetchall()
            fees[student[0]] = student_fees
        
        return render_template('mentor_students.html', username=session['username'], mentor=mentor, students=students_with_profile, fees=fees)

    return redirect(url_for('home')) 



@app.route('/delete_mentor/<int:mentor_id>', methods=['POST'])
def delete_mentor(mentor_id):
    if 'username' in session and session['username']:
        # Display a confirmation page to ensure the user wants to delete the mentor
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM MENTOR WHERE Mentor_id = %s", (mentor_id,))
        mentor = cursor.fetchone()
        if mentor:
            return render_template('delete_mentor_confirmation.html', mentor=mentor)
        else:
            flash('Mentor not found.')
            return redirect(url_for('admin_home'))
    else:
        return redirect(url_for('home'))


@app.route('/confirm_delete_mentor/<int:mentor_id>', methods=['POST'])
def confirm_delete_mentor(mentor_id):
    if 'username' in session and session['username']:
        cursor = mysql.connection.cursor()

        # Check if the user executing the procedure is an admin
        cursor.execute("SELECT is_admin FROM users WHERE username = %s", (session['username'],))
        admin_check = cursor.fetchone()

        if admin_check and admin_check[0] == 1:
            result_message = ""  # Initialize an empty string for the result message

            # This user is an admin, so call the delete mentor procedure
            cursor.callproc('DeleteMentorProcedure', (session['username'], mentor_id, result_message))
            mysql.connection.commit()

            flash(result_message)  # Flash the result message

            return redirect(url_for('admin_home'))
        else:
            flash('User does not have admin privileges.')
            return redirect(url_for('admin_home'))
    else:
        return redirect(url_for('home'))


@app.route('/mentor_students/<int:mentor_id>/add_student', methods=['POST', 'GET'])
def add_student_to_mentor(mentor_id):
    if 'username' in session and session['username']:
        if request.method == 'POST':
            p_student_name = request.form['student_name']
            p_mobile = request.form['mobile']
            p_email = request.form['email']
            p_address = request.form['address']
            p_dob = request.form['dob']
            p_bloodgp = request.form['bloodgp']
            p_program = request.form['program']
            p_semester = request.form['semester']
            p_section = request.form['section']
            p_father_name = request.form['father_name']
            p_f_mobile = request.form['father_mobile']
            p_f_email = request.form['father_email']
            p_mother_name = request.form['mother_name']
            p_m_mobile = request.form['mother_mobile']
            p_m_email = request.form['mother_email']

            try:
                # Use 'with' statement to automatically close the cursor
                with mysql.connection.cursor() as cursor:
                    # Execute a simple query to clear the result set
                    cursor.execute("SELECT 1")

                    # Call the AddStudentProcedure to add a student to the mentor
                    cursor.callproc('AddStudentProcedure', (
                        session['username'], 'password_placeholder',
                        p_student_name, p_mobile, p_email, p_address, p_dob, p_bloodgp,
                        p_program, p_semester, p_section,
                        p_father_name, p_f_mobile, p_f_email,
                        p_mother_name, p_m_mobile, p_m_email,
                        mentor_id  # Pass the mentor_id to the procedure
                    ))

                mysql.connection.commit()
                flash("Student added successfully.")

            except Exception as e:
                print(f"SQL ERROR: {str(e)}")
                flash(f"An error occurred: {str(e)}")
                # Add more detailed error logging if needed

        return redirect(url_for('admin_home'))

    return redirect(url_for('home'))





@app.route('/mentor_home', methods=['GET'])
def mentor_home():
    if 'username' in session and session['username']:
        if 'mentor_id' in session:
            mentor_id = session['mentor_id']
            cursor = mysql.connection.cursor()

            # Fetch students, their profiles, and feedbacks
            cursor.execute("""
                SELECT 
                    S.Student_id, 
                    S.Student_name, 
                    S.S_mobile, 
                    S.Student_email, 
                    S.Student_address, 
                    S.Student_dob, 
                    S.Student_bloodgp, 
                    S.Mentor_id,
                    P.Student_program,
                    P.Student_Sem,
                    P.Student_sec,
                    P.Father_name,
                    P.F_mobile,
                    P.F_email,
                    P.Mother_name,
                    P.M_mobile,
                    P.M_email,
                    F.feedback_text,
                    F.fees_paid,
                    F.issues,
                    F.achievements,
                    F.backlogs,
                    F.remarks,
                    F.submission_date
                FROM STUDENT S
                LEFT JOIN PROFILE P ON S.Student_id = P.Std_id
                LEFT JOIN FEEDBACK F ON S.Student_id = F.Student_id
                WHERE S.Mentor_id = %s
            """, (mentor_id,))
            
            students_data = cursor.fetchall()

            return render_template('mentor_home.html', username=session['username'], students_data=students_data)

        else:
            print("Mentor ID not found in the session. Please log in again.")
            return redirect(url_for('home'))
    return redirect(url_for('home'))



@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form.get('role')

        cursor = mysql.connection.cursor()

        if role == '0':  # Mentor registration
            mentor_name = request.form['mentor_name']
            mentor_mobile = request.form['mentor_mobile']
            mentor_email = request.form['mentor_email']
            mentor_address = request.form['mentor_address']

            password_hash = hashlib.md5(password.encode()).hexdigest()

            cursor.execute("INSERT INTO users (username, password, is_admin) VALUES (%s, %s, 0)", (username, password_hash))
            mysql.connection.commit()

            user_id = cursor.lastrowid

            cursor.execute("INSERT INTO MENTOR (Mentor_name, Mentor_mobile, Mentor_email, Mentor_address, User_id) VALUES (%s, %s, %s, %s, %s)",
                           (mentor_name, mentor_mobile, mentor_email, mentor_address, user_id))
            mysql.connection.commit()

            return "Mentor registration successful! <a href='/login'>Log in</a>"
        
        elif role == '1':  # Admin registration
            # Hash the password before storing it in the database
            mentor_name = request.form['mentor_name']
            mentor_mobile = request.form['mentor_mobile']
            mentor_email = request.form['mentor_email']
            mentor_address = request.form['mentor_address']
            
            password_hash = hashlib.md5(password.encode()).hexdigest()

            cursor.execute("INSERT INTO users (username, password, is_admin) VALUES (%s, %s, 1)", (username, password_hash))
            mysql.connection.commit()

            user_id = cursor.lastrowid

            cursor.execute("INSERT INTO MENTOR (Mentor_name, Mentor_mobile, Mentor_email, Mentor_address, User_id) VALUES (%s, %s, %s, %s, %s)",
                           (mentor_name, mentor_mobile, mentor_email, mentor_address, user_id))
            mysql.connection.commit()
            
            return "Admin registration successful! <a href='/login'>Log in</a>"

        else:
            return "Invalid role selected. Please choose a valid role."

    return render_template('register.html')


@app.route('/update_fee', methods=['POST'])
def update_fee():
    if 'username' in session and session['username']:
        cursor = mysql.connection.cursor()

        try:
            # Retrieve form data
            amount = request.form['amount']
            due_date = request.form['due_date']
            std_id = request.form['std_id']
            fee_id = request.form['fee_id']

            # Update fee
            cursor.execute("UPDATE fees SET Amount = %s, Due_Date = %s WHERE Fee_id = %s", (amount, due_date, fee_id))
            mysql.connection.commit()

            flash('Fee updated successfully!', 'success')

        except Exception as e:
            flash(f"An error occurred: {str(e)}", 'error')

        return redirect(url_for('admin_home'))  # Replace with the actual mentor_id

    return redirect(url_for('home'))


'''

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    if 'username' in session and session['username']:
        if request.method == 'POST':
            student_id = request.form['student_id']
            feedback_text = request.form['feedback_text']
            admin_only = 'admin_only' in request.form  # Set to True if checkbox is checked, False otherwise
            mentor_feedback = 'mentor' in request.form  # Set to True if checkbox is checked, False otherwise

            cursor = mysql.connection.cursor()

            try:
                # Check if feedback already exists for the student
                cursor.execute("SELECT * FROM feedback WHERE student_id = %s", (student_id,))
                existing_feedback = cursor.fetchone()

                if existing_feedback:
                    # Feedback exists, update it
                    cursor.execute("UPDATE feedback SET feedback_text = %s, admin_only = %s, mentor_feedback = %s "
                                   "WHERE student_id = %s",
                                   (hash_text(feedback_text) if admin_only else feedback_text,
                                    admin_only, mentor_feedback, student_id))
                else:
                    # Feedback doesn't exist, insert it
                    cursor.execute("INSERT INTO feedback (student_id, feedback_text, admin_only, mentor_feedback) "
                                   "VALUES (%s, %s, %s, %s)",
                                   (student_id, hash_text(feedback_text) if admin_only else feedback_text,
                                    admin_only, mentor_feedback))

                mysql.connection.commit()

                flash('Feedback submitted successfully!')

            except Exception as e:
                print(f"SQL Error: {str(e)}")
                flash(f"An error occurred while submitting feedback: {str(e)}")

            finally:
                cursor.close()

    # Render the mentor_home template with the updated data
    return render_template('submitted_feedback.html', username=session['username'])
'''

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    if 'username' in session and session['username']:
        if request.method == 'POST':
            student_id = request.form['student_id']
            feedback_text = request.form['feedback_text']
            fees_paid = request.form['fees_paid']
            issues = request.form['issues']
            achievements = request.form['achievements']
            backlogs = request.form['backlogs']
            remarks = request.form['remarks']

            cursor = mysql.connection.cursor()

            try:
                # Check if feedback already exists for the student
                cursor.execute("SELECT * FROM feedback WHERE student_id = %s", (student_id,))
                existing_feedback = cursor.fetchone()

                if existing_feedback:
                    # Feedback exists, update it
                    cursor.execute("""
                        UPDATE feedback
                        SET feedback_text = %s, fees_paid = %s, issues = %s, achievements = %s, backlogs = %s, remarks = %s
                        WHERE student_id = %s
                    """, (feedback_text, fees_paid, issues, achievements, backlogs, remarks, student_id))
                else:
                    # Feedback doesn't exist, insert it
                    cursor.execute("""
                        INSERT INTO feedback (student_id, feedback_text, fees_paid, issues, achievements, backlogs, remarks)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (student_id, feedback_text, fees_paid, issues, achievements, backlogs, remarks))

                mysql.connection.commit()

                flash('Feedback submitted successfully!')

            except Exception as e:
                print(f"SQL Error: {str(e)}")
                flash(f"An error occurred while submitting feedback: {str(e)}")

            finally:
                cursor.close()

    # Render the mentor_home template with the updated data
    return render_template('submitted_feedback.html', username=session['username'])



# Function to fetch all submitted feedback (replace this with your actual logic)


@app.route('/fees/<int:student_id>')
def fees(student_id):
    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT * FROM fees
        WHERE Std_id = %s
    """, (student_id,))
    fees_data = cursor.fetchone()
    return render_template('fees.html', username=session['username'], student_id=student_id, fees_data=fees_data)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
