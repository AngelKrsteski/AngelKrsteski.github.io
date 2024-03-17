from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

# SQLite database file
DATABASE = 'database.db'

# Function to connect to the database
def connect_db():
    return sqlite3.connect(DATABASE)

# Create users table if it doesn't exist
def create_table():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Insert sample data into the users table
def insert_sample_data():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('user1', 'password1'))
    cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('user2', 'password2'))
    cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('angel', 'angel123'))
    conn.commit()
    conn.close()

# Route for rendering the login page
@app.route('/')
def login_page():
    return render_template('login.html')

# Route for handling the login form submission
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Connect to the database
    conn = connect_db()
    cur = conn.cursor()

    # Check if the username and password exist in the database (simplified example)
    cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cur.fetchone()

    conn.close()

    if user:
        return redirect(url_for('index'))  # Redirect to index page on successful login
    else:
        return "Login Failed"

# Route for rendering the index page
@app.route('/index')
def index():
    return render_template('index.html')

app.static_folder = 'static'

if __name__ == '__main__':
    create_table()         # Create the users table if it doesn't exist
    insert_sample_data()   # Insert sample data into the users table
    app.run(debug=False, host='0.0.0.0')


