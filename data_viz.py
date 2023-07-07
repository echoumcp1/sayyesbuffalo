import streamlit as st
import pyodbc
import pandas as pd
import plotly.express as px

server = 'sayyesbuffalo1.database.windows.net'
database = 'sayyesbuffalo1'
username = 'echou1'
password = 'qaqsiw-Cyksyw-1nupcy'   
driver= '{ODBC Driver 17 for SQL Server}'

connection = f'DRIVER={driver};SERVER=tcp:{server};PORT=1433;DATABASE={database};UID={username};PWD={password}'
conn = pyodbc.connect(connection)
cur = conn.cursor()

cur.execute("SELECT Email FROM Application")
data = cur.fetchall()
num_applications = len(data)
num_users = len(set([email[0] for email in data]))

cur.execute("SELECT Status FROM Application WHERE Status = 1")
num_offers = len(cur.fetchall())

cur.execute("SELECT Status FROM Application WHERE Status = 0")
num_in_progress = len(cur.fetchall())

num_rejections = num_applications - num_offers - num_in_progress

st.markdown("<h1 style='text-align: center; color: white;'>Say Yes Buffalo Metrics</h1>", unsafe_allow_html=True)

st.divider()

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Number of users", num_users)

with c2:
    st.metric("Number of applications", num_applications)

with c3:
    st.metric("Number of offers", num_offers)

categories = ['In progress', 'Offers', 'Rejections']
nums = [num_in_progress, num_offers, num_rejections]
df = pd.DataFrame({"categories":categories,'vals':nums})
fig = px.pie(df, values='vals', names='categories',
                 title=f'Job placement breakdown')
st.plotly_chart(fig, use_container_width=True)


