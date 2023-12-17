from email.message import EmailMessage
import os
import smtplib
import ssl
from dotenv import load_dotenv
def sendmail(subject, html_email, email_receiver):
        load_dotenv()
        email_sender = os.getenv("EMAIL_SENDER")
        email_password = os.getenv("EMAIL_PWD")

        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        em.add_alternative(html_email, subtype='html')


        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.send_message(em)