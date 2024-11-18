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

    def connect(self):
        try:
            return mysql.connector.connect(**self.db_config)
        except mysql.connector.Error as e:
            raise Exception(f"Could not connect to database: {e}")

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

    def cancel_appointment(self, appointment_id):
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