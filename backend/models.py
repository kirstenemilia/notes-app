from extensions import db

class NoteModel(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    content = db.Column(db.Text, nullable = False)

    def __repr__(self):
        return f"Note(title={self.title}, content={self.content})"
    