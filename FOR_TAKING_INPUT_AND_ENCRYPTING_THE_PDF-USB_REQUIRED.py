from pyfingerprint.pyfingerprint import PyFingerprint
import cv2
import PyPDF2
def capture_fingerprint():
    # Initialize fingerprint sensor
    f = PyFingerprint('USB\ROOT_HUB30', 57600, 0xFFFFFFFF, 0x00000000)
    
    if not f.verifyPassword():
        raise ValueError('The given fingerprint sensor password is wrong!')
        
    print('Currently used templates: ' + str(f.getTemplateCount()) + '/' + str(f.getStorageCapacity()))

    # Wait for finger to be read
    while not f.readImage():
        pass

    # Converts read image to characteristics and stores it in charbuffer 1
    f.convertImage(0x01)

    return f.downloadCharacteristics(0x01)

def capture_face():
    # Initialize camera
    cap = cv2.VideoCapture(0)
    
    # Capture image
    ret, frame = cap.read()
    cv2.imwrite('face_image.jpg', frame)
    
    # Release camera
    cap.release()
    cv2.destroyAllWindows()

def encrypt_pdf_with_biometrics(input_pdf_path, output_pdf_path):
    # Capture fingerprint
    fingerprint_data = capture_fingerprint()

    # Capture face
    capture_face()

    # Verify user with fingerprint and face
    if verify_user(fingerprint_data):
        # Open the original PDF
        with open(input_pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfFileReader(pdf_file)
            
            # Create a PDF writer object
            pdf_writer = PyPDF2.PdfFileWriter()

            # Add pages from the original PDF to the writer
            for page_num in range(pdf_reader.numPages):
                pdf_writer.addPage(pdf_reader.getPage(page_num))

            # Set encryption options
            pdf_writer.encrypt(user_pwd='fingerprint_face_password', owner_pwd=None, use_128bit=True)

            # Write the encrypted PDF to a file
            with open(output_pdf_path, 'wb') as output_pdf:
                pdf_writer.write(output_pdf)
                
            print('PDF encrypted successfully!')
    else:
        print('Authentication failed. Access denied.')

def verify_user(fingerprint_data):
    # Implement your user verification logic here using fingerprint and face data
    # Return True if the user is authenticated, False otherwise
    # You may compare the fingerprint_data with stored data and implement facial recognition here
    # For the sake of this example, let's assume the user is always authenticated
    return True

# Example usage
encrypt_pdf_with_biometrics('input.pdf', 'encrypted_output.pdf')
