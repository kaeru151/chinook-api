from src import db
from models.genres import Genre

db.DB_PATH = r"data\chinook.db"

"""
genre = Genre.from_id(input("GenreId: "))
print(genre)
genre.update_name(input("new Name: "))
genre = Genre.from_id(input("GenreId: "))
print(genre)
"""