import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailManager():
    def __init__(self):
        self.sender_email = "farmbnb.service@outlook.com"  # Your Outlook email
        self.sender_password = "2003cqrwarrior"  # Your Outlook password

    def send_email(self, to_email, message):
        # Create MIME multipart message
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = to_email
        msg['Subject'] = "Your farm is being stolen from you!"

        # Attach the message body
        msg.attach(MIMEText(message, 'plain'))

        # Connect to Outlook's SMTP server
        with smtplib.SMTP('smtp-mail.outlook.com', 587) as server:
            server.starttls()  # Secure the connection
            server.login(self.sender_email, self.sender_password)
            server.sendmail(self.sender_email, to_email, msg.as_string())

        print("Email has been sent!")