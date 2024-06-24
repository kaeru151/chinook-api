from src import db
from .tracks import Track
from dataclasses import dataclass, field

@dataclass
class Album:
    """Represents a row of table `albums`"""
    id: int
    title: str
    artist_id: int = field(repr=False)

    @classmethod
    def from_id(cls, album_id: int):
        """Creates a `Album` object from the provided `album_id` if it exists
        
        Example:
            >>> Album.from_id(7) 
            Album(id=7, name='Facelift')
            >>> Album.from_id(-1)
            ValueError: Album -1 does not exist!
        """
        res = db.execute_sql(
            query = "SELECT AlbumId, Title, ArtistId FROM albums WHERE AlbumId = ?;",
            params = (album_id,) 
        )
        if not res:
            raise ValueError(f"AlbumId {album_id} does not exist!")
        return cls(*res.pop())

    def get_tracks(self) -> list[Track]:
        """Returns a list containing rows of table `tracks` with this album
        
        Example:
            >>> Album.from_id(43).get_tracks()
            [Track(id=15, name='Go Down'), Track(id=16, name='Dog Eat Dog'), Track(id=17, name='Let There Be Rock'), ...]
        """
        res = db.execute_sql(
            query = """
                    SELECT TrackId FROM tracks t 
                    INNER JOIN albums a ON t.AlbumId = a.AlbumId
                    WHERE a.AlbumId = ?;""",
            params = (self.id,)
        )
        return [Track.from_id(elem[0]) for elem in res]