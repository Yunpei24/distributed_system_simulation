from pydantic import BaseModel
import sqlite3
#import socket


#def ip_address():
    # On récupère le nom d'hôte de la machine
#    hostname = socket.gethostname()

    # On récupère l'adresse IP associée au nom d'hôte
#    ip_address = socket.gethostbyname(hostname)

#    return ip_address

class Fruit(BaseModel):
    fruit: str

class INGREDIENT(BaseModel):
    id: int
    fruit: str
    execution_time: int


db_path = "commands.db"

def create_table():
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS commands")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS commands (
            message TEXT NOT NULL,
            time INTEGER NOT NULL
        )
    """)
    connection.commit()
    connection.close()

def insert_command(message, time, db_path):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO commands (message, time) VALUES (?, ?)
    """, (message, time))
    connection.commit()
    connection.close()

def get_commands(db_path):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM commands")
    commands = cursor.fetchall()
    cursor.execute("DELETE FROM commands")
    connection.commit()
    connection.close()

    return commands