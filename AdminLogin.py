import tkinter as tk
from tkinter import messagebox, ttk
from mysql.connector import connect, Error

# Function to handle login
def master_login():
    username = username_entry.get()
    password = password_entry.get()

    if username == ".\\hhhdba" and password == "hhh_admin!":
        messagebox.showinfo("Login Successful", "Welcome to Hopkins Health Hub Database Admin!")
        root.destroy()  # Close the initial login window
        open_admin_dashboard()  # Open the admin dashboard
    else:
        messagebox.showerror("Login Failed", "Invalid Username or Password.")

# Function to handle record lookup
def find_record():
    selection = dropdown_var.get()
    record_id = id_entry.get()
    output_text.delete("1.0", tk.END)  # Clear previous output

    # Initialize query with a default value of None
    query = None

    if selection == "Employees":
        query = f"SELECT * FROM Healthcare_Professional WHERE healthcare_professional_id = '{record_id}'"
    elif selection == "Patients":
        query = f"SELECT * FROM Patients WHERE patient_id = '{record_id}'"

    # Check if a valid selection was made
    if query is None:
        output_text.insert(tk.END, "Please select a valid option (Employees or Patients)")
        return

    try:
        connection = connect(
            host="localhost",
            user="root",
            password="COSC578_Hopkins",
            database="hopkins_health_hub"
        )
        cursor = connection.cursor()
        cursor.execute(query)
        record = cursor.fetchone()

        if record:
            formatted_output = []
            for col, val in zip(cursor.column_names, record):
                if col == "healthprof_password" or col == "patient_password":
                    val = "*" * len(val)  # Mask the password
                formatted_output.append(f"{col}: {val}")
            output_text.insert(tk.END, "\n".join(formatted_output))
        else:
            output_text.insert(tk.END, "No record found.")
    except Error as e:
        output_text.insert(tk.END, f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Function to open the admin dashboard
def open_admin_dashboard():
    dashboard = tk.Tk()  # Create a new instance of Tk
    dashboard.title("Hopkins Health Hub - Admin Dashboard")
    dashboard.geometry("600x600")

    label = tk.Label(dashboard, text="Hopkins Health Hub Database Admin", font=("Arial", 16), fg="black")
    label.pack(pady=20)

    # Dropdown menu for selection
    global dropdown_var, id_entry, output_text
    dropdown_var = tk.StringVar(value="Select Option")
    dropdown_label = tk.Label(dashboard, text="Select Type:", font=("Arial", 12))
    dropdown_label.pack()

    dropdown_menu = ttk.Combobox(dashboard, textvariable=dropdown_var, values=["Employees", "Patients"])
    dropdown_menu.pack(pady=5)

    # ID Entry
    id_label = tk.Label(dashboard, text="ID:", font=("Arial", 12))
    id_label.pack(pady=(10, 0))

    id_entry = tk.Entry(dashboard, font=("Arial", 12), width=30)
    id_entry.pack(pady=5)

    # Find Now Button
    find_button = tk.Button(
        dashboard,
        text="Find Now",
        command=find_record,
        font=("Arial", 12, "bold"),
        bg="#007ACC",
        fg="white",
        width=15
    )
    find_button.pack(pady=10)

    # Reset Password Button
    reset_button = tk.Button(
        dashboard,
        text="Reset Password",
        command=reset_password_window,
        font=("Arial", 12, "bold"),
        bg="#FF5733",  # Orange button color
        fg="white",
        width=15
    )
    reset_button.pack(pady=10)

    # Output Text Box
    output_text = tk.Text(dashboard, height=15, width=70, font=("Arial", 10))
    output_text.pack(pady=10)

    dashboard.mainloop()

# Function to open reset password window
def reset_password_window():
    reset_window = tk.Toplevel()
    reset_window.title("Reset Password")
    reset_window.geometry("400x300")

    tk.Label(reset_window, text="Enter New Password:", font=("Arial", 12)).pack(pady=(20, 0))
    new_password_entry = tk.Entry(reset_window, font=("Arial", 12), show="*", width=30)
    new_password_entry.pack(pady=5)

    tk.Label(reset_window, text="Confirm Password:", font=("Arial", 12)).pack(pady=(20, 0))
    confirm_password_entry = tk.Entry(reset_window, font=("Arial", 12), show="*", width=30)
    confirm_password_entry.pack(pady=5)

    def reset_password():
        new_password = new_password_entry.get()
        confirm_password = confirm_password_entry.get()

        if new_password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return

        if not is_password_valid(new_password):
            messagebox.showerror("Error", "Password doesn't adhere to policy:\n- At least 8 characters\n- Includes uppercase, lowercase, number, and symbol")
            return

        try:
            connection = connect(
                host="localhost",
                user="root",
                password="COSC578_Hopkins",
                database="hopkins_health_hub"
            )
            cursor = connection.cursor()
            user_id = id_entry.get()
            update_query = f"UPDATE Healthcare_Professional SET healthprof_password = '{new_password}' WHERE healthcare_professional_id = '{user_id}'"
            cursor.execute(update_query)
            connection.commit()
            messagebox.showinfo("Success", "Password successfully changed!")
            reset_window.destroy()
        except Error as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    reset_button = tk.Button(
        reset_window,
        text="Reset Password",
        command=reset_password,
        font=("Arial", 12, "bold"),
        bg="#007ACC",
        fg="white"
    )
    reset_button.pack(pady=20)

# Password policy validator
def is_password_valid(password):
    import re
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True

# Main Login Screen
root = tk.Tk()
root.title("Hopkins Health Hub Login")
root.geometry("400x300")
root.configure(bg="#E3F2FD")  # Light blue background to match the previous examples

# Title Label
title_label = tk.Label(
    root,
    text="Hopkins Health Hub Login",
    font=("Arial", 16, "bold"),
    fg="#007ACC",  # Blue text color
    bg="#E3F2FD"
)
title_label.pack(pady=20)

# Username Label and Entry
username_label = tk.Label(root, text="Username:", font=("Arial", 12), bg="#E3F2FD")
username_label.pack(pady=(10, 0))
username_entry = tk.Entry(root, font=("Arial", 12), width=30)
username_entry.pack(pady=5)

# Password Label and Entry
password_label = tk.Label(root, text="Password:", font=("Arial", 12), bg="#E3F2FD")
password_label.pack(pady=(10, 0))
password_entry = tk.Entry(root, show="*", font=("Arial", 12), width=30)
password_entry.pack(pady=5)

# Login Button
login_button = tk.Button(
    root,
    text="Login",
    command=master_login,
    font=("Arial", 12, "bold"),
    bg="#007ACC",  # Blue button color
    fg="white",
    width=15
)
login_button.pack(pady=20)

# Start Tkinter Mainloop
root.mainloop()