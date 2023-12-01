
import sqlite3


def init_database():
    conn = sqlite3.connect("AEF.db")
    c = conn.cursor()
    c.execute("""
                    CREATE TABLE IF NOT EXISTS AEF
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    etats TEXT,
                    alphabet TEXT,
                    transitions TEXT,
                    etats_finaux TEXT,
                    etat_initial TEXT
                   )
                   """)
    conn.commit()
    return conn

def insert_AEF(conn, AEF):
    c = conn.cursor()
    c.execute("""INSERT INTO AEF (etats, alphabet, transitions, etats_finaux, etat_initial) 
          VALUES (?, ?, ?, ?, ?)""", (str(AEF["states"]), str(AEF["alphabet"]), str(AEF["transitions"]), str(AEF["final_states"]), str(AEF["start_state"])))
    conn.commit()
    