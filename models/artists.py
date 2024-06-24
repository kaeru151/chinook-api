from src import db
from dataclasses import dataclass, field

@dataclass
class Artist:
    """Represents a row of table `artists`"""
    id: int
    name: str

    @classmethod
    def from_id(cls, artist_id: int):
        """Creates a `Artist` object from the provided `artist_id` if it exists
        
        Example:
            >>> Artist.from_id(1) 
            Artist(id=1, name='AC/DC')
            >>> Artist.from_id(-1)
            ValueError: Artist -1 does not exist!
        """
        res = db.execute_sql(
            query = "SELECT ArtistId, Name FROM artists WHERE ArtistId = ?;",
            params = (artist_id,) 
        )
        if not res:
            raise ValueError(f"ArtistId {artist_id} does not exist!")
        return cls(*res.pop())
