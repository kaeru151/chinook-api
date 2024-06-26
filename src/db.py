import sqlite3
from pathlib import Path

DB_PATH = ""

def execute_sql(query: str, params: tuple = ()) -> list[tuple]:
    """
    Connects to database specified by global `DB_PATH` and executes `query` (with optional `params`)
    
    Example:
        >>> execute_sql("SELECT DISTINCT City FROM customers WHERE Country = 'France';")
        [("Paris",), ("Lyon",), ("Bordeaux",), ("Dijon",)]
        >>> execute_sql("SELECT DISTINCT City FROM customers WHERE Country = ?;", ("United Kingdom",))
        [("London",), ("Edinburgh",)]
        >>> execute_sql("INSERT INTO artists(Name) VALUES ('Black Eyed Python');")
    """
    if DB_PATH == "":
        raise Exception("DB_PATH is not set! please set db.DB_PATH = r'path/to/file.db'")
    if not Path(DB_PATH).is_file():
        raise FileNotFoundError(DB_PATH)
    if Path(DB_PATH).suffix != ".db":
        raise ValueError(f"{DB_PATH} is not a database")
    
    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        cur.execute(query, params)
        res = cur.fetchall()
    con.close()
    return res

