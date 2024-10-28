import os
def createStorage():
    directories = ["storage", "storage/data", "storage/music", "storage/tv", "storage/movies", "storage/photos"]
    for directory in directories:
        if not os.path.exists(directory):
            os.mkdir(directory)
    print("Done Creating Storages")

if __name__ == "__main__":
    createStorage()