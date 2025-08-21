-- Create Database
CREATE DATABASE RoutineManagement;
USE RoutineManagement;

-- Department
CREATE TABLE DEPARTMENT (
    department_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    building_no VARCHAR(10),
    department_code VARCHAR(10) UNIQUE -- Added for teacher ID generation (e.g., 'BEI', 'BCT')
);

-- Semester
CREATE TABLE SEMESTER (
    semester_id INT AUTO_INCREMENT PRIMARY KEY,
    semester_name VARCHAR(20) NOT NULL
);

-- Student
CREATE TABLE STUDENT (
    student_id VARCHAR(20) PRIMARY KEY,
    first_name VARCHAR(20) NOT NULL,
    last_name VARCHAR(20) NOT NULL,
    address VARCHAR(50),
    phone_number VARCHAR(15),
    guardian_name VARCHAR(30),
    department_id INT,
    semester_id INT,
    FOREIGN KEY (department_id) REFERENCES DEPARTMENT(department_id),
    FOREIGN KEY (semester_id) REFERENCES SEMESTER(semester_id)
);

-- Teacher (Modified to use custom teacher IDs)
CREATE TABLE TEACHER (
    teacher_id VARCHAR(20) PRIMARY KEY, -- Changed to VARCHAR for custom IDs like 'teacherbei1'
    first_name VARCHAR(20) NOT NULL,
    last_name VARCHAR(20) NOT NULL,
    email VARCHAR(50) UNIQUE,
    phone_number VARCHAR(15),
    department_id INT,
    FOREIGN KEY (department_id) REFERENCES DEPARTMENT(department_id)
);

-- Course
CREATE TABLE COURSE (
    course_id INT AUTO_INCREMENT PRIMARY KEY,
    course_name VARCHAR(50) NOT NULL,
    department_id INT,
    semester_id INT,
    FOREIGN KEY (department_id) REFERENCES DEPARTMENT(department_id),
    FOREIGN KEY (semester_id) REFERENCES SEMESTER(semester_id)
);

-- Subject
CREATE TABLE SUBJECT (
    subject_id INT AUTO_INCREMENT PRIMARY KEY,
    subject_name VARCHAR(50) NOT NULL,
    course_id INT,
    teacher_id VARCHAR(20), -- Updated to match TEACHER.teacher_id
    FOREIGN KEY (course_id) REFERENCES COURSE(course_id),
    FOREIGN KEY (teacher_id) REFERENCES TEACHER(teacher_id)
);

-- Classrooms
CREATE TABLE CLASS (
    class_id INT AUTO_INCREMENT PRIMARY KEY,
    room_no VARCHAR(20) NOT NULL,
    building_no VARCHAR(10),
    capacity INT
);

-- Weekly routine
CREATE TABLE FIXEDROUTINE (
    routine_id INT AUTO_INCREMENT PRIMARY KEY,
    subject_id INT,
    teacher_id VARCHAR(20), -- Updated to match TEACHER.teacher_id
    class_id INT,
    semester_id INT,
    day_of_week ENUM('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'),
    start_time TIME,
    end_time TIME,
    FOREIGN KEY (subject_id) REFERENCES SUBJECT(subject_id),
    FOREIGN KEY (teacher_id) REFERENCES TEACHER(teacher_id),
    FOREIGN KEY (class_id) REFERENCES CLASS(class_id),
    FOREIGN KEY (semester_id) REFERENCES SEMESTER(semester_id)
);

-- Daily routine (overrides)
CREATE TABLE DAILYROUTINE (
    daily_routine_id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    subject_id INT,
    teacher_id VARCHAR(20), -- Updated to match TEACHER.teacher_id
    class_id INT,
    semester_id INT,
    start_time TIME,
    end_time TIME,
    status ENUM('Scheduled','Rescheduled','Cancelled') DEFAULT 'Scheduled',
    FOREIGN KEY (subject_id) REFERENCES SUBJECT(subject_id),
    FOREIGN KEY (teacher_id) REFERENCES TEACHER(teacher_id),
    FOREIGN KEY (class_id) REFERENCES CLASS(class_id),
    FOREIGN KEY (semester_id) REFERENCES SEMESTER(semester_id)
);

-- Teacher unavailability
CREATE TABLE TeacherUnavailability (
    unavailability_id INT AUTO_INCREMENT PRIMARY KEY,
    teacher_id VARCHAR(20), -- Updated to match TEACHER.teacher_id
    unavailable_date DATE,
    start_time TIME,
    end_time TIME,
    reason VARCHAR(100),
    FOREIGN KEY (teacher_id) REFERENCES TEACHER(teacher_id)
);
