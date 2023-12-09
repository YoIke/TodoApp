from models import db
from app import create_app

def init_db():
    app = create_app()
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    init_db()
