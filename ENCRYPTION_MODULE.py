import tkinter as tk
from tkinter import filedialog
from PyPDF2 import PdfReader, PdfWriter
from PIL import Image
import os

def select_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        pdf_entry.delete(0, tk.END)
        pdf_entry.insert(tk.END, file_path)

def select_image(entry):
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        entry.delete(0, tk.END)
        entry.insert(tk.END, file_path)

def encrypt_pdf():
    pdf_path = pdf_entry.get()
    password = password_entry.get()
    fingerprint_path = fingerprint_entry.get()
    pre_fed_image_path = pre_fed_image_entry.get()

    output_path = os.path.splitext(pdf_path)[0] + "_encrypted.pdf"

    pdf_writer = PdfWriter()

    with open(pdf_path, 'rb') as file:
        pdf_reader = PdfReader(file)
        num_pages = len(pdf_reader.pages)
        for page_num in range(num_pages):
            pdf_writer.add_page(pdf_reader.pages[page_num])

    pdf_writer.encrypt(password)

    with open(fingerprint_path, 'rb') as fingerprint_file:
        pdf_writer.add_attachment(fingerprint_file.read(), 'fingerprint.png')

    with open(pre_fed_image_path, 'rb') as pre_fed_image_file:
        pdf_writer.add_attachment(pre_fed_image_file.read(), 'pre_fed_image.png')

    with open(output_path, 'wb') as output_file:
        pdf_writer.write(output_file)

    tk.messagebox.showinfo("Success", f"PDF encrypted and saved as '{output_path}'")

root = tk.Tk()
root.title("PDF Encrypter")

# Labels and Entries
tk.Label(root, text="Select PDF:").pack()
pdf_entry = tk.Entry(root)
pdf_entry.pack()
tk.Button(root, text="Browse", command=select_pdf).pack()

tk.Label(root, text="Password:").pack()
password_entry = tk.Entry(root, show="*")
password_entry.pack()

tk.Label(root, text="Select Fingerprint Image:").pack()
fingerprint_entry = tk.Entry(root)
fingerprint_entry.pack()
tk.Button(root, text="Browse", command=lambda: select_image(fingerprint_entry)).pack()

tk.Label(root, text="Select Pre-fed Image:").pack()
pre_fed_image_entry = tk.Entry(root)
pre_fed_image_entry.pack()
tk.Button(root, text="Browse", command=lambda: select_image(pre_fed_image_entry)).pack()

tk.Button(root, text="Encrypt", command=encrypt_pdf).pack()

root.mainloop()
