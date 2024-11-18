import string
import random

import mysql.connector
from datetime import datetime, timedelta


class HealthcareDatabase:
    def __init__(self):
        self.db_config = {
            "host": "localhost",
            "user": "root",
            "password": "COSC578_Hopkins",
            "database": "hopkins_health_hub"
        }

    # Database connection
    def connect(self):
        try:
            return mysql.connector.connect(**self.db_config)
        except mysql.connector.Error as e:
            raise Exception(f"Could not connect to database: {e}")

    # Login verification for patient
    def verify_patient_login(self, patient_id, password):
        connection = self.connect()
        cursor = connection.cursor()
        try:
            query = """SELECT patient_id 
                      FROM Patient 
                      WHERE patient_id = %s 
                      AND patient_password = %s"""
            cursor.execute(query, (patient_id, password))
            return cursor.fetchone() is not None
        finally:
            cursor.close()
            connection.close()

    # Log in verification for professional
    def verify_professional_login(self, healthcare_id, password):
        connection = self.connect()
        cursor = connection.cursor()
        try:
            query = """SELECT healthcare_professional_id 
                      FROM Healthcare_Professional 
                      WHERE healthcare_professional_id = %s 
                      AND healthprof_password = %s"""
            cursor.execute(query, (healthcare_id, password))
            return cursor.fetchone() is not None
        finally:
            cursor.close()
            connection.close()

    # Patient Submission for Patient
    def submit_appointment(self, visit_type, appointment_date, appointment_time, healthcare_professional_id, notes,
                           patient_id):
        connection = self.connect()
        cursor = connection.cursor()

        try:
            # Convert the appointment time string to a proper time object
            appointment_time = datetime.strptime(appointment_time, '%I:%M %p').time()

            # Convert appointment_date to datetime.date if it's not already
            if isinstance(appointment_date, str):
                appointment_date = datetime.strptime(appointment_date, '%Y-%m-%d').date()

            # Check if the healthcare professional is available at this time
            day_of_week = appointment_date.strftime('%A')
            check_query = """
            SELECT COUNT(*) 
            FROM Professional_Availability 
            WHERE healthcare_professional_id = %s 
            AND day_of_week = %s 
            AND start_time <= %s 
            AND end_time >= %s
            """

            cursor.execute(check_query, (
                healthcare_professional_id,
                day_of_week,
                appointment_time,
                appointment_time
            ))

            if cursor.fetchone()[0] == 0:
                raise Exception("This healthcare professional is not available at this time.")

            # Check if there's already an appointment at this time
            check_existing = """
            SELECT COUNT(*) 
            FROM Appointment 
            WHERE healthcare_professional_id = %s 
            AND appointment_date = %s 
            AND appointment_time = %s
            """

            cursor.execute(check_existing, (
                healthcare_professional_id,
                appointment_date,
                appointment_time
            ))

            if cursor.fetchone()[0] > 0:
                raise Exception("This time slot is already booked.")

            # Insert the new appointment
            insert_query = """
            INSERT INTO Appointment 
            (patient_id, healthcare_professional_id, appointment_date, appointment_time, 
             visit_type, appointment_notes) 
            VALUES (%s, %s, %s, %s, %s, %s)
            """

            cursor.execute(insert_query, (
                patient_id,
                healthcare_professional_id,
                appointment_date,
                appointment_time,
                visit_type,
                notes
            ))

            connection.commit()
            return True

        except mysql.connector.Error as e:
            connection.rollback()
            raise Exception(f"Database error: {str(e)}")
        finally:
            cursor.close()
            connection.close()

    # Finds the appointments for a patient
    def get_appointments(self, patient_id):
        connection = self.connect()
        cursor = connection.cursor(dictionary=True)
        try:
            query = """
                SELECT 
                    a.appointment_id,
                    a.appointment_date,
                    TIME_FORMAT(a.appointment_time, '%I:%i %p') as appointment_time,
                    a.visit_type,
                    CONCAT(h.first_name, ' ', h.last_name) as doctor_name,
                    h.healthcare_professional_id,
                    a.appointment_notes
                FROM Appointment a
                JOIN Healthcare_Professional h ON a.healthcare_professional_id = h.healthcare_professional_id
                WHERE a.patient_id = %s
                AND (a.appointment_date > CURDATE() 
                     OR (a.appointment_date = CURDATE() AND a.appointment_time >= CURTIME()))
                ORDER BY a.appointment_date, a.appointment_time
            """
            cursor.execute(query, (patient_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            connection.close()

    # Updates appointment table when appointment is cancelled
    def delete_appointment(self, appointment_id):
        connection = self.connect()
        cursor = connection.cursor()
        try:
            query = "DELETE FROM Appointment WHERE appointment_id = %s"
            cursor.execute(query, (appointment_id,))
            connection.commit()
            return True
        finally:
            cursor.close()
            connection.close()

    # Get possible appointment times based on professionals availibility
    def get_available_time_slots(self):
        connection = self.connect()
        cursor = connection.cursor()
        try:
            query = """
            SELECT DISTINCT start_time, end_time 
            FROM Professional_Availability
            ORDER BY start_time;
            """
            cursor.execute(query)
            results = cursor.fetchall()

            time_slots = set()
            for start_time, end_time in results:
                # Convert times to minutes
                if isinstance(start_time, timedelta):
                    start_minutes = start_time.seconds // 60
                    end_minutes = end_time.seconds // 60
                else:
                    start_minutes = (start_time.hour * 60) + start_time.minute
                    end_minutes = (end_time.hour * 60) + end_time.minute

                # Generate 30-minute slots
                current_minutes = start_minutes
                while current_minutes < end_minutes:
                    hours = current_minutes // 60
                    minutes = current_minutes % 60
                    period = 'AM' if hours < 12 else 'PM'
                    display_hour = hours if hours <= 12 else hours - 12
                    if display_hour == 0:
                        display_hour = 12
                    time_slots.add(f"{display_hour}:{minutes:02d} {period}")
                    current_minutes += 30

            return sorted(time_slots, key=lambda x: datetime.strptime(x, '%I:%M %p'))
        finally:
            cursor.close()
            connection.close()

    # Find health care professionals available at specific date and time
    def get_available_doctors(self, selected_date, selected_time):
        connection = self.connect()
        cursor = connection.cursor(dictionary=True)
        try:
            time_obj = datetime.strptime(selected_time, '%I:%M %p').time()
            day_of_week = selected_date.strftime('%A')

            query = """
            SELECT DISTINCT 
                h.healthcare_professional_id,
                h.first_name,
                h.last_name,
                CONCAT(h.first_name, ' ', h.last_name) AS doctor_name,
                CASE 
                    WHEN d.healthcare_professional_id IS NOT NULL THEN 'Doctor'
                    WHEN n.healthcare_professional_id IS NOT NULL THEN 'Nurse'
                    WHEN pa.healthcare_professional_id IS NOT NULL THEN 'PA'
                END AS role
            FROM Healthcare_Professional h
            LEFT JOIN Doctor d ON h.healthcare_professional_id = d.healthcare_professional_id
            LEFT JOIN Nurse n ON h.healthcare_professional_id = n.healthcare_professional_id
            LEFT JOIN Physician_Assistant pa ON h.healthcare_professional_id = pa.healthcare_professional_id
            JOIN Professional_Availability pa_av ON h.healthcare_professional_id = pa_av.healthcare_professional_id
            WHERE pa_av.day_of_week = %s
            AND %s BETWEEN pa_av.start_time AND pa_av.end_time
            AND NOT EXISTS (
                SELECT 1 FROM Appointment a 
                WHERE a.healthcare_professional_id = h.healthcare_professional_id
                AND a.appointment_date = %s
                AND a.appointment_time = %s
            )
            ORDER BY h.last_name, h.first_name;
            """

            cursor.execute(query, (day_of_week, time_obj, selected_date, time_obj))
            return cursor.fetchall()
        finally:
            cursor.close()
            connection.close()

    # allows professionals to add new patients
    def add_new_patient(self, first_name, last_name, birth_date, gender, phone, zipcode, ssn, allergies):
        connection = self.connect()
        cursor = connection.cursor()

        try:
            # Get max ID and increment
            cursor.execute("SELECT MAX(patient_id) FROM Patient")
            result = cursor.fetchone()[0]
            patient_id = 10001 if result is None else int(result) + 1

            # Generate password
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

            # Insert new patient
            query = """
                INSERT INTO Patient 
                (patient_id, first_name, last_name, birth_date, gender,
                 phone_number, zip_code, ssn, allergies, patient_password)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """

            cursor.execute(query, (
                patient_id,
                first_name,
                last_name,
                birth_date,
                gender,
                phone,
                zipcode,
                ssn,
                allergies,
                password
            ))

            connection.commit()
            return patient_id, password

        finally:
            cursor.close()
            connection.close()

    # retrieves a professionals appointments
    def get_professional_appointments(self, healthcare_id):
        connection = self.connect()
        cursor = connection.cursor(dictionary=True)

        try:
            query = """
            SELECT 
                a.appointment_id,
                a.appointment_date,
                TIME_FORMAT(a.appointment_time, '%h:%i %p') as appointment_time,
                a.visit_type,
                a.appointment_notes,
                p.first_name,
                p.last_name,
                p.patient_id
            FROM Appointment a
            JOIN Patient p ON a.patient_id = p.patient_id
            WHERE a.healthcare_professional_id = %s
            AND a.appointment_date >= CURDATE()
            ORDER BY a.appointment_date, a.appointment_time;
            """

            cursor.execute(query, (healthcare_id,))
            return cursor.fetchall()

        finally:
            cursor.close()
            connection.close()

    # Get appointment details for professional view
    def get_appointment_details(self, appointment_id):
        connection = self.connect()
        cursor = connection.cursor(dictionary=True)

        try:
            query = """
            SELECT 
                a.*,
                p.first_name,
                p.last_name,
                p.allergies,
                p.patient_id
            FROM Appointment a
            JOIN Patient p ON a.patient_id = p.patient_id
            WHERE a.appointment_id = %s
            """

            cursor.execute(query, (appointment_id,))
            return cursor.fetchone()

        finally:
            cursor.close()
            connection.close()

    def get_patient_info(self, patient_id):
        connection = self.connect()
        cursor = connection.cursor(dictionary=True)

        try:
            query = """
            SELECT * FROM Patient 
            WHERE patient_id = %s
            """
            cursor.execute(query, (patient_id,))
            return cursor.fetchone()
        finally:
            cursor.close()
            connection.close()

    def get_medications(self, patient_id):
        connection = self.connect()
        cursor = connection.cursor(dictionary=True)

        try:
            query = """
            SELECT medication_name, dosage, side_effects, start_date, end_date
            FROM medication 
            WHERE patient_id = %s
            """
            cursor.execute(query, (patient_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            connection.close()

    def get_medical_history(self, patient_id):
        connection = self.connect()
        cursor = connection.cursor(dictionary=True)

        try:
            query = """
            SELECT treatment_date, diagnosis, notes 
            FROM medical_history 
            WHERE patient_id = %s 
            ORDER BY treatment_date DESC
            """
            cursor.execute(query, (patient_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            connection.close()

    def process_payment(self, bill_id, amount):
        connection = self.connect()
        cursor = connection.cursor()

        try:
            query = """
            UPDATE bill 
            SET status = 'Paid', 
                payment_date = CURDATE() 
            WHERE bill_id = %s
            """
            cursor.execute(query, (bill_id,))
            connection.commit()
        finally:
            cursor.close()
            connection.close()

    # Allows professional to add medical history during an appointment
    def add_medical_history(self, patient_id, healthcare_id, diagnosis, notes, treatment_date=None):
        connection = self.connect()
        cursor = connection.cursor()

        try:
            if treatment_date is None:
                treatment_date = datetime.now().date()

            query = """
            INSERT INTO medical_history 
            (patient_id, healthcare_professional_id, treatment_date, diagnosis, notes)
            VALUES (%s, %s, %s, %s, %s)
            """

            cursor.execute(query, (
                patient_id,
                healthcare_id,
                treatment_date,
                diagnosis if diagnosis else None,  # Allow NULL diagnosis
                notes
            ))

            history_id = cursor.lastrowid
            connection.commit()
            return history_id

        finally:
            cursor.close()
            connection.close()

    # Allows professional to prescribe a medication
    def add_medication(self, patient_id, medication_name, dosage=None, side_effects=None):
        connection = self.connect()
        cursor = connection.cursor()

        try:
            query = """
            INSERT INTO medication 
            (patient_id, medication_name, dosage, side_effects)
            VALUES (%s, %s, %s, %s)
            """

            cursor.execute(query, (
                patient_id,
                medication_name,
                dosage,
                side_effects
            ))

            connection.commit()

        finally:
            cursor.close()
            connection.close()

    # Allows professional to generate billing
    def create_bill(self, patient_id, appointment_id, amount):
        connection = self.connect()
        cursor = connection.cursor(dictionary=True)

        try:
            # First get the appointment date
            query = """
                SELECT appointment_date 
                FROM Appointment 
                WHERE appointment_id = %s
                """
            cursor.execute(query, (appointment_id,))
            appointment = cursor.fetchone()

            # Calculate due date as one year from appointment date
            appointment_date = appointment['appointment_date']
            due_date = appointment_date + timedelta(days=365)

            # Insert bill
            insert_query = """
                INSERT INTO bill 
                (patient_id, appointment_id, amount, date_issued, due_date, status)
                VALUES (%s, %s, %s, CURDATE(), %s, %s)
                """

            cursor.execute(insert_query, (
                patient_id,
                appointment_id,
                amount,
                due_date,
                'Unpaid'
            ))

            bill_id = cursor.lastrowid
            connection.commit()
            return bill_id

        finally:
            cursor.close()
            connection.close()