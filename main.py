from flask import *
import sqlite3
import os

# Flask Configuration
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'files'
app.config['DATABASE'] = 'classicweb.db'
app.config['SCHEMA'] = 'init.sql'
app.secret_key = 'supersecretkey'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize Database
def init_db():
    if not os.path.exists(app.config['DATABASE']):
        print("Database does not exist. Creating and initializing...")
        with sqlite3.connect(app.config['DATABASE']) as conn:
            with open(app.config['SCHEMA'], 'r') as f:
                conn.executescript(f.read())  # Execute all SQL commands from init.sql
            print("Database created and initialized successfully.")
    else:
        print("Database already exists.")

def getDB():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row  # Enable dictionary-like row access
    return conn

# Home Page
@app.route('/')
def index():
    return render_template("index.html")

# Data Page
@app.route('/data')
def data():
    conn = getDB()
    rows = conn.execute("SELECT * FROM data").fetchall()
    conn.close()
    return render_template("data.html", rows=rows)

# Music Page
@app.route('/music')
def music():
    conn = getDB()
    rows = conn.execute("SELECT * FROM music").fetchall()
    conn.close()
    return render_template("music.html", rows=rows)

# TV Page
@app.route('/tv')
def tv():
    conn = getDB()
    rows = conn.execute("SELECT * FROM tv").fetchall()
    conn.close()
    return render_template("tv.html", rows=rows)

# Movies Page
@app.route('/movies')
def movies():
    conn = getDB()
    rows = conn.execute("SELECT * FROM movies").fetchall()
    conn.close()
    return render_template("movies.html", rows=rows)

# Photos Page
@app.route('/photos')
def photos():
    conn = getDB()
    rows = conn.execute("SELECT * FROM photos").fetchall()
    conn.close()
    return render_template("photos.html", rows=rows)

# Run the application
if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5002, debug=True)