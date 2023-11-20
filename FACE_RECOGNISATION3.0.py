import cv2
import os

# Path to the pre-fed image for recognition
pre_fed_image_path = 'c:/Users/ANKIT KUMAR/OneDrive/Pictures/Camera Roll/WIN_20231120_04_19_25_Pro.jpg'
pre_fed_image = cv2.imread(pre_fed_image_path)
pre_fed_image_gray = cv2.cvtColor(pre_fed_image, cv2.COLOR_BGR2GRAY)

# Path to the pre-fed PDF file
pdf_file_path = 'file:///C:/Users/ANKIT%20KUMAR/Downloads/CSI_selection_mail[1].pdf'  # Replace with the actual PDF path

# Load the face detection classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Initialize the webcam
cap = cv2.VideoCapture(0)

face_recognition_active = True

while face_recognition_active:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the video stream
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]

        # Compare the newly captured face with the pre-fed image
        new_face_data = cv2.resize(roi_gray, (pre_fed_image_gray.shape[1], pre_fed_image_gray.shape[0]))

        # Calculate the absolute difference between the faces
        diff = cv2.absdiff(pre_fed_image_gray, new_face_data)
        diff_mean = diff.mean()

        # Define a threshold for similarity
        similarity_threshold = 50  # Adjust this value according to your requirement

        # Display comparison result
        if diff_mean < similarity_threshold:
            cv2.putText(frame, 'Match Found', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            # Open the pre-fed PDF file when a match is found
            os.startfile(pdf_file_path)
            face_recognition_active = False  # Disable face recognition loop
            break  # Exit the face detection loop

        else:
            cv2.putText(frame, 'No Match', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

        # Display a rectangle around the face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    cv2.imshow('Face Recognition', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
