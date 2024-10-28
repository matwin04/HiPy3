import os
from flask import *
app = Flask(__name__)
def createStorage():
    directories = ["storage", "storage/data", "storage/music", "storage/tv", "storage/movies", "storage/photos"]
    for directory in directories:
        if not os.path.exists(directory):
            os.mkdir(directory)
    print("Done Creating Storages")
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    return render_template('data.html')

@app.route('/music')
def music():
    return render_template('music.html')

@app.route('/tv')
def tv():
    return render_template('tv.html')

@app.route('/movies')
def movies():
    return render_template('movies.html')

@app.route('/photos')
def photos():
    return render_template('photos.html')
if __name__ == "__main__":
    createStorage()
    app.run(
        port=9000,
        debug=True,
    )