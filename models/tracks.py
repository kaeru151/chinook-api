from src import db
from dataclasses import dataclass, field

@dataclass
class Track:
    """Represents a row of table `tracks`"""
    id: int
    name: str
    album_id: int = field(repr=False)
    media_type_id: int = field(repr=False)
    genre_id: int = field(repr=False)
    composer: str = field(repr=False)
    millisecons: int = field(repr=False)
    bytes: int = field(repr=False)
    unit_price: float = field(repr=False)

    @classmethod
    def from_id(cls, track_id: int):
        """Creates a `Track` object from the provided `track_id` if it exists
        
        Example:
            >>> Track.from_id(2) 
            Track(id=2, name='Balls to the Wall')
            >>> Track.from_id(-1)
            ValueError: TrackId -1 does not exist!
        """
        res = db.execute_sql(
            query = "SELECT TrackId,Name,AlbumId,MediaTypeId,GenreId,Composer,Milliseconds,Bytes,UnitPrice FROM tracks WHERE TrackId = ?;",
            params = (track_id,) 
        )
        if not res:
            raise ValueError(f"TrackId {track_id} does not exist!")
        return cls(*res.pop())