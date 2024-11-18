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
            'Type': {'width': 120, 'minwidth': 100},
            'Doctor': {'width': 160, 'minwidth': 140},
            'Notes': {'width': 180, 'minwidth': 140}
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
                if self.db.cancel_appointment(appointment_id):
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

        date_cal = DateEntry(form_frame,
                             width=30,
                             background='darkblue',
                             foreground='white',
                             borderwidth=2,
                             date_pattern='mm/dd/yyyy',
                             mindate=min_date,
                             maxdate=max_date)
        date_cal.grid(row=1, column=1, pady=5)
        date_cal.set_date(current_date)

        # Time Selection
        ttk.Label(form_frame, text="Select Time:").grid(row=2, column=0, pady=5, sticky='w')
        time_slots = self.db.get_available_time_slots()

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

        # Doctor Selection
        ttk.Label(form_frame, text="Select Doctor:").grid(row=3, column=0, pady=5, sticky='w')
        doctor_var = tk.StringVar()
        doctor_dropdown = ttk.Combobox(form_frame, textvariable=doctor_var, width=30)
        doctor_dropdown.grid(row=3, column=1, pady=5)
        doctor_dropdown.set("Select Time and Date First")

        # Find available doctors for date and time selection
        def update_available_doctors(*args):
            selected_date = date_cal.get_date()
            selected_time = time_var.get()

            if selected_time == "Select Time":
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

        # Notes/Comments entry form
        ttk.Label(form_frame, text="Additional Notes:").grid(row=4, column=0, pady=5, sticky='w')
        notes_text = tk.Text(form_frame, height=3, width=30)
        notes_text.grid(row=4, column=1, pady=5)

        # Validate appointment submission
        def validate_and_submit():
            selected_date = date_cal.get_date()

            if (type_var.get() == "Select Type" or
                    time_var.get() == "Select Time" or
                    doctor_var.get() == "Select Time and Date First" or
                    doctor_var.get() == "Select Healthcare Professional"):
                messagebox.showerror("Error", "Please fill in all fields")
                return

            selected_doctor = doctor_var.get()
            healthcare_professional_id = self.doctor_map[selected_doctor]

            success = self.db.submit_appointment(
                type_var.get(),
                selected_date,
                time_var.get(),
                healthcare_professional_id,
                notes_text.get("1.0", tk.END).strip(),
                patient_id
            )

            if success:
                messagebox.showinfo("Success", "Appointment scheduled successfully!")
                self.view_appointment_patient(patient_id)

        # Button frame
        button_frame = ttk.Frame(form_frame, style='Custom.TFrame')
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)

        # Buttons
        tk.Button(button_frame,
                  text="Submit",
                  command=validate_and_submit,
                  **self.button_style).grid(row=0, column=0, padx=10)

        tk.Button(button_frame,
                  text="Back",
                  command=lambda: self.appointments_patient(patient_id),
                  **self.button_style).grid(row=0, column=1, padx=10)

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


if __name__ == "__main__":
    root = tk.Tk()
    app = HealthcareGUI(root)
    root.mainloop()