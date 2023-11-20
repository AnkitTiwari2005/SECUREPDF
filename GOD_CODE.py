import tkinter as tk
from tkinter import messagebox, filedialog
import os
import cv2

class PDFApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Secure PDF Viewer")
        self.master.geometry("300x150")  # Enlarged window size
        self.initial_password = "Hackathon"

        # Centering the window on the screen
        window_width = self.master.winfo_reqwidth()
        window_height = self.master.winfo_reqheight()
        position_right = int(self.master.winfo_screenwidth() / 2 - window_width / 2)
        position_down = int(self.master.winfo_screenheight() / 2 - window_height / 2)
        self.master.geometry("+{}+{}".format(position_right, position_down))

        self.label = tk.Label(master, text="Enter Password:")
        self.label.pack()

        self.password_entry = tk.Entry(master, show='*')
        self.password_entry.pack()

        self.open_button = tk.Button(master, text="Open PDF", command=self.start_verification)
        self.open_button.pack()

    def start_verification(self):
        entered_password = self.password_entry.get()
        if entered_password == self.initial_password:
            if messagebox.askyesno("Fingerprint Verification", "Do you want to upload fingerprint data?"):
                self.verify_fingerprint()
            else:
                self.start_face_recognition()
        else:
            messagebox.showerror("Error", "Incorrect Password.")

    def verify_fingerprint(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.tif;*.tiff")])
        if file_path:
            fingerprint_data = self.read_fingerprint_data(file_path)
            pre_fed_fingerprint_data = self.read_fingerprint_data("c:/Users/ANKIT KUMAR/OneDrive/Desktop/HACKATHON/FingerData.tif")
            if fingerprint_data == pre_fed_fingerprint_data:
                self.start_face_recognition()
            else:
                messagebox.showerror("Error", "Fingerprint data doesn't match. Access denied.")

    def read_fingerprint_data(self, file_path):
        with open(file_path, 'rb') as file:
            fingerprint_data = file.read()
        return fingerprint_data

    def start_face_recognition(self):
        pre_fed_image_path = 'c:/Users/ANKIT KUMAR/OneDrive/Pictures/Camera Roll/WIN_20231120_04_19_25_Pro.jpg'
        pre_fed_image = cv2.imread(pre_fed_image_path)
        pre_fed_image_gray = cv2.cvtColor(pre_fed_image, cv2.COLOR_BGR2GRAY)

        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        cap = cv2.VideoCapture(0)

        face_recognition_active = True

        while face_recognition_active:
            ret, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

            for (x, y, w, h) in faces:
                roi_gray = gray[y:y+h, x:x+w]

                new_face_data = cv2.resize(roi_gray, (pre_fed_image_gray.shape[1], pre_fed_image_gray.shape[0]))

                diff = cv2.absdiff(pre_fed_image_gray, new_face_data)
                diff_mean = diff.mean()

                similarity_threshold = 50

                if diff_mean < similarity_threshold:
                    cv2.putText(frame, 'Match Found', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                    pdf_path = r'c:\Users\ANKIT KUMAR\Downloads\CSI_selection_mail[1].pdf'
                    if os.path.exists(pdf_path):
                        os.system('start "" "' + pdf_path + '"')
                        face_recognition_active = False
                        break
                    else:
                        messagebox.showerror("Error", "PDF file not found.")
                else:
                    cv2.putText(frame, 'No Match', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            cv2.imshow('Face Recognition', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        self.show_result("Access Denied", "red")

    def show_result(self, message, color):
        result_label.config(text=message, fg=color)

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFApp(root)
    result_label = tk.Label(root, text="", font=("Arial", 14))
    result_label.pack(pady=20)
    root.mainloop()
