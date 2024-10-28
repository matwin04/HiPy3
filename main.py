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
if __name__ == "__main__":
    createStorage()
    app.run(
        port=9000,
        debug=True,
    )