import os
import smtplib
import pythoncom
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from PyPDF2 import PdfWriter, PdfReader
from docx2pdf import convert
from datetime import datetime, timedelta

def encrypt_pdf(input_pdf_path, output_pdf_path, password):
    pdf_writer = PdfWriter()
    pdf_reader = PdfReader(input_pdf_path)

    for page_num in range(len(pdf_reader.pages)):
        pdf_writer.add_page(pdf_reader.pages[page_num])

    pdf_writer.encrypt(password)

    with open(output_pdf_path, 'wb') as pdf_output_file:
        pdf_writer.write(pdf_output_file)

def mail_pdf(input_word_path, recipient_email, email_sender, email_password, pdf_password, mail_subject):
    try:
        # Initialize COM
        pythoncom.CoInitialize()

        # Convert Word to PDF
        convert(input_word_path)
        input_pdf_path = os.path.splitext(input_word_path)[0] + '.pdf'

        # Define output PDF path
        output_pdf_path = os.path.splitext(input_word_path)[0] + '_password_protected.pdf'

        # Set a password for the PDF
        encrypt_pdf(input_pdf_path, output_pdf_path, pdf_password)

        username = email_sender
        password = email_password

        to_email = recipient_email

        subject = mail_subject
        body = "Hi,\n\nPlease find the attached statement PDF. Password of the PDF is the one which is set while generating statement. Let us know if any issues.\n\n"+"Thanks and Regrads,\nEmail: xyz.bank.35@gmail.com,\nXYZ Bank."
        msg = MIMEMultipart()
        msg['From'] = username
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
    
        # Attach the PDF to the email
        with open(output_pdf_path, 'rb') as pdf_attachment:
            pdf_part = MIMEApplication(pdf_attachment.read(), Name=os.path.basename(output_pdf_path))
            pdf_part['Content-Disposition'] = f'attachment; filename="{os.path.basename(output_pdf_path)}"'
            msg.attach(pdf_part)
    
        # Send the email
        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(username, password)
            server.sendmail(username, to_email, msg.as_string())
            server.quit()
            print('Email sent successfully with PDF attachment!')
        except Exception as e:
            print(f'Error sending email: {str(e)}')

        # Uninitialize COM
        pythoncom.CoUninitialize()

    except Exception as e:
        print(f'Error: {str(e)}')

    current_directory = os.getcwd()
    relative_folder_path = f'website/static/user_statement_files'
    folder_path = os.path.join(current_directory, relative_folder_path)  

    current_time = datetime.now()

    # Define the time threshold (60 minutes ago)
    time_threshold = current_time - timedelta(minutes=60)

    # Iterate through files in the folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        # Check if the file is a regular file and not a directory
        if os.path.isfile(file_path):
            # Get the file's creation time
            file_creation_time = datetime.fromtimestamp(os.path.getctime(file_path))
            
            # Compare the creation time with the time threshold
            if file_creation_time < time_threshold:
                # Delete the file
                os.remove(file_path)
                print(f"Deleted: {file_path}")

