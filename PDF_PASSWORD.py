import tkinter as tk
from tkinter import messagebox
import os

class PDFApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Secure PDF Viewer")
        self.initial_password = "Hackathon"

        self.label = tk.Label(master, text="Enter Password:")
        self.label.pack()

        self.password_entry = tk.Entry(master, show='*')
        self.password_entry.pack()

        self.open_button = tk.Button(master, text="Open PDF", command=self.open_pdf)
        self.open_button.pack()

    def open_pdf(self):
        entered_password = self.password_entry.get()
        if entered_password == self.initial_password:
            pdf_path = r'c:\Users\ANKIT KUMAR\Downloads\CSI_selection_mail[1].pdf'
            if os.path.exists(pdf_path):
                os.system('start "" "' + pdf_path + '"')
            else:
                messagebox.showerror("Error", "PDF file not found.")
        else:
            messagebox.showerror("Error", "Incorrect Password.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFApp(root)
    root.mainloop()
    
