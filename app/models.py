from app import db

class Canvas(db.Model):
    __tablename__ = "canvas"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    canvasstring = db.Column(db.Text)
