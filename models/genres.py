from src import db
from .tracks import Track
from .albums import Album
from .artists import Artist
from dataclasses import dataclass

@dataclass
class Genre:
    """Represents a row of table `genres`"""
    id: int
    name: str

    @classmethod
    def from_id(cls, genre_id: int):
        """Creates a `Genre` object from the provided `genre_id` if it exists
        
        Example:
            >>> Genre.from_id(1)
            Genre(id=1, name='Rock')
            >>> Genre.from_id(-1)
            ValueError: GenreId -1 does not exist!
        """
        res = db.execute_sql(
            query = "SELECT GenreId, Name FROM genres WHERE GenreId = ?;",
            params = (genre_id,) 
        )
        if not res:
            raise ValueError(f"GenreId {genre_id} does not exist!")
        return cls(*res.pop())
    
    def update_name(self, new_name: str):
        """Updates the value of column `Name` in table `genres`
        
        Example:
            >>> genre = Genre.from_id(1)
            >>> genre
            Genre(id=1, name='Rock')
            >>> genre.update_name('Block')
            >>> Genre.from_id(1)
            Genre(id=1, name='Block')
        """
        db.execute_sql(
            query = "UPDATE genres SET Name = ? WHERE GenreId = ?;",
            params = (new_name, self.id)
        )
        self.name = new_name

    def insert_into_table(self):
        """Adds a new row in table `genres` with the data from this object"""
        db.execute_sql(
            query = "INSERT INTO genres(Name) VALUES (?);",
            params = (self.name,)
        )

    def delete_from_table(self):
        """Deletes the row in table `genres`"""
        db.execute_sql(
            query = "DELETE FROM genres WHERE GenreId = ?;",
            params = (self.id,)
        )

    def get_tracks(self) -> list[Track]:
        """Returns a list containing rows of table `tracks` with this genre
        
        Example:
            >>> Genre.from_id(3).get_tracks()
            [Track(id=77, name='Enter Sandman'), Track(id=78, name='Master Of Puppets'), Track(id=79, name='Harvester Of Sorrow'), ...]
        """
        res = db.execute_sql(
            query = """
                    SELECT TrackId FROM tracks t 
                    INNER JOIN genres g ON t.GenreId = g.GenreId
                    WHERE g.GenreId = ?;""",
            params = (self.id,)
        )
        return [Track.from_id(elem[0]) for elem in res]
    
    def get_albums(self) -> list[Album]:
        """Returns a list containing rows of table `albums` with this genre
        
        Example:
            >>> Genre.from_id(4).get_albums()
            [Album(id=11, title='Out Of Exile'), Album(id=18, title='Body Count'), Album(id=39, title='International Superhits'), ...]

        """
        res = db.execute_sql(
            query = """
                    SELECT DISTINCT a.AlbumId FROM albums a
                    INNER JOIN tracks t ON a.AlbumId = t.AlbumId 
                    INNER JOIN genres g ON t.GenreId = g.GenreId
                    WHERE g.GenreId = ?;""",
            params = (self.id,)
        )
        return [Album.from_id(elem[0]) for elem in res]
    
    def get_artists(self) -> list[Artist]:
        """Returns a list containing rows of table `artists` with this genre
        
        Example:
            >>> Genre.from_id(9).get_artists()
            [Artist(id=21, name='Various Artists'), Artist(id=150, name='U2'), Artist(id=252, name='Amy Winehouse'), ...]

        """
        res = db.execute_sql(
            query = """
                    SELECT DISTINCT ar.ArtistId FROM artists ar
                    INNER JOIN albums al ON ar.ArtistId = al.ArtistId
                    INNER JOIN tracks t ON al.AlbumId = t.AlbumId 
                    INNER JOIN genres g ON t.GenreId = g.GenreId
                    WHERE g.GenreId = ?;""",
            params = (self.id,)
        )
        return [Artist.from_id(elem[0]) for elem in res]