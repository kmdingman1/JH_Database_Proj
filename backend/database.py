from contextlib import contextmanager
from datetime import datetime, timedelta
import string
import random
import mysql.connector
from typing import Optional, Dict, List, Any, Union, Tuple
from decimal import Decimal


class DatabaseError(Exception):
    """Custom exception for database errors"""
    pass


class HealthcareDatabase:

    def __init__(self):
        self.db_config = {
            "host": "localhost",
            "user": "root",
            "password": "COSC578_Hopkins",
            "database": "hopkins_health_hub"
        }

    @contextmanager
    def get_cursor(self, dictionary: bool = False):
        """Context manager for database connections"""
        connection = mysql.connector.connect(**self.db_config)
        cursor = connection.cursor(dictionary=dictionary)
        try:
            yield cursor
            connection.commit()
        except mysql.connector.Error as e:
            connection.rollback()
            raise DatabaseError(f"Database operation failed: {str(e)}")
        finally:
            cursor.close()
            connection.close()

    # Execute select
    def execute_query(self, query: str, params: tuple = None, dictionary: bool = False) -> List[Dict]:
        with self.get_cursor(dictionary=dictionary) as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()

    # Execute insert/delete/update
    def execute_update(self, query: str, params: tuple = None) -> int:
        with self.get_cursor() as cursor:
            cursor.execute(query, params)
            return cursor.rowcount

    # Generate password for new patient
    def generate_password(self, length: int = 8) -> str:
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    # Authentication Methods
    def verify_login(self, user_id: str, password: str, user_type: str) -> bool:
        queries = {
            'patient': """
                SELECT patient_id 
                FROM Patient 
                WHERE patient_id = %s 
                AND patient_password = %s
            """,
            'professional': """
                SELECT healthcare_professional_id 
                FROM Healthcare_Professional 
                WHERE healthcare_professional_id = %s 
                AND healthprof_password = %s
            """
        }
        query = queries.get(user_type)
        if not query:
            raise ValueError("Invalid user type")

        return bool(self.execute_query(query, (user_id, password)))

    def verify_patient_login(self, patient_id: str, password: str) -> bool:
        return self.verify_login(patient_id, password, 'patient')

    def verify_professional_login(self, healthcare_id: str, password: str) -> bool:
        """Verify healthcare professional login credentials"""
        return self.verify_login(healthcare_id, password, 'professional')

    # Check that professional is available
    def validate_appointment_time(self, healthcare_id: str, date: datetime.date, time: datetime.time) -> bool:
        day_of_week = date.strftime('%A')
        query = """
            SELECT COUNT(*) 
            FROM Professional_Availability 
            WHERE healthcare_professional_id = %s 
            AND day_of_week = %s 
            AND start_time <= %s 
            AND end_time >= %s
        """
        result = self.execute_query(query, (healthcare_id, day_of_week, time, time))
        return result[0][0] > 0

    # Check for existing appointments
    def check_existing_appointment(self, healthcare_id: str, date: datetime.date, time: datetime.time) -> bool:
        query = """
            SELECT COUNT(*) 
            FROM Appointment 
            WHERE healthcare_professional_id = %s 
            AND appointment_date = %s 
            AND appointment_time = %s
        """
        result = self.execute_query(query, (healthcare_id, date, time))
        return result[0][0] > 0

    # Submit a new appointment
    def submit_appointment(self, visit_type: str, appointment_date: Union[str, datetime.date],
                           appointment_time: str, healthcare_id: str, notes: str,
                           patient_id: str) -> bool:
        # Convert string dates/times to proper objects if needed
        if isinstance(appointment_date, str):
            appointment_date = datetime.strptime(appointment_date, '%Y-%m-%d').date()
        if isinstance(appointment_time, str):
            appointment_time = datetime.strptime(appointment_time, '%I:%M %p').time()

        # Validate availability
        if not self.validate_appointment_time(healthcare_id, appointment_date, appointment_time):
            raise DatabaseError("Healthcare professional is not available at this time")

        # Check for existing appointments
        if self.check_existing_appointment(healthcare_id, appointment_date, appointment_time):
            raise DatabaseError("This time slot is already booked")

        # Insert appointment
        query = """
            INSERT INTO Appointment 
            (patient_id, healthcare_professional_id, appointment_date, appointment_time, 
             visit_type, appointment_notes) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        self.execute_update(query, (
            patient_id, healthcare_id, appointment_date,
            appointment_time, visit_type, notes
        ))
        return True

    # Get appointments for patients or professionals
    def get_appointments_by_type(self, id_value: str, user_type: str) -> List[Dict]:
        base_query = """
            SELECT 
                a.appointment_id,
                a.appointment_date,
                TIME_FORMAT(a.appointment_time, '%I:%i %p') as appointment_time,
                a.visit_type,
                a.appointment_notes
        """

        if user_type == 'patient':
            query = base_query + """
                , CONCAT(h.first_name, ' ', h.last_name) as doctor_name
                , h.healthcare_professional_id
                FROM Appointment a
                JOIN Healthcare_Professional h ON a.healthcare_professional_id = h.healthcare_professional_id
                WHERE a.patient_id = %s
                AND (a.appointment_date > CURDATE() 
                     OR (a.appointment_date = CURDATE() AND a.appointment_time >= CURTIME()))
                ORDER BY a.appointment_date, a.appointment_time
            """
        else:
            query = base_query + """
                , CONCAT(p.first_name, ' ', p.last_name) as patient_name
                , p.patient_id
                FROM Appointment a
                JOIN Patient p ON a.patient_id = p.patient_id
                WHERE a.healthcare_professional_id = %s
                AND a.appointment_date >= CURDATE()
                ORDER BY a.appointment_date, a.appointment_time
            """

        return self.execute_query(query, (id_value,), dictionary=True)

    # Retrieve Patient Appointments
    def get_appointments(self, patient_id: str) -> List[Dict]:
        with self.get_cursor(dictionary=True) as cursor:
            query = """
            SELECT 
                a.appointment_id,
                a.appointment_date,
                TIME_FORMAT(a.appointment_time, '%h:%i %p') as appointment_time,
                a.visit_type,
                CONCAT(h.first_name, ' ', h.last_name) as doctor_name,
                COALESCE(a.appointment_notes, 'N/A') as appointment_notes,
                h.healthcare_professional_id
            FROM Appointment a
            JOIN Healthcare_Professional h ON a.healthcare_professional_id = h.healthcare_professional_id
            WHERE a.patient_id = %s
            AND (a.appointment_date >= CURDATE())
            ORDER BY a.appointment_date, a.appointment_time
            """

            cursor.execute(query, (patient_id,))
            appointments = cursor.fetchall()

            # Format the dates and times
            for appt in appointments:
                if isinstance(appt['appointment_date'], datetime):
                    appt['appointment_date'] = appt['appointment_date'].date()
                if not isinstance(appt['appointment_time'], str):
                    # Convert 24-hour time to 12-hour format
                    time_obj = datetime.strptime(str(appt['appointment_time']), '%H:%M:%S').time()
                    appt['appointment_time'] = time_obj.strftime('%I:%M %p')

            return appointments

    # Retrieve appointments for healthcare professional
    def get_professional_appointments(self, healthcare_id: str) -> List[Dict]:
        with self.get_cursor(dictionary=True) as cursor:
            query = """
            SELECT 
                a.appointment_id,
                a.appointment_date,
                TIME_FORMAT(a.appointment_time, '%h:%i %p') as appointment_time,
                a.visit_type,
                a.appointment_notes,
                p.first_name as patient_first_name,
                p.last_name as patient_last_name,
                p.patient_id
            FROM Appointment a
            JOIN Patient p ON a.patient_id = p.patient_id
            WHERE a.healthcare_professional_id = %s
            AND a.appointment_date >= CURDATE()
            ORDER BY a.appointment_date, a.appointment_time
            """

            cursor.execute(query, (healthcare_id,))
            appointments = cursor.fetchall()

            # Format the appointments to ensure consistent field names
            formatted_appointments = []
            for appt in appointments:
                formatted_appt = {
                    'appointment_id': appt['appointment_id'],
                    'appointment_date': appt['appointment_date'],
                    'appointment_time': appt['appointment_time'],
                    'visit_type': appt['visit_type'],
                    'appointment_notes': appt['appointment_notes'] if appt['appointment_notes'] else '',
                    'first_name': appt['patient_first_name'],
                    'last_name': appt['patient_last_name'],
                    'patient_id': appt['patient_id']
                }
                formatted_appointments.append(formatted_appt)

            return formatted_appointments

    # Get appointment details for encounter
    def get_appointment_details(self, appointment_id: int) -> Dict:
        with self.get_cursor(dictionary=True) as cursor:
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

    # Cancel an appointments
    def delete_appointment(self, appointment_id: int) -> bool:
        query = "DELETE FROM Appointment WHERE appointment_id = %s"
        return bool(self.execute_update(query, (appointment_id,)))

    # Find available time slots for appointments
    def get_available_time_slots(self) -> List[str]:
        query = """
            SELECT DISTINCT start_time, end_time 
            FROM Professional_Availability
            ORDER BY start_time
        """
        results = self.execute_query(query)
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

    # Find available doctors for appointment time
    def get_available_doctors(self, selected_date: datetime.date, selected_time: str) -> List[Dict]:
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
            ORDER BY h.last_name, h.first_name
        """
        return self.execute_query(query, (day_of_week, time_obj, selected_date, time_obj), dictionary=True)

    # Patient Management Methods
    # Add a new patient into the system
    def add_new_patient(self, first_name: str, last_name: str, birth_date: str,
                        gender: str, phone: str, zipcode: str, ssn: str,
                        allergies: Optional[str] = None) -> Tuple[int, str]:
        with self.get_cursor() as cursor:
            # Get max ID and increment
            cursor.execute("SELECT MAX(patient_id) FROM Patient")
            result = cursor.fetchone()[0]
            patient_id = 10001 if result is None else int(result) + 1

            # Generate password
            password = self.generate_password()

            query = """
                INSERT INTO Patient 
                (patient_id, first_name, last_name, birth_date, gender,
                 phone_number, zip_code, ssn, allergies, patient_password)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                patient_id, first_name, last_name, birth_date, gender,
                phone, zipcode, ssn, allergies, password
            ))

            return patient_id, password

    # Retrieve patient information
    def get_patient_info(self, patient_id: str) -> Dict:
        query = "SELECT * FROM Patient WHERE patient_id = %s"
        results = self.execute_query(query, (patient_id,), dictionary=True)
        return results[0] if results else {}

    # Get a patients medical history
    def get_medical_history(self, patient_id: str) -> List[Dict]:
        query = """
            SELECT treatment_date, diagnosis, notes 
            FROM medical_history 
            WHERE patient_id = %s 
            ORDER BY treatment_date DESC
        """
        return self.execute_query(query, (patient_id,), dictionary=True)

    # Update medical history
    def add_medical_history(self, patient_id: str, healthcare_id: str,
                            diagnosis: Optional[str], notes: str,
                            treatment_date: Optional[datetime.date] = None) -> int:
        if treatment_date is None:
            treatment_date = datetime.now().date()

        query = """
            INSERT INTO medical_history 
            (patient_id, healthcare_professional_id, treatment_date, diagnosis, notes)
            VALUES (%s, %s, %s, %s, %s)
        """
        return self.execute_update(query, (
            patient_id, healthcare_id, treatment_date,
            diagnosis if diagnosis else None, notes
        ))

    # Medication and Prescription Methods

    # Get medications
    def get_medications(self) -> List[Dict]:
        query = """
            SELECT medication_id, medication_name, side_effects, cost
            FROM medication
        """
        return self.execute_query(query, dictionary=True)

    # Retrieve patient prescription
    def get_patient_prescriptions(self, patient_id: str) -> List[Dict]:
        query = """
            SELECT p.*, m.medication_name, m.side_effects, m.cost
            FROM prescription p
            JOIN medication m ON p.medication_id = m.medication_id
            WHERE p.patient_id = %s
        """
        return self.execute_query(query, (patient_id,), dictionary=True)

    # Add presciption method
    def add_prescription(self, patient_id: str, medication_id: int, dosage: str,
                         start_date: datetime.date, end_date: datetime.date,
                         healthcare_id: str) -> int:
        query = """
            INSERT INTO prescription 
            (patient_id, medication_id, dosage, start_date, end_date, healthcare_professional_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        return self.execute_update(query, (
            patient_id, medication_id, dosage,
            start_date, end_date, healthcare_id
        ))

    # Billing Methods
    # Create bill
    def create_bill(self, patient_id: str, appointment_id: int, amount: float) -> int:
        with self.get_cursor(dictionary=True) as cursor:
            try:
                # Get appointment date
                cursor.execute("""
                    SELECT appointment_date 
                    FROM Appointment 
                    WHERE appointment_id = %s
                """, (appointment_id,))
                appointment = cursor.fetchone()

                if not appointment:
                    raise DatabaseError("Appointment not found")

                # Calculate due date as one year from appointment date
                due_date = appointment['appointment_date'] + timedelta(days=365)

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
                print(f"Created bill with ID: {bill_id}")  # Debug print
                return bill_id

            except Exception as e:
                print(f"Error creating bill: {str(e)}")  # Debug print
                raise DatabaseError(f"Failed to create bill: {str(e)}")

    # Get patient bills
    def get_patient_bills(self, patient_id: str) -> List[Dict]:
        with self.get_cursor(dictionary=True) as cursor:
            query = """
            SELECT 
                b.bill_id,
                b.amount,
                b.date_issued,
                b.due_date,
                b.status,
                a.appointment_date
            FROM bill b
            JOIN Appointment a ON b.appointment_id = a.appointment_id
            WHERE b.patient_id = %s AND b.amount > 0
            ORDER BY b.date_issued DESC
            """
            cursor.execute(query, (patient_id,))
            return cursor.fetchall()

    # Get bill details
    def get_bill_details(self, bill_id: int) -> Dict:
        query = """
            SELECT 
                b.*,
                a.appointment_date,
                a.appointment_time,
                a.visit_type,
                CONCAT(p.first_name, ' ', p.last_name) as patient_name,
                CONCAT(h.first_name, ' ', h.last_name) as doctor_name
            FROM bill b
            JOIN Appointment a ON b.appointment_id = a.appointment_id
            JOIN Patient p ON b.patient_id = p.patient_id
            JOIN Healthcare_Professional h ON a.healthcare_professional_id = h.healthcare_professional_id
            WHERE b.bill_id = %s
        """

        results = self.execute_query(query, (bill_id,), dictionary=True)
        if not results:
            raise DatabaseError(f"Bill with ID {bill_id} not found")

        bill = results[0]
        # Format decimal values and dates
        bill['amount'] = float(bill['amount'])
        bill['date_issued'] = bill['date_issued'].strftime('%m/%d/%Y')
        bill['due_date'] = bill['due_date'].strftime('%m/%d/%Y')
        bill['appointment_date'] = bill['appointment_date'].strftime('%m/%d/%Y')
        bill['appointment_time'] = bill['appointment_time'].strftime('%I:%M %p')

        return bill

    # Get summary of billing history
    def get_billing_summary(self, patient_id: str) -> Dict:
        query = """
            SELECT 
                SUM(CASE WHEN status != 'Paid' THEN amount ELSE 0 END) as outstanding_balance,
                SUM(CASE WHEN status = 'Paid' THEN amount ELSE 0 END) as total_paid,
                SUM(amount) as total_billed,
                COUNT(CASE WHEN status != 'Paid' AND due_date < CURDATE() THEN 1 END) as overdue_bills
            FROM bill
            WHERE patient_id = %s
        """

        results = self.execute_query(query, (patient_id,), dictionary=True)
        summary = results[0]

        # Format decimal values
        for key in ['outstanding_balance', 'total_paid', 'total_billed']:
            summary[key] = float(summary[key] if summary[key] is not None else 0)

        return summary

    # Proces payment for a bill
    def process_payment(self, bill_id: int, payment_amount: float) -> Dict:
        with self.get_cursor(dictionary=True) as cursor:
            # Get current bill amount
            cursor.execute("SELECT amount FROM bill WHERE bill_id = %s", (bill_id,))
            bill = cursor.fetchone()

            if not bill:
                raise DatabaseError(f"Bill not found")

            # Calculate new amount
            current_amount = float(bill['amount'])
            new_amount = current_amount - payment_amount

            if new_amount <= 0:
                # If paid in full, delete the bill
                cursor.execute("DELETE FROM bill WHERE bill_id = %s", (bill_id,))
            else:
                # If partial payment, update amount but keep status as Unpaid
                cursor.execute("""
                    UPDATE bill 
                    SET amount = %s, 
                        status = 'Unpaid'
                    WHERE bill_id = %s
                """, (new_amount, bill_id))