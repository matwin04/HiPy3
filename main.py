from flask import *
import sqlite3
import os
import re

# Flask Configuration
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'files'
app.config['DATABASE'] = 'HiPy.db'
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
#Edit Page
@app.route('/edit/<media_type>/<int:id>', methods=['GET', 'POST'])
def edit_metadata(media_type, id):
    conn = getDB()
    if request.method == 'POST':
        # Saving the updated metadata
        if media_type == 'music':
            title = request.form['title']
            album = request.form['album']
            artist = request.form['artist']
            track_number = request.form['track_number']
            genre = request.form['genre']
            year = request.form['year']
            conn.execute("UPDATE music SET title = ?, album = ?, artist = ?, track_number = ?, genre = ?, year = ? WHERE id = ?",
                         (title, album, artist, track_number, genre, year, id))

        elif media_type == 'tv':
            series = request.form['series']
            season = request.form['season']
            episode = request.form['episode']
            title = request.form['title']
            air_date = request.form['air_date']
            genre = request.form['genre']
            conn.execute("UPDATE tv SET series = ?, season = ?, episode = ?, title = ?, air_date = ?, genre = ? WHERE id = ?",
                         (series, season, episode, title, air_date, genre, id))

        elif media_type == 'movies':
            title = request.form['title']
            director = request.form['director']
            cast = request.form['cast']
            release_year = request.form['release_year']
            genre = request.form['genre']
            rating = request.form['rating']
            conn.execute("UPDATE movies SET title = ?, director = ?, cast = ?, release_year = ?, genre = ?, rating = ? WHERE id = ?",
                         (title, director, cast, release_year, genre, rating, id))

        conn.commit()
        conn.close()
        flash("Metadata updated successfully")
        return redirect(url_for(media_type))

    # If the request method is GET, display the current metadata in the edit form
    row = conn.execute(f"SELECT * FROM {media_type} WHERE id = ?", (id,)).fetchone()
    conn.close()
    return render_template('edit.html', media_type=media_type, id=id, row=row)
#Upload Page
@app.route('/upload', methods=['POST','GET'])
def upload_file():
    if request.method == 'POST':
        media_type = request.form.get('media_type')
        video_type = request.form.get('video_type')
        file = request.files['file']
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        conn = getDB()

        # Handle audio files
        if media_type == 'audio':
            title = request.form.get('title')
            artist = request.form.get('artist')
            album = request.form.get('album')
            track_number = request.form.get('track_number')

            artist_folder = os.path.join(app.config['UPLOAD_FOLDER'], "music", artist or "Unknown Artist")
            album_folder = os.path.join(artist_folder, album or "Unknown Album")
            os.makedirs(album_folder, exist_ok=True)

            new_filepath = os.path.join(album_folder, filename)
            os.rename(filepath, new_filepath)

            conn.execute("INSERT INTO music (title, artist, album, track_number, path) VALUES (?, ?, ?, ?, ?)",
                         (title, artist, album, track_number, new_filepath))

        # Handle movies
        elif media_type == 'video' and video_type == 'movie':
            title = request.form.get('title')
            director = request.form.get('director')
            year = request.form.get('year')
            genre = request.form.get('genre')

            movie_folder = os.path.join(app.config['UPLOAD_FOLDER'], "movies", title)
            os.makedirs(movie_folder, exist_ok=True)

            new_filepath = os.path.join(movie_folder, filename)
            os.rename(filepath, new_filepath)

            conn.execute("INSERT INTO movies (title, director, release_year, genre, path) VALUES (?, ?, ?, ?, ?)",
                         (title, director, year, genre, new_filepath))

        # Handle TV shows
        elif media_type == 'video' and video_type == 'tv_show':
            series = request.form.get('series')
            season = f"Season {request.form.get('season')}"
            episode = request.form.get('episode')
            episode_title = request.form.get('episode_title')

            series_folder = os.path.join(app.config['UPLOAD_FOLDER'], "tv", series)
            season_folder = os.path.join(series_folder, season)
            os.makedirs(season_folder, exist_ok=True)

            new_filepath = os.path.join(season_folder, filename)
            os.rename(filepath, new_filepath)

            conn.execute("INSERT INTO tv (series, season, episode, title, path) VALUES (?, ?, ?, ?, ?)",
                         (series, season, episode, episode_title, new_filepath))

        # Handle home videos
        elif media_type == 'video' and video_type == 'home_video':
            title = request.form.get('title')
            description = request.form.get('description')
            date = request.form.get('date')

            home_video_folder = os.path.join(app.config['UPLOAD_FOLDER'], "home_videos", title)
            os.makedirs(home_video_folder, exist_ok=True)

            new_filepath = os.path.join(home_video_folder, filename)
            os.rename(filepath, new_filepath)

            conn.execute("INSERT INTO home_videos (title, description, date, path) VALUES (?, ?, ?, ?)",
                         (title, description, date, new_filepath))

        conn.commit()
        conn.close()
        flash("File uploaded and metadata saved successfully")
        return redirect(url_for('index'))
    return render_template("upload.html")
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