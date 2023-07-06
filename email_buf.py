import smtplib
from email.mime.text import MIMEText

subject = "Application Follow-up"
sender = "SayYesTeam2@gmail.com"
password = "wxvajsarlasdavql"

# PASS 
body = "This is the body of the text message"
recipients = ["akvnzh@gmail.com"]

def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message sent!")


if __name__ == '__main__':
    send_email(subject, body, sender, recipients, password)