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

        patient_info = self.db.get_patient_info(patient_id)
        # Label frame
        ttk.Label(main_frame,
                  text= f"Welcome Back {patient_info['first_name']}",
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
            ("View My Medications", lambda: self.medications_patient(patient_id)),
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
                  text="Welcome to the Professional's Portal",
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

        patient_info = self.db.get_patient_info(patient_id)

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

        # Configure root window grid weights
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # Main frame
        main_frame = ttk.Frame(self.root, padding="20", style='Custom.TFrame')
        main_frame.grid(row=0, column=0, sticky='nsew')  # Add main_frame to root
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)

        # Add logo
        self._add_logo(main_frame)

        # Appointments frame
        appointments_frame = ttk.LabelFrame(main_frame, text="My Appointments",
                                            padding="20", style='Login.TLabelframe')
        appointments_frame.grid(row=1, column=0, padx=20, pady=20, sticky='nsew')
        appointments_frame.grid_columnconfigure(0, weight=1)
        appointments_frame.grid_rowconfigure(0, weight=1)

        # Column settings
        columns = {
            'ID': {'width': 0, 'stretch': False},
            'Date': {'width': 80, 'stretch': True},
            'Time': {'width': 80, 'stretch': True},
            'Type': {'width': 100, 'stretch': True},
            'Doctor': {'width': 100, 'stretch': True},
            'Notes': {'width': 160, 'stretch': True}
        }

        # Create Treeview for appointments
        tree = ttk.Treeview(appointments_frame, columns=list(columns.keys()), show='headings')
        for column_name, settings in columns.items():
            tree.heading(column_name, text=column_name)
            tree.column(column_name, width=settings['width'],
                        minwidth=settings.get('minwidth', settings['width']),
                        stretch=settings.get('stretch', True))

        # Scroll bars
        y_scrollbar = ttk.Scrollbar(appointments_frame, orient="vertical", command=tree.yview)
        x_scrollbar = ttk.Scrollbar(appointments_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

        # Grid layout for tree and scrollbars
        tree.grid(row=0, column=0, sticky='nsew')
        y_scrollbar.grid(row=0, column=1, sticky='ns')
        x_scrollbar.grid(row=1, column=0, sticky='ew')

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
                      font=('Verdana', 11),
                      style='Custom.TLabel').grid(row=2, column=0, pady=20)

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

        # Appointment type selection
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

        # Date selection
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

        # Time selection
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

        # Healthcare professional selection
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

        # Notes/comments entry form with placeholder
        ttk.Label(form_frame, text="Additional Notes:").grid(row=4, column=0, pady=5, sticky='w')
        notes_text = tk.Text(form_frame, height=3, width=40)
        notes_text.grid(row=4, column=1, pady=5)
        add_placeholder_to_text(notes_text, "Enter any concerns or conditions you may have")

        def validate_and_submit():
            # Get notes
            notes = notes_text.get("1.0", tk.END).strip()
            if notes == "Enter any concerns or conditions you may have":
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
        self.clear_window()
        self.root.geometry("900x800")

        # Main frame
        main_frame = ttk.Frame(self.root, padding="20", style='Custom.TFrame')
        main_frame.grid(row=0, column=0, sticky='nsew')

        # Configure grid
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # Logo and title
        self._add_logo(main_frame)
        ttk.Label(main_frame,
                  text="My Billing",
                  font=('Verdana', 20, 'bold'),
                  style='Login.TLabelframe.Label').grid(row=1, column=0, pady=(0, 20))

        # Bills frame
        bills_frame = ttk.LabelFrame(main_frame, text="Current Bills", padding="10", style='Login.TLabelframe')
        bills_frame.grid(row=2, column=0, sticky='nsew', padx=20, pady=5)
        bills_frame.grid_columnconfigure(0, weight=1)

        # Treeview of billing
        style = ttk.Style()
        style.configure("Treeview", font=('Verdana', 11), rowheight=25)
        style.configure("Treeview.Heading", font=('Verdana', 11, 'bold'))

        columns = ('Service Date', 'Date Issued', 'Due Date', 'Amount', 'Status')
        tree = ttk.Treeview(bills_frame, columns=columns, show='headings', height=10)

        # Configure columns
        for col in columns:
            tree.heading(col, text=col)
            width = 150 if col in ['Service Date', 'Date Issued', 'Due Date'] else 120
            tree.column(col, width=width)

        # Scrollbars
        y_scrollbar = ttk.Scrollbar(bills_frame, orient="vertical", command=tree.yview)
        x_scrollbar = ttk.Scrollbar(bills_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

        # Grid layout
        tree.grid(row=0, column=0, sticky='nsew', pady=5)
        y_scrollbar.grid(row=0, column=1, sticky='ns')
        x_scrollbar.grid(row=1, column=0, sticky='ew')

        # Get and display bills
        bills = self.db.get_patient_bills(patient_id)
        for bill in bills:
            tree.insert('', 'end', values=(
                bill['appointment_date'].strftime('%m/%d/%Y'),
                bill['date_issued'].strftime('%m/%d/%Y'),
                bill['due_date'].strftime('%m/%d/%Y'),
                f"${float(bill['amount']):.2f}",
                bill['status']
            ), tags=(str(bill['bill_id']),))

        # Payment frame
        payment_frame = ttk.LabelFrame(main_frame, text="Make Payment", padding="10", style='Login.TLabelframe')
        payment_frame.grid(row=3, column=0, sticky='ew', padx=20, pady=5)
        payment_frame.grid_remove()

        # Payment details
        payment_details = ttk.Frame(payment_frame, style='Custom.TFrame')
        payment_details.grid(row=0, column=0, sticky='ew', padx=10, pady=5)
        payment_details.grid_columnconfigure(1, weight=1)

        ttk.Label(payment_details,
                  text="Current Amount:",
                  font=('Verdana', 11, 'bold')).grid(row=0, column=0, sticky='w', pady=5, padx=5)
        amount_label = ttk.Label(payment_details, text="", font=('Verdana', 11))
        amount_label.grid(row=0, column=1, sticky='w', pady=5)

        ttk.Label(payment_details,
                  text="Payment Amount:",
                  font=('Verdana', 11, 'bold')).grid(row=1, column=0, sticky='w', pady=5, padx=5)
        payment_entry = ttk.Entry(payment_details, width=20, font=('Verdana', 11))
        payment_entry.grid(row=1, column=1, sticky='w', pady=5)

        def make_payment():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select a bill to pay")
                return

            item = tree.item(selected[0])
            current_amount = float(item['values'][3].replace('$', ''))

            if item['values'][4] == 'Paid':
                messagebox.showinfo("Information", "This bill has already been paid in full")
                return

            payment_frame.grid()
            amount_label.config(text=f"${current_amount:.2f}")
            payment_entry.delete(0, tk.END)
            payment_entry.insert(0, f"{current_amount:.2f}")
            process_payment_btn.grid()
            make_payment_btn.grid_remove()

        def process_payment():
            try:
                selected = tree.selection()[0]
                bill_id = int(tree.item(selected)['tags'][0])
                current_amount = float(tree.item(selected)['values'][3].replace('$', ''))
                payment_amount = float(payment_entry.get())

                if payment_amount <= 0:
                    messagebox.showerror("Error", "Please enter a valid amount greater than 0")
                    return
                if payment_amount > current_amount:
                    messagebox.showerror("Error", "Payment amount cannot exceed bill amount")
                    return

                self.db.process_payment(bill_id, payment_amount)
                messagebox.showinfo("Success", "Payment processed successfully")
                self.patient_portal(patient_id)

            except ValueError:
                messagebox.showerror("Error", "Please enter a valid payment amount")

        # Button frame
        button_frame = ttk.Frame(main_frame, style='Custom.TFrame')
        button_frame.grid(row=4, column=0, pady=20)

        make_payment_btn = tk.Button(button_frame,
                                     text="Make Payment",
                                     command=make_payment,
                                     **self.button_style)
        make_payment_btn.grid(row=0, column=0, padx=10)

        process_payment_btn = tk.Button(button_frame,
                                        text="Process Payment",
                                        command=process_payment,
                                        **self.button_style)
        process_payment_btn.grid(row=0, column=1, padx=10)
        process_payment_btn.grid_remove()

        tk.Button(button_frame,
                  text="Back",
                  command=lambda: [self.patient_portal(patient_id)],
                  **self.button_style).grid(row=0, column=2, padx=10)

    # Patient view for viewing their medication
    def medications_patient(self, patient_id):
        self.clear_window()
        self.root.geometry("900x600")

        main_frame = ttk.Frame(self.root, padding="20", style='Custom.TFrame')
        main_frame.grid(row=0, column=0, sticky='nsew')

        # Configure grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(2, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # Logo and Title
        self._add_logo(main_frame)
        ttk.Label(main_frame, text="My Medications",
                  font=('Verdana', 20, 'bold')).grid(row=1, column=0, pady=(0, 20))

        # Medications Frame
        med_frame = ttk.LabelFrame(main_frame, text="Current Medications",
                                   padding="10", style='Login.TLabelframe')
        med_frame.grid(row=2, column=0, sticky='nsew', padx=20, pady=5)
        med_frame.grid_columnconfigure(0, weight=1)

        # Treeview for medications
        tree = ttk.Treeview(med_frame, columns=('Medication', 'Dosage', 'Start Date', 'End Date', 'Side Effects'),
                            show='headings', height=10)

        # Configure columns
        tree.column('Medication', width=150, minwidth=150)
        tree.column('Dosage', width=100, minwidth=100)
        tree.column('Start Date', width=100, minwidth=100)
        tree.column('End Date', width=100, minwidth=100)
        tree.column('Side Effects', width=300, minwidth=200)

        # Set headings
        tree.heading('Medication', text='Medication')
        tree.heading('Dosage', text='Dosage')
        tree.heading('Start Date', text='Start Date')
        tree.heading('End Date', text='End Date')
        tree.heading('Side Effects', text='Side Effects')

        # Scrollbars
        y_scrollbar = ttk.Scrollbar(med_frame, orient="vertical", command=tree.yview)
        x_scrollbar = ttk.Scrollbar(med_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

        # Grid layout
        tree.grid(row=0, column=0, sticky='nsew')
        y_scrollbar.grid(row=0, column=1, sticky='ns')
        x_scrollbar.grid(row=1, column=0, sticky='ew')

        # Get and display prescriptions
        prescriptions = self.db.get_patient_prescriptions(patient_id)

        for prescription in prescriptions:
            tree.insert('', 'end', values=(
                prescription['medication_name'],
                prescription['dosage'],
                prescription['start_date'].strftime('%m/%d/%Y'),
                prescription['end_date'].strftime('%m/%d/%Y') if prescription['end_date'] else 'Ongoing',
                prescription['side_effects']
            ))

        # If no medications
        if not prescriptions:
            ttk.Label(med_frame, text="No current medications found.",
                      font=('Verdana', 11),
                      style='Custom.TLabel').grid(row=2, column=0, pady=20)

        # Button Frame
        button_frame = ttk.Frame(main_frame, style='Custom.TFrame')
        button_frame.grid(row=3, column=0, pady=20)

        tk.Button(button_frame,
                  text="Back",
                  command=lambda: self.patient_portal(patient_id),
                  width=15,
                  **self.button_style).grid(row=0, column=0)

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
            ("Schedule New Appointment", lambda: self.schedule_appointments_for_professional(healthcare_id)),
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

        # Appointment treeview
        tree = ttk.Treeview(appointments_frame,
                            columns=('ID', 'Date', 'Time', 'Patient', 'Type', 'Notes'),
                            show='headings',
                            height=10)

        # Column attributes
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

        # Scrollbar for appointments
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

        def cancel_appointment():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select an appointment to cancel")
                return

            appointment_id = tree.item(selected[0])['values'][0]

            if messagebox.askyesno("Confirm Cancellation",
                                   "Are you sure you want to cancel this appointment?"):
                try:
                    if self.db.delete_appointment(appointment_id):
                        messagebox.showinfo("Success", "Appointment cancelled successfully!")
                        # Refresh the appointments view
                        for item in tree.get_children():
                            tree.delete(item)
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
                    messagebox.showerror("Error", f"Failed to cancel appointment: {str(e)}")

        # Button frame
        button_frame = ttk.Frame(main_frame, style='Custom.TFrame')
        button_frame.grid(row=3, column=0, pady=20)

        # Add buttons
        buttons = [
            ("Start Encounter", start_encounter),
            ("Back", lambda: self.professional_portal(healthcare_id))
        ]

        buttons = [
            ("Start Encounter", start_encounter, 15),
            ("Cancel Selected", cancel_appointment, 15),
            ("Back", lambda: self.professional_portal(healthcare_id), 10)
        ]

        for i, (text, command, width) in enumerate(buttons):
            tk.Button(button_frame,
                      text=text,
                      command=command,
                      width=width,  # Individual widths for each button
                      **self.button_style).grid(row=0, column=i, padx=10)

        # No appointments message
        if not appointments:
            ttk.Label(appointments_frame,
                      text="No upcoming appointments found.",
                      style='Custom.TLabel').grid(row=1, column=0, pady=20)

        # Filter frame
        filter_frame = ttk.LabelFrame(main_frame, text="Filter by Date", padding="10", style='Login.TLabelframe')
        filter_frame.grid(row=4, column=0, sticky='ew', padx=20, pady=10)

        # Date filter
        ttk.Label(filter_frame, text="Date:").grid(row=0, column=0, padx=5)
        date_filter = DateEntry(filter_frame,
                                width=12,
                                background='#03294a',
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

        ttk.Button(filter_frame, text="Apply", command=apply_filters).grid(row=0, column=2, padx=5)
        ttk.Button(filter_frame, text="Clear", command=clear_filters).grid(row=0, column=3, padx=5)

    # Professional functionality to create encounter notes
    def create_encounter(self, healthcare_id, appointment_id):
        self.clear_window()
        self.root.geometry("800x1200")

        main_frame = ttk.Frame(self.root, padding="20", style='Custom.TFrame')
        main_frame.grid(row=0, column=0, sticky='nsew')

        # Centers elements
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(2, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # Logo and Title
        self._add_logo(main_frame)
        ttk.Label(main_frame, text="Appointment Notes", font=('Verdana', 20, 'bold')).grid(row=1, column=0,
                                                                                           pady=(0, 20))

        # Get data
        appointment = self.db.get_appointment_details(appointment_id)
        patient_info = self.db.get_patient_info(appointment['patient_id'])
        medical_history = self.db.get_medical_history(appointment['patient_id'])
        prescriptions = self.db.get_patient_prescriptions(appointment['patient_id'])

        # Calculate age
        birth_date = patient_info['birth_date']
        today = datetime.now()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

        # Patient & appointment infor frame
        info_frame = ttk.LabelFrame(main_frame, text="Patient & Appointment Information", padding="10",
                                    style='Login.TLabelframe')
        info_frame.grid(row=2, column=0, sticky='ew', padx=20, pady=5)

        details = [
            ("Patient ID:", f"{patient_info['patient_id']}"),
            ("Appointment ID:", f"{appointment['appointment_id']}"),
            ("Name:", f"{patient_info.get('first_name', '')} {patient_info.get('last_name', '')}"),
            ("Age:", f"{age}"),
            ("Gender:", f"{patient_info.get('gender', 'N/A')}"),
            ("Date:", f"{appointment['appointment_date'].strftime('%m/%d/%Y')}"),
            ("Time:", f"{appointment['appointment_time']}"),
            ("Visit Type:", f"{appointment['visit_type']}"),
            ("Allergies:", f"{patient_info.get('allergies', 'None')}")
        ]

        for i, (label, value) in enumerate(details):
            ttk.Label(info_frame, text=label, font=('Verdana', 11, 'bold')).grid(row=i, column=0, sticky='w', padx=5,
                                                                                 pady=2)
            ttk.Label(info_frame, text=value, font=('Verdana', 11), wraplength=900).grid(row=i, column=1, sticky='w',
                                                                                         padx=5, pady=2)

        # Prescriptions Frame
        med_frame = ttk.LabelFrame(main_frame, text="Current Prescriptions", padding="10", style='Login.TLabelframe')
        med_frame.grid(row=4, column=0, sticky='ew', padx=20, pady=5)
        med_frame.grid_columnconfigure(0, weight=1)

        # Create Treeview
        med_tree = ttk.Treeview(med_frame, columns=('Medication', 'Dosage', 'Start Date', 'End Date', 'Side Effects'),
                                show='headings', height=3)

        # Configure columns
        med_tree.column('Medication', width=150, minwidth=150)
        med_tree.column('Dosage', width=110, minwidth=110)
        med_tree.column('Start Date', width=100, minwidth=100)
        med_tree.column('End Date', width=100, minwidth=100)
        med_tree.column('Side Effects', width=300, minwidth=200)

        # Set column headings
        med_tree.heading('Medication', text='Medication')
        med_tree.heading('Dosage', text='Dosage')
        med_tree.heading('Start Date', text='Start Date')
        med_tree.heading('End Date', text='End Date')
        med_tree.heading('Side Effects', text='Side Effects')

        # Scrollbars
        med_y_scrollbar = ttk.Scrollbar(med_frame, orient="vertical", command=med_tree.yview)
        med_x_scrollbar = ttk.Scrollbar(med_frame, orient="horizontal", command=med_tree.xview)
        med_tree.configure(yscrollcommand=med_y_scrollbar.set, xscrollcommand=med_x_scrollbar.set)

        # Grid layout for medications
        med_tree.grid(row=0, column=0, sticky='nsew')
        med_y_scrollbar.grid(row=0, column=1, sticky='ns')
        med_x_scrollbar.grid(row=1, column=0, sticky='ew')

        # Insert prescription data
        for prescription in prescriptions:
            med_tree.insert('', 'end', values=(
                prescription['medication_name'],
                prescription['dosage'],
                prescription['start_date'].strftime('%m/%d/%Y'),
                prescription['end_date'].strftime('%m/%d/%Y') if prescription['end_date'] else 'Ongoing',
                prescription['side_effects']
            ))

        # Medical History frame
        history_frame = ttk.LabelFrame(main_frame, text="Medical History", padding="10", style='Login.TLabelframe')
        history_frame.grid(row=5, column=0, sticky='ew', padx=20, pady=5)
        history_frame.grid_columnconfigure(0, weight=1)

        # Medical History treeview
        history_tree = ttk.Treeview(history_frame, columns=('Date', 'Diagnosis', 'Notes'), show='headings', height=5)

        # Configure history columns
        history_tree.column('Date', width=100, minwidth=100)
        history_tree.column('Diagnosis', width=200, minwidth=150)
        history_tree.column('Notes', width=300, minwidth=200)

        # Set history headings
        history_tree.heading('Date', text='Date')
        history_tree.heading('Diagnosis', text='Diagnosis')
        history_tree.heading('Notes', text='Notes')

        # Scroll bar for history
        history_y_scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=history_tree.yview)
        history_x_scrollbar = ttk.Scrollbar(history_frame, orient="horizontal", command=history_tree.xview)
        history_tree.configure(yscrollcommand=history_y_scrollbar.set, xscrollcommand=history_x_scrollbar.set)

        # Grid layout for history
        history_tree.grid(row=0, column=0, sticky='nsew')
        history_y_scrollbar.grid(row=0, column=1, sticky='ns')
        history_x_scrollbar.grid(row=1, column=0, sticky='ew')

        # Insert history data
        for record in medical_history:
            history_tree.insert('', 'end', values=(
                record['treatment_date'].strftime('%m/%d/%Y'),
                record['diagnosis'] or 'No diagnosis',
                record['notes']
            ))

        # Appointment Notes Frame
        encounter_frame = ttk.LabelFrame(main_frame, text="Appointment Notes", padding="10", style='Login.TLabelframe')
        encounter_frame.grid(row=6, column=0, sticky='ew', padx=20, pady=5)

        ttk.Label(encounter_frame, text="Diagnosis:", font=('Verdana', 11, 'bold')).grid(row=0, column=0, sticky='w',
                                                                                         padx=5, pady=2)
        diagnosis = ttk.Entry(encounter_frame, width=80, font=('Verdana', 11))
        diagnosis.grid(row=1, column=0, sticky='ew', padx=5, pady=2)

        ttk.Label(encounter_frame, text="Notes:", font=('Verdana', 11, 'bold')).grid(row=2, column=0, sticky='w',
                                                                                     padx=5, pady=2)
        notes = tk.Text(encounter_frame, height=4, width=80, font=('Verdana', 11))
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
            self.show_encounter_confirmation(encounter_data, healthcare_id)

        # Button Frame
        button_frame = ttk.Frame(main_frame, style='Custom.TFrame')
        button_frame.grid(row=7, column=0, pady=20)

        tk.Button(button_frame, text="Next", command=submit, width=15, **self.button_style).grid(row=0, column=0,
                                                                                                 padx=10)
        tk.Button(button_frame, text="Back",
                  command=lambda: self.view_appointments_professional(healthcare_id),
                  width=15,
                  **self.button_style).grid(row=0, column=1, padx=10)

    # Encounter confirmation and payment
    def show_encounter_confirmation(self, encounter_data, healthcare_id):
        self.clear_window()
        self.root.geometry("900x800")

        main_frame = ttk.Frame(self.root, padding="20", style='Custom.TFrame')
        main_frame.grid(row=0, column=0, sticky='nsew')

        # Title
        ttk.Label(main_frame,
                  text="Encounter Summary",
                  font=('Verdana', 16, 'bold')).grid(row=0, column=0, pady=(0, 20))

        # Summary frame
        summary_frame = ttk.LabelFrame(main_frame, text="Encounter Details", padding="10", style='Login.TLabelframe')
        summary_frame.grid(row=1, column=0, sticky='ew', padx=10, pady=5)

        # Display encounter details
        ttk.Label(summary_frame, text="Diagnosis:", font=('Verdana', 11, 'bold')).grid(row=0, column=0, sticky='w',
                                                                                       pady=5)
        ttk.Label(summary_frame, text=encounter_data['diagnosis'], wraplength=500, font=('Verdana', 11)).grid(row=0,
                                                                                                              column=1,
                                                                                                              sticky='w',
                                                                                                              pady=5)

        ttk.Label(summary_frame, text="Notes:", font=('Verdana', 11, 'bold')).grid(row=1, column=0, sticky='w', pady=5)
        ttk.Label(summary_frame, text=encounter_data['notes'], wraplength=500, font=('Verdana', 11)).grid(row=1,
                                                                                                          column=1,
                                                                                                          sticky='w',
                                                                                                          pady=5)

        # Billing frame
        billing_frame = ttk.LabelFrame(main_frame, text="Billing Information", padding="10", style='Login.TLabelframe')
        billing_frame.grid(row=2, column=0, sticky='ew', padx=10, pady=20)

        ttk.Label(billing_frame, text="Visit Amount:", font=('Verdana', 11, 'bold')).grid(row=0, column=0, sticky='e',
                                                                                          pady=5)
        amount_entry = ttk.Entry(billing_frame, font=('Verdana', 11))
        amount_entry.grid(row=0, column=1, sticky='w', pady=5)
        amount_entry.insert(0, "0.00")

        total_cost_label = ttk.Label(billing_frame, text="Total Cost: $0.00", font=('Verdana', 11, 'bold'))
        total_cost_label.grid(row=2, column=0, columnspan=2, sticky='w', pady=5)

        # Medication frame
        med_frame = ttk.LabelFrame(main_frame, text="Prescribe Medication", padding="10", style='Login.TLabelframe')
        med_frame.grid(row=3, column=0, sticky='ew', padx=10, pady=5)

        # Get list of medications with their costs
        medications = self.db.get_medications()
        medication_names = {med['medication_name']: {'id': med['medication_id'], 'cost': med['cost']} for med in
                            medications}

        # Left side -> Medication info
        med_info_frame = ttk.Frame(med_frame, style='Custom.TFrame')
        med_info_frame.grid(row=0, column=0, padx=5)

        ttk.Label(med_info_frame, text="Medication:", font=('Verdana', 11, 'bold')).grid(row=0, column=0, sticky='e',
                                                                                         pady=5)
        med_name = ttk.Combobox(med_info_frame, values=list(medication_names.keys()), font=('Verdana', 11))
        med_name.grid(row=0, column=1, sticky='w', pady=5)

        ttk.Label(med_info_frame, text="Dosage:", font=('Verdana', 11, 'bold')).grid(row=1, column=0, sticky='e',
                                                                                     pady=5)
        med_dosage = ttk.Entry(med_info_frame, font=('Verdana', 11))
        med_dosage.grid(row=1, column=1, sticky='w', pady=5)

        ttk.Label(med_info_frame, text="Cost:", font=('Verdana', 11, 'bold')).grid(row=2, column=0, sticky='e', pady=5)
        med_cost_label = ttk.Label(med_info_frame, text="$0.00", font=('Verdana', 11))
        med_cost_label.grid(row=2, column=1, sticky='w', pady=5)

        # Right side -> Dates
        med_dates_frame = ttk.Frame(med_frame, style='Custom.TFrame')
        med_dates_frame.grid(row=0, column=1, padx=5)

        ttk.Label(med_dates_frame, text="Start Date:", font=('Verdana', 11, 'bold')).grid(row=0, column=0, sticky='e',
                                                                                          pady=5)
        start_date = DateEntry(med_dates_frame,
                               width=12,
                               background='#dae8f5',
                               foreground='white',
                               borderwidth=2,
                               date_pattern='mm/dd/yyyy',
                               font=('Verdana', 11))
        start_date.grid(row=0, column=1, sticky='w', pady=5)

        ttk.Label(med_dates_frame, text="End Date:", font=('Verdana', 11, 'bold')).grid(row=1, column=0, sticky='e',
                                                                                        pady=5)
        end_date = DateEntry(med_dates_frame,
                             width=12,
                             background='#dae8f5',
                             foreground='white',
                             borderwidth=2,
                             date_pattern='mm/dd/yyyy',
                             font=('Verdana', 11))
        end_date.grid(row=1, column=1, sticky='w', pady=5)

        # Add cost of medication to visit cost
        def calculate_total_cost():
            visit_amount = float(amount_entry.get() or 0)
            med_cost = 0
            if med_name.get().strip():
                med_cost = float(medication_names[med_name.get()]['cost'])
            return visit_amount + med_cost

        # Update the cost
        def update_cost(*args):
            try:
                selected_med = med_name.get()
                visit_amount = float(amount_entry.get() or 0)

                if selected_med:
                    med_cost = float(medication_names[selected_med]['cost'])
                    med_cost_label.config(text=f"${med_cost:.2f}")
                    total_cost = visit_amount + med_cost
                    total_cost_label.config(text=f"Total Cost: ${total_cost:.2f}")
                else:
                    med_cost_label.config(text="$0.00")
                    total_cost_label.config(text=f"Total Cost: ${visit_amount:.2f}")
            except ValueError:
                pass

        # Bind cost updates
        med_name.bind('<<ComboboxSelected>>', update_cost)
        amount_entry.bind('<KeyRelease>', update_cost)

        # Payment frame
        payment_frame = ttk.LabelFrame(main_frame, text="Payment Details", padding="10", style='Login.TLabelframe')
        payment_frame.grid(row=4, column=0, sticky='ew', padx=10, pady=5)
        payment_frame.grid_remove()

        ttk.Label(payment_frame, text="Payment Amount:", font=('Verdana', 11, 'bold')).grid(row=0, column=0, sticky='w',
                                                                                            pady=5)
        payment_entry = ttk.Entry(payment_frame, width=20, font=('Verdana', 11))
        payment_entry.grid(row=0, column=1, sticky='w', pady=5)

        def show_payment():
            payment_frame.grid()
            process_payment_btn.grid()
            submit_bill_btn.grid_remove()
            # Sets initial payment amount to total cost
            total = calculate_total_cost()
            payment_entry.delete(0, tk.END)
            payment_entry.insert(0, f"{total:.2f}")

        # Save encounter/appointment data
        def save_encounter_data():
            if encounter_data['notes'].strip() or encounter_data.get('diagnosis'):
                self.db.add_medical_history(
                    encounter_data['patient_id'],
                    encounter_data['healthcare_id'],
                    encounter_data.get('diagnosis', ''),
                    encounter_data['notes']
                )

            if med_name.get().strip():
                self.db.add_prescription(
                    encounter_data['patient_id'],
                    medication_names[med_name.get()]['id'],
                    med_dosage.get(),
                    start_date.get_date(),
                    end_date.get_date(),
                    encounter_data['healthcare_id']
                )

        # Process the payment & delete the appointment
        def process_payment():
            try:
                total_amount = calculate_total_cost()
                payment_amount = float(payment_entry.get())

                if payment_amount <= 0:
                    messagebox.showerror("Error", "Please enter a valid amount greater than 0")
                    return
                if payment_amount > total_amount:
                    messagebox.showerror("Error", "Payment amount cannot exceed bill amount")
                    return

                save_encounter_data()
                bill_id = self.db.create_bill(
                    encounter_data['patient_id'],
                    encounter_data['appointment_id'],
                    total_amount
                )

                self.db.process_payment(bill_id, payment_amount)
                self.db.mark_appointment_completed(encounter_data['appointment_id'])
                remaining = total_amount - payment_amount

                if remaining > 0:
                    messagebox.showinfo("Success",
                                        f"Payment processed successfully\nRemaining balance: ${remaining:.2f}")
                else:
                    messagebox.showinfo("Success", "Payment processed successfully\nBill paid in full")

                self.professional_portal(healthcare_id)

            except ValueError:
                messagebox.showerror("Error", "Please enter valid payment amount")

        # Continue without making a payment, delete appointment
        def submit_without_payment():
            try:
                total_amount = calculate_total_cost()
                save_encounter_data()
                self.db.create_bill(
                    encounter_data['patient_id'],
                    encounter_data['appointment_id'],
                    total_amount
                )
                self.db.mark_appointment_completed(encounter_data['appointment_id'])

                messagebox.showinfo("Success", "Encounter saved and bill generated.\nPayment can be processed later.")
                self.professional_portal(healthcare_id)
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid bill amount")

        # Button frame
        button_frame = ttk.Frame(main_frame, style='Custom.TFrame')
        button_frame.grid(row=5, column=0, pady=20)

        submit_bill_btn = tk.Button(button_frame,
                                    text="Submit and Generate Bill",
                                    command=show_payment,
                                    **self.button_style)
        submit_bill_btn.grid(row=0, column=0, padx=10)

        process_payment_btn = tk.Button(button_frame,
                                        text="Process Payment",
                                        command=process_payment,
                                        **self.button_style)
        process_payment_btn.grid(row=0, column=1, padx=10)
        process_payment_btn.grid_remove()

        tk.Button(button_frame,
                  text="Submit without Payment",
                  command=submit_without_payment,
                  **self.button_style).grid(row=0, column=2, padx=10)

        tk.Button(button_frame,
                  text="Cancel",
                  command=lambda: [self.professional_portal(healthcare_id)],
                  **self.button_style).grid(row=0, column=3, padx=10)

    # Professional side way to look up appointments
    def search_appointments_professional(self, healthcare_id):
        self.clear_window()
        self.root.geometry("950x900")

        main_frame = ttk.Frame(self.root, padding="20", style='Custom.TFrame')
        main_frame.grid(row=0, column=0, sticky='nsew')

        # Logo and Title
        self._add_logo(main_frame)
        ttk.Label(main_frame,
                  text="Search Appointments",
                  font=('Verdana', 20, 'bold')).grid(row=1, column=0, pady=(0, 20))

        # Search Frame
        search_frame = ttk.LabelFrame(main_frame, text="Search Criteria", padding="10", style='Login.TLabelframe')
        search_frame.grid(row=2, column=0, sticky='ew', padx=20, pady=5)

        # Professional search
        ttk.Label(search_frame, text="Healthcare Professional ID:").grid(row=0, column=0, padx=5, pady=5)
        prof_id_entry = ttk.Entry(search_frame, width=20)
        prof_id_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(search_frame, text="OR").grid(row=1, column=0, columnspan=4, pady=5)

        ttk.Label(search_frame, text="Professional First Name:").grid(row=2, column=0, padx=5, pady=5)
        prof_fname_entry = ttk.Entry(search_frame, width=20)
        prof_fname_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(search_frame, text="Professional Last Name:").grid(row=2, column=2, padx=5, pady=5)
        prof_lname_entry = ttk.Entry(search_frame, width=20)
        prof_lname_entry.grid(row=2, column=3, padx=5, pady=5)

        ttk.Label(search_frame, text="OR").grid(row=3, column=0, columnspan=4, pady=5)

        # Patient Search
        ttk.Label(search_frame, text="Patient ID:").grid(row=4, column=0, padx=5, pady=5)
        patient_id_entry = ttk.Entry(search_frame, width=20)
        patient_id_entry.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(search_frame, text="OR").grid(row=5, column=0, columnspan=4, pady=5)

        ttk.Label(search_frame, text="Patient First Name:").grid(row=6, column=0, padx=5, pady=5)
        patient_fname_entry = ttk.Entry(search_frame, width=20)
        patient_fname_entry.grid(row=6, column=1, padx=5, pady=5)

        ttk.Label(search_frame, text="Patient Last Name:").grid(row=6, column=2, padx=5, pady=5)
        patient_lname_entry = ttk.Entry(search_frame, width=20)
        patient_lname_entry.grid(row=6, column=3, padx=5, pady=5)

        # Results Frame
        results_frame = ttk.LabelFrame(main_frame, text="Search Results", padding="10", style='Login.TLabelframe')
        results_frame.grid(row=3, column=0, sticky='nsew', padx=20, pady=5)
        results_frame.grid_columnconfigure(0, weight=1)

        # Treeview for appointments
        columns = {
            'ID': {'width': 70, 'stretch': False},
            'Date': {'width': 100, 'stretch': True},
            'Time': {'width': 100, 'stretch': True},
            'Professional': {'width': 150, 'stretch': True},
            'Patient': {'width': 150, 'stretch': True},
            'Type': {'width': 120, 'stretch': True},
            'Notes': {'width': 200, 'stretch': True}
        }

        tree = ttk.Treeview(results_frame, columns=list(columns.keys()), show='headings', height=10)

        # Configure columns
        for col, settings in columns.items():
            tree.heading(col, text=col, anchor='w')
            tree.column(col, width=settings['width'], stretch=settings['stretch'])

        # Add scrollbars
        y_scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=tree.yview)
        x_scrollbar = ttk.Scrollbar(results_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

        tree.grid(row=0, column=0, sticky='nsew')
        y_scrollbar.grid(row=0, column=1, sticky='ns')
        x_scrollbar.grid(row=1, column=0, sticky='ew')

        def search_appointments():
            for item in tree.get_children():
                tree.delete(item)

            # Get search criteria
            prof_id = prof_id_entry.get().strip()
            prof_fname = prof_fname_entry.get().strip()
            prof_lname = prof_lname_entry.get().strip()
            patient_id = patient_id_entry.get().strip()
            patient_fname = patient_fname_entry.get().strip()
            patient_lname = patient_lname_entry.get().strip()

            try:
                if not any([prof_id, prof_fname, prof_lname, patient_id, patient_fname, patient_lname]):
                    messagebox.showwarning("Invalid Search", "Please enter at least one search criteria")
                    return

                # Get appointments based on search criteria
                appointments = self.db.search_appointments(
                    prof_id=prof_id,
                    prof_fname=prof_fname,
                    prof_lname=prof_lname,
                    patient_id=patient_id,
                    patient_fname=patient_fname,
                    patient_lname=patient_lname
                )

                for appt in appointments:
                    tree.insert('', 'end', values=(
                        appt['appointment_id'],
                        appt['appointment_date'].strftime('%m/%d/%Y'),
                        appt['appointment_time'],
                        f"{appt['professional_first_name']} {appt['professional_last_name']}",
                        f"{appt['patient_first_name']} {appt['patient_last_name']}",
                        appt['visit_type'],
                        appt['appointment_notes'] if appt['appointment_notes'] else 'N/A'
                    ))

                if not appointments:
                    messagebox.showinfo("No Results", "No appointments found matching search criteria")

            except Exception as e:
                messagebox.showerror("Error", f"Search failed: {str(e)}")

        def cancel_appointment():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select an appointment to cancel")
                return

            if messagebox.askyesno("Confirm Cancellation", "Are you sure you want to cancel this appointment?"):
                try:
                    appointment_id = tree.item(selected[0])['values'][0]
                    if self.db.delete_appointment(appointment_id):
                        messagebox.showinfo("Success", "Appointment cancelled successfully!")
                        search_appointments()  # Refresh the results
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to cancel appointment: {str(e)}")

        # Button Frame
        button_frame = ttk.Frame(main_frame, style='Custom.TFrame')
        button_frame.grid(row=4, column=0, pady=20)

        buttons = [
            ("Search", search_appointments, 15),
            ("Cancel Selected", cancel_appointment, 15),
            ("Back", lambda: self.appointments_professional(healthcare_id), 10)
        ]

        for i, (text, command, width) in enumerate(buttons):
            tk.Button(button_frame,
                      text=text,
                      command=command,
                      width=width,
                      **self.button_style).grid(row=0, column=i, padx=10)

    # Professional Side view to schedule appointments w/ any professional
    def schedule_appointments_for_professional(self, healthcare_id):
        self.clear_window()
        self.root.geometry("900x900")

        main_frame = ttk.Frame(self.root, padding="20", style='Custom.TFrame')
        main_frame.grid(row=0, column=0, sticky='nsew')

        # Header
        self._add_logo(main_frame)
        ttk.Label(main_frame,
                  text="Schedule New Appointment",
                  font=('Verdana', 20, 'bold')).grid(row=1, column=0, pady=(0, 20))

        # Search Frame
        search_frame = ttk.LabelFrame(main_frame, text="Search Patient", padding="10", style='Login.TLabelframe')
        search_frame.grid(row=2, column=0, sticky='ew', padx=20, pady=5)

        # Search by ID
        ttk.Label(search_frame, text="Patient ID:").grid(row=0, column=0, padx=5, pady=5)
        id_entry = ttk.Entry(search_frame, width=20)
        id_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(search_frame, text="OR").grid(row=1, column=0, columnspan=4, pady=5)

        # Search by Name
        ttk.Label(search_frame, text="First Name:").grid(row=2, column=0, padx=5, pady=5)
        fname_entry = ttk.Entry(search_frame, width=20)
        fname_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(search_frame, text="Last Name:").grid(row=2, column=2, padx=5, pady=5)
        lname_entry = ttk.Entry(search_frame, width=20)
        lname_entry.grid(row=2, column=3, padx=5, pady=5)

        # Results Frame
        results_frame = ttk.LabelFrame(main_frame, text="Search Results", padding="10", style='Login.TLabelframe')
        results_frame.grid(row=3, column=0, sticky='nsew', padx=20, pady=5)
        results_frame.grid_columnconfigure(0, weight=1)

        # Treeview for patient data
        tree = ttk.Treeview(results_frame,
                            columns=('ID', 'First Name', 'Last Name', 'DOB', 'Gender', 'Phone'),
                            show='headings',
                            height=5)

        # Configure columns
        tree.column('ID', width=80)
        tree.column('First Name', width=120)
        tree.column('Last Name', width=120)
        tree.column('DOB', width=100)
        tree.column('Gender', width=80)
        tree.column('Phone', width=120)

        for col in tree['columns']:
            tree.heading(col, text=col)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')

        # Appointment Form Frame
        appointment_frame = ttk.LabelFrame(main_frame, text="Appointment Details", padding="10",
                                           style='Login.TLabelframe')
        appointment_frame.grid(row=4, column=0, sticky='ew', padx=20, pady=5)
        appointment_frame.grid_remove()

        def search_patients():
            for item in tree.get_children():
                tree.delete(item)

            patient_id = id_entry.get().strip()
            first_name = fname_entry.get().strip()
            last_name = lname_entry.get().strip()

            try:
                if patient_id:
                    results = self.db.search_patients(patient_id=patient_id)
                elif first_name and last_name:
                    results = self.db.search_patients(first_name=first_name, last_name=last_name)
                else:
                    messagebox.showwarning("Invalid Search",
                                           "Please enter either a Patient ID or both First and Last Name")
                    return

                for patient in results:
                    tree.insert('', 'end', values=(
                        patient['patient_id'],
                        patient['first_name'],
                        patient['last_name'],
                        patient['birth_date'].strftime('%m/%d/%Y'),
                        patient['gender'],
                        patient['phone_number']
                    ))

                if not results:
                    messagebox.showinfo("No Results", "No patients found matching search criteria")
                else:
                    appointment_frame.grid()  # Show appointment form when results found

            except Exception as e:
                messagebox.showerror("Error", f"Search failed: {str(e)}")

        # Search button
        tk.Button(search_frame,
                  text="Search",
                  command=search_patients,
                  width=15,
                  **self.button_style).grid(row=3, column=1, columnspan=2, pady=15)

        # Appointment Form Fields
        ttk.Label(appointment_frame, text="Appointment Type:").grid(row=0, column=0, pady=5, sticky='w')
        appointment_types = [
            'Regular Checkup - General health examination',
            'Follow-up - Review previous visit',
            'Consultation - Specific health concern',
            'Vaccination - Immunization services'
        ]
        type_var = tk.StringVar()
        type_dropdown = ttk.Combobox(appointment_frame, textvariable=type_var, values=appointment_types, width=40)
        type_dropdown.grid(row=0, column=1, pady=5)
        type_dropdown.set("Select Type of Appointment")

        # Date Selection
        ttk.Label(appointment_frame, text="Select Date:").grid(row=1, column=0, pady=5, sticky='w')
        current_date = datetime.now()
        min_date = current_date
        max_date = current_date + timedelta(days=365)

        date_cal = DateEntry(appointment_frame,
                             width=37,
                             background='#dae8f5',
                             foreground='white',
                             borderwidth=2,
                             date_pattern='mm/dd/yyyy',
                             mindate=min_date,
                             maxdate=max_date)
        date_cal.grid(row=1, column=1, pady=5)
        date_cal.set_date(current_date)

        # Time Selection
        ttk.Label(appointment_frame, text="Select Time:").grid(row=2, column=0, pady=5, sticky='w')
        time_var = tk.StringVar()
        time_dropdown = ttk.Combobox(
            appointment_frame,
            textvariable=time_var,
            width=37,
            state='readonly'
        )
        time_dropdown.grid(row=2, column=1, pady=5)
        time_dropdown.set("Select Available Time Slot")

        # Update time slots w/ those available
        def update_available_times(*args):
            selected_date = date_cal.get_date()
            available_times = self.db.get_professional_available_slots(healthcare_id, selected_date)

            if not available_times:
                time_dropdown['values'] = ['No available time slots']
                time_dropdown.set('No available time slots')
            else:
                time_dropdown['values'] = available_times
                time_dropdown.set("Select Available Time Slot")

        # Bind date selection to update time slots
        date_cal.bind('<<DateEntrySelected>>', update_available_times)

        # Notes
        ttk.Label(appointment_frame, text="Notes:").grid(row=3, column=0, pady=5, sticky='w')
        notes_text = tk.Text(appointment_frame, height=3, width=40)
        notes_text.grid(row=3, column=1, pady=5)

        def schedule_appointment():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select a patient")
                return

            patient_id = tree.item(selected[0])['values'][0]

            if type_var.get() == "Select Type of Appointment" or time_var.get() == "Select Available Time Slot":
                messagebox.showerror("Error", "Please fill in all required fields")
                return

            # Validate availability
            selected_date = date_cal.get_date()
            selected_time = time_var.get()

            try:
                if not self.db.validate_appointment_time(healthcare_id, selected_date, selected_time):
                    messagebox.showerror("Error", "This time slot is not available")
                    return

                if self.db.check_existing_appointment(healthcare_id, selected_date, selected_time):
                    messagebox.showerror("Error", "This time slot is already booked")
                    return

                notes = notes_text.get("1.0", tk.END).strip()
                success = self.db.submit_appointment(
                    type_var.get().split(' - ')[0],
                    selected_date,
                    selected_time,
                    healthcare_id,
                    notes,
                    patient_id
                )

                if success:
                    messagebox.showinfo("Success", "Appointment scheduled successfully!")
                    self.appointments_professional(healthcare_id)

            except Exception as e:
                messagebox.showerror("Error", f"Failed to schedule appointment: {str(e)}")

        # Button Frame
        button_frame = ttk.Frame(main_frame, style='Custom.TFrame')
        button_frame.grid(row=5, column=0, pady=20)

        buttons = [
            ("Schedule Appointment", schedule_appointment),
            ("Back", lambda: self.appointments_professional(healthcare_id))
        ]

        for i, (text, command) in enumerate(buttons):
            tk.Button(button_frame,
                      text=text,
                      command=command,
                      width=20,
                      **self.button_style).grid(row=0, column=i, padx=10)

    # Allows professional to add a patient, generates and ID and password for new patient
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

    # Search for a specific patient
    def search_patient(self, healthcare_id):
        self.clear_window()
        self.root.geometry("900x900")

        main_frame = ttk.Frame(self.root, padding="20", style='Custom.TFrame')
        main_frame.grid(row=0, column=0, sticky='nsew')
        main_frame.grid_columnconfigure(0, weight=1)

        # Logo and Title
        self._add_logo(main_frame)
        ttk.Label(main_frame, text="Patient Search", font=('Verdana', 20, 'bold')).grid(row=1, column=0, pady=(0, 20))

        # Search Frame
        search_frame = ttk.LabelFrame(main_frame, text="Search Criteria", padding="5", style='Login.TLabelframe')
        search_frame.grid(row=2, column=0, sticky='ew', padx=20, pady=5)

        # Search by ID
        ttk.Label(search_frame, text="Patient ID:").grid(row=0, column=0, padx=5, pady=5)
        id_entry = ttk.Entry(search_frame, width=20)
        id_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(search_frame, text="OR").grid(row=1, column=0, columnspan=4, pady=5)

        # Search by Name
        ttk.Label(search_frame, text="First Name:").grid(row=2, column=0, padx=5, pady=5)
        fname_entry = ttk.Entry(search_frame, width=20)
        fname_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(search_frame, text="Last Name:").grid(row=2, column=2, padx=5, pady=5)
        lname_entry = ttk.Entry(search_frame, width=20)
        lname_entry.grid(row=2, column=3, padx=5, pady=5)

        def search_patients():
            for item in tree.get_children():
                tree.delete(item)

            patient_id = id_entry.get().strip()
            first_name = fname_entry.get().strip()
            last_name = lname_entry.get().strip()

            try:
                if patient_id:
                    results = self.db.search_patients(patient_id=patient_id)
                elif first_name and last_name:
                    results = self.db.search_patients(first_name=first_name, last_name=last_name)
                else:
                    messagebox.showwarning("Invalid Search",
                                           "Please enter either a Patient ID or both First and Last Name")
                    return

                for patient in results:
                    tree.insert('', 'end', values=(
                        patient['patient_id'],
                        patient['first_name'],
                        patient['last_name'],
                        patient['birth_date'].strftime('%m/%d/%Y'),
                        patient['gender'],
                        patient['phone_number']
                    ))

                if not results:
                    messagebox.showinfo("No Results", "No patients found matching search criteria")

            except Exception as e:
                messagebox.showerror("Error", f"Search failed: {str(e)}")

        # Search button
        tk.Button(search_frame, text="Search", command=search_patients, width=15,
                  **self.button_style).grid(row=3, column=1, columnspan=2, pady=15)

        # Results Frame
        results_frame = ttk.LabelFrame(main_frame, text="Search Results", padding="10", style='Login.TLabelframe')
        results_frame.grid(row=3, column=0, sticky='nsew', padx=20, pady=5)
        results_frame.grid_columnconfigure(0, weight=1)
        results_frame.grid_rowconfigure(0, weight=1)

        # Treeview for patient info
        tree = ttk.Treeview(results_frame,
                            columns=('ID', 'First Name', 'Last Name', 'DOB', 'Gender', 'Phone'),
                            show='headings',
                            height=10)

        # Configure columns
        tree.column('ID', width=80)
        tree.column('First Name', width=120)
        tree.column('Last Name', width=120)
        tree.column('DOB', width=100)
        tree.column('Gender', width=80)
        tree.column('Phone', width=120)

        for col in tree['columns']:
            tree.heading(col, text=col)

        # Scrollbars
        y_scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=y_scrollbar.set)

        tree.grid(row=0, column=0, sticky='nsew')
        y_scrollbar.grid(row=0, column=1, sticky='ns')

        def view_medications():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select a patient")
                return
            patient_id = tree.item(selected[0])['values'][0]
            self.medications_professional(str(patient_id), healthcare_id)  # Convert to string

        def schedule_appointment():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select a patient")
                return
            patient_id = tree.item(selected[0])['values'][0]
            self.schedule_appointments_professional(str(patient_id), healthcare_id)  # Convert to string

        # Action Buttons
        button_frame = ttk.Frame(main_frame, style='Custom.TFrame')
        button_frame.grid(row=4, column=0, pady=20)

        buttons = [
            ("View Medications", view_medications),
            ("Schedule Appointment", schedule_appointment),
            ("Back", lambda: self.professional_portal(healthcare_id))
        ]

        for i, (text, command) in enumerate(buttons):
            tk.Button(button_frame,
                      text=text,
                      command=command,
                      width=15,
                      **self.button_style).grid(row=0, column=i, padx=5)

    # View medications for specific patient
    def medications_professional(self, patient_id, healthcare_id):
        self.clear_window()
        self.root.geometry("900x700")

        main_frame = ttk.Frame(self.root, padding="20", style='Custom.TFrame')
        main_frame.grid(row=0, column=0, sticky='nsew')

        # Grid configuration
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(2, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # Header
        self._add_logo(main_frame)
        patient_info = self.db.get_patient_info(patient_id)
        ttk.Label(main_frame,
                  text=f"Medications for {patient_info['first_name']} {patient_info['last_name']}",
                  font=('Verdana', 20, 'bold')).grid(row=1, column=0, pady=(0, 20))

        # Medications Frame
        med_frame = ttk.LabelFrame(main_frame, text="Current Medications", padding="10", style='Login.TLabelframe')
        med_frame.grid(row=2, column=0, sticky='nsew')
        med_frame.grid_columnconfigure(0, weight=1)


        # Treeview
        tree = ttk.Treeview(med_frame,
                            columns=('MedID', 'Medication', 'Dosage', 'Start Date', 'End Date', 'Side Effects'),
                            show='headings',
                            height=15)

        # Configure columns
        tree.column('MedID', width=0, stretch=False)  # Hidden column for medication ID
        tree.column('Medication', width=150)
        tree.column('Dosage', width=100)
        tree.column('Start Date', width=100)
        tree.column('End Date', width=100)
        tree.column('Side Effects', width=300)

        # Set headings
        tree.heading('MedID', text='MedID')
        tree.heading('Medication', text='Medication')
        tree.heading('Dosage', text='Dosage')
        tree.heading('Start Date', text='Start Date')
        tree.heading('End Date', text='End Date')
        tree.heading('Side Effects', text='Side Effects')

        # Scrollbars
        y_scrollbar = ttk.Scrollbar(med_frame, orient="vertical", command=tree.yview)
        x_scrollbar = ttk.Scrollbar(med_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

        tree.grid(row=0, column=0, sticky='nsew')
        y_scrollbar.grid(row=0, column=1, sticky='ns')
        x_scrollbar.grid(row=1, column=0, sticky='ew')

        # Display medications
        prescriptions = self.db.get_patient_prescriptions(patient_id)
        for prescription in prescriptions:
            tree.insert('', 'end', values=(
                prescription['medication_id'],  # Store medication ID in hidden column
                prescription['medication_name'],
                prescription['dosage'],
                prescription['start_date'].strftime('%m/%d/%Y'),
                prescription['end_date'].strftime('%m/%d/%Y') if prescription['end_date'] else 'Ongoing',
                prescription['side_effects']
            ))

        def cancel_medication():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select a medication to cancel")
                return

            if messagebox.askyesno("Confirm Cancellation", "Are you sure you want to cancel this medication?"):
                try:
                    values = tree.item(selected[0])['values']
                    if values and values[0]:  # Check if medication ID exists
                        medication_id = values[0]
                        self.db.cancel_prescription(patient_id, medication_id)  # Updated to use both IDs
                        messagebox.showinfo("Success", "Medication cancelled successfully")
                        self.medications_professional(patient_id, healthcare_id)
                    else:
                        messagebox.showerror("Error", "Could not find medication ID")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to cancel medication: {str(e)}")

        # Button Frame
        button_frame = ttk.Frame(main_frame, style='Custom.TFrame')
        button_frame.grid(row=3, column=0, pady=20)

        buttons = [
            ("Discontinue Medication", cancel_medication),
            ("Back", lambda: self.search_patient(healthcare_id))
        ]

        for i, (text, command) in enumerate(buttons):
            tk.Button(button_frame,
                      text=text,
                      command=command,
                      width=15,
                      **self.button_style).grid(row=0, column=i, padx=5)

    # Schedule appointments for a specific patient
    def schedule_appointments_professional(self, patient_id, healthcare_id):
        self.clear_window()
        self.root.geometry("700x800")

        main_frame = ttk.Frame(self.root, padding="20", style='Custom.TFrame')
        main_frame.grid(row=0, column=0, sticky='nsew')

        # Header
        self._add_logo(main_frame)
        patient_info = self.db.get_patient_info(patient_id)
        ttk.Label(main_frame,
                  text=f"Schedule Appointment for {patient_info['first_name']} {patient_info['last_name']}",
                  font=('Verdana', 16, 'bold')).grid(row=1, column=0, pady=(0, 20))

        # Appointment Form
        form_frame = ttk.LabelFrame(main_frame, text="Appointment Details", padding="10", style='Login.TLabelframe')
        form_frame.grid(row=2, column=0, sticky='ew', padx=20, pady=5)

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

        # Date Selection
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

        # Time Selection
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

        # Notes/comments entry
        ttk.Label(form_frame, text="Additional Notes:").grid(row=4, column=0, pady=5, sticky='w')
        notes_text = tk.Text(form_frame, height=3, width=40)
        notes_text.grid(row=4, column=1, pady=5)

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

        add_placeholder_to_text(notes_text, "Enter any concerns or conditions")

        def validate_and_submit():
            # Get notes
            notes = notes_text.get("1.0", tk.END).strip()
            if notes == "Enter any concerns or conditions":
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
                    self.search_patient(healthcare_id)

            except Exception as e:
                messagebox.showerror("Error", f"Failed to schedule appointment: {str(e)}")

        # Button frame
        button_frame = ttk.Frame(form_frame, style='Custom.TFrame')
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)

        # Add buttons
        tk.Button(button_frame,
                  text="Schedule Appointment",
                  command=validate_and_submit,
                  **self.button_style).grid(row=0, column=0, padx=10)

        tk.Button(button_frame,
                  text="Back",
                  command=lambda: self.search_patient(healthcare_id),
                  **self.button_style).grid(row=0, column=1, padx=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = HealthcareGUI(root)
    root.mainloop()