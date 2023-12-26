from flask import Flask, jsonify 
from models import db
from auth import auth_bp
from todo import todo_bp
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_temporary_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@db:5432/todo-db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route('/')
    def index():
        return "Hello World"

    app.register_blueprint(auth_bp)
    app.register_blueprint(todo_bp)

    CORS(app, supports_credentials=True)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
