import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime

# Email configuration
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_username = 'gilblankenship'
smtp_password = 'Pepsi2182!@#'
sender_email = 'gilblankenship@mddevelopmentcenter.com' 
recipient_email = 'gilblankenship@gmail.com'
subject = 'Daily Report'

def send_daily_report():
    # Create message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Get today's date
    today = datetime.date.today().strftime('%Y-%m-%d')

    # Email content
    body = f"Hello,\n\nHere is your daily report for {today}.\n\nBest regards,\nYour Name"
    msg.attach(MIMEText(body, 'plain'))

    # Connect to SMTP server and send email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())

if __name__ == '__main__':
    send_daily_report()
    print("Daily report email sent!")
