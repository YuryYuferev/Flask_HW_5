# Создать RESTful API для управления списком задач. Приложение должно использовать FastAPI и
# поддерживать следующие функции:
# Получение списка всех задач.
# Получение информации о задаче по её ID.
# Добавление новой задачи.
# Обновление информации о задаче по её ID.
# Удаление задачи по её ID.
# Каждая задача должна содержать следующие поля: ID (целое число), Название (строка), Описание (строка),
# Статус (строка): "todo", "in progress", "done".

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Модель данных задачи с использованием Pydantic
class Task(BaseModel):
    id: int
    title: str
    description: str
    status: str

# Список задач
tasks = [
    Task(id=1, title="Покупки", description="Зайти в торговый центр", status="todo"),
    Task(id=2, title="Проект", description="Завтра начать новый проект", status="in progress"),
    Task(id=3, title="Тренировка", description="Увеличить нагрузку на 10 кг.", status="done")
]

# Получение списка всех задач
@app.get("/tasks", response_model=List[Task])
async def get_tasks():
    return tasks

# Получение информации о задаче по её ID
@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Задача не найдена")

# Добавление новой задачи
@app.post("/tasks", response_model=Task)
async def create_task(task: Task):
    tasks.append(task)
    return task

# Обновление информации о задаче по её ID
@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task: Task):
    for idx, existing_task in enumerate(tasks):
        if existing_task.id == task_id:
            tasks[idx] = task
            return task
    raise HTTPException(status_code=404, detail="Задача не найдена")

# Удаление задачи по её ID
@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    for idx, existing_task in enumerate(tasks):
        if existing_task.id == task_id:
            del tasks[idx]
            return {"message": "Задача удалена"}
    raise HTTPException(status_code=404, detail="Задача не найдена")


