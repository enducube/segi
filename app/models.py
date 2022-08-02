from flask import Flask
from app import db, UserMixin, StringField, PasswordField, FlaskForm
from wtforms.validators import InputRequired
from werkzeug.security import check_password_hash, generate_password_hash

UserUpvoteCanvas = db.Table("user_upvote_canvas",
    db.Column("id",db.Integer, primary_key=True),
    db.Column("canvas_id",db.Integer, db.ForeignKey("canvas.id")),
    db.Column("user_id",db.Integer, db.ForeignKey("user.id"))
)

class Canvas(db.Model):
    __tablename__ = "canvas"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    canvasstring = db.Column(db.Text)

class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    upvoted = db.relationship("Canvas", secondary=UserUpvoteCanvas, backref="upvotes")
    def set_password(self, password):
        self.password = generate_password_hash(password,method="sha256")
    def check_password(self, password):
        return check_password_hash(self.password, password)


class LoginForm(FlaskForm):
    username = StringField(InputRequired())
    password = PasswordField(InputRequired())