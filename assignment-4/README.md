# Assignment 4 · SQLite database with pandas

## Aim

Build a menu-driven employee register that supports create, read, update and delete (CRUD). Standalone functions implement the four operations. The records and find functions use pandas.read_sql_query to load selected employees into a DataFrame. INSERT, UPDATE and DELETE use parameterized SQL inside SQLite transactions. This changes only the selected records and preserves the primary key.

## Employee record

| Field | Meaning |
|---|---|
| employee_id | Positive integer key entered at creation |
| name | Employee name |
| department | Department name |
| salary_paise | Nonnegative integer amount in paise. The menu accepts and displays rupees to two decimal places. |

## Run and demonstrate

Install pandas first with `py -m pip install -r requirements.txt`. Run `py main.py` in this folder.

| Step | Menu input | Expected result |
|---|---|---|
| Create | 1, ID 101, Mira, IT, 35000.50 | Employee added. |
| Read all | 2 | 101, Mira, IT, 35000.50 |
| Update | 4, ID 101, Mira, Analytics, 41000.75 | Employee updated. |
| Test persistence | 0, restart, then 3 and ID 101 | 101, Mira, Analytics, 41000.75 |
| Delete | 5, ID 101, y | Employee deleted. |
| Verify deletion | 3, ID 101 | Employee not found. |

Enter each value at its own prompt. A duplicate ID is rejected. At the delete confirmation, entering n keeps the record. Select 0 to exit.
