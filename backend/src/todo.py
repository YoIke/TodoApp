from auth import token_required
from flask import request, jsonify, Blueprint
from models import db, Todo
import datetime
import pytz

todo_bp = Blueprint('todo', __name__)

@todo_bp.route('/todos', methods=['GET', 'POST'])
@token_required
def handle_todos(current_user):
    if request.method == 'GET':
        todos = Todo.query.filter_by(user_id=current_user.id).all()
        return jsonify([{'id': todo.id, 'title': todo.title, 'description': todo.description, 'complete': todo.complete, 'created_at': todo.created_at, 'updated_at': todo.updated_at} for todo in todos])

    if request.method == 'POST':
        data = request.get_json()
        new_todo = Todo(
            user_id=current_user.id,
            title=data['title'],
            description=data.get('description', ''),
            complete=False,
        )
        db.session.add(new_todo)
        db.session.commit()
        return jsonify({'id': new_todo.id, 'title': new_todo.title, 'description': new_todo.description, 'complete': new_todo.complete, 'created_at': new_todo.created_at, 'updated_at': new_todo.updated_at}), 201
    
@todo_bp.route('/todos/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@token_required
def handle_todo(current_user, id):
    todo = Todo.query.get_or_404(id)

    if request.method == 'GET':
        return jsonify({'id': todo.id, 'title': todo.title, 'description': todo.description, 'complete': todo.complete, 'created_at': todo.created_at, 'updated_at': todo.updated_at})

    elif request.method == 'PUT':
        data = request.get_json()
        todo.title = data.get('title', todo.title)
        todo.description = data.get('description', todo.description)
        todo.complete = data.get('complete', todo.complete)
        db.session.commit()
        return jsonify({'message': 'Todo updated successfully'})

    elif request.method == 'DELETE':
        db.session.delete(todo)
        db.session.commit()
        return jsonify({'message': 'Todo deleted successfully'})
