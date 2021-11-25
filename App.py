# Import Flask app
from flask import Flask, jsonify, render_template, redirect, flash, request

# Import Restfull needs
from flask_restful import Api, Resource, abort


# Configure Log Module
import logging

# Import DB handler, Todo Class
from models import db, Todo


# Configure Flask app
todo_flask_app = Flask(__name__)

# Configure Restful APi
todo_api = Api(todo_flask_app)

# Configure Secret Key
todo_flask_app.config['SECRET_KEY'] = '0zx5c34as65d4654&%^#$#$@'

# Configure Database
todo_flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
todo_flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

todo_list = [
    {'name': 'a', 'id': 0, 'priority': 5},
    {'name': 'b', 'id': 1, 'priority': 5},
    {'name': 'c', 'id': 2, 'priority': 5}
]


# --------------------------
# Normal Views
# --------------------------

# Hello View
@todo_flask_app.route('/', methods=['GET'])
def hello_view():
    print(request.args)
    print('name -> ', request.args.get('name'))
    print('age -> ', request.args.get('age'))
    print("Request -> ", request)
    print("req method -> ", request.method)
    return f'Hello {request.args.get("name")} from flask your age is {request.args.get("age")}'


@todo_flask_app.route('/todo/', methods=['GET', 'POST'])
@todo_flask_app.route('/todo', methods=['GET', 'POST'])
def list_todo_tasks():
    if request.method == 'GET':
        return jsonify(todo_list)
    elif request.method == 'POST':
        print(request.form)
        task_name = request.form.get('task_name')
        task_id = request.form.get('task_id')
        task_priority = request.form.get('task_priority')

        todo_list.append(
            {'name': task_name, 'id': task_id, 'priority': task_priority}

        )
        return jsonify(todo_list)


@todo_flask_app.route('/todo/<int:task_id>', methods=['GET', 'DELETE'])
def todoRD(task_id):
    if request.method == 'GET':
        return jsonify(todo_list[task_id])

    elif request.method == 'DELETE':
        del todo_list[task_id]
        return {'message': 'deleted task'}, 200


@todo_flask_app.route('/todo/<string:task_name>', methods=['GET'])
def task_detail(task_name):
    try:
        print(task_name)
        return jsonify(todo_list[1])
    except Exception as e:
        pass
    return "No task found"

@todo_flask_app.route('/todo/<int:task_id>', methods=['GET', 'POST'])
def todo_update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)







# Register The TodoLC Resource class
# todo_api.add_resource(TodoLC, '/api/v1/todo')
#
# # Register TodoRud Resource class
# todo_api.add_resource(TodoRUD, '/api/v1/todo/<int:todo_id>')

# Attach Sqlalchemy to app
db.init_app(todo_flask_app)


# Create Database Tables
@todo_flask_app.before_first_request
def initiate_data_base_tables():
    db.create_all()


# Run Server
todo_flask_app.run(port=5080, debug=True)
