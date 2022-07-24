from app import db, UserMixin

UserUpvoteCanvas = db.Table("user_upvote_canvas",
    db.Column("canvas_id",db.Integer, db.ForeignKey("Canvas.id")),
    db.Column("user_id",db.Integer, db.ForeignKey("User.id"))
)


class Canvas(db.Model):
    __tablename__ = "canvas"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    canvasstring = db.Column(db.Text)
    # upvotes = db.relationship("User", secondary=UserUpvoteCanvas, backref="Canvas")


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
   # upvoted = db.relationship("User", secondary=UserUpvoteCanvas, backref="Canvas")
