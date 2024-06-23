import sqlite3
from pathlib import Path

DB_PATH = ""

def execute_sql(query: str, params: tuple = ()):
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

