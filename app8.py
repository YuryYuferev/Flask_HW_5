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


from flask import Flask, request, jsonify
from marshmallow import Schema, fields, ValidationError, validates_schema, post_load

app = Flask(__name__)

# Модель данных задачи с использованием Marshmallow
class Task:
    def __init__(self, id, title, description, status):
        self.id = id
        self.title = title
        self.description = description
        self.status = status

class TaskSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    status = fields.Str(required=True)

    @validates_schema
    def validate_status(self, data, **kwargs):
        if data['status'] not in ['выполнена', 'не выполнена']:
            raise ValidationError('Статус должен быть: "выполнена" или "не выполнена".')

    @post_load
    def make_task(self, data, **kwargs):
        return Task(**data)
# Список задач
tasks = [
        Task(id=1, title="Покупки", description="Купить продукты в магазине", status="todo"),
        Task(id=2, title="Проект", description="Завершить проект к концу недели", status="in progress"),
        Task(id=3, title="Тренировка", description="Пробежать 5 км", status="done")
        ]

# Получение списка всех задач
@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks_schema = TaskSchema(many=True)
    return jsonify(tasks_schema.dump(tasks))

# Получение задачи по ID
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    if 0 <= task_id < len(tasks):
        task_schema = TaskSchema()
        return jsonify(task_schema.dump(tasks[task_id]))
    else:
        return "Задача не найдена", 404

# Добавление новой задачи
@app.route('/tasks', methods=['POST'])
def add_task():
    try:
        data = request.get_json()
        task_schema = TaskSchema()
        new_task = task_schema.load(data)
        new_task.id = len(tasks)  # Присваиваем ID новой задаче
        tasks.append(new_task)
        return "Задача добавлена", 201
    except ValidationError as e:
        return str(e), 400

# Обновление задачи по ID
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    if 0 <= task_id < len(tasks):
        try:
            data = request.get_json()
            task_schema = TaskSchema()
            updated_task = task_schema.load(data)
            updated_task.id = task_id  # Устанавливаем ID обновляемой задачи
            tasks[task_id] = updated_task
            return "Задача обновлена"
        except ValidationError as e:
            return str(e), 400
    else:
        return "Задача не найдена", 404

# Удаление задачи по ID
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    if 0 <= task_id < len(tasks):
        del tasks[task_id]
        return "Задача удалена"
    else:
        return "Задача не найдена", 404

if __name__ == '__main__':
    app.run(debug=True)
