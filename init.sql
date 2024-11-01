-- Drop existing tables if they exist
DROP TABLE IF EXISTS data;
DROP TABLE IF EXISTS music;
DROP TABLE IF EXISTS tv;
DROP TABLE IF EXISTS movies;
DROP TABLE IF EXISTS photos;

-- Create tables for each folder type with detailed metadata columns

-- General files table (for miscellaneous data files)
CREATE TABLE "data" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "name" TEXT NOT NULL,
    "path" TEXT NOT NULL,
    "size" INTEGER,
    "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "modified_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "file_type" TEXT,  -- Type of file (e.g., PDF, DOCX, etc.)
    "description" TEXT -- Optional description of the file
);

-- Music table with specific metadata for music files
CREATE TABLE "music" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "name" TEXT NOT NULL,
    "path" TEXT NOT NULL,
    "size" INTEGER,
    "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "modified_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "title" TEXT,          -- Song title
    "album" TEXT,          -- Album name
    "artist" TEXT,         -- Artist name
    "track_number" INTEGER,-- Track number in the album
    "genre" TEXT,          -- Music genre
    "year" INTEGER         -- Release year
);

-- TV Shows table with specific metadata for episodes
CREATE TABLE "tv" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "name" TEXT NOT NULL,
    "path" TEXT NOT NULL,
    "size" INTEGER,
    "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "modified_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "series" TEXT,          -- Series name
    "season" INTEGER,       -- Season number
    "episode" INTEGER,      -- Episode number
    "title" TEXT,           -- Episode title
    "air_date" DATE,        -- Original air date
    "genre" TEXT            -- Genre of the series
);

-- Movies table with specific metadata for films
CREATE TABLE "movies" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "name" TEXT NOT NULL,
    "path" TEXT NOT NULL,
    "size" INTEGER,
    "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "modified_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "title" TEXT,           -- Movie title
    "director" TEXT,        -- Director's name
    "cast" TEXT,            -- Main cast members
    "release_year" INTEGER, -- Release year
    "genre" TEXT,           -- Genre
    "rating" REAL           -- Viewer rating (e.g., IMDB score)
);

-- Photos table with specific metadata for images
CREATE TABLE "photos" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "name" TEXT NOT NULL,
    "path" TEXT NOT NULL,
    "size" INTEGER,
    "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "modified_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "camera_model" TEXT,    -- Camera model used to take the photo
    "resolution" TEXT,      -- Resolution (e.g., 1920x1080)
    "location" TEXT,        -- Location where the photo was taken
    "date_taken" DATE,      -- Date the photo was taken
    "description" TEXT      -- Optional description
);