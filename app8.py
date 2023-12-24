# Необходимо создать API для управления списком задач. Каждая задача должна содержать заголовок и описание.
# Для каждой задачи должна быть возможность указать статус (выполнена/не выполнена).
# API должен содержать следующие конечные точки:
# * GET /tasks - возвращает список всех задач.
# * GET /tasks/{id} - возвращает задачу с указанным идентификатором.
# * POST /tasks - добавляет новую задачу.
# * PUT /tasks/{id} - обновляет задачу с указанным идентификатором.
# * DELETE /tasks/{id} - удаляет задачу с указанным идентификатором.
# Для каждой конечной точки необходимо проводить валидацию данных запроса и ответа.
# Для этого использовать библиотеку Pydantic.


from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel

app = FastAPI()
class Task(BaseModel):
    id: int
    title: str
    description: str
    status: str


# Список задач
tasks = [
        Task(id=1, title="Покупки", description="Купить продукты в магазине", status="выполнена"),
        Task(id=2, title="Проект", description="Завершить проект к концу недели", status="не выполнена"),
        Task(id=3, title="Тренировка", description="Пробежать 5 км", status="выполнена")
        ]

# GET /tasks - возвращает список всех задач
@app.get("/tasks", response_model=List[Task])
async def get_tasks():
    return tasks

# GET /tasks/{id} - возвращает задачу с указанным идентификатором
@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Задача не найдена")
# POST /tasks - добавляет новую задачу
@app.post("/tasks", response_model=Task)
async def create_task(task: Task):
    tasks.append(task)
    return task

# PUT /tasks/{id} - обновляет задачу с указанным идентификатором
@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task: Task):
    for idx, existing_task in enumerate(tasks):
        if existing_task.id == task_id:
            tasks[idx] = task
            return task
    raise HTTPException(status_code=404, detail="Задача не найдена")

# DELETE /tasks/{id} - удаляет задачу с указанным идентификатором
@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    for idx, existing_task in enumerate(tasks):
        if existing_task.id == task_id:
            del tasks[idx]
            return {"message": "Задача удалена"}
    raise HTTPException(status_code=404, detail="Задача не найдена")


# Запуск кода: uvicorn Task8:app --reload

