import smtplib
from email.mime.text import MIMEText
from flask import Flask, jsonify, request

subject = "Application Follow-up"
sender = "SayYesTeam2@gmail.com"
password = "wxvajsarlasdavql"

app = Flask(__name__)

@app.route('/send_email', methods=['POST'])
def send_email():
    msg = MIMEText("Please update us about your application to " + request.args.get("company") + "!")
    
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = request.args.get("email")
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, request.args.get("email"), msg.as_string())
    return jsonify({'msg':'email sent'})


if __name__ == '__main__':
    app.run()