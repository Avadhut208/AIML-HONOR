from decimal import Decimal, InvalidOperation
from pathlib import Path
import csv
from tempfile import NamedTemporaryFile


class EmployeeCSV:
    fields = ["employee_id", "name", "department", "salary_paise"]

    def __init__(self, path):
        self.path = path
        if not path.exists():
            self.save([])

    def records(self):
        with self.path.open(encoding="utf-8", newline="") as source:
            reader = csv.DictReader(source)
            if reader.fieldnames != self.fields:
                raise ValueError("Unexpected CSV header.")
            return [(int(row["employee_id"]), row["name"], row["department"],
                     int(row["salary_paise"])) for row in reader]

    def save(self, rows):
        # Replace the old CSV only after the complete new file is closed.
        with NamedTemporaryFile("w", dir=self.path.parent, delete=False,
                                newline="", encoding="utf-8") as target:
            temporary = Path(target.name)
            try:
                writer = csv.writer(target)
                writer.writerow(self.fields)
                writer.writerows(rows)
            except BaseException:
                target.close()
                temporary.unlink(missing_ok=True)
                raise
        try:
            temporary.replace(self.path)
        finally:
            temporary.unlink(missing_ok=True)

    def find(self, employee_id):
        return next((row for row in self.records() if row[0] == employee_id), None)

    def create(self, employee_id, name, department, salary):
        rows = self.records()
        if any(row[0] == employee_id for row in rows):
            raise ValueError("ID already exists.")
        rows.append((employee_id, name, department, salary))
        self.save(rows)

    def update(self, employee_id, name, department, salary):
        rows = self.records()
        for index, row in enumerate(rows):
            if row[0] == employee_id:
                rows[index] = (employee_id, name, department, salary)
                self.save(rows)
                return
        raise ValueError("Employee not found.")

    def delete(self, employee_id):
        rows = self.records()
        remaining = [row for row in rows if row[0] != employee_id]
        if len(remaining) == len(rows):
            raise ValueError("Employee not found.")
        self.save(remaining)


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


def menu(store):
    while True:
        print("\n1 Add   2 List   3 Find   4 Update   5 Delete   0 Exit")
        choice = input("Choice: ").strip()
        try:
            if choice == "0":
                return
            if choice == "2":
                display(store.records())
                continue
            if choice not in {"1", "3", "4", "5"}:
                print("Choose a listed option.")
                continue
            employee_id = read_id()
            record = store.find(employee_id)
            if choice == "1":
                if record is not None:
                    raise ValueError("ID already exists.")
                store.create(employee_id, *read_details())
                print("Employee added.")
            elif record is None:
                print("Employee not found.")
            elif choice == "3":
                display([record])
            elif choice == "4":
                store.update(employee_id, *read_details())
                print("Employee updated.")
            elif input("Confirm deletion (y/n): ").strip().lower() == "y":
                store.delete(employee_id)
                print("Employee deleted.")
            else:
                print("Deletion cancelled.")
        except InvalidOperation:
            print("Enter a numeric salary.")
        except (ValueError, OSError, csv.Error) as error:
            print(error)


if __name__ == "__main__":
    try:
        menu(EmployeeCSV(Path(__file__).with_name("employees.csv")))
    except (EOFError, KeyboardInterrupt):
        print("\nSession closed.")
