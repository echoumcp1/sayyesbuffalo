import pyodbc
from flask import Flask, jsonify, request

server = 'sayyesbuffalo1.database.windows.net'
database = 'sayyesbuffalo1'
username = 'echou1'
password = 'toqwyD-modpak-pigte4'   
driver= '{ODBC Driver 17 for SQL Server}'

connection = f'DRIVER={driver};SERVER=tcp:{server};PORT=1433;DATABASE={database};UID={username};PWD={password}'
conn = pyodbc.connect(connection)
cur = conn.cursor()

app = Flask(__name__)

@app.route('/insert_user', methods=['POST'])
def insert_user():
    data = request.get_json()  
    first, last, email = data['Firstname'], data['Lastname'], data['Email']

    cur.execute("INSERT INTO Users VALUES (?,?,?);", (first, last, email))
    conn.commit()

    return jsonify({'msg':'data insertion success'})

if __name__ == '__main__':
    app.run()
    
        
