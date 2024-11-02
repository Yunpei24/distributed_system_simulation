from fastapi import APIRouter
from fastapi.responses import JSONResponse
import time
from typing import Optional
from models.model import *
import random
import requests

# Create a FastAPI router
router = APIRouter()

# Shared address to get the list of tasks to do
shared_address = "http://192.168.131.251:8001/get_tasks_to_do/"

# Variables to manage tasks and their state
start_time = None
reponse_shared = None
Fruits = None
tasks_to_do = []
tasks_being_done = {}
command_dict = {}
task_already_done = []
task_len = None

# Event on startup
@router.on_event("startup")
async def startup_event():
    """
    Event that is triggered on application startup.
    """
    create_table()  # Create the table if it doesn't exist in the database

# Send a task to a worker
@router.post("/send_task")
async def send_task(nom_worker: dict):
    """
    Send a task to a worker.

    Parameters:
    - nom_worker (dict): A dictionary containing the worker's name.

    Returns:
    - JSONResponse: JSON response containing the task details if available, or a message if no tasks are available.
    """
    global tasks_to_do, start_time, tasks_being_done, reponse_shared, task_len, task_already_done
    nom_worker = nom_worker.get("nom_worker")
    reponse_shared = requests.get(shared_address)

    if reponse_shared.status_code == 200:
        Fruits = reponse_shared.json()
        task_len = len(Fruits)
        tasks_to_do = [INGREDIENT(id=i, fruit=ingredient['fruit'], execution_time=random.randint(4, 20)) for i, ingredient in enumerate(Fruits)]
        start_time = None
        task_already_done = []
        tasks_being_done = {}

    if start_time is None:
        start_time = time.time()

    if tasks_to_do:
        task = tasks_to_do.pop(0)
        tasks_being_done[task.id] = task
        print(f"Sending task [id: {task.id}, fruit: {task.fruit}] to worker {nom_worker}")
        return JSONResponse(content={"id": task.id, "fruit": task.fruit, "execution_time": task.execution_time}, status_code=200)
    else:
        print(f"The worker {nom_worker} asks for more tasks to do")
        return JSONResponse(content={"message": "No more tasks"}, status_code=202)

# Receive a result from a worker
@router.post("/result")
async def receive_result(result_data: Optional[dict]):
    """
    Receive a result from a worker.

    Parameters:
    - result_data (Optional[dict]): A dictionary containing the result data including the task and result.

    Returns:
    None
    """
    global tasks_to_do, start_time, tasks_being_done, task_already_done, task_len

    task = dict(result_data.get("task"))
    result = result_data.get("result")

    task_already_done.append(task.get("id"))

    tasks_being_done.pop(int(task.get("id")), None)

    if not tasks_to_do and not tasks_being_done:
        print("Task to do: ", tasks_to_do,"\nTask being done : ", tasks_being_done)
        end_time = time.time()
        command_dict = {
            "message": "The salad is ready! Enjoy!",
            "preparation_time": end_time - start_time
        }
        insert_command(command_dict["message"], command_dict["preparation_time"], db_path)
    else:
        print(f"Task: {result}; came from worker {task.get('nom_worker')}")

# Get a command to send
@router.get("/send_command")
async def send_command():
    """
    Get a command to send.

    Returns:
    - JSONResponse: JSON response containing the command details if available, or a message if no commands are available.
    """
    command_list = get_commands(db_path)

    if len(command_list) != 0:
        command_dict = {
            "message": command_list[0][0],
            "preparation_time": command_list[0][1]
        }
        return JSONResponse(content=command_dict, status_code=200)
    else:
        return JSONResponse(content={"message": "No command"}, status_code=202)
