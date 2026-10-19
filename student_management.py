import sqlite3

DB_NAME = "students.db"

def connect_db():
    return sqlite3.connect(DB_NAME)

def setup_database():
    with connect_db() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS students (
            roll_no TEXT PRIMARY KEY, name TEXT NOT NULL, age INTEGER NOT NULL,
            course TEXT NOT NULL, phone TEXT, email TEXT, marks REAL NOT NULL)""")

def grade(marks):
    if marks >= 90: return "A+"
    if marks >= 80: return "A"
    if marks >= 70: return "B"
    if marks >= 60: return "C"
    if marks >= 50: return "D"
    return "F"

def get_marks():
    while True:
        try:
            marks = float(input("Marks (0-100): "))
            if 0 <= marks <= 100: return marks
            print("Marks must be between 0 and 100.")
        except ValueError:
            print("Enter a valid number.")

def add_student():
    roll = input("Roll number: ").strip()
    name = input("Name: ").strip()
    if not roll or not name:
        print("Roll number and name are required."); return
    try:
        age = int(input("Age: "))
        if not 1 <= age <= 120:
            print("Enter a valid age."); return
    except ValueError:
        print("Age must be a number."); return
    course = input("Course: ").strip()
    phone = input("Phone (optional): ").strip()
    email = input("Email (optional): ").strip()
    marks = get_marks()
    try:
        with connect_db() as conn:
            conn.execute("""INSERT INTO students
                (roll_no,name,age,course,phone,email,marks)
                VALUES (?,?,?,?,?,?,?)""",
                (roll,name,age,course,phone,email,marks))
        print("Student added successfully!")
    except sqlite3.IntegrityError:
        print("That roll number already exists.")

def view_students():
    with connect_db() as conn:
        rows = conn.execute("SELECT * FROM students ORDER BY roll_no").fetchall()
    if not rows:
        print("No students found."); return
    print("\n--- STUDENT LIST ---")
    for roll,name,age,course,phone,email,marks in rows:
        print(f"Roll: {roll} | Name: {name} | Age: {age} | Course: {course} | "
              f"Phone: {phone or '-'} | Email: {email or '-'} | "
              f"Marks: {marks:.2f} | Grade: {grade(marks)}")

def search_student():
    roll = input("Enter roll number: ").strip()
    with connect_db() as conn:
        row = conn.execute("SELECT * FROM students WHERE roll_no=?", (roll,)).fetchone()
    if not row:
        print("Student not found."); return
    roll,name,age,course,phone,email,marks = row
    print(f"Roll: {roll}\nName: {name}\nAge: {age}\nCourse: {course}")
    print(f"Phone: {phone or '-'}\nEmail: {email or '-'}")
    print(f"Marks: {marks:.2f}\nGrade: {grade(marks)}")

def update_student():
    roll = input("Roll number to update: ").strip()
    with connect_db() as conn:
        row = conn.execute("SELECT * FROM students WHERE roll_no=?", (roll,)).fetchone()
        if not row:
            print("Student not found."); return
        _, old_name, old_age, old_course, old_phone, old_email, old_marks = row
        print("Press Enter to keep the current value.")
        name = input(f"Name [{old_name}]: ").strip() or old_name
        age_text = input(f"Age [{old_age}]: ").strip()
        course = input(f"Course [{old_course}]: ").strip() or old_course
        phone = input(f"Phone [{old_phone or '-'}]: ").strip() or old_phone
        email = input(f"Email [{old_email or '-'}]: ").strip() or old_email
        marks_text = input(f"Marks [{old_marks}]: ").strip()
        try:
            age = int(age_text) if age_text else old_age
            marks = float(marks_text) if marks_text else old_marks
            if not 1 <= age <= 120 or not 0 <= marks <= 100:
                print("Age or marks is outside the valid range."); return
        except ValueError:
            print("Age and marks must be valid numbers."); return
        conn.execute("""UPDATE students SET name=?,age=?,course=?,phone=?,email=?,marks=?
                        WHERE roll_no=?""",
                     (name,age,course,phone,email,marks,roll))
    print("Student updated successfully!")

def delete_student():
    roll = input("Roll number to delete: ").strip()
    if input("Type yes to confirm deletion: ").strip().lower() != "yes":
        print("Delete cancelled."); return
    with connect_db() as conn:
        cur = conn.execute("DELETE FROM students WHERE roll_no=?", (roll,))
        print("Student deleted successfully!" if cur.rowcount else "Student not found.")

def main():
    setup_database()
    while True:
        print("\n====== STUDENT MANAGEMENT SYSTEM ======")
        print("1. Add student\n2. View all students\n3. Search student")
        print("4. Update student\n5. Delete student\n6. Exit")
        choice = input("Choose (1-6): ").strip()
        if choice == "1": add_student()
        elif choice == "2": view_students()
        elif choice == "3": search_student()
        elif choice == "4": update_student()
        elif choice == "5": delete_student()
        elif choice == "6":
            print("Thank you!"); break
        else: print("Choose a number from 1 to 6.")

if __name__ == "__main__":
    main()
