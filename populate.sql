-- Insert Departments with codes
INSERT INTO DEPARTMENT (name, building_no, department_code) VALUES
('Bachelor of Engineering in Information', 'A', 'BEI'),
('Bachelor of Computer Technology', 'B', 'BCT'),
('Bachelor of Civil Engineering', 'C', 'BCE'),
('Bachelor of Electronics Engineering', 'D', 'BEE');

-- Insert Semesters
INSERT INTO SEMESTER (semester_name) VALUES
('First Semester'),
('Second Semester'),
('Third Semester'),
('Fourth Semester'),
('Fifth Semester'),
('Sixth Semester'),
('Seventh Semester'),
('Eighth Semester');

-- Insert Sample Teachers with custom IDs
INSERT INTO TEACHER (teacher_id, first_name, last_name, email, phone_number, department_id) VALUES
('teacherbei1', 'John', 'Smith', 'john.smith@college.edu', '+977-9841234567', 1),
('teacherbei2', 'Sarah', 'Johnson', 'sarah.johnson@college.edu', '+977-9841234568', 1),
('teacherbct1', 'Michael', 'Brown', 'michael.brown@college.edu', '+977-9841234569', 2),
('teacherbct2', 'Emily', 'Davis', 'emily.davis@college.edu', '+977-9841234570', 2),
('teacherbce1', 'David', 'Wilson', 'david.wilson@college.edu', '+977-9841234571', 3),
('teacherbee1', 'Lisa', 'Anderson', 'lisa.anderson@college.edu', '+977-9841234572', 4);

-- Insert Sample Classes
INSERT INTO CLASS (room_no, building_no, capacity) VALUES
('101', 'A', 40),
('102', 'A', 45),
('201', 'B', 50),
('202', 'B', 35),
('301', 'C', 60);

-- Insert Sample Courses
INSERT INTO COURSE (course_name, department_id, semester_id) VALUES
('Programming Fundamentals', 1, 1),
('Data Structures', 1, 2),
('Web Development', 2, 3),
('Database Systems', 2, 4),
('Structural Engineering', 3, 3),
('Digital Electronics', 4, 2);

-- Insert Sample Subjects
INSERT INTO SUBJECT (subject_name, course_id, teacher_id) VALUES
('C Programming', 1, 'teacherbei1'),
('Python Programming', 1, 'teacherbei2'),
('Algorithms', 2, 'teacherbei1'),
('HTML/CSS', 3, 'teacherbct1'),
('JavaScript', 3, 'teacherbct2'),
('MySQL', 4, 'teacherbct1'),
('Concrete Design', 5, 'teacherbce1'),
('Digital Logic', 6, 'teacherbee1');

-- Insert Sample Students
INSERT INTO STUDENT (student_id, first_name, last_name, address, phone_number, guardian_name, department_id, semester_id) VALUES
('079bei005', 'Sujan', 'Shrestha', 'Kathmandu', '9841000001', 'Ram Shrestha', 1, 1),
('079bct002', 'Pratik', 'Karki', 'Lalitpur', '9841000002', 'Sita Karki', 2, 1),
('079bei007', 'Bibek', 'Ghimire', 'Bhaktapur', '9841000003', 'Hari Ghimire', 1, 2),
('079bct009', 'Aashish', 'Basnet', 'Pokhara', '9841000004', 'Maya Basnet', 2, 2),
('079bce003', 'Santoshi', 'Sharma', 'Biratnagar', '9841000005', 'Ramesh Sharma', 3, 1),
('079bee001', 'Pramila', 'Tamang', 'Dharan', '9841000006', 'Gopal Tamang', 4, 1),
('079bei010', 'Rupesh', 'Thapa', 'Butwal', '9841000007', 'Manju Thapa', 1, 3),
('079bct011', 'Sandhya', 'Shrestha', 'Janakpur', '9841000008', 'Bishnu Shrestha', 2, 3),
('079bce005', 'Rajan', 'Yadav', 'Birgunj', '9841000009', 'Sunita Yadav', 3, 2),
('079bee003', 'Sushil', 'Lama', 'Hetauda', '9841000010', 'Kamal Lama', 4, 2);

INSERT INTO FIXEDROUTINE (subject_id, teacher_id, class_id, semester_id, day_of_week, start_time, end_time) VALUES

-- ========== SUNDAY ==========
-- Class 1 (Room 101, Building A)
(1, 'teacherbei1', 1, 1, 'Sunday', '09:00:00', '10:30:00'),    -- C Programming
(3, 'teacherbei1', 1, 2, 'Sunday', '10:45:00', '12:15:00'),   -- Algorithms
(1, 'teacherbei1', 1, 1, 'Sunday', '13:00:00', '14:30:00'),   -- C Programming
(3, 'teacherbei1', 1, 2, 'Sunday', '14:45:00', '16:15:00'),   -- Algorithms

-- Class 2 (Room 102, Building A)
(2, 'teacherbei2', 2, 1, 'Sunday', '09:00:00', '10:30:00'),   -- Python Programming
(8, 'teacherbee1', 2, 2, 'Sunday', '10:45:00', '12:15:00'),   -- Digital Logic
(2, 'teacherbei2', 2, 1, 'Sunday', '13:00:00', '14:30:00'),   -- Python Programming
(8, 'teacherbee1', 2, 2, 'Sunday', '14:45:00', '16:15:00'),   -- Digital Logic

-- ========== MONDAY ==========
-- Class 1 (Room 101, Building A)
(4, 'teacherbct1', 1, 3, 'Monday', '09:00:00', '10:30:00'),   -- HTML/CSS
(6, 'teacherbct1', 1, 4, 'Monday', '10:45:00', '12:15:00'),   -- MySQL
(1, 'teacherbei1', 1, 1, 'Monday', '13:00:00', '14:30:00'),   -- C Programming
(7, 'teacherbce1', 1, 3, 'Monday', '14:45:00', '16:15:00'),   -- Concrete Design

-- Class 2 (Room 102, Building A)
(5, 'teacherbct2', 2, 3, 'Monday', '09:00:00', '10:30:00'),   -- JavaScript
(2, 'teacherbei2', 2, 1, 'Monday', '10:45:00', '12:15:00'),   -- Python Programming
(8, 'teacherbee1', 2, 2, 'Monday', '13:00:00', '14:30:00'),   -- Digital Logic
(5, 'teacherbct2', 2, 3, 'Monday', '14:45:00', '16:15:00'),   -- JavaScript

-- ========== TUESDAY ==========
-- Class 1 (Room 101, Building A)
(3, 'teacherbei1', 1, 2, 'Tuesday', '09:00:00', '10:30:00'),  -- Algorithms
(4, 'teacherbct1', 1, 3, 'Tuesday', '10:45:00', '12:15:00'),  -- HTML/CSS
(6, 'teacherbct1', 1, 4, 'Tuesday', '13:00:00', '14:30:00'),  -- MySQL
(1, 'teacherbei1', 1, 1, 'Tuesday', '14:45:00', '16:15:00'),  -- C Programming

-- Class 2 (Room 102, Building A)
(2, 'teacherbei2', 2, 1, 'Tuesday', '09:00:00', '10:30:00'),  -- Python Programming
(7, 'teacherbce1', 2, 3, 'Tuesday', '10:45:00', '12:15:00'),  -- Concrete Design
(5, 'teacherbct2', 2, 3, 'Tuesday', '13:00:00', '14:30:00'),  -- JavaScript
(8, 'teacherbee1', 2, 2, 'Tuesday', '14:45:00', '16:15:00'),  -- Digital Logic

-- ========== WEDNESDAY ==========
-- Class 1 (Room 101, Building A)
(1, 'teacherbei1', 1, 1, 'Wednesday', '09:00:00', '10:30:00'), -- C Programming
(3, 'teacherbei1', 1, 2, 'Wednesday', '10:45:00', '12:15:00'), -- Algorithms
(4, 'teacherbct1', 1, 3, 'Wednesday', '13:00:00', '14:30:00'), -- HTML/CSS
(7, 'teacherbce1', 1, 3, 'Wednesday', '14:45:00', '16:15:00'), -- Concrete Design

-- Class 2 (Room 102, Building A)
(5, 'teacherbct2', 2, 3, 'Wednesday', '09:00:00', '10:30:00'), -- JavaScript
(2, 'teacherbei2', 2, 1, 'Wednesday', '10:45:00', '12:15:00'), -- Python Programming
(8, 'teacherbee1', 2, 2, 'Wednesday', '13:00:00', '14:30:00'), -- Digital Logic
(6, 'teacherbct1', 2, 4, 'Wednesday', '14:45:00', '16:15:00'), -- MySQL

-- ========== THURSDAY ==========
-- Class 1 (Room 101, Building A)
(6, 'teacherbct1', 1, 4, 'Thursday', '09:00:00', '10:30:00'),  -- MySQL
(1, 'teacherbei1', 1, 1, 'Thursday', '10:45:00', '12:15:00'),  -- C Programming
(3, 'teacherbei1', 1, 2, 'Thursday', '13:00:00', '14:30:00'),  -- Algorithms
(4, 'teacherbct1', 1, 3, 'Thursday', '14:45:00', '16:15:00'),  -- HTML/CSS

-- Class 2 (Room 102, Building A)
(2, 'teacherbei2', 2, 1, 'Thursday', '09:00:00', '10:30:00'),  -- Python Programming
(5, 'teacherbct2', 2, 3, 'Thursday', '10:45:00', '12:15:00'),  -- JavaScript
(7, 'teacherbce1', 2, 3, 'Thursday', '13:00:00', '14:30:00'),  -- Concrete Design
(8, 'teacherbee1', 2, 2, 'Thursday', '14:45:00', '16:15:00'),  -- Digital Logic

-- ========== FRIDAY ==========
-- Class 1 (Room 101, Building A)
(1, 'teacherbei1', 1, 1, 'Friday', '09:00:00', '10:30:00'),    -- C Programming
(7, 'teacherbce1', 1, 3, 'Friday', '10:45:00', '12:15:00'),    -- Concrete Design
(6, 'teacherbct1', 1, 4, 'Friday', '13:00:00', '14:30:00'),    -- MySQL
(3, 'teacherbei1', 1, 2, 'Friday', '14:45:00', '16:15:00'),    -- Algorithms

-- Class 2 (Room 102, Building A)
(8, 'teacherbee1', 2, 2, 'Friday', '09:00:00', '10:30:00'),    -- Digital Logic
(2, 'teacherbei2', 2, 1, 'Friday', '10:45:00', '12:15:00'),    -- Python Programming
(5, 'teacherbct2', 2, 3, 'Friday', '13:00:00', '14:30:00'),    -- JavaScript
(4, 'teacherbct1', 2, 3, 'Friday', '14:45:00', '16:15:00');    -- HTML/CSS
