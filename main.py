from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

# Initialize FastAPI app
app = FastAPI()

# SQLite database connection
conn = sqlite3.connect('tasks.db')
cursor = conn.cursor()

# Create tasks table if not exists
cursor.execute('''CREATE TABLE IF NOT EXISTS tasks
                  (id INTEGER PRIMARY KEY, title TEXT, description TEXT)''')
conn.commit()

# Pydantic model for task
class Task(BaseModel):
    title: str
    description: str = None

# CRUD operations
@app.post("/tasks/")
async def create_task(task: Task):
    cursor.execute('''INSERT INTO tasks (title, description) VALUES (?, ?)''', (task.title, task.description))
    conn.commit()
    return {"message": "Task created successfully"}

@app.get("/tasks/{task_id}")
async def read_task(task_id: int):
    cursor.execute('''SELECT * FROM tasks WHERE id = ?''', (task_id,))
    task = cursor.fetchone()
    if task:
        return {"id": task[0], "title": task[1], "description": task[2]}
    else:
        raise HTTPException(status_code=404, detail="Task not found")

@app.put("/tasks/{task_id}")
async def update_task(task_id: int, task: Task):
    cursor.execute('''UPDATE tasks SET title = ?, description = ? WHERE id = ?''', (task.title, task.description, task_id))
    conn.commit()
    return {"message": "Task updated successfully"}

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    cursor.execute('''DELETE FROM tasks WHERE id = ?''', (task_id,))
    conn.commit()
    return {"message": "Task deleted successfully"}
