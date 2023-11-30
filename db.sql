-- Drop the database if it exists
DROP DATABASE IF EXISTS user_management;

-- Create a new database and use it
CREATE DATABASE user_management;
USE user_management;

-- Create the 'users' table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Add an 'is_admin' column to the 'users' table
ALTER TABLE users ADD is_admin TINYINT(1) NOT NULL DEFAULT 0;

ALTER TABLE users
ADD UNIQUE (username);

-- Create the 'MENTOR' table
CREATE TABLE MENTOR (
    Mentor_id INT AUTO_INCREMENT PRIMARY KEY,
    Mentor_name VARCHAR(25),
    Mentor_mobile BIGINT NOT NULL,
    Mentor_email VARCHAR(20),
    Mentor_address VARCHAR(100),
    User_id INT,
    CONSTRAINT fk_mentor_user_id
    FOREIGN KEY (User_id)
    REFERENCES users (id) ON DELETE CASCADE
);

CREATE TABLE STUDENT (
    Student_id INT AUTO_INCREMENT PRIMARY KEY,
    Student_name VARCHAR(25),
    S_mobile BIGINT NOT NULL,
    Student_email VARCHAR(20),
    Student_address VARCHAR(100),
    Student_dob DATE,
    Student_bloodgp VARCHAR(5),
    Mentor_id INT,
    CONSTRAINT fk_student_mentor_id
    FOREIGN KEY (Mentor_id)
    REFERENCES MENTOR (Mentor_id) ON DELETE SET NULL
);

DELIMITER //
CREATE TRIGGER CheckStudentDob
BEFORE INSERT ON STUDENT
FOR EACH ROW
BEGIN
    IF NEW.Student_dob > CURDATE() THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Student date of birth cannot be in the future.';
    END IF;
END;
//
DELIMITER ;

-- Create the 'PROFILE' table
CREATE TABLE PROFILE (
    Std_id INT,
    Student_name VARCHAR(25),
    Student_program VARCHAR(50),
    Student_Sem VARCHAR(15),
    Student_sec VARCHAR(12),
    Father_name VARCHAR(25),
    F_mobile BIGINT,
    F_email VARCHAR(30),
    Mother_name VARCHAR(25),
    M_mobile BIGINT,
    M_email VARCHAR(30),
    CONSTRAINT fk_profile_std_id
    FOREIGN KEY (Std_id)
    REFERENCES STUDENT (Student_id),
    CHECK (F_email REGEXP '^[A-Za-z0-9+_.-]+@(.+)$'),
    CHECK (M_email REGEXP '^[A-Za-z0-9+_.-]+@(.+)$')
);

-- Create the 'COURSES' table
CREATE TABLE COURSES (
    Course_id INT PRIMARY KEY,
    Course_name VARCHAR(25),
    Course_desc VARCHAR(100),
    Course_stu_id INT,
    CONSTRAINT fk_course_stu_id
    FOREIGN KEY (Course_stu_id)
    REFERENCES STUDENT (Student_id)
);

-- Create the 'RESULTS' table
CREATE TABLE RESULTS (
    Result_grade CHAR(2),
    Result_remark VARCHAR(100),
    Course_result_id INT,
    Student_result_id INT,
    CONSTRAINT fk1_results_course_id
    FOREIGN KEY (Course_result_id)
    REFERENCES COURSES (Course_id),
    CONSTRAINT fk2_results_student_id
    FOREIGN KEY (Student_result_id)
    REFERENCES STUDENT (Student_id)
);

-- Create the 'FEES' table
CREATE TABLE FEES (
    Fee_id INT AUTO_INCREMENT PRIMARY KEY,
    Std_id INT,
    Amount DECIMAL(10, 2) NOT NULL,
    Status VARCHAR(10) NOT NULL,
    Due_Date DATE NOT NULL,
    CONSTRAINT fk_fees_std_id
    FOREIGN KEY (Std_id)
    REFERENCES STUDENT (Student_id)
);

-- Create the 'MENTOR_MENTEE' table
CREATE TABLE MENTOR_MENTEE (
    Mentee_id INT,
    Fees_Paid ENUM('YES', 'NO'),
    Issues TEXT,
    Achievements TEXT,
    Backlogs TEXT,
    Remarks TEXT,
    Interaction_Date DATE,
    CONSTRAINT fk_mentor_mentee_mentee_id
    FOREIGN KEY (Mentee_id)
    REFERENCES STUDENT (Student_id)
);



INSERT INTO users (username, password,is_admin) VALUES ('user1', 'password1',0);
INSERT INTO users (username, password,is_admin) VALUES ('user2', 'password2',0);
INSERT INTO users (username, password,is_admin) VALUES ('user3', 'password3',0);
INSERT INTO users (username, password) VALUES ('user4', 'password4');
INSERT INTO users (username, password) VALUES ('user5', 'password5');



INSERT INTO MENTOR (Mentor_id, Mentor_name, Mentor_mobile, Mentor_email, Mentor_address)VALUES (1, 'Mentor 1', 9876543210, 'mentor1@example.com', '123 Mentor St');
INSERT INTO MENTOR (Mentor_id, Mentor_name, Mentor_mobile, Mentor_email, Mentor_address)VALUES (2, 'Mentor 2', 1234567890, 'mentor2@example.com', '456 Mentor St');
INSERT INTO MENTOR (Mentor_id, Mentor_name, Mentor_mobile, Mentor_email, Mentor_address)VALUES (3, 'Mentor 3', 14567567890, 'mentor3@example.com', '789 Mentor St');


INSERT INTO STUDENT (Student_id, Student_name, S_mobile, Student_email, Student_address, Student_dob, Student_bloodgp,Mentor_id)VALUES (1, 'John Doe', 1234567890, 'john@example.com', '123 Main St', '2000-01-01', 'AB',1);
INSERT INTO STUDENT (Student_id, Student_name, S_mobile, Student_email, Student_address, Student_dob, Student_bloodgp,Mentor_id)VALUES (2, 'Jane Smith', 9876543210, 'jane@example.com', '456 Elm St', '1999-02-15', 'O',2);
INSERT INTO STUDENT (Student_id, Student_name, S_mobile, Student_email, Student_address, Student_dob, Student_bloodgp, Mentor_id)VALUES (3, 'Alice Johnson', 5551234567, 'alice@example.com', '789 Oak St', '2001-05-20', 'A', 1);
INSERT INTO STUDENT (Student_id, Student_name, S_mobile, Student_email, Student_address, Student_dob, Student_bloodgp, Mentor_id)VALUES (4, 'Bob Wilson', 8889876543, 'bob@example.com', '321 Pine St', '2002-03-10', 'B', 1);
--INSERT INTO STUDENT (Student_id, Student_name, S_mobile, Student_email, Student_address, Student_dob, Student_bloodgp, Mentor_id)VALUES (5, 'Eva Davis', 7775678901, 'eva@example.com', '654 Cedar St', '2001-08-05', 'O', 2);
--INSERT INTO STUDENT (Student_id, Student_name, S_mobile, Student_email, Student_address, Student_dob, Student_bloodgp,Mentor_id)VALUES (1, 'Joe', 123452190, 'joe@example.com', '12 Main rd', '2001-11-01', 'A',4);

INSERT INTO PROFILE (Std_id, Student_name, Student_program, Student_Sem, Student_sec, Father_name, F_mobile, F_email, Mother_name, M_mobile, M_email)VALUES (1, 'John Doe', 'Computer Science', '4th Semester', 'Section A', 'Robert Doe', 1234567890, 'robert@example.com', 'Lisa Doe', 9876543210, 'lisa@example.com');
INSERT INTO PROFILE (Std_id, Student_name, Student_program, Student_Sem, Student_sec, Father_name, F_mobile, F_email, Mother_name, M_mobile, M_email)VALUES (2, 'Jane Smith', 'Electrical Engineering', '3rd Semester', 'Section B', 'Bob Smith', 9876543210, 'bob@example.com', 'Carol Smith', 1234567890, 'carol@example.com');

INSERT INTO PROFILE (Std_id, Student_name, Student_program, Student_Sem, Student_sec, Father_name, F_mobile, F_email, Mother_name, M_mobile, M_email)VALUES (3, 'Alice Johnson', 'Mathematics', '2nd Semester', 'Section C', 'John Johnson', 5552223333, 'john@example.com', 'Linda Johnson', 4447778888, 'linda@example.com');

INSERT INTO PROFILE (Std_id, Student_name, Student_program, Student_Sem, Student_sec, Father_name, F_mobile, F_email, Mother_name, M_mobile, M_email)VALUES (4, 'Bob Wilson', 'Physics', '3rd Semester', 'Section A', 'David Wilson', 8883332222, 'david@example.com', 'Emily Wilson', 9996663333, 'emily@example.com');

INSERT INTO PROFILE (Std_id, Student_name, Student_program, Student_Sem, Student_sec, Father_name, F_mobile, F_email, Mother_name, M_mobile, M_email)VALUES (5, 'Eva Davis', 'Chemistry', '2nd Semester', 'Section B', 'Michael Davis', 7778889999, 'michael@example.com', 'Susan Davis', 8889990000, 'susan@example.com');


INSERT INTO COURSES (Course_id, Course_name, Course_desc, Course_stu_id)VALUES (1, 'Course 1', 'Description for Course 1', 1);
INSERT INTO COURSES (Course_id, Course_name, Course_desc, Course_stu_id)VALUES (2, 'Course 2', 'Description for Course 2', 2);



INSERT INTO RESULTS (Result_grade, Result_remark, Course_result_id, Student_result_id)VALUES ('A', 'Excellent performance', 1, 1);
INSERT INTO RESULTS (Result_grade, Result_remark, Course_result_id, Student_result_id)VALUES ('B', 'Good progress', 1, 2);


-- Create a trigger for updating fees status to 'UNPAID' if due date is crossed
DELIMITER $$

CREATE TRIGGER UpdateFeesStatus
BEFORE INSERT ON FEES
FOR EACH ROW
BEGIN
    IF NEW.Due_Date < CURDATE() THEN
        SET NEW.Status = 'UNPAID';
    END IF;
END$$

DELIMITER ;


DELIMITER $$

CREATE PROCEDURE AddStudentProcedure(
    IN p_username VARCHAR(255),
    IN p_password VARCHAR(255),
    IN p_student_name VARCHAR(25),
    IN p_mobile INT,
    IN p_email VARCHAR(20),
    IN p_address VARCHAR(100),
    IN p_dob DATE,
    IN p_bloodgp VARCHAR(5),
    IN p_program VARCHAR(255),
    IN p_semester VARCHAR(255),
    IN p_section VARCHAR(255),
    IN p_father_name VARCHAR(255),
    IN p_f_mobile VARCHAR(255),
    IN p_f_email VARCHAR(255),
    IN p_mother_name VARCHAR(255),
    IN p_m_mobile VARCHAR(255),
    IN p_m_email VARCHAR(255),
    IN p_mentor_id INT
)
BEGIN
    DECLARE admin_check INT;

    -- Check if the user executing the procedure is an admin
    SELECT is_admin INTO admin_check FROM users WHERE username = p_username LIMIT 1;

    IF admin_check = 1 THEN
        -- This user is an admin, so add the student
        INSERT INTO STUDENT (Student_name, S_mobile, Student_email, Student_address, Student_dob, Student_bloodgp, Mentor_id)
        VALUES (p_student_name, p_mobile, p_email, p_address, p_dob, p_bloodgp, p_mentor_id); -- Use the provided mentor_id

        -- Get the student_id of the newly added student
        SELECT LAST_INSERT_ID() INTO @student_id;

        -- Insert data into the profile table
        INSERT INTO profile (Std_id, Student_program, Student_Sem, Student_sec, Father_name, F_mobile, F_email, Mother_name, M_mobile, M_email)
        VALUES (@student_id, p_program, p_semester, p_section, p_father_name, p_f_mobile, p_f_email, p_mother_name, p_m_mobile, p_m_email);

        SELECT 'Student added by admin.';
    ELSE
        SELECT 'User does not have admin privileges.';
    END IF;
END $$

DELIMITER ;






DELIMITER $$
CREATE PROCEDURE DeleteMentorProcedure(IN p_username VARCHAR(255), IN p_mentor_id INT, OUT result_message VARCHAR(255))
BEGIN
    DECLARE admin_check INT;
    -- Check if the user executing the procedure is an admin
    SELECT is_admin INTO admin_check FROM users WHERE username = p_username LIMIT 1;
    IF admin_check = 1 THEN
        -- This user is an admin, so delete the mentor
        DELETE FROM MENTOR WHERE Mentor_id = p_mentor_id;
        -- Set the Mentor_id in the students table to NULL for students assigned to the deleted mentor
        UPDATE STUDENT SET Mentor_id = NULL WHERE Mentor_id = p_mentor_id;
        SET result_message = 'Mentor deleted by admin.';
    ELSE
        SET result_message = 'User does not have admin privileges.';
    END IF;
END $$

DELIMITER ;

DELIMITER $$


CREATE PROCEDURE AssignMentorToStudentProcedure(IN p_username VARCHAR(255), IN p_password VARCHAR(255), IN p_student_id INT, IN p_mentor_id INT)
BEGIN
    DECLARE admin_check INT;
    DECLARE mentor_student_count INT;

    -- Check if the user executing the procedure is an admin
    SELECT is_admin INTO admin_check FROM users WHERE username = p_username;

    IF admin_check = 1 THEN
        -- This user is an admin, check the number of students assigned to the mentor
        SELECT COUNT(*) INTO mentor_student_count FROM STUDENT WHERE Mentor_id = p_mentor_id;

        IF mentor_student_count < 2 THEN
            -- Assign the mentor to the student
            UPDATE STUDENT SET Mentor_id = p_mentor_id WHERE Student_id = p_student_id;
            SELECT 'Mentor assigned to student by admin.';
        ELSE
            SELECT 'The selected mentor already has the maximum number of students assigned.';
        END IF;
    ELSE
        SELECT 'User does not have admin privileges.';
    END IF;
END $$
DELIMITER ;


DELIMITER $$

CREATE TRIGGER update_fee_status
BEFORE UPDATE ON fees
FOR EACH ROW
BEGIN
    IF NEW.Due_Date < CURDATE() THEN
        SET NEW.Status = 'Unpaid';
    END IF;
END $$

DELIMITER ;


CREATE TABLE feedback (
    feedback_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    feedback_text TEXT,
    fees_paid ENUM('YES', 'NO'),
    issues TEXT,
    achievements TEXT,
    backlogs TEXT,
    remarks TEXT,
    submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES student(Student_id)
);

