import tkinter as tk
from frontend.gui import HealthcareGUI

def main():
    root = tk.Tk()
    app = HealthcareGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()