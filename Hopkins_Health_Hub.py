import tkinter as tk
from tkinter import messagebox, StringVar, ttk
import pymysql


def check_password(password):
    """Check the provided password by attempting to connect to the MySQL database."""
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',  # MySQL username
            password=password,  # Password to verify
            database='hopkins_health_hub_db'  # Replace with your database name
        )
        connection.close()
        return True  # Password is correct
    except pymysql.MySQLError:
        return False  # Password is incorrect


def open_main_menu():
    global main_menu
    login_window.destroy()

    main_menu = tk.Tk()
    main_menu.title("EHR Main Menu")

    tk.Label(main_menu, text="Welcome to the EHR System").pack(pady=10)

    tk.Button(main_menu, text="Add New Patient", command=open_patient_form).pack(pady=5)
    tk.Button(main_menu, text="Search Patient", command=open_search_form).pack(pady=5)
    tk.Button(main_menu, text="Create Encounter for Patient", command=open_encounter_search_form).pack(pady=5)
    tk.Button(main_menu, text="Add Bill for Patient", command=open_bill_search_form).pack(pady=5)
    tk.Button(main_menu, text="Add Appointment for Patient", command=open_appointment_search_form).pack(pady=5)

    main_menu.mainloop()


def open_login_window():
    global login_window
    login_window = tk.Tk()
    login_window.title("Login")

    tk.Label(login_window, text="Enter Password").pack(pady=10)
    password_entry = tk.Entry(login_window, show='*')
    password_entry.pack(pady=5)

    tk.Button(login_window, text="Login", command=lambda: validate_login(password_entry.get())).pack(pady=10)

    login_window.mainloop()


def validate_login(password):
    if check_password(password):
        open_main_menu()
    else:
        messagebox.showerror("Error", "Incorrect Password. Please try again.")


def open_patient_form():
    patient_form = tk.Tk()
    patient_form.title("Add New Patient")

    tk.Label(patient_form, text="Patient ID").pack(pady=5)
    patient_id_entry = tk.Entry(patient_form)
    patient_id_entry.pack(pady=5)

    tk.Label(patient_form, text="Name").pack(pady=5)
    name_entry = tk.Entry(patient_form)
    name_entry.pack(pady=5)

    tk.Label(patient_form, text="Birth Date (YYYY-MM-DD)").pack(pady=5)
    birth_date_entry = tk.Entry(patient_form)
    birth_date_entry.pack(pady=5)

    tk.Label(patient_form, text="Gender").pack(pady=5)
    gender_entry = tk.Entry(patient_form)
    gender_entry.pack(pady=5)

    tk.Label(patient_form, text="SSN").pack(pady=5)
    ssn_entry = tk.Entry(patient_form)
    ssn_entry.pack(pady=5)

    tk.Label(patient_form, text="Phone Number").pack(pady=5)
    phone_number_entry = tk.Entry(patient_form)
    phone_number_entry.pack(pady=5)

    tk.Label(patient_form, text="Zip Code").pack(pady=5)
    zip_code_entry = tk.Entry(patient_form)
    zip_code_entry.pack(pady=5)

    tk.Label(patient_form, text="Allergies").pack(pady=5)
    allergies_entry = tk.Entry(patient_form)
    allergies_entry.pack(pady=5)

    def submit_patient():
        # Retrieve data from input fields
        patient_id = patient_id_entry.get()
        name = name_entry.get()
        birth_date = birth_date_entry.get()
        gender = gender_entry.get()
        ssn = ssn_entry.get()
        phone_number = phone_number_entry.get()
        zip_code = zip_code_entry.get()
        allergies = allergies_entry.get()

        try:
            connection = pymysql.connect(
                host='localhost',
                user='root',
                password='COSC578_Hopkins',  # Replace with your actual password
                database='hopkins_health_hub_db'
            )
            with connection.cursor() as cursor:
                sql = """INSERT INTO patients 
                         (patient_id, name, birth_date, gender, ssn, phone_number, zip_code, allergies) 
                         VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
                cursor.execute(sql, (patient_id, name, birth_date, gender, ssn, phone_number, zip_code, allergies))
            connection.commit()  # Commit the changes to the database
            messagebox.showinfo("Success", "Patient added successfully!")
            if messagebox.askyesno("Create Encounter", "Would you like to create an encounter for this patient?"):
                open_encounter_form(patient_id)  # Pass the patient_id to the encounter form
        except pymysql.MySQLError as e:
            messagebox.showerror("Error", f"Error adding patient: {e}")
        finally:
            connection.close()  # Close the connection
            patient_form.destroy()

    tk.Button(patient_form, text="Submit", command=submit_patient).pack(pady=10)


def open_encounter_form(patient_id):
    encounter_form = tk.Tk()
    encounter_form.title("Create Encounter")

    tk.Label(encounter_form, text="Encounter ID (Auto-filled)").pack(pady=5)
    encounter_id_entry = tk.Entry(encounter_form)
    encounter_id_entry.pack(pady=5)
    encounter_id_entry.insert(0, f"EN{patient_id}")  # Auto-fill Encounter ID with "EN" + Patient ID

    tk.Label(encounter_form, text="Patient ID (Auto-filled)").pack(pady=5)
    patient_id_label = tk.Label(encounter_form, text=patient_id)  # Display the patient ID
    patient_id_label.pack(pady=5)

    tk.Label(encounter_form, text="Notes").pack(pady=5)
    notes_entry = tk.Entry(encounter_form)
    notes_entry.pack(pady=5)

    visit_type_var = StringVar(value="Outpatient")
    tk.Radiobutton(encounter_form, text="Inpatient", variable=visit_type_var, value="Inpatient").pack(pady=5)
    tk.Radiobutton(encounter_form, text="Outpatient", variable=visit_type_var, value="Outpatient").pack(pady=5)

    def submit_encounter():
        encounter_id = encounter_id_entry.get()
        notes = notes_entry.get()
        visit_type = visit_type_var.get()

        try:
            connection = pymysql.connect(
                host='localhost',
                user='root',
                password='COSC578_Hopkins',  # Replace with your actual password
                database='hopkins_health_hub_db'
            )
            with connection.cursor() as cursor:
                sql = """INSERT INTO encounters 
                         (encounter_id, patient_id, encounter_date, notes) 
                         VALUES (%s, %s, NOW(), %s)"""
                cursor.execute(sql, (encounter_id, patient_id, notes))
            connection.commit()  # Commit the changes to the database
            messagebox.showinfo("Success", "Encounter created successfully!")
            encounter_form.destroy()
            open_appointment_form(patient_id)  # Open appointment form after encounter submission
        except pymysql.MySQLError as e:
            messagebox.showerror("Error", f"Error creating encounter: {e}")
        finally:
            connection.close()  # Close the connection

    tk.Button(encounter_form, text="Submit", command=submit_encounter).pack(pady=10)


def open_appointment_form(patient_id):
    appointment_form = tk.Tk()
    appointment_form.title("Create Appointment")

    tk.Label(appointment_form, text="Appointment ID (Auto-filled)").pack(pady=5)
    appointment_id_entry = tk.Entry(appointment_form)
    appointment_id_entry.pack(pady=5)
    appointment_id_entry.insert(0, f"AP{patient_id}")  # Auto-fill Appointment ID with "AP" + Patient ID

    tk.Label(appointment_form, text="Select Specialty").pack(pady=5)

    # Create a frame for the scrollbar
    frame = tk.Frame(appointment_form)
    frame.pack(pady=5)

    # Create a canvas for scrolling
    canvas = tk.Canvas(frame, width=300, height=200)
    scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    specialty_frame = tk.Frame(canvas)

    # Configure the canvas
    canvas.create_window((0, 0), window=specialty_frame, anchor='nw')
    specialty_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    specialty_var = StringVar()
    specialty_buttons = []

    # Fetch specialties from the database
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='COSC578_Hopkins',  # Use the actual MySQL root password
            database='hopkins_health_hub_db'
        )
        cursor = connection.cursor()
        cursor.execute("SELECT DISTINCT specialty FROM doctors")  # Fetch distinct specialties
        specialties = cursor.fetchall()
        specialty_names = [spec[0] for spec in specialties]  # Extract names into a list

        # Create radio buttons for each specialty in the specialty_frame
        for specialty in specialty_names:
            radio_button = tk.Radiobutton(specialty_frame, text=specialty, variable=specialty_var, value=specialty,
                                           command=lambda: update_doctors(specialty))
            radio_button.pack(anchor='w')
            specialty_buttons.append(radio_button)
    except pymysql.MySQLError as e:
        messagebox.showerror("Error", f"Error fetching specialties: {e}")
        return
    finally:
        connection.close()

    tk.Label(appointment_form, text="Select Primary Care Physician").pack(pady=5)
    primary_care_physician_var = StringVar()
    primary_care_physician_dropdown = ttk.Combobox(appointment_form, textvariable=primary_care_physician_var)
    primary_care_physician_dropdown.pack(pady=5)

    def update_doctors(selected_specialty):
        if selected_specialty:
            try:
                connection = pymysql.connect(
                    host='localhost',
                    user='root',
                    password='COSC578_Hopkins',  # Replace with your actual password
                    database='hopkins_health_hub_db'
                )
                cursor = connection.cursor()
                cursor.execute("SELECT name FROM doctors WHERE specialty = %s", (selected_specialty,))
                doctors = cursor.fetchall()
                doctor_names = [doc[0] for doc in doctors]  # Extract names into a list
                primary_care_physician_dropdown['values'] = doctor_names
                primary_care_physician_var.set('')  # Clear previous selection
            except pymysql.MySQLError as e:
                messagebox.showerror("Error", f"Error fetching doctors: {e}")
            finally:
                connection.close()

    tk.Label(appointment_form, text="Visit Type").pack(pady=5)
    visit_type_entry = tk.Entry(appointment_form)
    visit_type_entry.pack(pady=5)

    tk.Label(appointment_form, text="Appointment Date (YYYY-MM-DD)").pack(pady=5)
    appointment_date_entry = tk.Entry(appointment_form)
    appointment_date_entry.pack(pady=5)

    def submit_appointment():
        appointment_id = appointment_id_entry.get()
        doctor_name = primary_care_physician_var.get()
        visit_type = visit_type_entry.get()
        appointment_date = appointment_date_entry.get()

        try:
            connection = pymysql.connect(
                host='localhost',
                user='root',
                password='COSC578_Hopkins',  # Replace with your actual password
                database='hopkins_health_hub_db'
            )
            with connection.cursor() as cursor:
                sql = """INSERT INTO appointments 
                         (appointment_id, patient_id, doctor_id, visit_type, appointment_date, primary_care_physician) 
                         VALUES (%s, %s, (SELECT doctor_id FROM doctors WHERE name = %s), %s, %s, %s)"""
                cursor.execute(sql, (appointment_id, patient_id, doctor_name, visit_type, appointment_date))
            connection.commit()  # Commit the changes to the database
            messagebox.showinfo("Success", "Appointment created successfully!")
            appointment_form.destroy()
        except pymysql.MySQLError as e:
            messagebox.showerror("Error", f"Error creating appointment: {e}")
        finally:
            connection.close()  # Close the connection

    tk.Button(appointment_form, text="Submit", command=submit_appointment).pack(pady=10)


def open_search_form():
    search_form = tk.Tk()
    search_form.title("Search Patient")

    tk.Label(search_form, text="Enter Patient ID or Name").pack(pady=5)
    search_entry = tk.Entry(search_form)
    search_entry.pack(pady=5)

    def search_patient():
        search_value = search_entry.get()
        try:
            connection = pymysql.connect(
                host='localhost',
                user='root',
                password='COSC578_Hopkins',  # Use the actual MySQL root password
                database='hopkins_health_hub_db'  # Replace with your database name
            )
            with connection.cursor() as cursor:
                sql = "SELECT * FROM patients WHERE patient_id = %s OR name LIKE %s"
                cursor.execute(sql, (search_value, '%' + search_value + '%'))
                result = cursor.fetchall()

                if result:
                    display_patient_info(result)  # Display patient info in a single window
                else:
                    messagebox.showinfo("Not Found", "No patient found with that ID or name.")
        except pymysql.MySQLError as e:
            messagebox.showerror("Error", f"Error searching for patient: {e}")
        finally:
            connection.close()

    tk.Button(search_form, text="Search", command=search_patient).pack(pady=10)

    search_form.mainloop()


def display_patient_info(patients):
    """Display patient details along with encounters, appointments, and billing info in one window."""
    patient_info_window = tk.Tk()
    patient_info_window.title("Patient Details")

    details = ""
    for row in patients:
        patient_id = row[0]
        details += f"Patient ID: {patient_id}\nName: {row[1]}\nPhone: {row[5]}\n\n"

        # Fetch additional information
        try:
            connection = pymysql.connect(
                host='localhost',
                user='root',
                password='COSC578_Hopkins',  # Use the actual MySQL root password
                database='hopkins_health_hub_db'
            )
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM encounters WHERE patient_id = %s", (patient_id,))
                encounters = cursor.fetchall()
                cursor.execute("SELECT * FROM appointments WHERE patient_id = %s", (patient_id,))
                appointments = cursor.fetchall()
                cursor.execute("SELECT * FROM billing WHERE patient_id = %s", (patient_id,))
                billing_info = cursor.fetchall()

                details += "Encounters:\n"
                details += "\n".join(
                    [f"Encounter ID: {row[0]}, Notes: {row[3]}" for row in encounters]) or "No encounters."
                details += "\n\nAppointments:\n"
                details += "\n".join([f"Appointment ID: {row[0]}, Visit Type: {row[3]}, Date: {row[4]}" for row in
                                      appointments]) or "No appointments."
                details += "\n\nBilling Info:\n"
                details += "\n".join(
                    [f"Bill ID: {row[0]}, Amount: {row[2]}, Due Date: {row[3]}, Status: {row[4]}" for row in
                     billing_info]) or "No billing info."
        except pymysql.MySQLError as e:
            messagebox.showerror("Error", f"Error fetching patient details: {e}")
        finally:
            connection.close()

    tk.Label(patient_info_window, text=details).pack(pady=10)
    tk.Button(patient_info_window, text="Close", command=patient_info_window.destroy).pack(pady=10)


def open_encounter_search_form():
    encounter_search_form = tk.Tk()
    encounter_search_form.title("Create Encounter for Patient")

    tk.Label(encounter_search_form, text="Enter Patient ID or Name").pack(pady=5)
    search_entry = tk.Entry(encounter_search_form)
    search_entry.pack(pady=5)

    def search_patient_for_encounter():
        search_value = search_entry.get()
        try:
            connection = pymysql.connect(
                host='localhost',
                user='root',
                password='COSC578_Hopkins',  # Use the actual MySQL root password
                database='hopkins_health_hub_db'  # Replace with your database name
            )
            with connection.cursor() as cursor:
                sql = "SELECT * FROM patients WHERE patient_id = %s OR name LIKE %s"
                cursor.execute(sql, (search_value, '%' + search_value + '%'))
                result = cursor.fetchall()

                if result:
                    patient_list = [f"ID: {row[0]}, Name: {row[1]}" for row in result]
                    selected_patient = StringVar()
                    selected_patient.set(patient_list[0])  # Default to first patient
                    patient_dropdown = ttk.Combobox(encounter_search_form, textvariable=selected_patient,
                                                    values=patient_list)
                    patient_dropdown.pack(pady=5)

                    def create_encounter():
                        selected = selected_patient.get().split(",")[0].split(":")[1].strip()  # Get patient ID
                        open_encounter_form_for_selected_patient(selected)

                    tk.Button(encounter_search_form, text="Create Encounter", command=create_encounter).pack(pady=10)
                else:
                    messagebox.showinfo("Not Found", "No patient found with that ID or name.")
        except pymysql.MySQLError as e:
            messagebox.showerror("Error", f"Error searching for patient: {e}")
        finally:
            connection.close()

    tk.Button(encounter_search_form, text="Search", command=search_patient_for_encounter).pack(pady=10)

    encounter_search_form.mainloop()


def open_encounter_form_for_selected_patient(patient_id):
    encounter_form = tk.Tk()
    encounter_form.title("Create Encounter")

    tk.Label(encounter_form, text="Encounter ID (Auto-filled)").pack(pady=5)
    encounter_id_entry = tk.Entry(encounter_form)
    encounter_id_entry.pack(pady=5)
    encounter_id_entry.insert(0, f"EN{patient_id}")  # Auto-fill Encounter ID with "EN" + Patient ID

    tk.Label(encounter_form, text="Patient ID (Auto-filled)").pack(pady=5)
    patient_id_label = tk.Label(encounter_form, text=patient_id)  # Display the patient ID
    patient_id_label.pack(pady=5)

    tk.Label(encounter_form, text="Notes").pack(pady=5)
    notes_entry = tk.Entry(encounter_form)
    notes_entry.pack(pady=5)

    visit_type_var = StringVar(value="Outpatient")
    tk.Radiobutton(encounter_form, text="Inpatient", variable=visit_type_var, value="Inpatient").pack(pady=5)
    tk.Radiobutton(encounter_form, text="Outpatient", variable=visit_type_var, value="Outpatient").pack(pady=5)

    def submit_encounter():
        encounter_id = encounter_id_entry.get()
        notes = notes_entry.get()
        visit_type = visit_type_var.get()

        try:
            connection = pymysql.connect(
                host='localhost',
                user='root',
                password='COSC578_Hopkins',  # Replace with your actual password
                database='hopkins_health_hub_db'
            )
            with connection.cursor() as cursor:
                sql = """INSERT INTO encounters 
                         (encounter_id, patient_id, encounter_date, notes) 
                         VALUES (%s, %s, NOW(), %s)"""
                cursor.execute(sql, (encounter_id, patient_id, notes))
            connection.commit()  # Commit the changes to the database
            messagebox.showinfo("Success", "Encounter created successfully!")
            encounter_form.destroy()
            open_appointment_form(patient_id)  # Open appointment form after encounter submission
        except pymysql.MySQLError as e:
            messagebox.showerror("Error", f"Error creating encounter: {e}")
        finally:
            connection.close()  # Close the connection

    tk.Button(encounter_form, text="Submit", command=submit_encounter).pack(pady=10)  # Add this line


def open_bill_search_form():
    bill_search_form = tk.Tk()
    bill_search_form.title("Add Bill for Patient")

    tk.Label(bill_search_form, text="Enter Patient ID or Name").pack(pady=5)
    search_entry = tk.Entry(bill_search_form)
    search_entry.pack(pady=5)

    def search_patient_for_bill():
        search_value = search_entry.get()
        try:
            connection = pymysql.connect(
                host='localhost',
                user='root',
                password='COSC578_Hopkins',  # Use the actual MySQL root password
                database='hopkins_health_hub_db'  # Replace with your database name
            )
            with connection.cursor() as cursor:
                sql = "SELECT * FROM patients WHERE patient_id = %s OR name LIKE %s"
                cursor.execute(sql, (search_value, '%' + search_value + '%'))
                result = cursor.fetchall()

                if result:
                    patient_list = [f"ID: {row[0]}, Name: {row[1]}" for row in result]
                    selected_patient = StringVar()
                    selected_patient.set(patient_list[0])  # Default to first patient
                    patient_dropdown = ttk.Combobox(bill_search_form, textvariable=selected_patient,
                                                    values=patient_list)
                    patient_dropdown.pack(pady=5)

                    def add_bill():
                        selected = selected_patient.get().split(",")[0].split(":")[1].strip()  # Get patient ID
                        open_bill_form(selected)

                    tk.Button(bill_search_form, text="Add Bill", command=add_bill).pack(pady=10)
                else:
                    messagebox.showinfo("Not Found", "No patient found with that ID or name.")
        except pymysql.MySQLError as e:
            messagebox.showerror("Error", f"Error searching for patient: {e}")
        finally:
            connection.close()

    tk.Button(bill_search_form, text="Search", command=search_patient_for_bill).pack(pady=10)

    bill_search_form.mainloop()


def open_bill_form(patient_id):
    bill_form = tk.Tk()
    bill_form.title("Add Bill")

    tk.Label(bill_form, text="Bill ID (Auto-filled)").pack(pady=5)
    bill_id_entry = tk.Entry(bill_form)
    bill_id_entry.pack(pady=5)
    bill_id_entry.insert(0, f"BL{patient_id}")  # Auto-fill Bill ID with "BL" + Patient ID

    tk.Label(bill_form, text="Amount").pack(pady=5)
    amount_entry = tk.Entry(bill_form)
    amount_entry.pack(pady=5)

    tk.Label(bill_form, text="Due Date (YYYY-MM-DD)").pack(pady=5)
    due_date_entry = tk.Entry(bill_form)
    due_date_entry.pack(pady=5)

    tk.Label(bill_form, text="Status").pack(pady=5)
    status_entry = tk.Entry(bill_form)
    status_entry.pack(pady=5)

    def submit_bill():
        bill_id = bill_id_entry.get()
        amount = amount_entry.get()
        due_date = due_date_entry.get()
        status = status_entry.get()

        try:
            connection = pymysql.connect(
                host='localhost',
                user='root',
                password='COSC578_Hopkins',  # Replace with your actual password
                database='hopkins_health_hub_db'
            )
            with connection.cursor() as cursor:
                sql = """INSERT INTO billing 
                         (bill_id, patient_id, amount, due_date, status) 
                         VALUES (%s, %s, %s, %s, %s)"""
                cursor.execute(sql, (bill_id, patient_id, amount, due_date, status))
            connection.commit()  # Commit the changes to the database
            messagebox.showinfo("Success", "Bill added successfully!")
            bill_form.destroy()
        except pymysql.MySQLError as e:
            messagebox.showerror("Error", f"Error adding bill: {e}")
        finally:
            connection.close()  # Close the connection

    # Adding the submit button for the bill form
    tk.Button(bill_form, text="Submit", command=submit_bill).pack(pady=10)


def open_appointment_search_form():
    appointment_search_form = tk.Tk()
    appointment_search_form.title("Add Appointment for Patient")

    tk.Label(appointment_search_form, text="Enter Patient ID or Name").pack(pady=5)
    search_entry = tk.Entry(appointment_search_form)
    search_entry.pack(pady=5)

    def search_patient_for_appointment():
        search_value = search_entry.get()
        try:
            connection = pymysql.connect(
                host='localhost',
                user='root',
                password='COSC578_Hopkins',  # Use the actual MySQL root password
                database='hopkins_health_hub_db'  # Replace with your database name
            )
            with connection.cursor() as cursor:
                sql = "SELECT * FROM patients WHERE patient_id = %s OR name LIKE %s"
                cursor.execute(sql, (search_value, '%' + search_value + '%'))
                result = cursor.fetchall()

                if result:
                    patient_list = [f"ID: {row[0]}, Name: {row[1]}" for row in result]
                    selected_patient = StringVar()
                    selected_patient.set(patient_list[0])  # Default to first patient
                    patient_dropdown = ttk.Combobox(appointment_search_form, textvariable=selected_patient,
                                                    values=patient_list)
                    patient_dropdown.pack(pady=5)

                    def add_appointment():
                        selected = selected_patient.get().split(",")[0].split(":")[1].strip()  # Get patient ID
                        open_appointment_form(selected)  # Pass selected patient ID here

                    tk.Button(appointment_search_form, text="Add Appointment", command=add_appointment).pack(pady=10)
                else:
                    messagebox.showinfo("Not Found", "No patient found with that ID or name.")
        except pymysql.MySQLError as e:
            messagebox.showerror("Error", f"Error searching for patient: {e}")
        finally:
            connection.close()

    tk.Button(appointment_search_form, text="Search", command=search_patient_for_appointment).pack(pady=10)

    appointment_search_form.mainloop()


if __name__ == "__main__":
    open_login_window()
