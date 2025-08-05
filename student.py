import csv
import json

students = {}


def register_student():
    student_id = input("Enter Student Id: ")
    name = input("Enter Student Name: ")
    batch = input("Enter Student Batch: ")
    if student_id not in students:
        students[student_id] = {
            "name": name,
            "batch": batch,
            "attendance": {"total_days": 0, "present_days": 0},
            "terms": {},
        }
        print(f"Student {name} registered successfully.")
    else:
        print("Student ID already exists.")


def add_term_result():
    student_id = input("Enter Student Id: ")
    term = input("Enter Term Name: ")
    n = int(input("Enter number of subjects: "))
    subjects = {}
    for _ in range(n):
        subject_name = input("Enter Subject Name: ")
        marks = int(input(f"Enter Marks for {subject_name}: "))
        subjects[subject_name] = marks

    if student_id in students:
        students[student_id]["terms"][term] = subjects
        print(f"Marks for term {term} added successfully.")
    else:
        print("Student ID not found. Please register the student first.")


def update_subject_mark():
    student_id = input("Enter Student Id: ")
    term = input("Enter Term Name: ")
    subject_name = input("Enter Subject Name: ")
    new_marks = int(input("Enter New Marks: "))
    try:
        students[student_id]["terms"][term][subject_name] = new_marks
        print("Marks updated successfully.")
    except KeyError:
        print("Invalid student ID, term, or subject name.")


def record_attendance():
    student_id = input("Enter Student Id: ")
    present_days = int(input("Enter Number of Days Present: "))
    total_days = int(input("Enter Total Number of Days: "))

    if student_id in students:
        students[student_id]["attendance"]["present_days"] += present_days
        students[student_id]["attendance"]["total_days"] += total_days
        print("Attendance recorded successfully.")
    else:
        print("Student ID not found. Please register the student first.")


def calculate_average(student_id):
    terms = students[student_id]["terms"]
    total_marks = 0
    count = 0
    for term in terms.values():
        for marks in term.values():
            total_marks += marks
            count += 1
    return total_marks / count if count else 0


def calculate_attendance_percentage(student_id):
    attendance = students[student_id]["attendance"]
    total = attendance["total_days"]
    present = attendance["present_days"]
    if total > 0:
        return (present / total) * 100
    return 0


def get_term_average(student_id, term):
    term_data = students[student_id]["terms"].get(term)
    if not term_data:
        return 0
    return sum(term_data.values()) / len(term_data)


def get_topper_by_term_name(term_name):
    top_student = None
    top_avg = -1
    for sid, data in students.items():
        if term_name in data["terms"]:
            avg = get_term_average(sid, term_name)
            if avg > top_avg:
                top_avg = avg
                top_student = (data["name"], avg)
    return top_student


def generate_student_report():
    sid = input("Enter student ID: ").strip()
    if sid not in students:
        print("Student not found.\n")
        return

    data = students[sid]
    print(f"\nStudent Report: {data['name']} ({sid})")
    print(f"Batch: {data['batch']}")
    print(f"Attendance: {calculate_attendance_percentage(sid):.1f}%")

    term_averages = {}
    for term in data["terms"]:
        avg = get_term_average(sid, term)
        term_averages[term] = avg
        print(f"{term} Average: {avg:.1f}")

    overall_avg = calculate_average(sid)
    print(f"Overall Average: {overall_avg:.2f}")

    for term in data["terms"]:
        top_student = get_topper_by_term_name(term)
        if top_student:
            name, avg = top_student
            print(f"Top Performer: {name} in {term} with {avg:.1f} average.")
    print()


def rank_students_by_overall_average():
    batch = input("Enter batch year: ")
    ranking = []
    for sid, data in students.items():
        if data["batch"] == batch:
            avg = calculate_average(sid)
            ranking.append((sid, data["name"], avg))
    ranking.sort(key=lambda x: x[2], reverse=True)
    print(f"\nRanking for Batch {batch}:")
    for idx, (sid, name, avg) in enumerate(ranking, 1):
        print(f"{idx}. {name} (ID: {sid}) - Average: {avg:.2f}")
    print()


def export_data_to_json():
    filename = input("Enter filename to export (e.g., data.json): ")
    with open(filename, "w") as f:
        json.dump(students, f, indent=4)
    print("Data exported to JSON.")

    save_to_csv(students)
    print("Data also exported to CSV\n")


def import_data_from_json():
    global students
    filename = input("Enter filename to import (e.g., data.json): ")
    try:
        with open(filename, "r") as f:
            students = json.load(f)
        print("Data imported successfully.\n")
    except FileNotFoundError:
        print("File not found.\n")


def save_to_csv(data):
    with open("student_data.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "Student ID",
                "Name",
                "Batch",
                "Total Days",
                "Present Days",
                "Term",
                "Math",
                "Physics",
                "English",
            ]
        )

        for sid, student in data.items():
            name = student["name"]
            batch = student["batch"]
            total = student["attendance"]["total_days"]
            present = student["attendance"]["present_days"]

            for term, subjects in student["terms"].items():
                math = subjects.get("Math", "")
                physics = subjects.get("Physics", "")
                english = subjects.get("English", "")
                writer.writerow(
                    [sid, name, batch, total, present, term, math, physics, english]
                )


if __name__ == "__main__":
    while True:
        print("\n1. Register Student")
        print("2. Add Term Result")
        print("3. Update Subject Mark")
        print("4. Record Attendance")
        print("5. Calculate Average Marks")
        print("6. Calculate Attendance Percentage")
        print("7. Get Topper by Term")
        print("8. Rank Students by Average (Batch)")
        print("9. Generate Student Report")
        print("10. Export Data to JSON")
        print("11. Import Data from JSON")
        print("12. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            register_student()
        elif choice == "2":
            add_term_result()
        elif choice == "3":
            update_subject_mark()
        elif choice == "4":
            record_attendance()
        elif choice == "5":
            sid = input("Enter Student ID: ").strip()
            if sid in students:
                avg = calculate_average(sid)
                print(f"Average marks for {sid}: {avg:.2f}")
            else:
                print("Student not found.")
        elif choice == "6":
            sid = input("Enter Student ID: ").strip()
            if sid in students:
                attendance = calculate_attendance_percentage(sid)
                print(f"Attendance percentage for {sid}: {attendance:.2f}%")
            else:
                print("Student not found.")
        elif choice == "7":
            term = input("Enter Term Name: ")
            top = get_topper_by_term_name(term)
            if top:
                print(f"Topper for term {term} is {top[0]} with average {top[1]:.1f}")
            else:
                print(f"No results for term {term}.")
        elif choice == "8":
            rank_students_by_overall_average()
        elif choice == "9":
            generate_student_report()
        elif choice == "10":
            export_data_to_json()
        elif choice == "11":
            import_data_from_json()
        elif choice == "12":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")
