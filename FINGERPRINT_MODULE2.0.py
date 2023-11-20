import tkinter as tk
from tkinter import filedialog, messagebox
import os

def read_fingerprint_data(file_path):
    with open(file_path, 'rb') as file:
        fingerprint_data = file.read()
    return fingerprint_data

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.tif;*.tiff")])
    if file_path:
        fingerprint_data = read_fingerprint_data(file_path)
        match_fingerprint(fingerprint_data)

def match_fingerprint(upload_data):
    pre_fed_fingerprint_data = read_fingerprint_data("c:/Users/ANKIT KUMAR/OneDrive/Desktop/HACKATHON/FingerData.tif")
    if upload_data == pre_fed_fingerprint_data:
        show_result("Access Granted", "green")
        open_pdf()
    else:
        show_result("Access Denied", "red")

def open_pdf():
    pdf_path = r'c:\Users\ANKIT KUMAR\Downloads\CSI_selection_mail[1].pdf'
    if os.path.exists(pdf_path):
        os.system('start "" "' + pdf_path + '"')
    else:
        messagebox.showerror("Error", "PDF file not found.")

def show_result(message, color):
    result_label.config(text=message, fg=color)

root = tk.Tk()
root.title("Fingerprint Matching")

main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

file_label = tk.Label(main_frame, text="Select Fingerprint Data (.tif)")
file_label.pack(pady=20)

select_button = tk.Button(main_frame, text="Select File", command=select_file)
select_button.pack()

result_label = tk.Label(main_frame, text="", font=("Arial", 14))
result_label.pack(pady=20)

root.mainloop()
