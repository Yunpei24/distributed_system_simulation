from fastapi import APIRouter
from models.model import INGREDIENT
import time
import requests
import httpx

# Worker's name
nom_workers = "Worker_Josh"

# Create a FastAPI router
router = APIRouter()

# URL of the master server (where tasks are managed)
master_url = "http://localhost:8000"

# Simulated fruit preparation function
def prepared_fruit(id_, fruit, t):
    time.sleep(t)
    return f"{id_} {fruit} prepared in {t} seconds"

# Function to send a result to the master server
def send_result(url, data):
    with httpx.Client() as session:
        session.post(url, json=data)

# Function to get a task from the master server
def get_task():
    response = requests.post(f"{master_url}/send_task", json={"nom_worker": nom_workers})
    if response.status_code == 200:
        task = response.json()
        return task
    else:
        return None

# Function to execute a task
def do_task():
    while True:
        task_data = get_task()
        while task_data:
            task = INGREDIENT(**task_data)  # Convert the task data to an INGREDIENT object
            
            prepare_fruit = prepared_fruit(task.id, task.fruit, task.execution_time)
            print("Result sent to master:", prepare_fruit)
            url = f"{master_url}/result"
            data = {
                "task": {
                    "id" : task.id,
                    "fruit": task.fruit,
                    "execution_time": task.execution_time,
                    "nom_worker": nom_workers
                    },
                "result": prepare_fruit
            }
            send_result(url, data)

            task_data = get_task()
        
        time.sleep(3)
        print("No task available. Waiting...")

# Add a docstring for the `send_result` function
def send_result(url, data):
    """
    Sends a result to the master server.

    Parameters:
    - url (str): The URL to send the result to.
    - data (dict): The result data to send.

    Returns:
    None
    """
    with httpx.Client() as session:
        session.post(url, json=data)

# Add a docstring for the `do_task` function
def do_task():
    """
    Continuously fetches and performs tasks.

    Returns:
    None
    """
    while True:
        task_data = get_task()
        while task_data:
            task = INGREDIENT(**task_data)  # Convert the task data to an INGREDIENT object
            
            prepare_fruit = prepared_fruit(task.id, task.fruit, task.execution_time)
            print("Result sent to master:", prepare_fruit)
            url = f"{master_url}/result"
            data = {
                "task": {
                    "id" : task.id,
                    "fruit": task.fruit,
                    "execution_time": task.execution_time,
                    "nom_worker": nom_workers
                    },
                "result": prepare_fruit
            }
            send_result(url, data)

            task_data = get_task()
        
        time.sleep(3)
        print("No task available. Waiting...")
