import pyodbc
from flask import Flask, jsonify, request
import datetime

server = 'sayyesbuffalo1.database.windows.net'
database = 'sayyesbuffalo1'
username = 'echou1'
password = 'toqwyD-modpak-pigte4'   
driver= '{ODBC Driver 17 for SQL Server}'

connection = f'DRIVER={driver};SERVER=tcp:{server};PORT=1433;DATABASE={database};UID={username};PWD={password}'
conn = pyodbc.connect(connection)
cur = conn.cursor()

app = Flask(__name__)
app.debug = True

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

    cur.execute("INSERT INTO Application VALUES (?, ?, ?);", (email, company_id, datetime.datetime.now()))
    conn.commit()

    return jsonify({'msg': 'application insertion success'})

@app.route('/get_companies', methods=['GET'])
def get_companies():
    cur.execute("SELECT * FROM Companies")
    data = cur.fetchall()

    return jsonify([{'Name':company.Name, 
                    'URL':company.URL, 
                    'Title':company.Title, 
                    'ID':company.ID} for company in data])



if __name__ == '__main__':
    app.run()