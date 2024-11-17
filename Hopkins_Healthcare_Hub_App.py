import tkinter as tk
from datetime import datetime, timedelta
from tkinter import ttk, messagebox
import mysql
from PIL import Image, ImageTk
from mysql.connector import connect, Error
from tkcalendar import Calendar


class HealthcareHub:
    def __init__(self, root):

        # Initialize root window and db configuration
        self.root = root
        self.db_config = {
            "host": "localhost",
            "user": "root",
            "password": "COSC578_Hopkins",
            "database": "hopkins_health_hub"
        }

        # Main window settings
        self._configure_window()
        # Set up visual styles
        self._setup_styles()
        # Show initial selection screen
        self.selection_screen()

    # Configurations for windows
    def _configure_window(self):
        self.root.title("Hopkins Health Hub")
        self.root.geometry("700x550")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.configure(bg='#dae8f5')

        # Set window icon
        icon = tk.PhotoImage(file="images/HopkinsLogo.png")
        self.root.iconphoto(True, icon)

    # Configurations for style
    def _setup_styles(self):
        # Button styling
        self.button_style = {
            'font': ('Verdana', 12),
            'bg': '#03294a',
            'fg': 'white',
            'activebackground': '#0b8dd4',
            'activeforeground': 'white',
            'relief': 'flat',
            'padx': 30,
            'pady': 10,
            'cursor': 'hand2',
        }

        # TTK styles
        self.style = ttk.Style()
        self.style.configure('Custom.TFrame', background='#dae8f5')
        self.style.configure('Image.TLabel', padding=0, background='#dae8f5')
        self.style.configure('Login.TLabelframe', background='#dae8f5')
        self.style.configure('Login.TLabelframe.Label',
                             font=('Verdana', 20, 'bold'),
                             background='#dae8f5',
                             foreground='#010100')
        self.style.configure('TLabel',
                             background='#dae8f5',
                             foreground='#010100',
                             font=('Verdana', 13))

    # Hopkins Logo
    def _add_logo(self, parent, size=(181, 60), row=0, column=0, pady=(0, 10)):
        try:
            # Load and resize the image
            img = Image.open("images/DB Logo.png")
            img = img.resize(size)
            photo = ImageTk.PhotoImage(img)

            # Create and place the logo label
            image_label = ttk.Label(parent, image=photo, style='Image.TLabel')
            image_label.image = photo  # Keep a reference to avoid garbage collection
            image_label.grid(row=row, column=column, pady=pady)
        except Exception as e:
            messagebox.showerror("Error", f"Unable to load logo: {e}")

    # Create and return DB connection
    def create_db_connection(self):
        try:
            return mysql.connector.connect(**self.db_config)
        except Error as e:
            messagebox.showerror("Database Error", f"Could not connect to database: {e}")
            return None

    # Main selection screen on start up
    def selection_screen(self):
        self.clear_window()

        # Main frame
        main_frame = ttk.Frame(self.root, padding="40", style='Custom.TFrame')
        main_frame.grid(row=0, column=0)

        # Add logo
        self._add_logo(main_frame, size=(362, 120))

        # Button container
        button_frame = ttk.Frame(main_frame, style='Custom.TFrame')
        button_frame.grid(row=1, column=0)
        button_frame.grid_columnconfigure(0, weight=1)

        # Log in buttons
        patient_btn = tk.Button(button_frame,
                                text="Patient Login",
                                command=self.patient_login,
                                **self.button_style)
        patient_btn.grid(row=0, column=0, pady=(0, 20))

        professional_btn = tk.Button(button_frame,
                                     text="Healthcare Professional Login",
                                     command=self.professional_login,
                                     **self.button_style)
        professional_btn.grid(row=1, column=0)

    # Patient Log in
    def patient_login(self):
        self.clear_window()

        # Main frame
        main_frame = ttk.Frame(self.root, padding="20", style='Custom.TFrame')
        main_frame.grid(row=0, column=0, sticky='nsew')

        # Logo
        self._add_logo(main_frame)

        # Login frame
        login_frame = ttk.LabelFrame(
            main_frame,
            text="Patient Login",
            padding="20",
            style='Login.TLabelframe'
        )
        login_frame.grid(row=1, column=0, padx=20, pady=20, sticky=(tk.W, tk.E))

        # Entry fields
        ttk.Label(login_frame, text="Patient ID:").grid(row=0, column=0, pady=5, sticky=tk.W)
        patient_id = ttk.Entry(login_frame, width=30)
        patient_id.grid(row=0, column=1, pady=5)

        ttk.Label(login_frame, text="Password:").grid(row=1, column=0, pady=5, sticky=tk.W)
        password = ttk.Entry(login_frame, show="*", width=30)
        password.grid(row=1, column=1, pady=5)

        # Buttons
        button_frame = ttk.Frame(login_frame, style='Custom.TFrame')
        button_frame.grid(row=2, column=0, columnspan=2, pady=20)

        submit_btn = tk.Button(
            button_frame,
            text="Submit",
            command=lambda: self.login_patient(patient_id.get(), password.get()),
            **self.button_style
        )
        submit_btn.grid(row=0, column=0, padx=10)

        back_btn = tk.Button(
            button_frame,
            text="Back",
            command=self.selection_screen,
            **self.button_style
        )
        back_btn.grid(row=0, column=1, padx=10)

    # Professional Log in
    def professional_login(self):
        self.clear_window()

        # Main frame
        main_frame = ttk.Frame(self.root, padding="20", style='Custom.TFrame')
        main_frame.grid(row=0, column=0, sticky='nsew')

        # Logo
        self._add_logo(main_frame)

        # Login frame
        frame = ttk.LabelFrame(main_frame, text="Healthcare Professional Login",
                               padding="20", style='Login.TLabelframe')
        frame.grid(row=1, column=0, padx=20, pady=20, sticky=(tk.W, tk.E))

        # Entry fields
        ttk.Label(frame, text="Healthcare ID:").grid(row=0, column=0, pady=5)
        healthcare_id = ttk.Entry(frame, width=30)
        healthcare_id.grid(row=0, column=1, pady=5)

        ttk.Label(frame, text="Password:").grid(row=1, column=0, pady=5)
        password = ttk.Entry(frame, show="*", width=30)
        password.grid(row=1, column=1, pady=5)

        # Buttons
        button_frame = ttk.Frame(frame, style='Custom.TFrame')
        button_frame.grid(row=2, column=0, columnspan=2, pady=20)

        submit_btn = tk.Button(button_frame, text="Submit",
                               command=lambda: self.login_professional(healthcare_id.get(), password.get()),
                               **self.button_style)
        submit_btn.grid(row=0, column=0, padx=10)

        back_btn = tk.Button(button_frame, text="Back",
                             command=self.selection_screen,
                             **self.button_style)
        back_btn.grid(row=0, column=1, padx=10)

    # Log in authentication for patient
    def login_patient(self, patient_id, password):
        if not patient_id or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return

        try:
            connection = self.create_db_connection()
            if connection is None:
                return

            cursor = connection.cursor()

            # Query to check patient credentials
            query = """SELECT patient_id 
                      FROM Patient 
                      WHERE patient_id = %s 
                      AND patient_password = %s"""

            cursor.execute(query, (patient_id, password))
            result = cursor.fetchone()

            if result:
                messagebox.showinfo("Success", "Login successful!")
                self.patient_portal(patient_id)
            else:
                messagebox.showerror("Error", "Invalid ID or password")

        except Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()

    # Log in authentication for professional
    def login_professional(self, healthcare_id, password):
        if not healthcare_id or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return

        try:
            connection = self.create_db_connection()
            if connection is None:
                return

            cursor = connection.cursor()

            # Query to check healthcare professional credentials
            query = """SELECT healthcare_professional_id 
                              FROM Healthcare_Professional 
                              WHERE healthcare_professional_id = %s 
                              AND healthprof_password = %s"""

            cursor.execute(query, (healthcare_id, password))
            result = cursor.fetchone()

            if result:
                messagebox.showinfo("Success", "Login successful!")
                self.professional_portal(healthcare_id)
            else:
                messagebox.showerror("Error", "Invalid ID or password")

        except Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()

    # Patient Portal
    def patient_portal(self, patient_id):
        self.clear_window()

        # Main frame
        main_frame = ttk.Frame(self.root, padding="20", style='Custom.TFrame')
        main_frame.grid(row=0, column=0, sticky='nsew')

        # Grid weights for centering
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(2, weight=1)  # For button frame
        main_frame.grid_columnconfigure(0, weight=1)

        # Logo
        self._add_logo(main_frame)

        # Centers header and buttons
        ttk.Label(main_frame,
                  text="Welcome to Patient Portal",
                  font=('Verdana', 20, 'bold')).grid(row=1, column=0, pady=(0, 30))
        button_frame = ttk.Frame(main_frame, style='Custom.TFrame')
        button_frame.grid(row=2, column=0, sticky='n')
        button_frame.grid_columnconfigure(0, weight=1)

        # Patient Portal Buttons
        button_width = 25

        appointments_btn = tk.Button(button_frame,
                                     text="View or Schedule Appointment",
                                     width=button_width,
                                     command=lambda: self.appointments_patient(patient_id),
                                     **self.button_style)
        appointments_btn.grid(row=0, column=0, pady=5)

        view_bill_btn = tk.Button(button_frame,
                                  text="View My Bills",
                                  width=button_width,
                                  command=lambda: self.bills_patient(patient_id),
                                  **self.button_style)
        view_bill_btn.grid(row=1, column=0, pady=5)

        medications_btn = tk.Button(button_frame,
                                    text="View My Medications",
                                    width=button_width,
                                    command=lambda: self.medications_patient(),
                                    **self.button_style)
        medications_btn.grid(row=2, column=0, pady=5)

        # Logout button
        logout_btn = tk.Button(button_frame,
                               text="Logout",
                               width=button_width,
                               command=self.selection_screen,
                               **self.button_style)
        logout_btn.grid(row=3, column=0, pady=(20, 0))

    # Patient side view for Appointments
    def appointments_patient(self, patient_id):
        self.clear_window()

        # Main frame
        main_frame = ttk.Frame(self.root, padding="20", style='Custom.TFrame')
        main_frame.grid(row=0, column=0, sticky='nsew')

        # Grid weights for centering
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(2, weight=1)  # For button frame
        main_frame.grid_columnconfigure(0, weight=1)

        # Logo
        self._add_logo(main_frame)

        # Centers header and button containers
        ttk.Label(main_frame,
                  text="My Appointments",
                  font=('Verdana', 20, 'bold')).grid(row=1, column=0, pady=(0, 30))
        button_frame = ttk.Frame(main_frame, style='Custom.TFrame')
        button_frame.grid(row=2, column=0, sticky='n')
        button_frame.grid_columnconfigure(0, weight=1)

        # Patient Appointment Buttons
        button_width = 25

        view_appointments_btn = tk.Button(button_frame,
                                          text="View my Upcoming Appointments",
                                          width=button_width,
                                          command=lambda: self.view_appointment_patient(patient_id),
                                          **self.button_style)
        view_appointments_btn.grid(row=0, column=0, pady=5)

        schedule_appointment_btn = tk.Button(button_frame,
                                             text="Schedule New Appointment",
                                             width=button_width,
                                             command=lambda: self.schedule_appointment_patient(patient_id),
                                             **self.button_style)
        schedule_appointment_btn.grid(row=1, column=0, pady=5)

        # Back button
        back_btn = tk.Button(button_frame,
                             text="Back to Portal",
                             width=button_width,
                             command=lambda: self.patient_portal(patient_id),
                             **self.button_style)
        back_btn.grid(row=2, column=0, pady=5)

    # Patient Side view for scheduling appointments
    # Need to fix -- getting a bug not allowing us to view dates and times
    def schedule_appointment_patient(self, patient_id):
        self.clear_window()

        # Main frame
        main_frame = ttk.Frame(self.root, padding="20", style='Custom.TFrame')
        main_frame.grid(row=0, column=0, sticky='nsew')

        # Logo
        self._add_logo(main_frame)

        # Appointment Form Frame
        form_frame = ttk.LabelFrame(main_frame, text="Schedule New Appointment",
                                    padding="20", style='Login.TLabelframe')
        form_frame.grid(row=1, column=0, padx=20, pady=20, sticky=(tk.W, tk.E))

        # Appointment Type Selection
        ttk.Label(form_frame, text="Appointment Type:").grid(row=0, column=0, pady=5, sticky='w')
        appointment_types = ['Regular Checkup', 'Follow-up', 'Consultation', 'Vaccination']
        type_var = tk.StringVar()
        type_dropdown = ttk.Combobox(form_frame, textvariable=type_var, values=appointment_types, width=30)
        type_dropdown.grid(row=0, column=1, pady=5)
        type_dropdown.set("Select Type")

        # Date Selection
        ttk.Label(form_frame, text="Select Date:").grid(row=1, column=0, pady=5, sticky='w')
        current_date = datetime.now()
        min_date = current_date
        max_date = current_date + timedelta(days=365)

        date_cal = self.DateEntry(form_frame,
                             width=30,
                             background='darkblue',
                             foreground='white',
                             borderwidth=2,
                             date_pattern='mm/dd/yyyy',
                             mindate=min_date,
                             maxdate=max_date)
        date_cal.grid(row=1, column=1, pady=5)
        date_cal.set_date(current_date)

     # Retrieve the names of doctors based on availability
        def update_available_doctors(*args):
            selected_date = date_cal.get_date()
            selected_time = time_var.get()

            if selected_time == "Select Time":
                return

            try:
                time_obj = datetime.strptime(selected_time, '%I:%M %p').time()
            except ValueError:
                return

            try:
                connection = mysql.connector.connect(**self.db_config)
                cursor = connection.cursor(dictionary=True)

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
                available_doctors = cursor.fetchall()

                # Maps doctor_name to healthcare_professional_id in a dictionary
                doctor_map = {f"{doc['doctor_name']} - {doc['role']}": doc['healthcare_professional_id']
                              for doc in available_doctors}

                doctor_dropdown['values'] = list(doctor_map.keys()) if doctor_map else [
                    'No healthcare professionals available']
                doctor_dropdown.set("Select Healthcare Professional")

                # Store the mapping for later use
                self.doctor_map = doctor_map

            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", f"An error occurred: {e}")
            finally:
                if 'connection' in locals() and connection.is_connected():
                    cursor.close()
                    connection.close()

        # Time Selection
        ttk.Label(form_frame, text="Select Time:").grid(row=2, column=0, pady=5, sticky='w')

        try:
            connection = mysql.connector.connect(**self.db_config)
            cursor = connection.cursor()

            # Query to get start and end times
            time_query = """
            SELECT DISTINCT start_time, end_time 
            FROM Professional_Availability
            ORDER BY start_time;
            """
            cursor.execute(time_query)
            results = cursor.fetchall()

            time_slots = set()  # Use set for unique times

            for start_time, end_time in results:
                # Convert start and end times to minutes
                if isinstance(start_time, timedelta):
                    start_minutes = start_time.seconds // 60
                    end_minutes = end_time.seconds // 60
                else:
                    start_minutes = (start_time.hour * 60) + start_time.minute
                    end_minutes = (end_time.hour * 60) + end_time.minute

                # 30-minute slots between start and end time
                current_minutes = start_minutes
                while current_minutes < end_minutes:
                    hours = current_minutes // 60
                    minutes = current_minutes % 60

                    # Convert to 12-hour format
                    period = 'AM' if hours < 12 else 'PM'
                    display_hour = hours if hours <= 12 else hours - 12
                    if display_hour == 0:
                        display_hour = 12

                    formatted_time = f"{display_hour}:{minutes:02d} {period}"
                    time_slots.add(formatted_time)

                    # Increment by 30 minutes
                    current_minutes += 30

            # Helper function to convert time string to minutes for sorting
            def convert_to_minutes(time_str):
                time, period = time_str.rsplit(' ', 1)
                hour, minute = map(int, time.split(':'))
                if period == 'PM' and hour != 12:
                    hour += 12
                elif period == 'AM' and hour == 12:
                    hour = 0
                return hour * 60 + minute

            time_slots = sorted(time_slots, key=convert_to_minutes)

        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
            # Fallback time slots if query fails
            time_slots = ['9:00 AM', '10:00 AM', '11:00 AM', '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM']
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()

        # Dropdown for time selection
        time_var = tk.StringVar()
        time_dropdown = ttk.Combobox(
            form_frame,
            textvariable=time_var,
            values=time_slots,
            width=30,
            height=20
        )
        time_dropdown.grid(row=2, column=1, pady=5)
        time_dropdown.set("Select Time")

        # Bind time and date selection to update available doctors
        time_dropdown.bind('<<ComboboxSelected>>', update_available_doctors)
        date_cal.bind('<<DateEntrySelected>>', update_available_doctors)

        # Doctor Selection
        ttk.Label(form_frame, text="Select Doctor:").grid(row=3, column=0, pady=5, sticky='w')
        doctor_var = tk.StringVar()
        doctor_dropdown = ttk.Combobox(form_frame, textvariable=doctor_var, width=30)
        doctor_dropdown.grid(row=3, column=1, pady=5)
        doctor_dropdown.set("Select Time and Date First")

        # Notes/Comments entry form
        ttk.Label(form_frame, text="Additional Notes:").grid(row=4, column=0, pady=5, sticky='w')
        notes_text = tk.Text(form_frame, height=3, width=30)
        notes_text.grid(row=4, column=1, pady=5)

        # Validation method to make sure all fields are filled in before submission
        def validate_and_submit():
            selected_date = date_cal.get_date()

            if (type_var.get() == "Select Type" or
                    time_var.get() == "Select Time" or
                    doctor_var.get() == "Select Time and Date First" or
                    doctor_var.get() == "Select Healthcare Professional"):
                messagebox.showerror("Error", "Please fill in all fields")
                return

            selected_doctor = doctor_var.get()

            # Submit appointment if successful
            self.submit_appointment_patient(
                type_var.get(),
                selected_date.strftime('%m/%d/%Y'),
                time_var.get(),
                selected_doctor,
                notes_text.get("1.0", tk.END).strip(),
                patient_id
            )

        # Button container
        button_frame = ttk.Frame(form_frame, style='Custom.TFrame')
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)

        # Buttons for submit & back
        submit_btn = tk.Button(button_frame,
                               text="Submit",
                               command=validate_and_submit,
                               **self.button_style)
        submit_btn.grid(row=0, column=0, padx=10)

        back_btn = tk.Button(button_frame,
                             text="Back",
                             command=lambda: self.appointments_patient(patient_id),
                             **self.button_style)
        back_btn.grid(row=0, column=1, padx=10)

    # Submits valid appointment, updates the DB to add the appointment to the table & alter professionals availability
    def submit_appointment_patient(self, visit_type, date_str, time_str, healthcare_professional_id, notes, patient_id):
        try:
            # Convert date and time strings to proper format
            appointment_date = datetime.strptime(date_str, '%m/%d/%Y').date()
            appointment_time = datetime.strptime(time_str, '%I:%M %p').time()

            connection = mysql.connector.connect(**self.db_config)
            cursor = connection.cursor()

            # Get the actual healthcare_professional_id from the doctor_map
            selected_doctor = healthcare_professional_id  # This should be the full name + role string
            actual_healthcare_professional_id = self.doctor_map.get(selected_doctor)

            if not actual_healthcare_professional_id:
                messagebox.showerror("Error", "Invalid healthcare professional selection")
                return False

            # Debug: Print formatted values for query
            print("Parameters:", actual_healthcare_professional_id, appointment_date, appointment_time)

            # Modified availability check query
            check_query = """
                SELECT 1 
                FROM Professional_Availability pa
                WHERE pa.healthcare_professional_id = %s
                AND pa.day_of_week = %s
                AND %s BETWEEN pa.start_time AND pa.end_time
                AND NOT EXISTS (
                    SELECT 1 
                    FROM Appointment a
                    WHERE a.healthcare_professional_id = pa.healthcare_professional_id
                    AND a.appointment_date = %s
                    AND a.appointment_time = %s
                )
                """

            day_of_week = appointment_date.strftime('%A')
            cursor.execute(check_query, (
                actual_healthcare_professional_id,
                day_of_week,
                appointment_time,
                appointment_date,
                appointment_time
            ))

            # Debug: Print query result
            is_available = cursor.fetchone()
            print("Availability Query Result:", is_available)

            if not is_available:
                messagebox.showerror(
                    "Error",
                    "This time slot is no longer available. Please select another time."
                )
                return False

            # If available, insert the appointment
            insert_query = """
                INSERT INTO Appointment (
                    patient_id,
                    healthcare_professional_id,
                    appointment_date,
                    appointment_time,
                    visit_type,
                    appointment_notes
                ) VALUES (%s, %s, %s, %s, %s, %s)
                """

            cursor.execute(insert_query, (
                patient_id,
                actual_healthcare_professional_id,
                appointment_date,
                appointment_time,
                visit_type,
                notes
            ))

            connection.commit()
            messagebox.showinfo("Success", "Appointment scheduled successfully!")

            # Return to appointments view
            self.appointments_patient(patient_id)
            return True

        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
            return False
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()

    # Patient side view for their upcoming appointments
    # Includes options for updating and cancelling appointments
    def view_appointment_patient(self, patient_id):
        try:
            self.clear_window()
            self.root.geometry("700x550")

            main_frame = ttk.Frame(self.root, padding="20", style='Custom.TFrame')
            main_frame.grid(row=0, column=0, sticky='nsew')

            # Logo
            self._add_logo(main_frame)

            # Upcoming appointments frame
            appointments_frame = ttk.LabelFrame(main_frame, text="My Appointments",
                                                padding="20", style='Login.TLabelframe')
            appointments_frame.grid(row=1, column=0, padx=20, pady=20, sticky='nsew')

            # Create Treeview for appointments
            tree = ttk.Treeview(appointments_frame,
                                columns=('ID', 'Date', 'Time', 'Type', 'Doctor', 'Notes'),
                                show='headings',
                                height=8)

            # Column headings
            tree.heading('ID', text='ID')
            tree.heading('Date', text='Date', anchor='w')
            tree.heading('Time', text='Time', anchor='w')
            tree.heading('Type', text='Type', anchor='w')
            tree.heading('Doctor', text='Doctor', anchor='w')
            tree.heading('Notes', text='Notes', anchor='w')

            # Adjust column widths (including hidden ID column)
            tree.column('ID', width=0, stretch=False)  # Hidden column
            tree.column('Date', width=80, minwidth=80)
            tree.column('Time', width=80, minwidth=80)
            tree.column('Type', width=120, minwidth=100)
            tree.column('Doctor', width=160, minwidth=140)
            tree.column('Notes', width=180, minwidth=140)

            # Add scrollbar
            scrollbar = ttk.Scrollbar(appointments_frame, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)

            tree.grid(row=0, column=0, sticky='nsew', padx=(0, 5))
            scrollbar.grid(row=0, column=1, sticky='ns')

            # Get appointments for this patient
            connection = mysql.connector.connect(**self.db_config)
            cursor = connection.cursor(dictionary=True)

            # Query to retrieve appointments for this patient
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
            appointments = cursor.fetchall()

            # Insert appointments
            for appt in appointments:
                tree.insert('', 'end', values=(
                    appt['appointment_id'],  # Hidden ID
                    appt['appointment_date'].strftime('%m/%d/%Y'),
                    appt['appointment_time'],
                    appt['visit_type'],
                    appt['doctor_name'],
                    (appt['appointment_notes'][:20] + '...') if appt['appointment_notes'] and len(
                        appt['appointment_notes']) > 20
                    else (appt['appointment_notes'] if appt['appointment_notes'] else '')
                ))

            # Method to allow patient to update a selected appointment
            def update_selected_appointment():
                selected_item = tree.selection()
                if not selected_item:
                    messagebox.showwarning("Warning", "Please select an appointment to update.")
                    return
                appointment_id = tree.item(selected_item[0])['values'][0]
                self.update_appointment_patient(patient_id, appointment_id)

            # Method to cancel selected appointment
            def cancel_selected_appointment():
                selected_item = tree.selection()
                if not selected_item:
                    messagebox.showwarning("Warning", "Please select an appointment to cancel.")
                    return
                appointment_id = tree.item(selected_item[0])['values'][0]

                # Confirm cancellation
                if messagebox.askyesno("Confirm Cancellation",
                                       "Are you sure you want to cancel this appointment?"):
                    try:
                        connection = mysql.connector.connect(**self.db_config)
                        cursor = connection.cursor()

                        # Delete the appointment
                        delete_query = "DELETE FROM Appointment WHERE appointment_id = %s"
                        cursor.execute(delete_query, (appointment_id,))
                        connection.commit()

                        messagebox.showinfo("Success", "Appointment cancelled successfully!")

                        # Refresh the appointments view
                        self.view_appointment_patient(patient_id)

                    except mysql.connector.Error as e:
                        messagebox.showerror("Error", f"Failed to cancel appointment: {e}")
                    finally:
                        if 'connection' in locals() and connection.is_connected():
                            cursor.close()
                            connection.close()

            # Button frame
            button_frame = ttk.Frame(main_frame, style='Custom.TFrame')
            button_frame.grid(row=2, column=0, pady=20)

            # Add all buttons
            schedule_btn = tk.Button(button_frame,
                                     text="Schedule New",
                                     command=lambda: self.schedule_appointment_patient(patient_id),
                                     **self.button_style)
            schedule_btn.grid(row=0, column=0, padx=5)

            update_btn = tk.Button(button_frame,
                                   text="Update Selected",
                                   command=update_selected_appointment,
                                   **self.button_style)
            update_btn.grid(row=0, column=1, padx=5)

            cancel_btn = tk.Button(button_frame,
                                   text="Cancel Selected",
                                   command=cancel_selected_appointment,
                                   **self.button_style)
            cancel_btn.grid(row=0, column=2, padx=5)

            back_btn = tk.Button(button_frame,
                                 text="Back",
                                 command=lambda: self.patient_dashboard(patient_id),
                                 **self.button_style)
            back_btn.grid(row=0, column=3, padx=5)

            # No appointments message
            if not appointments:
                no_appt_label = ttk.Label(appointments_frame,
                                          text="No upcoming appointments found.",
                                          style='Custom.TLabel')
                no_appt_label.grid(row=1, column=0, pady=20)

        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()

    # Allows patient to update a selected appointment
    def update_appointment_patient(self, patient_id, appointment_id):
        try:
            # Get current appointment details
            connection = mysql.connector.connect(**self.db_config)
            cursor = connection.cursor(dictionary=True)

            query = """
                SELECT 
                    a.appointment_id,
                    a.appointment_date,
                    a.appointment_time,
                    a.visit_type,
                    a.healthcare_professional_id,
                    a.appointment_notes
                FROM Appointment a
                WHERE a.appointment_id = %s
            """

            cursor.execute(query, (appointment_id,))
            appointment = cursor.fetchone()

            if appointment:
                # You can reuse most of your schedule_appointment_patient method here,
                # but populate the fields with current values and update instead of insert
                self.schedule_appointment_patient(patient_id, appointment)
            else:
                messagebox.showerror("Error", "Appointment not found")

        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()


    # Patient side view for billing
    # Have not done yet
    def billing_patient(self, patient_id):
        self.clear_window()

    # Patient side for medications
    # Not done yet
    def medications_patient(self):
        self.clear_window()

    # Patient side view of their billing
    # Not done yet
    def billing_patient(self):
        self.clear.window()

    # Healthcare Professional portal
    def professional_portal(self, healthcare_id):
        self.clear_window()

        # Main frame with center alignment
        main_frame = ttk.Frame(self.root, padding="20", style='Custom.TFrame')
        main_frame.grid(row=0, column=0, sticky='nsew')

        # Configure grid weights for centering
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(2, weight=1)  # For button frame
        main_frame.grid_columnconfigure(0, weight=1)

        # Image Label
        img = Image.open("images/DB Logo.png")

        img = img.resize((181, 60))
        photo = ImageTk.PhotoImage(img)
        image_label = ttk.Label(main_frame, image=photo, style='Image.TLabel')
        image_label.image = photo
        image_label.grid(row=0, column=0, pady=(0, 0))

        # Welcome header centered
        ttk.Label(main_frame,
                  text="Welcome to Professionals Portal",
                  font=('Verdana', 20, 'bold')).grid(row=1, column=0, pady=(0, 30))

        # Button container centered
        button_frame = ttk.Frame(main_frame, style='Custom.TFrame')
        button_frame.grid(row=2, column=0, sticky='n')
        button_frame.grid_columnconfigure(0, weight=1)

        # Portal buttons
        button_width = 25

        view_appointments_btn = tk.Button(button_frame,
                                          text="View or Schedule Appointment",
                                          width=button_width,
                                          command=lambda: self.appointments_professional(healthcare_id),
                                          **self.button_style)
        view_appointments_btn.grid(row=0, column=0, pady=5)

        patient_add_btn = tk.Button(button_frame,
                                    text="Add new Patient",
                                    width=button_width,
                                    command=lambda: self.add_patient(healthcare_id),
                                    **self.button_style)
        patient_add_btn.grid(row=1, column=0, pady=5)

        search_add_btn = tk.Button(button_frame,
                                   text="Search Patients",
                                   width=button_width,
                                   command=lambda: self.search_patient(healthcare_id),
                                   **self.button_style)
        search_add_btn.grid(row=2, column=0, pady=5)

        billing_btn = tk.Button(button_frame,
                                text="Get Patient Billing Information",
                                width=button_width,
                                command=lambda: self.medications_patient(),
                                **self.button_style)
        billing_btn.grid(row=3, column=0, pady=5)

        # Logout button
        logout_btn = tk.Button(button_frame,
                               text="Logout",
                               width=button_width,
                               command=self.selection_screen,
                               **self.button_style)
        logout_btn.grid(row=4, column=0, pady=(20, 0))

    # healthcare prof side view of appointments
    def appointments_professional(self, healthcare_id):
        self.clear_window()

        # Main frame with center alignment
        main_frame = ttk.Frame(self.root, padding="20", style='Custom.TFrame')
        main_frame.grid(row=0, column=0, sticky='nsew')

        # Configure grid weights for centering
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(2, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # Image Label
        img = Image.open("images/DB Logo.png")

        img = img.resize((181, 60))
        photo = ImageTk.PhotoImage(img)
        image_label = ttk.Label(main_frame, image=photo, style='Image.TLabel')
        image_label.image = photo
        image_label.grid(row=0, column=0, pady=(0, 0))

        # Header centered
        ttk.Label(main_frame,
                  text="Appointments",
                  font=('Verdana', 20, 'bold')).grid(row=1, column=0, pady=(0, 30))

        # Button container centered
        button_frame = ttk.Frame(main_frame, style='Custom.TFrame')
        button_frame.grid(row=2, column=0, sticky='n')
        button_frame.grid_columnconfigure(0, weight=1)

        # Portal buttons
        button_width = 25

        my_appointments_btn = tk.Button(button_frame,
                                        text="My Appointments",
                                        width=button_width,
                                        command=lambda: self.my_appointments_prof(healthcare_id),
                                        **self.button_style)
        my_appointments_btn.grid(row=0, column=0, pady=5)

        search_appointments_btn = tk.Button(button_frame,
                                            text="Search Appointments",
                                            width=button_width,
                                            command=lambda: self.search_appointments(healthcare_id),
                                            **self.button_style)
        search_appointments_btn.grid(row=1, column=0, pady=5)

        schedule_appointment_btn = tk.Button(button_frame,
                                             text="Schedule New Appointment",
                                             width=button_width,
                                             command=lambda: self.show_schedule_appointment_patient(healthcare_id),
                                             **self.button_style)
        schedule_appointment_btn.grid(row=2, column=0, pady=5)

        # Back button
        back_btn = tk.Button(button_frame,
                             text="Back to Portal",
                             width=button_width,
                             command=lambda: self.professional_portal(healthcare_id),  # Changed to professional_portal
                             **self.button_style)
        back_btn.grid(row=3, column=0, pady=(20, 0))

    # Healthcare Prof's appointments
    # Not done yet
    def my_appointments_prof(self,healthcare_id):
        self.clear_window()

    # healthcare prof side of viewing upcoming appointments
    def search_appointments(self,healthcare_id):
        self.clear_window()

        # Main frame
        main_frame = ttk.Frame(self.root, padding="20", style='Custom.TFrame')
        main_frame.grid(row=0, column=0, sticky='nsew')

        # Configure weights for centering
        main_frame.grid_rowconfigure(1, weight=1)  # Content row
        main_frame.grid_columnconfigure(0, weight=1)

        # Image Label
        img = Image.open("images/DB Logo.png")

        img = img.resize((181, 60))
        photo = ImageTk.PhotoImage(img)
        image_label = ttk.Label(main_frame, image=photo, style='Image.TLabel')
        image_label.image = photo
        image_label.grid(row=0, column=0, pady=(0, 0))

        # Button container centered
        button_frame = ttk.Frame(main_frame, style='Custom.TFrame')
        button_frame.grid(row=1, column=0)
        button_frame.grid_columnconfigure(0, weight=1)

        # Appointment buttons
        button_width = 25  # Wider buttons for appointment options

        view_appointments_btn = tk.Button(button_frame,
                                          text="View My Appointments",
                                          width=button_width,
                                          command=self.show_upcoming_appointments_patient(healthcare_id),
                                          **self.button_style)
        view_appointments_btn.grid(row=0, column=0, pady=5)

        schedule_appointment_btn = tk.Button(button_frame,
                                             text="Schedule new Patient Appointment",
                                             width=button_width,
                                             command=self.show_schedule_appointment_patient(healthcare_id),
                                             **self.button_style)
        schedule_appointment_btn.grid(row=1, column=0, pady=5)

        search_appointment_btn = tk.Button(button_frame,
                                             text="Search Appointments",
                                             width=button_width,
                                             command=self.show_schedule_appointment_patient(healthcare_id),
                                             **self.button_style)
        search_appointment_btn.grid(row=2, column=0, pady=5)

        # Back button
        back_btn = tk.Button(button_frame,
                             text="Back to Portal",
                             width=button_width,
                             command=lambda: self.professional_portal(healthcare_id),
                             **self.button_style)
        back_btn.grid(row=3, column=0, pady=(20, 0))

    # Prof side of scheduling appointment
    # Not done yet
    def schedule_appointment_prof(self, healthcare_id):
        self.clear_window()

    # healthcare prof side to add new patient
    def add_patient(self, healthcare_id):
        self.clear_window()
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20", style='Custom.TFrame')
        main_frame.grid(row=0, column=0, sticky='nsew')

        # Image Label
        img = Image.open("images/DB Logo.png")

        img = img.resize((181, 60))
        photo = ImageTk.PhotoImage(img)
        image_label = ttk.Label(main_frame, image=photo, style='Image.TLabel')
        image_label.image = photo
        image_label.grid(row=0, column=0, pady=(0, 0))

        # Patient Form Frame
        form_frame = ttk.LabelFrame(main_frame, text="New Patient",
                                    padding="20", style='Login.TLabelframe')
        form_frame.grid(row=1, column=0, padx=20, pady=20, sticky=(tk.W, tk.E))

        # Patient Information Fields
        ttk.Label(form_frame, text="First Name:").grid(row=0, column=0, pady=5)
        first_name = ttk.Entry(form_frame, width=30)
        first_name.grid(row=0, column=1, pady=5)

        ttk.Label(form_frame, text="Last Name:").grid(row=1, column=0, pady=5)
        last_name = ttk.Entry(form_frame, width=30)
        last_name.grid(row=1, column=1, pady=5)

        ttk.Label(form_frame, text="Date of Birth:").grid(row=2, column=0, pady=5)
        dob = ttk.Entry(form_frame, width=30)
        dob.grid(row=2, column=1, pady=5)
        dob.insert(0, "MM/DD/YYYY")

        ttk.Label(form_frame, text="SSN:").grid(row=3, column=0, pady=5)
        ssn = ttk.Entry(form_frame, width=30)
        ssn.grid(row=3, column=1, pady=5)

        ttk.Label(form_frame, text="Zip Code:").grid(row=4, column=0, pady=5)
        zip_code = ttk.Entry(form_frame, width=30)
        zip_code.grid(row=4, column=1, pady=5)

        ttk.Label(form_frame, text="Phone Number:").grid(row=5, column=0, pady=5)
        phone = ttk.Entry(form_frame, width=30)
        phone.grid(row=5, column=1, pady=5)

        ttk.Label(form_frame, text="Gender:").grid(row=6, column=0, pady=5)
        gender_var = tk.StringVar()
        gender_combobox = ttk.Combobox(form_frame, textvariable=gender_var, width=27)
        gender_combobox['values'] = ('Male', 'Female', 'Other')
        gender_combobox.grid(row=6, column=1, pady=5)
        gender_combobox.set("Select Gender")

        ttk.Label(form_frame, text="Allergies:").grid(row=7, column=0, pady=5)
        allergies = tk.Text(form_frame, height=3, width=30)
        allergies.grid(row=7, column=1, pady=5)

        # Button container
        button_frame = ttk.Frame(form_frame, style='Custom.TFrame')
        button_frame.grid(row=8, column=0, columnspan=2, pady=20)

        # Submit and Back buttons
        submit_btn = tk.Button(button_frame,
                               text="Submit",
                               command=lambda: self.submit_new_patient(
                                   first_name.get(),
                                   last_name.get(),
                                   dob.get(),
                                   ssn.get(),
                                   zip_code.get(),
                                   phone.get(),
                                   gender_var.get(),
                                   allergies.get("1.0", tk.END)
                               ),
                               **self.button_style)
        submit_btn.grid(row=0, column=0, padx=10)

        back_btn = tk.Button(button_frame,
                             text="Back",
                             command=lambda:self.professional_portal(healthcare_id),
                             **self.button_style)
        back_btn.grid(row=0, column=1, padx=10)

    def submit_new_patient(self, first_name, last_name, dob, ssn, zip_code,
                           phone, gender, allergies):
        # Basic validation
        if (first_name and last_name and dob and ssn and zip_code and phone and gender):
            messagebox.showinfo("Success", f"Patient {first_name} {last_name} added successfully!")
            self.show_professional_portal()
        else:
            messagebox.showerror("Error", "Please fill in all required fields")


    # healthcare prof side to search patient
    # Not done yet
    def search_patient(self,healthcare_id):
        self.clear_window()

    # healthcare prof side view of patient billing
    # not done yet
    def billing_professional(self, healthcare_id):
        self.clear_window()

    def clear_window(self):
        for widget in self.root.winfo_children():
         widget.destroy()

def main():
    root = tk.Tk()
    app = HealthcareHub(root)
    root.mainloop()


if __name__ == "__main__":
    main()