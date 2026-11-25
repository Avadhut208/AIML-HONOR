# Assignment 2 · Class-based CSV file handling

## Aim

Build a menu-driven employee register that supports create, read, update and delete (CRUD). EmployeeCSV reads rows with csv.DictReader. Add checks the unique employee ID. Update and delete locate the ID and rewrite the rows. Each write uses a temporary CSV, then replaces employees.csv once writing succeeds.

## Employee record

| Field | Meaning |
|---|---|
| employee_id | Positive integer key entered at creation |
| name | Employee name |
| department | Department name |
| salary_paise | Nonnegative integer amount in paise. The menu accepts and displays rupees to two decimal places. |

## Run and demonstrate

Run `py main.py` in this folder.

| Step | Menu input | Expected result |
|---|---|---|
| Create | 1, ID 101, Mira, IT, 35000.50 | Employee added. |
| Read all | 2 | 101, Mira, IT, 35000.50 |
| Update | 4, ID 101, Mira, Analytics, 41000.75 | Employee updated. |
| Test persistence | 0, restart, then 3 and ID 101 | 101, Mira, Analytics, 41000.75 |
| Delete | 5, ID 101, y | Employee deleted. |
| Verify deletion | 3, ID 101 | Employee not found. |

Enter each value at its own prompt. A duplicate ID is rejected. At the delete confirmation, entering n keeps the record. Select 0 to exit.
