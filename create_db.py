import sqlite3
'''


seed = [
("admin", "Alice Admin", "alice.admin@example.com"),
("doctor", "Dr. Bob", "bob.doc@example.com"),
("patient", "Charlie Patient", "charlie.p@example.com"),
]


patients = [
("Charlie Patient", 29, "Male", "+91-9876543210", "123, Sample St, City"),
("Dana Patient", 42, "Female", "+91-9123456780", "45, Example Ave, City"),
]


appointments = [
(1, "Dr. Bob", "2025-11-05 10:30", "Routine checkup"),
(2, "Dr. Bob", "2025-11-06 14:00", "Follow-up"),
]


bills = [
(1, 1200.00, 0, "Consultation + tests"),
(2, 4500.00, 1, "Procedure charges"),
]


if __name__ == '__main__':
conn = sqlite3.connect(DB)
cur = conn.cursor()
cur.executescript(schema)


# seed users
for r, n, e in seed:
try:
cur.execute('INSERT INTO users (role, name, email) VALUES (?,?,?)', (r, n, e))
except sqlite3.IntegrityError:
pass


# seed patients
for p in patients:
cur.execute('SELECT id FROM patients WHERE name=?', (p[0],))
if not cur.fetchone():
cur.execute('INSERT INTO patients (name, age, gender, contact, address) VALUES (?,?,?,?,?)', p)


# seed appointments
cur.execute('SELECT id FROM patients WHERE name=?', (patients[0][0],))
pid1 = cur.fetchone()[0]
cur.execute('SELECT id FROM patients WHERE name=?', (patients[1][0],))
pid2 = cur.fetchone()[0]


for a in appointments:
# map first value to seeded patient ids
if a[0] == 1:
cur.execute('INSERT INTO appointments (patient_id, doctor, appt_date, notes) VALUES (?,?,?,?)', (pid1, a[1], a[2], a[3]))
else:
cur.execute('INSERT INTO appointments (patient_id, doctor, appt_date, notes) VALUES (?,?,?,?)', (pid2, a[1], a[2], a[3]))


for b in bills:
if b[0] == 1:
cur.execute('INSERT INTO bills (patient_id, amount, paid, description) VALUES (?,?,?,?)', (pid1, b[1], b[2], b[3]))
else:
cur.execute('INSERT INTO bills (patient_id, amount, paid, description) VALUES (?,?,?,?)', (pid2, b[1], b[2], b[3]))


conn.commit()
conn.close()
print('Database created and seeded as', DB)
