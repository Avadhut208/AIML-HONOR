# Assignment 3 · Class-based SQLite database

## Aim

Build a menu-driven employee register that supports create, read, update and delete (CRUD). EmployeeDatabase owns a SQLite connection and provides create, records, find, update and delete methods. The employee table uses employee_id as its primary key. Parameterized SQL handles values, and each write runs inside a transaction.

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
