from flask import Flask, render_template, g, redirect, url_for, request
return render_template('index.html')


@app.route('/admin')
def admin():
db = get_db()
users = db.execute('SELECT * FROM users').fetchall()
return render_template('admin_dashboard.html', users=users)


@app.route('/doctor')
def doctor():
db = get_db()
appts = db.execute('SELECT a.id, p.name as patient, a.doctor, a.appt_date FROM appointments a JOIN patients p ON a.patient_id = p.id').fetchall()
return render_template('doctor_dashboard.html', appointments=appts)


@app.route('/patient')
def patient():
db = get_db()
patients = db.execute('SELECT * FROM patients').fetchall()
return render_template('patient_dashboard.html', patients=patients)


@app.route('/register', methods=['GET', 'POST'])
def register():
db = get_db()
if request.method == 'POST':
name = request.form['name']
age = request.form.get('age')
gender = request.form.get('gender')
contact = request.form.get('contact')
address = request.form.get('address')
db.execute('INSERT INTO patients (name, age, gender, contact, address) VALUES (?,?,?,?,?)', (name, age, gender, contact, address))
db.commit()
return redirect(url_for('patient'))
return render_template('patient_registration.html')


@app.route('/records/<int:pid>')
def records(pid):
db = get_db()
patient = db.execute('SELECT * FROM patients WHERE id=?', (pid,)).fetchone()
appts = db.execute('SELECT * FROM appointments WHERE patient_id=?', (pid,)).fetchall()
bills = db.execute('SELECT * FROM bills WHERE patient_id=?', (pid,)).fetchall()
return render_template('patient_records.html', patient=patient, appointments=appts, bills=bills)


@app.route('/book', methods=['GET', 'POST'])
def book():
db = get_db()
if request.method == 'POST':
pid = request.form['patient_id']
doctor = request.form['doctor']
appt_date = request.form['appt_date']
notes = request.form.get('notes')
db.execute('INSERT INTO appointments (patient_id, doctor, appt_date, notes) VALUES (?,?,?,?)', (pid, doctor, appt_date, notes))
db.commit()
return redirect(url_for('doctor'))
patients = db.execute('SELECT id, name FROM patients').fetchall()
return render_template('appointment_booking.html', patients=patients)


@app.route('/billing')
def billing():
db = get_db()
bills = db.execute('SELECT b.*, p.name as patient FROM bills b JOIN patients p ON b.patient_id = p.id').fetchall()
return render_template('billing.html', bills=bills)


@app.route('/notifications')
def notifications():
return render_template('notifications.html')


if __name__ == '__main__':
app.run(debug=True)
