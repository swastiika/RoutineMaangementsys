# routine.py
import mysql.connector
from datetime import datetime, timedelta
from tabulate import tabulate
import os
import sys

# ===============================
# DB Connection - update credentials if needed
# ===============================
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",      # change to your MySQL user
        password="PUL079bei",  # change to your MySQL password
        database="RoutineManagement"
    )
    cursor = db.cursor(dictionary=True)
    print("✅ Database connected successfully!")
except mysql.connector.Error as err:
    print(f"❌ Database connection failed: {err}")
    sys.exit(1)

# ===============================
# Utility Functions
# ===============================
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    print("\n" + "="*60)
    print(f"  {title.upper()}")
    print("="*60)

def print_menu(options):
    print("\n📋 MENU:")
    for i, option in enumerate(options, 1):
        print(f"  {i}. {option}")
    print("  0. Back to Main Menu")
    print("-" * 40)

def get_choice(max_choice):
    while True:
        try:
            choice = int(input(f"👉 Enter your choice (0-{max_choice}): "))
            if 0 <= choice <= max_choice:
                return choice
            else:
                print(f"❌ Please enter a number between 0 and {max_choice}")
        except ValueError:
            print("❌ Please enter a valid number")

def print_table(data, title="DATA"):
    if data:
        print(f"\n📊 {title}:")
        print(tabulate(data, headers="keys", tablefmt="grid"))
    else:
        print(f"\n❌ No {title.lower()} found!")

def pause():
    input("\n📱 Press Enter to continue...")

# ===============================
# Student Functions
# ===============================
def student_login():
    print_header("Student Login")
    student_id = input("🆔 Enter your Student ID: ").strip()
    
    cursor.execute("SELECT * FROM StudentDetailsView WHERE student_id = %s", (student_id,))
    student = cursor.fetchone()
    
    if not student:
        print("❌ Student not found!")
        return None
    
    print(f"\n✅ Welcome, {student['student_name']}!")
    print(f"📚 Department: {student['department_name']} ({student['department_code']})")
    print(f"📖 Semester: {student['semester_name']}")
    return student

def student_dashboard(student):
    while True:
        clear_screen()
        print_header(f"Student Dashboard - {student['student_name']}")
        
        options = [
            "View Today's Schedule",
            "View Weekly Routine",
            "View This Week's Schedule", 
            "View My Profile",
            "View My Department Info",
            "View All Teachers",
            "View All Subjects"
        ]
        
        print_menu(options)
        choice = get_choice(len(options))
        
        if choice == 0:
            break
        elif choice == 1:
            view_daily_schedule(student['semester_name'])
        elif choice == 2:
            view_weekly_routine(student['semester_name'])
        elif choice == 3:
            view_week_schedule(student['semester_name'])
        elif choice == 4:
            view_student_profile(student['student_id'])
        elif choice == 5:
            view_department_info(student['department_code'])
        elif choice == 6:
            view_all_teachers()
        elif choice == 7:
            view_all_subjects()
        
        if choice != 0:
            pause()

def view_daily_schedule(semester_name):
    today = datetime.today().date()
    day_name = today.strftime('%A')
    print_header(f"Today's Schedule - {today} ({day_name})")

    # Call stored procedure: pass p_teacher_id = NULL to fetch all teachers
    cursor.execute("CALL sp_get_daily_routine(%s, %s, %s)", (today, semester_name, None))
    rows = cursor.fetchall()
    # consume remaining resultsets
    while cursor.nextset():
        pass

    if rows:
        display = []
        for r in rows:
            display.append({
                'start_time': r.get('start_time'),
                'end_time': r.get('end_time'),
                'subject_name': r.get('subject_name'),
                'teacher_name': r.get('teacher_name'),
                'classroom': r.get('classroom'),
                'status': r.get('status')
            })
        print_table(display, "TODAY'S SCHEDULE")
    else:
        print(f"\n🎉 No classes scheduled for today ({day_name})!")

def view_weekly_routine(semester_name):
    print_header(f"Weekly Routine - {semester_name}")
    
    cursor.execute("""
        SELECT day_of_week, start_time, end_time, subject_name, 
               teacher_name, classroom, course_name
        FROM WeeklyRoutineView 
        WHERE semester_name = %s
        ORDER BY 
            CASE day_of_week
                WHEN 'Sunday' THEN 1
                WHEN 'Monday' THEN 2
                WHEN 'Tuesday' THEN 3
                WHEN 'Wednesday' THEN 4
                WHEN 'Thursday' THEN 5
                WHEN 'Friday' THEN 6
                WHEN 'Saturday' THEN 7
            END,
            start_time
    """, (semester_name,))
    
    routine = cursor.fetchall()
    print_table(routine, "WEEKLY ROUTINE")

def view_week_schedule(semester_name):
    today = datetime.today().date()
    start_of_week = today - timedelta(days=today.weekday())
    
    print_header(f"This Week's Schedule ({start_of_week} onwards)")
    
    for i in range(7):
        current_date = start_of_week + timedelta(days=i)
        day_name = current_date.strftime('%A')
        
        print(f"\n📅 {day_name}, {current_date}")
        print("-" * 40)
        
        # Call stored proc for this date & semester
        cursor.execute("CALL sp_get_daily_routine(%s, %s, %s)", (current_date, semester_name, None))
        daily_rows = cursor.fetchall()
        while cursor.nextset():
            pass

        if daily_rows:
            for class_info in daily_rows:
                status_icon = "✅" if class_info['status'] == 'Scheduled' else "❌" if class_info['status'] == 'Cancelled' else "🔄"
                print(f"  {status_icon} {class_info['start_time']} - {class_info['end_time']} | {class_info['subject_name']} | {class_info['teacher_name']} | {class_info['classroom']}")
        else:
            print("  🎉 No classes today!")

def view_student_profile(student_id):
    print_header("My Profile")
    
    cursor.execute("SELECT * FROM StudentDetailsView WHERE student_id = %s", (student_id,))
    profile = cursor.fetchone()
    
    if profile:
        print(f"\n👤 STUDENT INFORMATION:")
        print(f"  🆔 Student ID: {profile['student_id']}")
        print(f"  📝 Name: {profile['student_name']}")
        print(f"  🏠 Address: {profile['address']}")
        print(f"  📞 Phone: {profile['phone_number']}")
        print(f"  👨‍👩‍👦 Guardian: {profile['guardian_name']}")
        print(f"  🏢 Department: {profile['department_name']} ({profile['department_code']})")
        print(f"  📖 Semester: {profile['semester_name']}")
        print(f"  🏢 Department Building: {profile['department_building']}")

# ===============================
# Teacher Functions
# ===============================
def teacher_login():
    print_header("Teacher Login")
    teacher_id = input("🆔 Enter your Teacher ID: ").strip()
    
    cursor.execute("SELECT * FROM TeacherDetailsView WHERE teacher_id = %s", (teacher_id,))
    teacher = cursor.fetchone()
    
    if not teacher:
        print("❌ Teacher not found!")
        return None
    
    print(f"\n✅ Welcome, {teacher['teacher_name']}!")
    print(f"🏢 Department: {teacher['department_name']} ({teacher['department_code']})")
    print(f"📚 Subjects Teaching: {teacher['subjects_taught']}")
    return teacher

def teacher_dashboard(teacher):
    while True:
        clear_screen()
        print_header(f"Teacher Dashboard - {teacher['teacher_name']}")
        
        options = [
            "View Today's Classes",
            "View Weekly Schedule",
            "View My Subjects",
            "Mark Unavailability",
            "View My Workload",
            "View All Students",
            "View Department Info"
        ]
        
        print_menu(options)
        choice = get_choice(len(options))
        
        if choice == 0:
            break
        elif choice == 1:
            view_teacher_today_classes(teacher['teacher_id'])
        elif choice == 2:
            view_teacher_weekly_schedule(teacher['teacher_id'])
        elif choice == 3:
            view_teacher_subjects(teacher['teacher_id'])
        elif choice == 4:
            mark_teacher_unavailability(teacher['teacher_id'])
        elif choice == 5:
            view_teacher_workload(teacher['teacher_id'])
        elif choice == 6:
            view_all_students()
        elif choice == 7:
            view_department_info(teacher['department_code'])
        
        if choice != 0:
            pause()

def view_teacher_today_classes(teacher_id):
    today = datetime.today().date()
    day_name = today.strftime('%A')
    
    print_header(f"Today's Classes - {today} ({day_name})")

    # find semesters where teacher has classes (so procedure can be called with semester names)
    cursor.execute("""
        SELECT DISTINCT sem.semester_name
        FROM FIXEDROUTINE fr
        JOIN SEMESTER sem ON fr.semester_id = sem.semester_id
        WHERE fr.teacher_id = %s
    """, (teacher_id,))
    sem_rows = cursor.fetchall()
    semesters = [r['semester_name'] for r in sem_rows] if sem_rows else []

    combined = []
    for sem_name in semesters:
        cursor.execute("CALL sp_get_daily_routine(%s, %s, %s)", (today, sem_name, teacher_id))
        rows = cursor.fetchall()
        while cursor.nextset():
            pass
        for r in rows:
            combined.append(r)

    if combined:
        combined.sort(key=lambda x: x.get('start_time_raw') or x.get('start_time'))
        display_rows = []
        for r in combined:
            display_rows.append({
                'start_time': r.get('start_time'),
                'end_time': r.get('end_time'),
                'subject_name': r.get('subject_name'),
                'classroom': r.get('classroom'),
                'status': r.get('status')
            })
        print_table(display_rows, "TODAY'S CLASSES")
    else:
        print(f"\n🎉 No classes scheduled for today!")

def view_teacher_weekly_schedule(teacher_id):
    print_header("My Weekly Schedule")
    
    # get semesters
    cursor.execute("""
        SELECT DISTINCT sem.semester_name
        FROM FIXEDROUTINE fr
        JOIN SEMESTER sem ON fr.semester_id = sem.semester_id
        WHERE fr.teacher_id = %s
    """, (teacher_id,))
    sem_rows = cursor.fetchall()
    semesters = [r['semester_name'] for r in sem_rows] if sem_rows else []

    week_days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    today = datetime.today().date()

    for day in week_days:
        # find nearest date with that weekday (starting from today)
        date_for_day = None
        for offset in range(0, 7):
            candidate = today + timedelta(days=offset)
            if candidate.strftime('%A') == day:
                date_for_day = candidate
                break

        print(f"\n📅 {day} ({date_for_day})")
        print("-" * 40)

        combined = []
        for sem_name in semesters:
            cursor.execute("CALL sp_get_daily_routine(%s, %s, %s)", (date_for_day, sem_name, teacher_id))
            rows = cursor.fetchall()
            while cursor.nextset():
                pass
            combined.extend(rows)

        if combined:
            combined.sort(key=lambda x: x.get('start_time_raw') or x.get('start_time'))
            for r in combined:
                status_icon = "✅" if r['status'] == 'Scheduled' else "❌"
                print(f"  {status_icon} {r['start_time']} - {r['end_time']} | {r['subject_name']} | {r['classroom']}")
        else:
            print("  🎉 No classes on this day!")

def view_teacher_subjects(teacher_id):
    print_header("My Subjects")
    
    cursor.execute("""
        SELECT subject_name, course_name, department_name, semester_name
        FROM SubjectDetailsView 
        WHERE teacher_id = %s
        ORDER BY course_name, subject_name
    """, (teacher_id,))
    
    subjects = cursor.fetchall()
    print_table(subjects, "MY SUBJECTS")

def mark_teacher_unavailability(teacher_id):
    print_header("Mark Unavailability")
    
    try:
        date_str = input("📅 Enter date (YYYY-MM-DD) or press Enter for today: ").strip()
        if not date_str:
            date = datetime.today().date()
        else:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        start_time = input("⏰ Enter start time (HH:MM): ").strip() + ":00"
        end_time = input("⏰ Enter end time (HH:MM): ").strip() + ":00"
        reason = input("📝 Enter reason: ").strip()
        
        # Insert unavailability
        cursor.execute("""
            INSERT INTO TeacherUnavailability (teacher_id, unavailable_date, start_time, end_time, reason)
            VALUES (%s, %s, %s, %s, %s)
        """, (teacher_id, date, start_time, end_time, reason))
        
        # Find affected fixed classes for that day & teacher (overlapping times)
        day_name = date.strftime('%A')
        cursor.execute("""
            SELECT * FROM FIXEDROUTINE
            WHERE teacher_id = %s AND day_of_week = %s
            AND (
                 (start_time BETWEEN %s AND %s) OR 
                 (end_time BETWEEN %s AND %s) OR 
                 (%s BETWEEN start_time AND end_time)
            )
        """, (teacher_id, day_name, start_time, end_time, start_time, end_time, start_time))
        
        affected_classes = cursor.fetchall()
        
        for cls in affected_classes:
            # insert a DAILYROUTINE cancelled row
            cursor.execute("""
                INSERT INTO DAILYROUTINE (date, subject_id, teacher_id, class_id, 
                                        semester_id, start_time, end_time, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, 'Cancelled')
            """, (date, cls['subject_id'], cls['teacher_id'], cls['class_id'], 
                  cls['semester_id'], cls['start_time'], cls['end_time']))
        
        db.commit()
        
        print(f"\n✅ Unavailability marked successfully!")
        print(f"📅 Date: {date}")
        print(f"⏰ Time: {start_time} - {end_time}")
        print(f"📝 Reason: {reason}")
        print(f"❌ Classes affected: {len(affected_classes)}")
        
        if affected_classes:
            print("\n❌ CANCELLED CLASSES:")
            for cls in affected_classes:
                print(f"  • {cls['start_time']} - {cls['end_time']} (Subject ID: {cls['subject_id']})")
        
    except ValueError:
        print("❌ Invalid date format! Please use YYYY-MM-DD")
    except mysql.connector.Error as err:
        print(f"❌ Database error: {err}")
        db.rollback()

def view_teacher_workload(teacher_id):
    print_header("My Workload")
    
    cursor.execute("""
        SELECT * FROM TeacherWorkloadView WHERE teacher_id = %s
    """, (teacher_id,))
    
    workload = cursor.fetchone()
    
    if workload:
        print(f"\n📊 WORKLOAD SUMMARY:")
        print(f"  👤 Teacher: {workload['teacher_name']}")
        print(f"  🏢 Department: {workload['department_name']}")
        print(f"  📚 Subjects Count: {workload['subjects_count']}")
        print(f"  📅 Weekly Classes: {workload['weekly_classes']}")
        print(f"  📖 Subjects: {workload['subjects_taught']}")
        print(f"  📆 Teaching Days: {workload['teaching_days']}")

# ===============================
# Viewer Functions (mostly unchanged)
# ===============================
def viewer_dashboard():
    while True:
        clear_screen()
        print_header("Information Viewer Dashboard")
        
        options = [
            "View All Departments",
            "View All Teachers", 
            "View All Students",
            "View All Subjects",
            "View All Courses",
            "View All Classrooms",
            "View Department Summary",
            "View Teacher Workloads",
            "View Classroom Utilization",
            "View Weekly Routines",
            "Search Student",
            "Search Teacher"
        ]
        
        print_menu(options)
        choice = get_choice(len(options))
        
        if choice == 0:
            break
        elif choice == 1:
            view_all_departments()
        elif choice == 2:
            view_all_teachers()
        elif choice == 3:
            view_all_students()
        elif choice == 4:
            view_all_subjects()
        elif choice == 5:
            view_all_courses()
        elif choice == 6:
            view_all_classrooms()
        elif choice == 7:
            view_department_summary()
        elif choice == 8:
            view_all_teacher_workloads()
        elif choice == 9:
            view_classroom_utilization()
        elif choice == 10:
            view_all_routines()
        elif choice == 11:
            search_student()
        elif choice == 12:
            search_teacher()
        
        if choice != 0:
            pause()

def view_all_departments():
    print_header("All Departments")
    
    cursor.execute("SELECT * FROM DepartmentSummaryView ORDER BY department_name")
    departments = cursor.fetchall()
    print_table(departments, "DEPARTMENTS")

def view_all_teachers():
    print_header("All Teachers")
    
    cursor.execute("SELECT * FROM TeacherDetailsView ORDER BY department_name, teacher_name")
    teachers = cursor.fetchall()
    print_table(teachers, "TEACHERS")

def view_all_students():
    print_header("All Students")
    
    cursor.execute("SELECT * FROM StudentDetailsView ORDER BY department_name, semester_name, student_name")
    students = cursor.fetchall()
    print_table(students, "STUDENTS")

def view_all_subjects():
    print_header("All Subjects")
    
    cursor.execute("SELECT * FROM SubjectDetailsView ORDER BY department_name, semester_name, subject_name")
    subjects = cursor.fetchall()
    print_table(subjects, "SUBJECTS")

def view_all_courses():
    print_header("All Courses")
    
    cursor.execute("""
        SELECT c.course_name, d.name as department_name, d.department_code,
               s.semester_name, COUNT(subj.subject_id) as subjects_count
        FROM COURSE c
        JOIN DEPARTMENT d ON c.department_id = d.department_id
        JOIN SEMESTER s ON c.semester_id = s.semester_id
        LEFT JOIN SUBJECT subj ON c.course_id = subj.course_id
        GROUP BY c.course_id, c.course_name, d.name, d.department_code, s.semester_name
        ORDER BY d.name, s.semester_name
    """)
    courses = cursor.fetchall()
    print_table(courses, "COURSES")

def view_all_classrooms():
    print_header("All Classrooms")
    
    cursor.execute("SELECT * FROM ClassroomUtilizationView ORDER BY classroom")
    classrooms = cursor.fetchall()
    print_table(classrooms, "CLASSROOMS")

def view_department_summary():
    print_header("Department Summary")
    
    cursor.execute("SELECT * FROM DepartmentSummaryView ORDER BY department_name")
    summary = cursor.fetchall()
    print_table(summary, "DEPARTMENT SUMMARY")

def view_all_teacher_workloads():
    print_header("Teacher Workloads")
    
    cursor.execute("SELECT * FROM TeacherWorkloadView ORDER BY department_name, teacher_name")
    workloads = cursor.fetchall()
    print_table(workloads, "TEACHER WORKLOADS")

def view_classroom_utilization():
    print_header("Classroom Utilization")
    
    cursor.execute("SELECT * FROM ClassroomUtilizationView ORDER BY weekly_classes DESC, classroom")
    utilization = cursor.fetchall()
    print_table(utilization, "CLASSROOM UTILIZATION")

def view_all_routines():
    print_header("Weekly Routines")
    
    semester = input("🔍 Enter semester name (or press Enter for all): ").strip()
    department = input("🔍 Enter department code (or press Enter for all): ").strip()
    
    query = "SELECT * FROM WeeklyRoutineView WHERE 1=1"
    params = []
    
    if semester:
        query += " AND semester_name LIKE %s"
        params.append(f"%{semester}%")
    
    if department:
        query += " AND department_name LIKE %s"
        params.append(f"%{department}%")
    
    query += """ ORDER BY 
        CASE day_of_week
            WHEN 'Sunday' THEN 1
            WHEN 'Monday' THEN 2
            WHEN 'Tuesday' THEN 3
            WHEN 'Wednesday' THEN 4
            WHEN 'Thursday' THEN 5
            WHEN 'Friday' THEN 6
            WHEN 'Saturday' THEN 7
        END,
        start_time"""
    
    cursor.execute(query, params)
    routines = cursor.fetchall()
    print_table(routines, "WEEKLY ROUTINES")

def search_student():
    print_header("Search Student")
    
    search_term = input("🔍 Enter student name or ID to search: ").strip()
    
    cursor.execute("""
        SELECT * FROM StudentDetailsView 
        WHERE student_name LIKE %s OR student_id LIKE %s
        ORDER BY student_name
    """, (f"%{search_term}%", f"%{search_term}%"))
    
    students = cursor.fetchall()
    print_table(students, "SEARCH RESULTS")

def search_teacher():
    print_header("Search Teacher")
    
    search_term = input("🔍 Enter teacher name or ID to search: ").strip()
    
    cursor.execute("""
        SELECT * FROM TeacherDetailsView 
        WHERE teacher_name LIKE %s OR teacher_id LIKE %s
        ORDER BY teacher_name
    """, (f"%{search_term}%", f"%{search_term}%"))
    
    teachers = cursor.fetchall()
    print_table(teachers, "SEARCH RESULTS")

def view_department_info(department_code):
    print_header(f"Department Information - {department_code}")
    
    cursor.execute("""
        SELECT * FROM DepartmentSummaryView 
        WHERE department_code = %s
    """, (department_code,))
    
    dept_info = cursor.fetchone()
    
    if dept_info:
        print(f"\n🏢 DEPARTMENT DETAILS:")
        print(f"  📝 Name: {dept_info['department_name']}")
        print(f"  🔤 Code: {dept_info['department_code']}")
        print(f"  🏢 Building: {dept_info['building_no']}")
        print(f"  👨‍🏫 Teachers: {dept_info['teachers_count']}")
        print(f"  👨‍🎓 Students: {dept_info['students_count']}")
        print(f"  📚 Courses: {dept_info['courses_count']}")
        print(f"  📖 Subjects: {dept_info['subjects_count']}")

# ===============================
# Main Application
# ===============================
def main_menu():
    while True:
        clear_screen()
        print("🎓" + "="*58 + "🎓")
        print("  🏫 COMPREHENSIVE ROUTINE MANAGEMENT SYSTEM 🏫")
        print("🎓" + "="*58 + "🎓")
        print("\n🔐 LOGIN OPTIONS:")
        print("  1. 👨‍🎓 Student Login")
        print("  2. 👨‍🏫 Teacher Login") 
        print("  3. 👁️  Information Viewer")
        print("  4. ❌ Exit System")
        print("-" * 60)
        
        choice = get_choice(4)
        
        if choice == 1:
            student = student_login()
            if student:
                student_dashboard(student)
        elif choice == 2:
            teacher = teacher_login()
            if teacher:
                teacher_dashboard(teacher)
        elif choice == 3:
            viewer_dashboard()
        elif choice == 4:
            print("\n👋 Thank you for using Routine Management System!")
            print("🎓 Have a great day!")
            break
        elif choice == 0:
            print("\n👋 Thank you for using Routine Management System!")
            print("🎓 Have a great day!")
            break

def main():
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\n👋 System interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
    finally:
        if db.is_connected():
            cursor.close()
            db.close()
            print("🔌 Database connection closed.")

if __name__ == "__main__":
    main()
