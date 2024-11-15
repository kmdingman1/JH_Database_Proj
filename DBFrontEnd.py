import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkfont
from PIL import Image, ImageTk


class HealthcareHub:
    def __init__(self, root):
        self.root = root
        self.root.title("Hopkins Health Hub")
        self.root.geometry("700x550")

        # Configure grid weights once
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Window Icon
        icon = tk.PhotoImage(file=r"C:\Users\kate\Pictures\HopkinsLogo.png")
        self.root.iconphoto(True, icon)

        # Button style dictionary
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

        # Style Config
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

        # Window Background
        self.root.configure(bg='#dae8f5')
        self.selection_screen()

    # Main Screen on start up
    def selection_screen(self):
        self.clear_window()

        main_frame = ttk.Frame(self.root, padding="40", style='Custom.TFrame')
        main_frame.grid(row=0, column=0)

        # Image Label
        img = Image.open(r"C:\Users\kate\Downloads\download.png")
        img = img.resize((362, 120))
        photo = ImageTk.PhotoImage(img)
        image_label = ttk.Label(main_frame, image=photo, style='Image.TLabel')
        image_label.image = photo
        image_label.grid(row=0, column=0, pady=(0, 0))

        # Button container
        button_frame = ttk.Frame(main_frame, style='Custom.TFrame')
        button_frame.grid(row=1, column=0)
        button_frame.grid_columnconfigure(0, weight=1)

        # Login buttons
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

        # Logo in upper left
        img = Image.open(r"C:\Users\kate\Downloads\download.png")
        img = img.resize((181, 60))  # Half size
        photo = ImageTk.PhotoImage(img)
        image_label = ttk.Label(main_frame, image=photo, style='Image.TLabel')
        image_label.image = photo
        image_label.grid(row=0, column=0, sticky='nw', pady=(0, 20))

        # Login frame
        frame = ttk.LabelFrame(main_frame, text="Patient Login",
                               padding="20", style='Login.TLabelframe')
        frame.grid(row=1, column=0, padx=20, pady=20, sticky=(tk.W, tk.E))

        # Entry fields
        ttk.Label(frame, text="Patient ID:").grid(row=0, column=0, pady=5)
        patient_id = ttk.Entry(frame, width=30)
        patient_id.grid(row=0, column=1, pady=5)

        ttk.Label(frame, text="Password:").grid(row=1, column=0, pady=5)
        password = ttk.Entry(frame, show="*", width=30)
        password.grid(row=1, column=1, pady=5)

        # Buttons
        button_frame = ttk.Frame(frame, style='Custom.TFrame')
        button_frame.grid(row=2, column=0, columnspan=2, pady=20)

        submit_btn = tk.Button(button_frame, text="Submit",
                               command=lambda: self.login_patient(patient_id.get(), password.get()),
                               **self.button_style)
        submit_btn.grid(row=0, column=0, padx=10)

        back_btn = tk.Button(button_frame, text="Back",
                             command=self.selection_screen,
                             **self.button_style)
        back_btn.grid(row=0, column=1, padx=10)

    # Professional Log in
    def professional_login(self):
        self.clear_window()

        # Main frame
        main_frame = ttk.Frame(self.root, padding="20", style='Custom.TFrame')
        main_frame.grid(row=0, column=0, sticky='nsew')

        # Logo in upper left
        img = Image.open(r"C:\Users\kate\Downloads\download.png")
        img = img.resize((181, 60))  # Half size
        photo = ImageTk.PhotoImage(img)
        image_label = ttk.Label(main_frame, image=photo, style='Image.TLabel')
        image_label.image = photo
        image_label.grid(row=0, column=0, sticky='nw', pady=(0, 20))

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

    # Log in validations
    def login_patient(self, patient_id, password):
        # Add your authentication logic here
        # If login successful:
        self.patient_portal(patient_id)

    def login_professional(self, healthcare_id, password):
        self.professional_portal(healthcare_id)


    # Patient Portal
    def patient_portal(self, patient_id):
        self.clear_window()

        # Main frame with center alignment
        main_frame = ttk.Frame(self.root, padding="20", style='Custom.TFrame')
        main_frame.grid(row=0, column=0, sticky='nsew')

        # Configure grid weights for centering
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(2, weight=1)  # For button frame
        main_frame.grid_columnconfigure(0, weight=1)

        # Logo in upper left
        img = Image.open(r"C:\Users\kate\Downloads\download.png")
        img = img.resize((181, 60))
        photo = ImageTk.PhotoImage(img)
        image_label = ttk.Label(main_frame, image=photo, style='Image.TLabel')
        image_label.image = photo
        image_label.grid(row=0, column=0, sticky='nw', pady=(0, 20))

        # Welcome header centered
        ttk.Label(main_frame,
                  text="Welcome to Patient Portal",
                  font=('Verdana', 20, 'bold')).grid(row=1, column=0, pady=(0, 30))

        # Button container centered
        button_frame = ttk.Frame(main_frame, style='Custom.TFrame')
        button_frame.grid(row=2, column=0, sticky='n')
        button_frame.grid_columnconfigure(0, weight=1)

        # Portal buttons
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


    def clear_window(self):
        for widget in self.root.winfo_children():
         widget.destroy()


    # Patient side view for Appointments
    def appointments_patient(self, patient_id):
        self.clear_window()

        # Main frame with center alignment
        main_frame = ttk.Frame(self.root, padding="20", style='Custom.TFrame')
        main_frame.grid(row=0, column=0, sticky='nsew')

        # Configure grid weights for centering
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(2, weight=1)  # For button frame
        main_frame.grid_columnconfigure(0, weight=1)

        # Logo in upper left
        img = Image.open(r"C:\Users\kate\Downloads\download.png")
        img = img.resize((181, 60))
        photo = ImageTk.PhotoImage(img)
        image_label = ttk.Label(main_frame, image=photo, style='Image.TLabel')
        image_label.image = photo
        image_label.grid(row=0, column=0, sticky='nw', pady=(0, 20))

        # Header centered
        ttk.Label(main_frame,
                  text="View or Schedule Appointment",
                  font=('Verdana', 20, 'bold')).grid(row=1, column=0, pady=(0, 30))

        # Button container centered
        button_frame = ttk.Frame(main_frame, style='Custom.TFrame')
        button_frame.grid(row=2, column=0, sticky='n')
        button_frame.grid_columnconfigure(0, weight=1)

        # Buttons
        button_width = 25

        view_appointments_btn = tk.Button(button_frame,
                                          text="View my Upcoming Appointments",
                                          width=button_width,
                                          command=lambda: self.upcoming_appointments_patient(patient_id),
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
    def schedule_appointments_patient(self, patient_id):
        self.clear_window()

        # Main frame
        main_frame = ttk.Frame(self.root, padding="20", style='Custom.TFrame')
        main_frame.grid(row=0, column=0, sticky='nsew')

        # Logo in upper left
        img = Image.open(r"C:\Users\kate\Downloads\download.png")
        img = img.resize((181, 60))
        photo = ImageTk.PhotoImage(img)
        image_label = ttk.Label(main_frame, image=photo, style='Image.TLabel')
        image_label.image = photo
        image_label.grid(row=0, column=0, sticky='nw', pady=(0, 20))

        # Appointment Form Frame
        form_frame = ttk.LabelFrame(main_frame, text="Schedule New Appointment",
                                    padding="20", style='Login.TLabelframe')
        form_frame.grid(row=1, column=0, padx=20, pady=20, sticky=(tk.W, tk.E))

        # Appointment Type
        ttk.Label(form_frame, text="Appointment Type:").grid(row=0, column=0, pady=5)
        appointment_types = ['Regular Checkup', 'Follow-up', 'Consultation', 'Vaccination']
        type_var = tk.StringVar()
        type_dropdown = ttk.Combobox(form_frame, textvariable=type_var, values=appointment_types, width=30)
        type_dropdown.grid(row=0, column=1, pady=5)
        type_dropdown.set("Select Type")

        # Date Selection
        ttk.Label(form_frame, text="Preferred Date:").grid(row=1, column=0, pady=5)
        date_entry = ttk.Entry(form_frame, width=30)
        date_entry.grid(row=1, column=1, pady=5)
        date_entry.insert(0, "MM/DD/YYYY")

        # Time Selection
        ttk.Label(form_frame, text="Preferred Time:").grid(row=2, column=0, pady=5)
        time_slots = ['9:00 AM', '10:00 AM', '11:00 AM', '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM']
        time_var = tk.StringVar()
        time_dropdown = ttk.Combobox(form_frame, textvariable=time_var, values=time_slots, width=30)
        time_dropdown.grid(row=2, column=1, pady=5)
        time_dropdown.set("Select Time")

        # Doctor Selection
        ttk.Label(form_frame, text="Select Doctor:").grid(row=3, column=0, pady=5)
        doctors = ['Dr. Smith - General', 'Dr. Johnson - Pediatrics', 'Dr. Williams - Cardiology']
        doctor_var = tk.StringVar()
        doctor_dropdown = ttk.Combobox(form_frame, textvariable=doctor_var, values=doctors, width=30)
        doctor_dropdown.grid(row=3, column=1, pady=5)
        doctor_dropdown.set("Select Doctor")

        # Notes/Comments
        ttk.Label(form_frame, text="Additional Notes:").grid(row=4, column=0, pady=5)
        notes_text = tk.Text(form_frame, height=3, width=30)
        notes_text.grid(row=4, column=1, pady=5)

        # Button container
        button_frame = ttk.Frame(form_frame, style='Custom.TFrame')
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

        # Submit and Back buttons side by side
        submit_btn = tk.Button(button_frame,
                               text="Submit",
                               command=lambda: self.submit_appointment_patient(type_var.get(), date_entry.get(),
                                                                               time_var.get(), doctor_var.get(),
                                                                               notes_text.get("1.0", tk.END)),
                               **self.button_style)
        submit_btn.grid(row=0, column=0, padx=10)

        back_btn = tk.Button(button_frame,
                             text="Back",
                             command=lambda: self.appointments_patient(patient_id),
                             **self.button_style)
        back_btn.grid(row=0, column=1, padx=10)

    # On successful appointment submission
    def submit_appointment_patient(self, app_type, date, time, doctor, notes):
        # Here you would normally save to database
        # For now, just show a success message
        messagebox.showinfo("Success", "Appointment scheduled successfully!")
        self.show_appointments()

    # Patient side view for billing
    def billing_patient(self, patient_id):
        self.clear_window()

    def medications_patient(self):
        self.clear_window()

    # Patient side view of their billing
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

        # Logo in upper left
        img = Image.open(r"C:\Users\kate\Downloads\download.png")
        img = img.resize((181, 60))
        photo = ImageTk.PhotoImage(img)
        image_label = ttk.Label(main_frame, image=photo, style='Image.TLabel')
        image_label.image = photo
        image_label.grid(row=0, column=0, sticky='nw', pady=(0, 20))

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

        # Logo in upper left
        img = Image.open(r"C:\Users\kate\Downloads\download.png")
        img = img.resize((181, 60))
        photo = ImageTk.PhotoImage(img)
        image_label = ttk.Label(main_frame, image=photo, style='Image.TLabel')
        image_label.image = photo
        image_label.grid(row=0, column=0, sticky='nw', pady=(0, 20))

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

        # Logo in upper left
        img = Image.open(r"C:\Users\kate\Downloads\download.png")
        img = img.resize((181, 60))
        photo = ImageTk.PhotoImage(img)
        image_label = ttk.Label(main_frame, image=photo, style='Image.TLabel')
        image_label.image = photo
        image_label.grid(row=0, column=0, sticky='nw', pady=(0, 20))

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
    def schedule_appointment_prof(self, healthcare_id):
        self.clear_window()

    # healtcare prof side to add new patient
    def add_patient(self, healthcare_id):
        self.clear_window()
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20", style='Custom.TFrame')
        main_frame.grid(row=0, column=0, sticky='nsew')

        # Logo in upper left
        img = Image.open(r"C:\Users\kate\Downloads\download.png")
        img = img.resize((181, 60))
        photo = ImageTk.PhotoImage(img)
        image_label = ttk.Label(main_frame, image=photo, style='Image.TLabel')
        image_label.image = photo
        image_label.grid(row=0, column=0, sticky='nw', pady=(0, 20))

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
    def search_patient(self,healthcare_id):
        self.clear_window()

    # healthcare prof side view of patient billing
    def billing_professional(self, healthcare_id):
        self.clear_window()

def main():
    root = tk.Tk()
    app = HealthcareHub(root)
    root.mainloop()


if __name__ == "__main__":
    main()