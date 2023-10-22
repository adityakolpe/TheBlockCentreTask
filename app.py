from flask import Flask, request, jsonify
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from flask_cors import CORS
import aspose.pdf as ap
import subprocess

app = Flask(__name__)
CORS(app, origins='http://localhost:3000')


@app.route('/process_data', methods=['POST','OPTIONS'])
def process_data():
    try:
        data = request.get_json()
        print(data)
        
        # Calling R script to calculate age 
        r_path = "C:\\Program Files\\R\\R-4.3.1\\bin\\x64\\Rscript"
        script_path = "C:\\Users\\kolpe\\react-windows\\my-react-app\\src\\ageScript.R"
        # Used as input arguments to the R code 
        args = [data['dateOfBirth'].split("-")[0]+data['dateOfBirth'].split("-")[1]+data['dateOfBirth'].split("-")[2]]
        # Execute command
        cmd = [r_path, script_path] + args
        # print("before subprocess")
        result = subprocess.check_output(cmd, universal_newlines=True)
        # Display result
        # print("The result is:", result, type(result))
        
        age = result
        print("age: "+age)
        
        # Determine the day of the week of birth
        # Calling R script to calculate day of the week of birth
        
        r_path = "C:\\Program Files\\R\\R-4.3.1\\bin\\x64\\Rscript"
        script_path = "C:\\Users\\kolpe\\react-windows\\my-react-app\\src\\weekdayScript.R"
        # Used as input arguments to the R code 
        
        args = [data['dateOfBirth'].split("-")[0]+data['dateOfBirth'].split("-")[1]+data['dateOfBirth'].split("-")[2]]
        # Execute command
        cmd = [r_path, script_path] + args
        # print("before subprocess")
        result = subprocess.check_output(cmd, universal_newlines=True)
        # Display result
        # print("The result is:", result, type(result))
        day_of_week = result
        print("day_of_week: "+day_of_week)
        
        # Create a PDF with the details
        document = ap.Document()

        # Add page
        page = document.pages.add()
        # Initialize textfragment object

        # Add text fragment to new page
        page.paragraphs.add(ap.text.TextFragment("Person's Name: {} {}".format(data['firstName'], data['lastName'])))
        page.paragraphs.add(ap.text.TextFragment("Age: {}".format(age)))
        page.paragraphs.add(ap.text.TextFragment("Day of the Week of Birth: {}".format(day_of_week)))
        print("paras added")
        # Save updated PDF
        document.save("output.pdf")
        print("pdf created")
        # Send the PDF as an email
        sender_email = "a....99@gmail.com"
        sender_password = ""
        recipient_email = data.get('email')
        subject = "PDF Report"
        body = "Please find the attached PDF report."
        
        msg = MIMEMultipart()                           # Used when we have attachments or want to provide alternative versions of the same content 
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        filename = "output.pdf"
        attachment = open(filename, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= " + filename)
        msg.attach(part)
        server = smtplib.SMTP('smtp.gmail.com', 587)    # Use the SMTP server of your email provider
        server.ehlo()                                   # initiates the SMTP session conversation
        server.starttls()                               # to use a secure connection
        print("Starttls")
        server.login(sender_email, sender_password)
        print("logged in")
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        print("mail sent")
        server.quit()

        return jsonify({'pdf_filename': filename, 'email_status': 'Email sent successfully','message': 'OK'})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
