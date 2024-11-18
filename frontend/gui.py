import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime, timedelta
from PIL import Image, ImageTk
from backend.database import HealthcareDatabase


class HealthcareGUI:
    def __init__(self, root):
        self.root = root
        self.db = HealthcareDatabase()

        # Main window settings
        self._configure_window()
        self._setup_styles()
        self.selection_screen()

    def _configure_window(self):
        self.root.title("Hopkins Health Hub")
        self.root.geometry("700x550")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.configure(bg='#dae8f5')

        # Set window icon
        icon = tk.PhotoImage(file="images/HopkinsLogo.png")
        self.root.iconphoto(True, icon)

    # Style Configurations
    def _setup_styles(self):
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

    # Logo for DB
    def _add_logo(self, parent, size=(181, 60), row=0, column=0, pady=(0, 10)):
        try:
            img = Image.open("images/DB Logo.png")
            img = img.resize(size)
            photo = ImageTk.PhotoImage(img)
            image_label = ttk.Label(parent, image=photo, style='Image.TLabel')
            image_label.image = photo
            image_label.grid(row=row, column=column, pady=pady)
        except Exception as e:
            messagebox.showerror("Error", f"Unable to load logo: {e}")

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # Main screen on start up
    def selection_screen(self):
        self.clear_window()

        # Main frame
        main_frame = ttk.Frame(self.root, padding="40", style='Custom.TFrame')
        main_frame.grid(row=0, column=0)

        # Logo
        self._add_logo(main_frame, size=(362, 120))

        # Buttons
        button_frame = ttk.Frame(main_frame, style='Custom.TFrame')
        button_frame.grid(row=1, column=0)
        button_frame.grid_columnconfigure(0, weight=1)

        tk.Button(button_frame,
                  text="Patient Login",
                  command=self.patient_login,
                  **self.button_style).grid(row=0, column=0, pady=(0, 20))

        tk.Button(button_frame,
                  text="Healthcare Professional Login",
                  command=self.professional_login,
                  **self.button_style).grid(row=1, column=0)

    # Login screen for patients
    def patient_login(self):
        self.clear_window()

        # Main frame
        main_frame = ttk.Frame(self.root, padding="20", style='Custom.TFrame')
        main_frame.grid(row=0, column=0, sticky='nsew')

        # Logo
        self._add_logo(main_frame)

        # Title Frame
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

        # Button frames
        button_frame = ttk.Frame(login_frame, style='Custom.TFrame')
        button_frame.grid(row=2, column=0, columnspan=2, pady=20)

        # Buttons
        tk.Button(button_frame,
                  text="Submit",
                  command=lambda: self.validate_patient_login(patient_id.get(), password.get()),
                  **self.button_style).grid(row=0, column=0, padx=10)

        tk.Button(button_frame,
                  text="Back",
                  command=self.selection_screen,
                  **self.button_style).grid(row=0, column=1, padx=10)

    # Login screen for professionals
    def professional_login(self):
        self.clear_window()

        # Main frame
        main_frame = ttk.Frame(self.root, padding="20", style='Custom.TFrame')
        main_frame.grid(row=0, column=0, sticky='nsew')

        # Logo
        self._add_logo(main_frame)

        # Title Frame
        login_frame = ttk.LabelFrame(
            main_frame,
            text="Healthcare Professional Login",
            padding="20",
            style='Login.TLabelframe'
        )
        login_frame.grid(row=1, column=0, padx=20, pady=20, sticky=(tk.W, tk.E))

        # Entry fields
        ttk.Label(login_frame, text="Healthcare ID:").grid(row=0, column=0, pady=5)
        healthcare_id = ttk.Entry(login_frame, width=30)
        healthcare_id.grid(row=0, column=1, pady=5)

        ttk.Label(login_frame, text="Password:").grid(row=1, column=0, pady=5)
        password = ttk.Entry(login_frame, show="*", width=30)
        password.grid(row=1, column=1, pady=5)

        # Button frame
        button_frame = ttk.Frame(login_frame, style='Custom.TFrame')
        button_frame.grid(row=2, column=0, columnspan=2, pady=20)

        tk.Button(button_frame,
                  text="Submit",
                  command=lambda: self.validate_professional_login(healthcare_id.get(), password.get()),
                  **self.button_style).grid(row=0, column=0, padx=10)

        tk.Button(button_frame,
                  text="Back",
                  command=self.selection_screen,
                  **self.button_style).grid(row=0, column=1, padx=10)

    # Login validation for patients
    def validate_patient_login(self, patient_id, password):
        if not patient_id or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return

        try:
            if self.db.verify_patient_login(patient_id, password):
                messagebox.showinfo("Success", "Login successful!")
                self.patient_portal(patient_id)
            else:
                messagebox.showerror("Error", "Invalid ID or password")
        except Exception as e:
            messagebox.showerror("Error", f"Login failed: {str(e)}")

    # Login validation for professionals
    def validate_professional_login(self, healthcare_id, password):
        if not healthcare_id or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return

        try:
            if self.db.verify_professional_login(healthcare_id, password):
                messagebox.showinfo("Success", "Login successful!")
                self.professional_portal(healthcare_id)
            else:
                messagebox.showerror("Error", "Invalid ID or password")
        except Exception as e:
            messagebox.showerror("Error", f"Login failed: {str(e)}")

    # Patient Portal
    def patient_portal(self, patient_id):
        self.clear_window()

        # Main frame
        main_frame = ttk.Frame(self.root, padding="20", style='Custom.TFrame')
        main_frame.grid(row=0, column=0, sticky='nsew')

        # Centers elements
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(2, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # Logo
        self._add_logo(main_frame)

        # Label frame
        ttk.Label(main_frame,
                  text="Welcome to Patient Portal",
                  font=('Verdana', 20, 'bold')).grid(row=1, column=0, pady=(0, 30))

        # Button frame
        button_frame = ttk.Frame(main_frame, style='Custom.TFrame')
        button_frame.grid(row=2, column=0, sticky='n')
        button_frame.grid_columnconfigure(0, weight=1)

        button_width = 25

        # Portal Buttons
        buttons = [
            ("View or Schedule Appointment", lambda: self.appointments_patient(patient_id)),
            ("View My Bills", lambda: self.bills_patient(patient_id)),
            ("View My Medications", self.medications_patient),
            ("Logout", self.selection_screen)
        ]

        for i, (text, command) in enumerate(buttons):
            tk.Button(button_frame,
                      text=text,
                      width=button_width,
                      command=command,
                      **self.button_style).grid(row=i, column=0, pady=5)

    # Professional Portal
    def professional_portal(self, healthcare_id):
        self.clear_window()

        # Main frame
        main_frame = ttk.Frame(self.root, padding="20", style='Custom.TFrame')
        main_frame.grid(row=0, column=0, sticky='nsew')

        # Centers elements
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(2, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)


        # Logo
        self._add_logo(main_frame)

        # Title frame
        ttk.Label(main_frame,
                  text="Welcome to Professionals Portal",
                  font=('Verdana', 20, 'bold')).grid(row=1, column=0, pady=(0, 30))

        # Button Frame
        button_frame = ttk.Frame(main_frame, style='Custom.TFrame')
        button_frame.grid(row=2, column=0, sticky='n')
        button_frame.grid_columnconfigure(0, weight=1)

        button_width = 25

        # Professional Portal Buttons
        buttons = [
            ("View or Schedule Appointment", lambda: self.appointments_professional(healthcare_id)),
            ("Add new Patient", lambda: self.add_patient(healthcare_id)),
            ("Search Patients", lambda: self.search_patient(healthcare_id)),
            ("Get Patient Billing Information", lambda: self.billing_professional(healthcare_id)),
            ("Logout", self.selection_screen)
        ]

        for i, (text, command) in enumerate(buttons):
            tk.Button(button_frame,
                      text=text,
                      width=button_width,
                      command=command,
                      **self.button_style).grid(row=i, column=0, pady=5)

    # Patient view for appointment page
    def appointments_patient(self, patient_id):
        self.clear_window()

        # Main frame
        main_frame = ttk.Frame(self.root, padding="20", style='Custom.TFrame')
        main_frame.grid(row=0, column=0, sticky='nsew')

        # Centers elements
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(2, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # Logo
        self._add_logo(main_frame)

        # Title frame
        ttk.Label(main_frame,
                  text="My Appointments",
                  font=('Verdana', 20, 'bold')).grid(row=1, column=0, pady=(0, 30))

        # Button Frame
        button_frame = ttk.Frame(main_frame, style='Custom.TFrame')
        button_frame.grid(row=2, column=0, sticky='n')
        button_frame.grid_columnconfigure(0, weight=1)

        button_width = 25

        # Buttons
        buttons = [
            ("View my Upcoming Appointments", lambda: self.view_appointment_patient(patient_id)),
            ("Schedule New Appointment", lambda: self.schedule_appointment_patient(patient_id)),
            ("Back to Portal", lambda: self.patient_portal(patient_id))
        ]

        for i, (text, command) in enumerate(buttons):
            tk.Button(button_frame,
                      text=text,
                      width=button_width,
                      command=command,
                      **self.button_style).grid(row=i, column=0, pady=5)

    # Patient view for upcoming appointments / cancelling appointments
    def view_appointment_patient(self, patient_id):
        self.clear_window()

        # Main frame
        main_frame = ttk.Frame(self.root, padding="20", style='Custom.TFrame')
        main_frame.grid(row=0, column=0, sticky='nsew')

        # Logo
        self._add_logo(main_frame)

        # Title frame
        appointments_frame = ttk.LabelFrame(main_frame, text="My Appointments",
                                            padding="20", style='Login.TLabelframe')
        appointments_frame.grid(row=1, column=0, padx=20, pady=20, sticky='nsew')

        # Create Treeview for appointments
        tree = ttk.Treeview(appointments_frame,
                            columns=('ID', 'Date', 'Time', 'Type', 'Doctor', 'Notes'),
                            show='headings',
                            height=8)

        # Column settings
        columns = {
            'ID': {'width': 0, 'stretch': False},
            'Date': {'width': 80, 'minwidth': 80},
            'Time': {'width': 80, 'minwidth': 80},
            'Type': {'width': 100, 'minwidth': 100},
            'Doctor': {'width': 100, 'minwidth': 140},
            'Notes': {'width': 160, 'minwidth': 140}
        }

        for col, props in columns.items():
            tree.heading(col, text=col, anchor='w')
            tree.column(col, **props)

        # Scroll bar
        scrollbar = ttk.Scrollbar(appointments_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.grid(row=0, column=0, sticky='nsew', padx=(0, 5))
        scrollbar.grid(row=0, column=1, sticky='ns')

        # Gets and display appointments
        appointments = self.db.get_appointments(patient_id)

        for appt in appointments:
            tree.insert('', 'end', values=(
                appt['appointment_id'],
                appt['appointment_date'].strftime('%m/%d/%Y'),
                appt['appointment_time'],
                appt['visit_type'],
                appt['doctor_name'],
                (appt['appointment_notes'][:20] + '...') if appt['appointment_notes'] and len(
                    appt['appointment_notes']) > 20
                else (appt['appointment_notes'] if appt['appointment_notes'] else '')
            ))

        # Cancellation verification
        def cancel_selected_appointment():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("Warning", "Please select an appointment to cancel.")
                return

            appointment_id = tree.item(selected_item[0])['values'][0]
            if messagebox.askyesno("Confirm Cancellation",
                                   "Are you sure you want to cancel this appointment?"):
                if self.db.delete_appointment(appointment_id):
                    messagebox.showinfo("Success", "Appointment cancelled successfully!")
                    self.view_appointment_patient(patient_id)

        # Button frame
        button_frame = ttk.Frame(main_frame, style='Custom.TFrame')
        button_frame.grid(row=2, column=0, pady=20)

        # Buttons
        buttons = [
            ("Schedule New Appointment", lambda: self.schedule_appointment_patient(patient_id)),
            ("Cancel Selected", cancel_selected_appointment),
            ("Back", lambda: self.patient_portal(patient_id))
        ]

        for i, (text, command) in enumerate(buttons):
            tk.Button(button_frame,
                      text=text,
                      command=command,
                      **self.button_style).grid(row=0, column=i, padx=5)

        # If no appointments
        if not appointments:
            ttk.Label(appointments_frame,
                      text="No upcoming appointments found.",
                      style='Custom.TLabel').grid(row=1, column=0, pady=20)

    # Patient view for scheduling appointments
    def schedule_appointment_patient(self, patient_id):
        self.clear_window()

        # Main frame
        main_frame = ttk.Frame(self.root, padding="20", style='Custom.TFrame')
        main_frame.grid(row=0, column=0, sticky='nsew')

        # Logo
        self._add_logo(main_frame)

        # Title Frame
        form_frame = ttk.LabelFrame(main_frame, text="Schedule New Appointment",
                                    padding="20", style='Login.TLabelframe')
        form_frame.grid(row=1, column=0, padx=20, pady=20, sticky=(tk.W, tk.E))

        # Place holders for data entry
        def add_placeholder_to_text(text_widget, placeholder):
            text_widget.insert('1.0', placeholder)
            text_widget.config(foreground='gray')

            def on_focus_in(event):
                if text_widget.get('1.0', 'end-1c') == placeholder:
                    text_widget.delete('1.0', tk.END)
                    text_widget.config(foreground='black')

            def on_focus_out(event):
                if not text_widget.get('1.0', 'end-1c'):
                    text_widget.insert('1.0', placeholder)
                    text_widget.config(foreground='gray')

            text_widget.bind('<FocusIn>', on_focus_in)
            text_widget.bind('<FocusOut>', on_focus_out)

        # Appointment Type Selection
        ttk.Label(form_frame, text="Appointment Type:").grid(row=0, column=0, pady=5, sticky='w')
        appointment_types = [
            'Regular Checkup - General health examination',
            'Follow-up - Review previous visit',
            'Consultation - Specific health concern',
            'Vaccination - Immunization services'
        ]
        type_var = tk.StringVar()
        type_dropdown = ttk.Combobox(form_frame, textvariable=type_var, values=appointment_types, width=40)
        type_dropdown.grid(row=0, column=1, pady=5)
        type_dropdown.set("Select Type of Appointment")

        # Date Selection with date picker and info
        ttk.Label(form_frame, text="Select Date:").grid(row=1, column=0, pady=5, sticky='w')
        current_date = datetime.now()
        min_date = current_date
        max_date = current_date + timedelta(days=365)

        date_cal = DateEntry(form_frame,
                             width=37,
                             background='#dae8f5',
                             foreground='white',
                             borderwidth=2,
                             date_pattern='mm/dd/yyyy',
                             mindate=min_date,
                             maxdate=max_date,
                             state='readonly')
        date_cal.grid(row=1, column=1, pady=5)
        date_cal.set_date(current_date)
        ttk.Label(form_frame,
                  text="(You can schedule up to one year in advance)",
                  font=('Helvetica', 8, 'italic'),
                  foreground='gray').grid(row=1, column=2, pady=5, padx=5, sticky='w')

        # Time Selection with formatted display
        ttk.Label(form_frame, text="Select Time:").grid(row=2, column=0, pady=5, sticky='w')
        time_slots = self.db.get_available_time_slots()
        time_var = tk.StringVar()
        time_dropdown = ttk.Combobox(
            form_frame,
            textvariable=time_var,
            values=time_slots,
            width=37,
            state='readonly'
        )
        time_dropdown.grid(row=2, column=1, pady=5)
        time_dropdown.set("Select Available Time Slot")

        # Healthcare Professional Selection
        ttk.Label(form_frame, text="Select Healthcare Provider:").grid(row=3, column=0, pady=5, sticky='w')
        doctor_var = tk.StringVar()
        doctor_dropdown = ttk.Combobox(form_frame, textvariable=doctor_var, width=37, state='readonly')
        doctor_dropdown.grid(row=3, column=1, pady=5)
        doctor_dropdown.set("First select date and time")

        def update_available_doctors(*args):
            selected_date = date_cal.get_date()
            selected_time = time_var.get()

            if selected_time == "Select Available Time Slot":
                return

            available_doctors = self.db.get_available_doctors(selected_date, selected_time)
            doctor_map = {f"{doc['doctor_name']} - {doc['role']}": doc['healthcare_professional_id']
                          for doc in available_doctors}

            doctor_dropdown['values'] = list(doctor_map.keys()) if doctor_map else [
                'No healthcare professionals available']
            doctor_dropdown.set("Select Healthcare Professional")
            self.doctor_map = doctor_map

        # Bind time and date selection to update available doctors
        time_dropdown.bind('<<ComboboxSelected>>', update_available_doctors)
        date_cal.bind('<<DateEntrySelected>>', update_available_doctors)

        # Notes/Comments entry form with placeholder
        ttk.Label(form_frame, text="Additional Notes:").grid(row=4, column=0, pady=5, sticky='w')
        notes_text = tk.Text(form_frame, height=3, width=40)
        notes_text.grid(row=4, column=1, pady=5)
        add_placeholder_to_text(notes_text, "Enter any special requests or relevant information for your appointment")

        def validate_and_submit():
            # Get notes, handling placeholder text
            notes = notes_text.get("1.0", tk.END).strip()
            if notes == "Enter any special requests or relevant information for your appointment":
                notes = ""

            # Validate selections
            if (type_var.get() == "Select Type of Appointment" or
                    time_var.get() == "Select Available Time Slot" or
                    doctor_var.get() == "First select date and time" or
                    doctor_var.get() == "Select Healthcare Professional"):
                messagebox.showerror("Error", "Please fill in all required fields")
                return

            try:
                selected_doctor = doctor_var.get()
                healthcare_professional_id = self.doctor_map[selected_doctor]

                success = self.db.submit_appointment(
                    type_var.get().split(' - ')[0],  # Get just the appointment type without description
                    date_cal.get_date().strftime('%Y-%m-%d'),
                    time_var.get(),
                    healthcare_professional_id,
                    notes,
                    patient_id
                )

                if success:
                    messagebox.showinfo("Success", "Appointment scheduled successfully!")
                    self.view_appointment_patient(patient_id)

            except Exception as e:
                messagebox.showerror("Error", f"Failed to schedule appointment: {str(e)}")

        # Button frame
        button_frame = ttk.Frame(form_frame, style='Custom.TFrame')
        button_frame.grid(row=5, column=0, columnspan=3, pady=20)

        # Add buttons
        tk.Button(button_frame,
                  text="Schedule Appointment",
                  command=validate_and_submit,
                  **self.button_style).grid(row=0, column=0, padx=10)

        tk.Button(button_frame,
                  text="Back",
                  command=lambda: self.appointments_patient(patient_id),
                  **self.button_style).grid(row=0, column=1, padx=10)

    # Patient view for viewing and paying their bills
    def bills_patient(self, patient_id):
        # Placeholder for billing functionality
        self.clear_window()
        main_frame = ttk.Frame(self.root, padding="20", style='Custom.TFrame')
        main_frame.grid(row=0, column=0, sticky='nsew')
        self._add_logo(main_frame)
        ttk.Label(main_frame, text="Billing functionality coming soon!").grid(row=1, column=0, pady=20)
        tk.Button(main_frame,
                  text="Back",
                  command=lambda: self.patient_portal(patient_id),
                  **self.button_style).grid(row=2, column=0, pady=20)

    # Patient view for viewing their medication
    def medications_patient(self):
        # Placeholder for medications functionality
        self.clear_window()
        main_frame = ttk.Frame(self.root, padding="20", style='Custom.TFrame')
        main_frame.grid(row=0, column=0, sticky='nsew')
        self._add_logo(main_frame)
        ttk.Label(main_frame, text="Medications functionality coming soon!").grid(row=1, column=0, pady=20)
        tk.Button(main_frame,
                  text="Back",
                  command=self.selection_screen,
                  **self.button_style).grid(row=2, column=0, pady=20)

    # Professional view for appointment side
    def appointments_professional(self, healthcare_id):
        self.clear_window()

        # Main frame
        main_frame = ttk.Frame(self.root, padding="20", style='Custom.TFrame')
        main_frame.grid(row=0, column=0, sticky='nsew')

        # Centers elements
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(2, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # Logo
        self._add_logo(main_frame)

        # Title frame
        ttk.Label(main_frame,
                  text="Appointment Manager",
                  font=('Verdana', 20, 'bold')).grid(row=1, column=0, pady=(0, 30))

        # Button Frame
        button_frame = ttk.Frame(main_frame, style='Custom.TFrame')
        button_frame.grid(row=2, column=0, sticky='n')
        button_frame.grid_columnconfigure(0, weight=1)

        button_width = 25

        # Buttons
        buttons = [
            ("My Appointments", lambda: self.view_appointments_professional(healthcare_id)),
            ("Schedule New Appointment", lambda: self.schedule_appointments_professional(healthcare_id)),
            ("Search Appointments", lambda: self.search_appointments_professional(healthcare_id)),
            ("Back to Portal", lambda: self.professional_portal(healthcare_id))
        ]

        for i, (text, command) in enumerate(buttons):
            tk.Button(button_frame,
                      text=text,
                      width=button_width,
                      command=command,
                      **self.button_style).grid(row=i, column=0, pady=5)

    # Professional view of their upcoming appointments
    def view_appointments_professional(self, healthcare_id):
        self.clear_window()

        # Main frame
        main_frame = ttk.Frame(self.root, padding="20", style='Custom.TFrame')
        main_frame.grid(row=0, column=0, sticky='nsew')

        # Centers elements
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(2, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # Logo
        self._add_logo(main_frame)

        # Title
        ttk.Label(main_frame,
                  text="My Appointments",
                  font=('Verdana', 20, 'bold')).grid(row=1, column=0, pady=(0, 20))

        # Appointments frame
        appointments_frame = ttk.Frame(main_frame, style='Custom.TFrame')
        appointments_frame.grid(row=2, column=0, sticky='nsew', padx=20)
        appointments_frame.grid_columnconfigure(0, weight=1)

        # Create Treeview for appointments
        tree = ttk.Treeview(appointments_frame,
                            columns=('ID', 'Date', 'Time', 'Patient', 'Type', 'Notes'),
                            show='headings',
                            height=10)

        # Define column attributes
        columns = {
            'ID': {'width': 0, 'stretch': False, 'text': 'ID'},
            'Date': {'width': 80, 'stretch': True, 'text': 'Date'},
            'Time': {'width': 80, 'stretch': True, 'text': 'Time'},
            'Patient': {'width': 140, 'stretch': True, 'text': 'Patient'},
            'Type': {'width': 120, 'stretch': True, 'text': 'Type'},
            'Notes': {'width': 200, 'stretch': True, 'text': 'Notes'}
        }

        # Configure columns
        for col, settings in columns.items():
            tree.heading(col, text=settings['text'], anchor='w')
            tree.column(col, width=settings['width'], stretch=settings['stretch'])

        # Add scrollbar
        scrollbar = ttk.Scrollbar(appointments_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')

        # Get and display appointments
        try:
            appointments = self.db.get_professional_appointments(healthcare_id)

            for appt in appointments:
                tree.insert('', 'end', values=(
                    appt['appointment_id'],
                    appt['appointment_date'].strftime('%m/%d/%Y'),
                    appt['appointment_time'],
                    f"{appt['first_name']} {appt['last_name']}",
                    appt['visit_type'],
                    appt['appointment_notes'] if appt['appointment_notes'] else 'N/A'
                ))

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load appointments: {str(e)}")
            appointments = []

        def start_encounter():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select an appointment")
                return

            appointment_id = tree.item(selected[0])['values'][0]

            try:
                # Verify appointment exists and get details
                appointment = self.db.get_appointment_details(appointment_id)
                if appointment:
                    self.create_encounter(healthcare_id, appointment_id)
                else:
                    messagebox.showerror("Error", "Appointment not found")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to start encounter: {str(e)}")

        # Button frame
        button_frame = ttk.Frame(main_frame, style='Custom.TFrame')
        button_frame.grid(row=3, column=0, pady=20)

        # Add buttons
        buttons = [
            ("Start Encounter", start_encounter),
            ("Back", lambda: self.professional_portal(healthcare_id))
        ]

        for i, (text, command) in enumerate(buttons):
            tk.Button(button_frame,
                      text=text,
                      command=command,
                      width=20,
                      **self.button_style).grid(row=0, column=i, padx=10)

        # No appointments message
        if not appointments:
            ttk.Label(appointments_frame,
                      text="No upcoming appointments found.",
                      style='Custom.TLabel').grid(row=1, column=0, pady=20)

        # Filter frame (optional enhancement)
        filter_frame = ttk.LabelFrame(main_frame, text="Filters", padding="10")
        filter_frame.grid(row=4, column=0, sticky='ew', padx=20, pady=10)

        # Date filter
        ttk.Label(filter_frame, text="Date:").grid(row=0, column=0, padx=5)
        date_filter = DateEntry(filter_frame,
                                width=12,
                                background='#dae8f5',
                                foreground='white',
                                borderwidth=2)
        date_filter.grid(row=0, column=1, padx=5)

        def apply_filters():
            selected_date = date_filter.get_date()
            # Clear tree
            for item in tree.get_children():
                tree.delete(item)

            # Reapply with filters
            for appt in appointments:
                if appt['appointment_date'] == selected_date:
                    tree.insert('', 'end', values=(
                        appt['appointment_id'],
                        appt['appointment_date'].strftime('%m/%d/%Y'),
                        appt['appointment_time'],
                        f"{appt['first_name']} {appt['last_name']}",
                        appt['visit_type'],
                        appt['appointment_notes'] if appt['appointment_notes'] else 'N/A'
                    ))

        def clear_filters():
            date_filter.set_date(datetime.now())
            # Refresh the view
            for item in tree.get_children():
                tree.delete(item)
            # Reload all appointments
            for appt in appointments:
                tree.insert('', 'end', values=(
                    appt['appointment_id'],
                    appt['appointment_date'].strftime('%m/%d/%Y'),
                    appt['appointment_time'],
                    f"{appt['first_name']} {appt['last_name']}",
                    appt['visit_type'],
                    appt['appointment_notes'] if appt['appointment_notes'] else 'N/A'
                ))

        ttk.Button(filter_frame, text="Apply Filters", command=apply_filters).grid(row=0, column=2, padx=5)
        ttk.Button(filter_frame, text="Clear Filters", command=clear_filters).grid(row=0, column=3, padx=5)

    # Professional functionality to create encounter notes
    def create_encounter(self, healthcare_id, appointment_id):
        self.clear_window()
        self.root.geometry("1200x900")

        # Main frame
        main_frame = ttk.Frame(self.root, padding="20", style='Custom.TFrame')
        main_frame.grid(row=0, column=0, sticky='nsew')

        # Centers elements
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(2, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # Logo
        self._add_logo(main_frame)

        # Title
        ttk.Label(main_frame,
                  text="Appointment Notes",
                  font=('Verdana', 20, 'bold')).grid(row=1, column=0, pady=(0, 20))

        # Get appointment and patient details
        appointment = self.db.get_appointment_details(appointment_id)
        patient_info = self.db.get_patient_info(appointment['patient_id'])
        medical_history = self.db.get_medical_history(appointment['patient_id'])
        medications = self.db.get_medications(appointment['patient_id'])

        # Appointment Details Frame
        appt_frame = ttk.LabelFrame(main_frame, text="Appointment Details", padding="10")
        appt_frame.grid(row=2, column=0, sticky='ew', padx=20, pady=5)

        details_text = f"""
        Patient: {patient_info['first_name']} {patient_info['last_name']}
        Date: {appointment['appointment_date'].strftime('%m/%d/%Y')}
        Time: {appointment['appointment_time']}
        Type: {appointment['visit_type']}
        """
        ttk.Label(appt_frame, text=details_text, justify='left').grid(row=0, column=0, sticky='w')

        # Patient Information Frame
        info_frame = ttk.LabelFrame(main_frame, text="Patient Information", padding="10")
        info_frame.grid(row=3, column=0, sticky='ew', padx=20, pady=5)

        ttk.Label(info_frame, text="Allergies:", font=('Verdana', 10, 'bold')).grid(row=0, column=0, sticky='w', padx=5)
        ttk.Label(info_frame, text=patient_info['allergies'] or "None", wraplength=900).grid(row=0, column=1,
                                                                                             sticky='w')

        # Current Medications Frame
        med_frame = ttk.LabelFrame(main_frame, text="Current Medications", padding="10")
        med_frame.grid(row=4, column=0, sticky='ew', padx=20, pady=5)

        med_tree = ttk.Treeview(med_frame,
                                columns=('Medication', 'Dosage', 'Start Date', 'End Date', 'Side Effects'),
                                show='headings',
                                height=3)
        med_tree.heading('Medication', text='Medication')
        med_tree.heading('Dosage', text='Dosage')
        med_tree.heading('Start Date', text='Start Date')
        med_tree.heading('End Date', text='End Date')
        med_tree.heading('Side Effects', text='Side Effects')

        # Adjust column widths
        med_tree.column('Medication', width=150)
        med_tree.column('Dosage', width=100)
        med_tree.column('Start Date', width=100)
        med_tree.column('End Date', width=100)
        med_tree.column('Side Effects', width=200)

        for med in medications:
            med_tree.insert('', 'end', values=(
                med['medication_name'],
                med['dosage'] or 'Not specified',
                med['start_date'].strftime('%m/%d/%Y') if med['start_date'] else 'Not specified',
                med['end_date'].strftime('%m/%d/%Y') if med['end_date'] else 'Ongoing',
                med['side_effects'] or 'None reported'
            ))
        med_tree.grid(row=0, column=0, sticky='ew')

        # Medical History Frame
        history_frame = ttk.LabelFrame(main_frame, text="Medical History", padding="10")
        history_frame.grid(row=5, column=0, sticky='ew', padx=20, pady=5)
        history_frame.grid_columnconfigure(0, weight=1)  # Allow horizontal expansion

        # Create Treeview with scrollbar
        history_tree = ttk.Treeview(history_frame,
                                    columns=('Date', 'Diagnosis', 'Notes'),
                                    show='headings',
                                    height=5)  # Show 5 rows at a time

        # Add vertical scrollbar
        y_scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=history_tree.yview)
        history_tree.configure(yscrollcommand=y_scrollbar.set)

        # Add horizontal scrollbar
        x_scrollbar = ttk.Scrollbar(history_frame, orient="horizontal", command=history_tree.xview)
        history_tree.configure(xscrollcommand=x_scrollbar.set)

        # Configure columns
        history_tree.heading('Date', text='Date')
        history_tree.heading('Diagnosis', text='Diagnosis')
        history_tree.heading('Notes', text='Notes')

        # Set column widths
        history_tree.column('Date', width=100, minwidth=100)
        history_tree.column('Diagnosis', width=200, minwidth=150)
        history_tree.column('Notes', width=300, minwidth=200)

        # Grid layout for tree and scrollbars
        history_tree.grid(row=0, column=0, sticky='nsew')
        y_scrollbar.grid(row=0, column=1, sticky='ns')
        x_scrollbar.grid(row=1, column=0, sticky='ew')

        # Populate history
        for record in medical_history:
            history_tree.insert('', 'end', values=(
                record['treatment_date'].strftime('%m/%d/%Y'),
                record['diagnosis'] or 'No diagnosis',
                record['notes']
            ))

        # Appointment Notes Frame
        encounter_frame = ttk.LabelFrame(main_frame, text="Appointment Notes", padding="10")
        encounter_frame.grid(row=6, column=0, sticky='ew', padx=20, pady=5)

        ttk.Label(encounter_frame, text="Diagnosis:").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        diagnosis = ttk.Entry(encounter_frame, width=80)
        diagnosis.grid(row=1, column=0, sticky='ew', padx=5, pady=2)

        ttk.Label(encounter_frame, text="Notes:").grid(row=2, column=0, sticky='w', padx=5, pady=2)
        notes = tk.Text(encounter_frame, height=4, width=80)
        notes.grid(row=3, column=0, sticky='ew', padx=5, pady=2)

        def submit():
            if not notes.get("1.0", "end-1c").strip() and not diagnosis.get().strip():
                messagebox.showwarning("Warning", "Please enter either notes or a diagnosis")
                return

            encounter_data = {
                'appointment_id': appointment_id,
                'patient_id': appointment['patient_id'],
                'healthcare_id': healthcare_id,
                'diagnosis': diagnosis.get() if diagnosis.get().strip() else None,
                'notes': notes.get("1.0", "end-1c")
            }

            self.show_encounter_confirmation(encounter_data)

        # Button Frame
        button_frame = ttk.Frame(main_frame, style='Custom.TFrame')
        button_frame.grid(row=7, column=0, pady=20)

        tk.Button(button_frame,
                  text="Next",
                  command=submit,
                  **self.button_style).grid(row=0, column=0, padx=10)

        tk.Button(button_frame,
                  text="Back",
                  command=lambda: self.view_appointments_professional(healthcare_id),
                  **self.button_style).grid(row=0, column=1, padx=10)

    # Encounter confirmation
    def show_encounter_confirmation(self, encounter_data):
        self.clear_window()
        self.root.geometry("700x550")

        # Main frame
        main_frame = ttk.Frame(self.root, padding="20", style='Custom.TFrame')
        main_frame.grid(row=0, column=0, sticky='nsew')

        # Title
        ttk.Label(main_frame,
                  text="Encounter Summary",
                  font=('Verdana', 16, 'bold')).grid(row=0, column=0, pady=(0, 20))

        # Summary frame
        summary_frame = ttk.LabelFrame(main_frame, text="Encounter Details", padding="10")
        summary_frame.grid(row=1, column=0, sticky='ew', padx=10, pady=5)

        # Display encounter details
        ttk.Label(summary_frame, text="Diagnosis:").grid(row=0, column=0, sticky='w', pady=5)
        ttk.Label(summary_frame, text=encounter_data['diagnosis'], wraplength=500).grid(row=0, column=1, sticky='w',
                                                                                        pady=5)

        ttk.Label(summary_frame, text="Notes:").grid(row=1, column=0, sticky='w', pady=5)
        ttk.Label(summary_frame, text=encounter_data['notes'], wraplength=500).grid(row=1, column=1, sticky='w', pady=5)

        # Billing frame
        billing_frame = ttk.LabelFrame(main_frame, text="Billing Information", padding="10")
        billing_frame.grid(row=2, column=0, sticky='ew', padx=10, pady=20)

        ttk.Label(billing_frame, text="Amount:").grid(row=0, column=0, sticky='e', pady=5)
        amount_entry = ttk.Entry(billing_frame)
        amount_entry.grid(row=0, column=1, sticky='w', pady=5)
        amount_entry.insert(0, "0.00")

        # Billing frame
        billing_frame = ttk.LabelFrame(main_frame, text="Billing Information", padding="10")
        billing_frame.grid(row=2, column=0, sticky='ew', padx=10, pady=20)

        ttk.Label(billing_frame, text="Amount:").grid(row=0, column=0, sticky='e', pady=5)
        amount_entry = ttk.Entry(billing_frame)
        amount_entry.grid(row=0, column=1, sticky='w', pady=5)
        amount_entry.insert(0, "0.00")

        # Medication frame
        med_frame = ttk.LabelFrame(main_frame, text="Prescribe Medication", padding="10")
        med_frame.grid(row=3, column=0, sticky='ew', padx=10, pady=5)

        # Left side - Medication info
        med_info_frame = ttk.Frame(med_frame)
        med_info_frame.grid(row=0, column=0, padx=5)

        ttk.Label(med_info_frame, text="Medication:").grid(row=0, column=0, sticky='e', pady=5)
        med_name = ttk.Entry(med_info_frame)
        med_name.grid(row=0, column=1, sticky='w', pady=5)

        ttk.Label(med_info_frame, text="Dosage:").grid(row=1, column=0, sticky='e', pady=5)
        med_dosage = ttk.Entry(med_info_frame)
        med_dosage.grid(row=1, column=1, sticky='w', pady=5)

        ttk.Label(med_info_frame, text="Amount:").grid(row=2, column=0, sticky='e', pady=5)
        med_amount = ttk.Entry(med_info_frame)
        med_amount.grid(row=2, column=1, sticky='w', pady=5)

        # Right side - Dates and side effects
        med_dates_frame = ttk.Frame(med_frame)
        med_dates_frame.grid(row=0, column=1, padx=5)

        ttk.Label(med_dates_frame, text="Start Date:").grid(row=0, column=0, sticky='e', pady=5)
        start_date = DateEntry(med_dates_frame,
                               width=12,
                               background='darkblue',
                               foreground='white',
                               borderwidth=2,
                               date_pattern='mm/dd/yyyy')
        start_date.grid(row=0, column=1, sticky='w', pady=5)

        ttk.Label(med_dates_frame, text="End Date:").grid(row=1, column=0, sticky='e', pady=5)
        end_date = DateEntry(med_dates_frame,
                             width=12,
                             background='darkblue',
                             foreground='white',
                             borderwidth=2,
                             date_pattern='mm/dd/yyyy')
        end_date.grid(row=1, column=1, sticky='w', pady=5)

        ttk.Label(med_dates_frame, text="Side Effects:").grid(row=2, column=0, sticky='e', pady=5)
        med_side_effects = ttk.Entry(med_dates_frame, width=30)
        med_side_effects.grid(row=2, column=1, sticky='w', pady=5)

        def submit_billing():
            try:
                amount = float(amount_entry.get())

                # Add medical history if there are notes or diagnosis
                if encounter_data['notes'].strip() or encounter_data.get('diagnosis'):
                    history_id = self.db.add_medical_history(
                        encounter_data['patient_id'],
                        encounter_data['healthcare_id'],
                        encounter_data.get('diagnosis', ''),
                        encounter_data['notes']
                    )

                # Add medication if prescribed
                if med_name.get().strip():
                    self.db.add_medication(
                        encounter_data['patient_id'],
                        med_name.get(),
                        med_dosage.get(),
                        med_amount.get(),
                        start_date.get_date(),
                        end_date.get_date(),
                        med_side_effects.get()
                    )

                # Create bill
                bill_id = self.db.create_bill(
                    encounter_data['patient_id'],
                    encounter_data['appointment_id'],
                    amount
                )

                if messagebox.askyesno("Process Payment", "Would you like to process payment now?"):
                    self.db.process_payment(bill_id, amount)
                    messagebox.showinfo("Success", "Payment processed successfully")
                else:
                    messagebox.showinfo("Success",
                                        "Encounter saved and bill generated.\nPayment can be processed later.")

                self.root.destroy()
                self.view_appointments_professional(encounter_data['healthcare_id'])

            except ValueError:
                messagebox.showerror("Error", "Please enter a valid amount")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save encounter: {str(e)}")
        # Button frame
        button_frame = ttk.Frame(main_frame, style='Custom.TFrame')
        button_frame.grid(row=4, column=0, pady=20)

        tk.Button(button_frame,
                  text="Submit and Generate Bill",
                  command=submit_billing,
                  **self.button_style).grid(row=0, column=0, padx=10)

        tk.Button(button_frame,
                  text="Cancel",
                  command=self.root.destroy,
                  **self.button_style).grid(row=0, column=1, padx=10)

    # Professional side view of appointments
    def search_appointments_professional(self,healthcare_id):
        self.clear_window()

    # Professional Side view to schedule appointments
    def schedule_appointments_professional(self, healthcare_id):
        self.clear_window()

    # Allows professional to add a patient
    def add_patient(self,healthcare_id):
        self.clear_window()

        # Main frame
        main_frame = ttk.Frame(self.root, padding="20", style='Custom.TFrame')
        main_frame.grid(row=0, column=0, sticky='nsew')

        # Centers elements
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(2, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # Logo
        self._add_logo(main_frame)

        # Title
        ttk.Label(main_frame,
                  text="Add New Patient",
                  font=('Verdana', 20, 'bold')).grid(row=1, column=0, pady=(0, 30))

        # Form frame
        form_frame = ttk.Frame(main_frame, style='Custom.TFrame')
        form_frame.grid(row=2, column=0, sticky='n')
        form_frame.grid_columnconfigure(0, weight=1)

        # Entry fields
        first_name = ttk.Entry(form_frame, width=30)
        last_name = ttk.Entry(form_frame, width=30)
        birth_date = ttk.Entry(form_frame, width=30)
        gender = ttk.Combobox(form_frame, values=['Male', 'Female', 'Other'], width=27)
        phone = ttk.Entry(form_frame, width=30)
        zip_code = ttk.Entry(form_frame, width=30)
        ssn = ttk.Entry(form_frame, width=30)
        allergies = ttk.Entry(form_frame, width=30)

        # Layout
        ttk.Label(form_frame, text="First Name:").grid(row=0, column=0, pady=5, sticky='e', padx=5)
        first_name.grid(row=0, column=1, pady=5)

        ttk.Label(form_frame, text="Last Name:").grid(row=1, column=0, pady=5, sticky='e', padx=5)
        last_name.grid(row=1, column=1, pady=5)

        ttk.Label(form_frame, text="Birth Date:").grid(row=2, column=0, pady=5, sticky='e', padx=5)
        birth_date.grid(row=2, column=1, pady=5)

        ttk.Label(form_frame, text="Gender:").grid(row=3, column=0, pady=5, sticky='e', padx=5)
        gender.grid(row=3, column=1, pady=5)
        gender.set("Select Gender")

        ttk.Label(form_frame, text="Phone:").grid(row=4, column=0, pady=5, sticky='e', padx=5)
        phone.grid(row=4, column=1, pady=5)

        ttk.Label(form_frame, text="Zip Code:").grid(row=5, column=0, pady=5, sticky='e', padx=5)
        zip_code.grid(row=5, column=1, pady=5)

        ttk.Label(form_frame, text="SSN:").grid(row=6, column=0, pady=5, sticky='e', padx=5)
        ssn.grid(row=6, column=1, pady=5)

        ttk.Label(form_frame, text="Allergies:").grid(row=7, column=0, pady=5, sticky='e', padx=5)
        allergies.grid(row=7, column=1, pady=5)

        # Add placeholders
        def add_placeholder(entry, placeholder):
            entry.insert(0, placeholder)
            entry.config(foreground='gray')

            def on_focus_in(event):
                if entry.get() == placeholder:
                    entry.delete(0, tk.END)
                    entry.config(foreground='black')

            def on_focus_out(event):
                if not entry.get():
                    entry.insert(0, placeholder)
                    entry.config(foreground='gray')

            entry.bind('<FocusIn>', on_focus_in)
            entry.bind('<FocusOut>', on_focus_out)

        # Add placeholders to fields
        add_placeholder(first_name, "Enter first name")
        add_placeholder(last_name, "Enter last name")
        add_placeholder(birth_date, "YYYY-MM-DD")
        add_placeholder(phone, "XXX-XXX-XXXX")
        add_placeholder(zip_code, "XXXXX")
        add_placeholder(ssn, "XXX-XX-XXXX")
        add_placeholder(allergies, "Enter allergies or None")

        def validate_and_submit():
            # Get values and remove placeholders
            fn = first_name.get()
            ln = last_name.get()
            bd = birth_date.get()
            gen = gender.get()
            ph = phone.get()
            zc = zip_code.get()
            ss = ssn.get()
            alg = allergies.get()

            # Remove placeholder text if present
            if fn == "Enter first name": fn = ""
            if ln == "Enter last name": ln = ""
            if bd == "YYYY-MM-DD": bd = ""
            if ph == "XXX-XXX-XXXX": ph = ""
            if zc == "XXXXX": zc = ""
            if ss == "XXX-XX-XXXX": ss = ""
            if alg == "Enter allergies or None": alg = ""

            # Validate required fields
            if not all([fn, ln, bd, ph, zc, ss]):
                messagebox.showerror("Error", "Please fill in all required fields")
                return

            if gen == "Select Gender":
                messagebox.showerror("Error", "Please select a gender")
                return

            try:
                # Try to create new patient
                patient_id, password = self.db.add_new_patient(
                    fn, ln, bd, gen, ph, zc, ss, alg or 'None'
                )

                # Show success message with credentials
                messagebox.showinfo(
                    "Success",
                    f"Patient added successfully!\n\n"
                    f"Patient ID: {patient_id}\n"
                    f"Password: {password}\n\n"
                    "Please provide these credentials to the patient."
                )

                self.professional_portal(healthcare_id)

            except Exception as e:
                messagebox.showerror("Error", f"Failed to add patient: {str(e)}")

        # Button frame
        button_frame = ttk.Frame(form_frame, style='Custom.TFrame')
        button_frame.grid(row=8, column=0, columnspan=2, pady=20)

        tk.Button(button_frame,
                  text="Submit",
                  command=validate_and_submit,
                  **self.button_style).grid(row=0, column=0, padx=10)

        tk.Button(button_frame,
                  text="Back",
                  command=lambda: self.professional_portal(healthcare_id),
                  **self.button_style).grid(row=0, column=1, padx=10)

    def search_patient(self,healthcare_id):
        self.clear_window()

    # Allows professionals to view billing
    def billing_professional(self,healthcare_id):
        self.clear_window()

if __name__ == "__main__":
    root = tk.Tk()
    app = HealthcareGUI(root)
    root.mainloop()