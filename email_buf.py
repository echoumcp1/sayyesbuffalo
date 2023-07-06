import smtplib
from email.mime.text import MIMEText
from flask import Flask, jsonify, request

subject = "Application Follow-up"
sender = "SayYesTeam2@gmail.com"
password = "wxvajsarlasdavql"

app = Flask(__name__)

@app.route('/send_email', methods=['POST'])
def send_email():
    # from json: email, company
    data = request.get_json()  
    
    msg = MIMEText("Please update us about your application to " + data["company"] + "!")
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = [data["email"]]
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message sent!")


if __name__ == '__main__':
    app.run()