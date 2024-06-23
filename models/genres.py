from src import db
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

    def get_track_ids(self) -> list[tuple]:
        """Returns a list of all `tracks` with this genre
        
        Example:
            >>> Genre.from_id(1).get_track_ids() 
            [(1,), (2,), (3,), ...]
        """
        res = db.execute_sql(
            query = """
                    SELECT TrackId FROM tracks t 
                    INNER JOIN genres g ON t.GenreId = g.GenreId
                    WHERE g.GenreId = ?;""",
            params = (self.id,)
        )
        return res
