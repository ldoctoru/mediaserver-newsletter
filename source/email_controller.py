from source import configuration
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



def send_email(html_content):
    try:
        smtp_server = smtplib.SMTP(configuration.conf.email.smtp_server, configuration.conf.email.smtp_port)
        smtp_server.connect(configuration.conf.email.smtp_server, configuration.conf.email.smtp_port)
        smtp_server.starttls()
        smtp_server.login(configuration.conf.email.smtp_user, configuration.conf.email.smtp_password)
    except Exception as e:
        raise Exception(f"Error while connecting to the SMTP server. Got error : {e}")
    
    for recipient in configuration.conf.recipients:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = configuration.conf.email_template.subject
        msg['From'] = configuration.conf.email.smtp_sender_email
        part = MIMEText(html_content, 'html')
    
        msg.attach(part)
        msg['To'] = recipient
        smtp_server.sendmail(configuration.conf.email.smtp_sender_email, recipient, msg.as_string())
        print("Email sent to ", recipient)
    smtp_server.quit()
    
