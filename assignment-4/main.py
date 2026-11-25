from decimal import Decimal, InvalidOperation
from pathlib import Path
import sqlite3
from contextlib import closing
import pandas as pd


def records(db):
    frame = pd.read_sql_query("SELECT * FROM employee ORDER BY employee_id", db)
    return list(frame.itertuples(index=False, name=None))


def find(db, employee_id):
    frame = pd.read_sql_query("SELECT * FROM employee WHERE employee_id = ?", db, params=(employee_id,))
    return next(frame.itertuples(index=False, name=None), None)


def create(db, employee_id, name, department, salary):
    with db:
        db.execute("INSERT INTO employee VALUES (?, ?, ?, ?)", (employee_id, name, department, salary))


def update(db, employee_id, name, department, salary):
    with db:
        result = db.execute("UPDATE employee SET name=?, department=?, salary_paise=? WHERE employee_id=?",
                            (name, department, salary, employee_id))
        if result.rowcount == 0:
            raise ValueError("Employee not found.")


def delete(db, employee_id):
    with db:
        result = db.execute("DELETE FROM employee WHERE employee_id=?", (employee_id,))
        if result.rowcount == 0:
            raise ValueError("Employee not found.")


def read_id():
    employee_id = int(input("Employee ID: "))
    if not 1 <= employee_id <= 2**63 - 1:
        raise ValueError("Enter a positive 64-bit employee ID.")
    return employee_id


def read_details():
    name = input("Name: ").strip()
    department = input("Department: ").strip()
    if not name or not department:
        raise ValueError("Name and department are required.")
    value = Decimal(input("Salary in INR: ").strip())
    if not value.is_finite() or not 0 <= value <= 10**12 or value != round(value, 2):
        raise ValueError("Salary must be between 0 and 1 trillion INR with at most two decimal places.")
    return name, department, int(value * 100)


def display(rows):
    if not rows:
        print("No employees.")
        return
    print("ID | Name | Department | Salary (INR)")
    for employee_id, name, department, salary in rows:
        print(f"{employee_id} | {name} | {department} | {Decimal(salary) / 100:.2f}")


def menu(db):
    while True:
        print("\n1 Add   2 List   3 Find   4 Update   5 Delete   0 Exit")
        choice = input("Choice: ").strip()
        try:
            if choice == "0":
                return
            if choice == "2":
                display(records(db))
                continue
            if choice not in {"1", "3", "4", "5"}:
                print("Choose a listed option.")
                continue
            employee_id = read_id()
            record = find(db, employee_id)
            if choice == "1":
                if record is not None:
                    raise ValueError("ID already exists.")
                create(db, employee_id, *read_details())
                print("Employee added.")
            elif record is None:
                print("Employee not found.")
            elif choice == "3":
                display([record])
            elif choice == "4":
                update(db, employee_id, *read_details())
                print("Employee updated.")
            elif input("Confirm deletion (y/n): ").strip().lower() == "y":
                delete(db, employee_id)
                print("Employee deleted.")
            else:
                print("Deletion cancelled.")
        except InvalidOperation:
            print("Enter a numeric salary.")
        except (ValueError, sqlite3.Error, pd.errors.DatabaseError) as error:
            print(error)


if __name__ == "__main__":
    try:
        with closing(sqlite3.connect(Path(__file__).with_name("employees.db"))) as db:
            db.execute("""CREATE TABLE IF NOT EXISTS employee (
                        employee_id INTEGER PRIMARY KEY CHECK(employee_id > 0),
                        name TEXT NOT NULL,
                        department TEXT NOT NULL,
                        salary_paise INTEGER NOT NULL CHECK(salary_paise >= 0)
                    )""")
            menu(db)
    except (EOFError, KeyboardInterrupt):
        print("\nSession closed.")
