from src import db
from models.genres import Genre
from models.tracks import Track
from models.albums import Album
from fastapi import FastAPI

db.DB_PATH = r"data\chinook.db"
app = FastAPI()

@app.get("/")
def read_root():
    return "root"

@app.get("/genres/{genre_id}")
def read_genre(genre_id: int):
    try:
        genre = Genre.from_id(genre_id)
    except ValueError:
        return None
    else:
        return genre
    
@app.get("/tracks/{track_id}")
def read_track(track_id: int):
    try:
        track = Track.from_id(track_id)
    except ValueError:
        return None
    else:
        return track
    
@app.get("/tracks/genre_id={genre_id}")
def filter_by_genre(genre_id: int):
    try:
        genre = Genre.from_id(genre_id)
    except ValueError:
        return None
    else:
        return {
            "name": genre.name,
            "tracks": genre.get_tracks()
        }
    
@app.get("/tracks/album_id={album_id}")
def filter_by_album(album_id: int):
    try:
        album = Album.from_id(album_id)
    except ValueError:
        return None
    else:
        return {
            "name": album.title,
            "tracks": album.get_tracks()
        }