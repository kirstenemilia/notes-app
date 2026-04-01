from api import app, db
from models import NoteModel


with app.app_context():
    db.create_all()
    

