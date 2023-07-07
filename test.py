import pyodbc
from flask import Flask, jsonify, request
from flask_cors import CORS
import datetime

server = 'sayyesbuffalo1.database.windows.net'
database = 'sayyesbuffalo1'
username = 'echou1'
password = 'Bonkers123'   
driver= '{ODBC Driver 17 for SQL Server}'

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
    email, company_id = data['Email'], data['ID']

    cur.execute("INSERT INTO Application VALUES (?, ?, ?, ?);", (email, company_id, datetime.datetime.now(), 0))
    conn.commit()

    return jsonify({'msg': 'application insertion success'})

def change_status():
    pass

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
    print(data)
    print(len(data))
    if len(data):
        return "Success", 200
    else:
        return "Failure", 400

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3001)

    