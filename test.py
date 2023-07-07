import pyodbc
from flask import Flask, jsonify, request
from flask_cors import CORS
import datetime
import smtplib
from email.mime.text import MIMEText

server = 'sayyesbuffalo1.database.windows.net'
database = 'sayyesbuffalo1'
username = 'echou1'
password = ""
driver= '{ODBC Driver 17 for SQL Server}'

subject = "Application Follow-up"
sender = "SayYesTeam2@gmail.com"
passwd = ""

connection = f'DRIVER={driver};SERVER=tcp:{server};PORT=1433;DATABASE={database};UID={username};PWD={password}'
conn = pyodbc.connect(connection)
cur = conn.cursor()

app = Flask(__name__)
app.config["DEBUG"] = True

CORS(app)

@app.route('/')
def test():
    return "hello"

@app.route('/insert_user', methods=['POST'])
def insert_user():
    data = request.get_json()  
    first, last, email = data['Firstname'], data['Lastname'], data['Email']

    cur.execute("INSERT INTO Users VALUES (?,?,?);", (first, last, email))
    conn.commit()

    return jsonify({'msg':'user insertion success'})

@app.route('/add_app', methods=['POST'])
def insert_app():
    data = request.get_json()
    email, company_id = data['Email'], data['Job']

    cur.execute("INSERT INTO Application VALUES (?, ?, ?, ?);", (email, company_id, datetime.datetime.now(), 0))
    conn.commit()

    cur.execute(f"SELECT Name FROM Companies WHERE ID = {company_id}")
    company_name = cur.fetchone()[0]
    send_email(email, company_name)

    return jsonify({'msg': 'application insertion success'})

def send_email(receiver, company):
    msg = MIMEText("Please update us about your application to " + company + "!")
    
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, passwd)
       smtp_server.sendmail(sender, receiver, msg.as_string())


@app.route('/submit', methods=['POST'])
def change_status():
    data = request.get_json()
    email, company_id, status = data['Email'], data['ID'], data['Status']
    cur.execute(f"UPDATE Applications SET Status={status} WHERE Email = \'{email}\' AND ID = {company_id}")
    conn.commit()

    return "Update success"

@app.route('/get_companies', methods=['GET'])
def get_companies():
    cur.execute("SELECT * FROM Companies")
    data = cur.fetchall()

    return jsonify([{'company':company.Name, 
                    'link':company.URL, 
                    'title':company.Title, 
                    'job_id':company.ID,
                    'location':company.Location,
                    'tools':company.Tools} for company in data])

@app.route('/login', methods=['GET'])
def exists_email():
    email = request.args["email"]
    cur.execute(f"SELECT * FROM Users WHERE Email = \'{email}\'")
    data = cur.fetchall()
    return ("Success", 200) if len(data) != 0 else ("Failure", 400)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3001)

    