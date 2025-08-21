CREATE VIEW SubjectDetailsView AS
SELECT 
    s.subject_id,
    s.subject_name,
    c.course_name,
    CONCAT(t.first_name, ' ', t.last_name) AS teacher_name,
    t.teacher_id,
    t.email AS teacher_email,
    t.phone_number AS teacher_phone,
    d.name AS department_name,
    d.department_code,
    sem.semester_name
FROM SUBJECT s
JOIN COURSE c ON s.course_id = c.course_id
JOIN TEACHER t ON s.teacher_id = t.teacher_id
JOIN DEPARTMENT d ON t.department_id = d.department_id
JOIN SEMESTER sem ON c.semester_id = sem.semester_id;

-- 2. Complete Student Records View
CREATE VIEW StudentDetailsView AS
SELECT 
    st.student_id,
    CONCAT(st.first_name, ' ', st.last_name) AS student_name,
    st.address,
    st.phone_number,
    st.guardian_name,
    d.name AS department_name,
    d.department_code,
    d.building_no AS department_building,
    sem.semester_name
FROM STUDENT st
JOIN DEPARTMENT d ON st.department_id = d.department_id
JOIN SEMESTER sem ON st.semester_id = sem.semester_id;

-- 3. Teacher Complete Profile View
CREATE VIEW TeacherDetailsView AS
SELECT 
    t.teacher_id,
    CONCAT(t.first_name, ' ', t.last_name) AS teacher_name,
    t.email,
    t.phone_number,
    d.name AS department_name,
    d.department_code,
    d.building_no,
    COUNT(s.subject_id) AS subjects_taught
FROM TEACHER t
JOIN DEPARTMENT d ON t.department_id = d.department_id
LEFT JOIN SUBJECT s ON t.teacher_id = s.teacher_id
GROUP BY t.teacher_id, t.first_name, t.last_name, t.email, t.phone_number, d.name, d.department_code, d.building_no;

-- 4. Complete Weekly Routine View
CREATE VIEW WeeklyRoutineView AS
SELECT 
    fr.routine_id,
    fr.day_of_week,
    TIME_FORMAT(fr.start_time, '%h:%i %p') AS start_time,
    TIME_FORMAT(fr.end_time, '%h:%i %p') AS end_time,
    s.subject_name,
    CONCAT(t.first_name, ' ', t.last_name) AS teacher_name,
    t.teacher_id,
    CONCAT('Room ', cl.room_no, ', Building ', cl.building_no) AS classroom,
    cl.capacity AS room_capacity,
    sem.semester_name,
    d.name AS department_name,
    c.course_name
FROM FIXEDROUTINE fr
JOIN SUBJECT s ON fr.subject_id = s.subject_id
JOIN TEACHER t ON fr.teacher_id = t.teacher_id
JOIN CLASS cl ON fr.class_id = cl.class_id
JOIN SEMESTER sem ON fr.semester_id = sem.semester_id
JOIN COURSE c ON s.course_id = c.course_id
JOIN DEPARTMENT d ON c.department_id = d.department_id
ORDER BY 
    CASE fr.day_of_week
        WHEN 'Sunday' THEN 1
        WHEN 'Monday' THEN 2
        WHEN 'Tuesday' THEN 3
        WHEN 'Wednesday' THEN 4
        WHEN 'Thursday' THEN 5
        WHEN 'Friday' THEN 6
        WHEN 'Saturday' THEN 7
    END,
    fr.start_time;

-- 5. Daily Routine View (for overrides/changes)
CREATE VIEW DailyRoutineView AS
SELECT 
    dr.daily_routine_id,
    dr.date,
    DAYNAME(dr.date) AS day_name,
    TIME_FORMAT(dr.start_time, '%h:%i %p') AS start_time,
    TIME_FORMAT(dr.end_time, '%h:%i %p') AS end_time,
    s.subject_name,
    CONCAT(t.first_name, ' ', t.last_name) AS teacher_name,
    t.teacher_id,
    CONCAT('Room ', cl.room_no, ', Building ', cl.building_no) AS classroom,
    sem.semester_name,
    d.name AS department_name,
    dr.status
FROM DAILYROUTINE dr
JOIN SUBJECT s ON dr.subject_id = s.subject_id
JOIN TEACHER t ON dr.teacher_id = t.teacher_id
JOIN CLASS cl ON dr.class_id = cl.class_id
JOIN SEMESTER sem ON dr.semester_id = sem.semester_id
JOIN COURSE c ON s.course_id = c.course_id
JOIN DEPARTMENT d ON c.department_id = d.department_id
ORDER BY dr.date DESC, dr.start_time;

-- 6. Classroom Utilization View
CREATE VIEW ClassroomUtilizationView AS
SELECT 
    cl.class_id,
    CONCAT('Room ', cl.room_no, ', Building ', cl.building_no) AS classroom,
    cl.capacity,
    COUNT(fr.routine_id) AS weekly_classes,
    GROUP_CONCAT(DISTINCT fr.day_of_week ORDER BY 
        CASE fr.day_of_week
            WHEN 'Sunday' THEN 1
            WHEN 'Monday' THEN 2
            WHEN 'Tuesday' THEN 3
            WHEN 'Wednesday' THEN 4
            WHEN 'Thursday' THEN 5
            WHEN 'Friday' THEN 6
            WHEN 'Saturday' THEN 7
        END SEPARATOR ', ') AS days_used
FROM CLASS cl
LEFT JOIN FIXEDROUTINE fr ON cl.class_id = fr.class_id
GROUP BY cl.class_id, cl.room_no, cl.building_no, cl.capacity;

-- 7. Teacher Workload View
CREATE VIEW TeacherWorkloadView AS
SELECT 
    t.teacher_id,
    CONCAT(t.first_name, ' ', t.last_name) AS teacher_name,
    d.name AS department_name,
    COUNT(DISTINCT s.subject_id) AS subjects_count,
    COUNT(fr.routine_id) AS weekly_classes,
    GROUP_CONCAT(DISTINCT s.subject_name ORDER BY s.subject_name SEPARATOR ', ') AS subjects_taught,
    GROUP_CONCAT(DISTINCT fr.day_of_week ORDER BY 
        CASE fr.day_of_week
            WHEN 'Sunday' THEN 1
            WHEN 'Monday' THEN 2
            WHEN 'Tuesday' THEN 3
            WHEN 'Wednesday' THEN 4
            WHEN 'Thursday' THEN 5
            WHEN 'Friday' THEN 6
            WHEN 'Saturday' THEN 7
        END SEPARATOR ', ') AS teaching_days
FROM TEACHER t
JOIN DEPARTMENT d ON t.department_id = d.department_id
LEFT JOIN SUBJECT s ON t.teacher_id = s.teacher_id
LEFT JOIN FIXEDROUTINE fr ON t.teacher_id = fr.teacher_id
GROUP BY t.teacher_id, t.first_name, t.last_name, d.name;

-- 8. Department Summary View
CREATE VIEW DepartmentSummaryView AS
SELECT 
    d.department_id,
    d.name AS department_name,
    d.department_code,
    d.building_no,
    COUNT(DISTINCT t.teacher_id) AS teachers_count,
    COUNT(DISTINCT st.student_id) AS students_count,
    COUNT(DISTINCT c.course_id) AS courses_count,
    COUNT(DISTINCT s.subject_id) AS subjects_count
FROM DEPARTMENT d
LEFT JOIN TEACHER t ON d.department_id = t.department_id
LEFT JOIN STUDENT st ON d.department_id = st.department_id
LEFT JOIN COURSE c ON d.department_id = c.department_id
LEFT JOIN SUBJECT s ON c.course_id = s.course_id
GROUP BY d.department_id, d.name, d.department_code, d.building_no;
