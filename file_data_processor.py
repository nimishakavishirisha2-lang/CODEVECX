
import csv
import os
from collections import Counter

FILE_NAME = "student_data.csv"


def create_file():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Name", "Age", "Marks"])
        print("Data file created successfully!")


def add_record():
    try:
        sid = input("Enter Student ID: ")
        name = input("Enter Name: ")
        age = int(input("Enter Age: "))
        marks = float(input("Enter Marks: "))

        if age <= 0 or not 0 <= marks <= 100:
            print("Invalid age or marks.")
            return

        with open(FILE_NAME, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([sid, name, age, marks])

        print("Record added successfully!")

    except ValueError:
        print("Please enter valid age and marks.")


def view_records():
    with open(FILE_NAME, "r", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            print(" | ".join(row))


def search_record():
    sid = input("Enter Student ID to search: ")

    with open(FILE_NAME, "r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["ID"] == sid:
                print("Record found:", row)
                return

    print("Record not found.")


def data_summary():
    ages = []
    marks = []

    with open(FILE_NAME, "r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            ages.append(int(row["Age"]))
            marks.append(float(row["Marks"]))

    if not marks:
        print("No records available for analysis.")
        return

    print("\n--- Data Summary ---")
    print("Total Students:", len(marks))
    print("Average Marks:", round(sum(marks) / len(marks), 2))
    print("Highest Marks:", max(marks))
    print("Lowest Marks:", min(marks))
    print("Average Age:", round(sum(ages) / len(ages), 2))


def count_names():
    names = []

    with open(FILE_NAME, "r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            names.append(row["Name"])

    if names:
        print("\nName Frequency:")
        for name, count in Counter(names).items():
            print(name, ":", count)
    else:
        print("No records available.")


def main():
    create_file()

    while True:
        print("\n===== FILE HANDLING & DATA PROCESSING =====")
        print("1. Add Student Record")
        print("2. View All Records")
        print("3. Search Student")
        print("4. Data Summary")
        print("5. Name Frequency")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_record()
        elif choice == "2":
            view_records()
        elif choice == "3":
            search_record()
        elif choice == "4":
            data_summary()
        elif choice == "5":
            count_names()
        elif choice == "6":
            print("Thank you!")
            break
        else:
            print("Invalid choice. Select 1-6.")


if __name__ == "__main__":
    main()
