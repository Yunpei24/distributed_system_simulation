from fastapi import APIRouter, HTTPException
from models.model import Fruit
from typing import List
import sqlite3
from fastapi.responses import JSONResponse


router = APIRouter()

db_path = "fruits.db"

def create_table():
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS fruits")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fruits (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
    """)
    connection.commit()
    connection.close()

@router.on_event("startup")
async def startup_event():
    create_table()

@router.post("/create_task/", response_model=List[Fruit])
async def create_task(liste_fruits: List[Fruit]):
    """
    Créer une tâche à exécuter. Il s'agit d'une liste de fruits à traiter. 

    Paramètres:
    - liste_fruits (List[Fruit]): liste de fruits à traiter

    """
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    for fruit in liste_fruits:
        cursor.execute("INSERT INTO fruits (name) VALUES (?)", (fruit.fruit,))

    connection.commit()
    connection.close()

    return JSONResponse(status_code=200, content={"message": "Task created"})

@router.get("/get_tasks_to_do/", response_model=List[Fruit])
async def get_tasks():
    """
    Récupère toutes les tâches à exécuter. 

    """
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM fruits")
    fruits = cursor.fetchall()
    # Convertir la liste de tuples en liste de Fruit
    fruits = [{"fruit": fruit[0]} for fruit in fruits]

    
    cursor.execute("DELETE FROM fruits")
    connection.commit()
    
    connection.close()
    if len(fruits) == 0:
        return JSONResponse(content=fruits, status_code=202)
    else:
        return JSONResponse(content=fruits, status_code=200)