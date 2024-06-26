from src import db
from models.genres import Genre
from models.tracks import Track, get_tracks_by_name
from models.albums import Album
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn
import requests
import os
from zipfile import ZipFile

if "chinook.db" not in os.listdir("data"):
    chinook_db_url = "https://www.sqlitetutorial.net/wp-content/uploads/2018/03/chinook.zip"
    with open(r"data/chinook.zip", "wb") as file:
        file.write(requests.get(chinook_db_url).content)
    with ZipFile(r"data/chinook.zip") as zip_file:
        zip_file.extractall(r"data/")
    os.remove("data/chinook.zip")   
    print("chinook.db downloaded successfully!")

db.DB_PATH = r"data/chinook.db"
app = FastAPI()

@app.get("/", include_in_schema=False)
def read_root():
    return RedirectResponse(url="/docs")

@app.get("/genres/{genre_id}")
def read_genre(genre_id: int):
    try:
        genre = Genre.from_id(genre_id)
    except ValueError:
        return None
    else:
        return genre

@app.post("/genres/")
def insert_genre(genre: Genre):
    genre.insert_into_table()
    return {"message": "Added genre"}

@app.delete("/genres/{genre_id}")
def delete_genre(genre_id: int):
    try:
        genre = Genre.from_id(genre_id)
    except ValueError:
        return {"message": "Not successful"}
    else:
        genre.delete_from_table()
        return {"message": "Deleted genre"}


    
@app.get("/tracks/search={track_name}")
def search_track(track_name: str):
    track_name = str(track_name)
    try:
        rows = get_tracks_by_name(track_name)
    except ValueError:
        return None
    else:
        return {
            "results": len(rows),
            "tracks": rows
        }

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

@app.get("/tracks/{track_id}")
def read_track(track_id: int):
    try:
        track = Track.from_id(track_id)
    except ValueError:
        return None
    else:
        return track

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
    

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)