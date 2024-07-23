import streamlit as st
import psycopg2
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import os

# Database connection details (adjust accordingly)
# Database connection details (adjust accordingly)
DB_HOST = os.environ.get('DB_HOST', 'db')  # Get host from environment variable
DB_NAME = 'predictions'
DB_USER = 'postgres'
DB_PASSWORD = 'postgres'

# Initialize database connection
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST
)

# Create database table if it doesn't exist
def create_table():
    with conn.cursor() as cur:
        cur.execute('''
            CREATE TABLE IF NOT EXISTS predictions (
                id SERIAL PRIMARY KEY,
                subject TEXT,
                email TEXT,
                timestamp TIMESTAMP
            )
        ''')
    conn.commit()

create_table()

# Function to send email notifications (REPLACE WITH YOUR EMAIL LOGIC)
def send_notification(email, subject):
    # Replace with your email sending implementation
    print(f"Sending notification to {email}: {subject}")

# Schedule notifications
scheduler = BackgroundScheduler()
scheduler.start()

@scheduler.scheduled_job('interval', minutes=1)  # Check every minute (adjust as needed)
def check_predictions():
    with conn.cursor() as cur:
        cur.execute("SELECT email, subject FROM predictions WHERE timestamp <= NOW()")
        for row in cur:
            send_notification(*row)
            cur.execute("DELETE FROM predictions WHERE email = %s AND subject = %s", row)
    conn.commit()

# Streamlit App
st.title("Make a Prediction")

with st.form("prediction_form"):
    subject = st.text_input("Subject")
    email = st.text_input("Email")
    timestamp = st.date_input("Date and Time")

    submitted = st.form_submit_button("Submit Prediction")

    if submitted:
        if subject and email and timestamp:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO predictions (subject, email, timestamp) VALUES (%s, %s, %s)",
                    (subject, email, timestamp)
                )
            conn.commit()
            st.success("Prediction submitted!")
        else:
            st.warning("Please fill in all fields.")
