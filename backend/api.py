from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from extensions import db
from models import NoteModel
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort

import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__)) #gives path of file, ensures full absolute path 
db_path = os.path.join(basedir, "instance", "database.db")#builds path + \instance\database.db
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_path #converts it into a proper SQLAlchemy SQLite URL
db.init_app(app)
api = Api(app)

note_args = reqparse.RequestParser()
note_args.add_argument('title', type=str, required=True, help="Title required")
note_args.add_argument('content', type=str, required=True, help="Content required")

noteFields = {
    'id': fields.Integer,
    'title': fields.String,
    'content': fields.String,
}

class Notes(Resource):
    @marshal_with(noteFields)
    def get(self):
        return NoteModel.query.all()
    
    @marshal_with(noteFields)
    def post(self):
        args = note_args.parse_args()
        note = NoteModel(title = args["title"], content = args["content"])
        db.session.add(note)
        db.session.commit()
        return note, 201
    
class Note(Resource):
     @marshal_with(noteFields)
     def get(self, id):
         note = NoteModel.query.filter_by(id = id).first()
         if not note: 
             abort(404, "Note not found")
         return note
     
     @marshal_with(noteFields)
     def patch(self, id):
        args = note_args.parse_args()
        print(args)
        note = NoteModel.query.filter_by(id=id).first()
        if not note:
            abort(404, "Note not found")
        if args["title"]:
            note.title = args["title"]
        if args["content"]:
            note.content = args["content"]
        db.session.commit()
        return note
     
     @marshal_with(noteFields)
     def delete(self, id):
         note = NoteModel.query.filter_by(id = id).first()
         if not note: 
             abort(404, "Note not found")
         db.session.delete(note)
         db.session.commit()
         return "", 204 #would use ",204" if not returning data at all

api.add_resource(Notes, '/api/notes/')
api.add_resource(Note, '/api/notes/<int:id>')

@app.route('/')
def home():
    return '<h1>Flask REST API </h1>'

if __name__ == '__main__':
    app.run(debug=True) #debug = True for development, never in production