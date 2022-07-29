from app import app, socketio, db, login_manager
from flask import redirect, render_template, url_for, request
from app.models import Canvas, User, UserUpvoteCanvas, LoginForm
from flask_socketio import join_room, leave_room, rooms
from flask_login import login_user, logout_user, login_required, current_user
import json

# Flask login user loader, required to get interactions between flask login and the sqlalchemy stuff
@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()
# Flask routes, used to deliver the html templates
@app.route("/",methods=["GET", "POST"])
def index():
    return render_template("index.html")

# The register page, for users to make new accounts
@app.route("/register",methods=["GET", "POST"])
def register():
    regform = LoginForm()
    if regform.validate_on_submit():
        user = User(username=regform.username.data)
        user.set_password(regform.password.data)
        db.session.add(user)
        db.session.commit()
        user = User.query.filter_by(username=regform.username.data).first()
        if user:
            login_user(user)
            return redirect("/")
    return render_template("login.html", form=regform, reference="register")

# The login page, for users to sign into existing accounts
@app.route("/login",methods=["GET", "POST"])
def login():
    loginform = LoginForm()
    if loginform.validate_on_submit():
        user = User.query.filter_by(username=loginform.username.data).first()
        if user and user.check_password(loginform.password.data):
            login_user(user)
            return redirect("/")
    return render_template("login.html", form=loginform, reference="login")

# Creating a new canvas
@app.route("/newcanvas",methods=["GET", "POST"])
def newcanvas():
    new_canvas = Canvas()
    new_canvas.canvasstring = ""
    db.session.add(new_canvas)
    db.session.commit()
    return redirect("/canvas/"+str(new_canvas.id))

# The actual canvas page
@app.route("/canvas/<int:canvasid>")
def canvas(canvasid):
    upvotenumber = len(Canvas.query.filter_by(id=canvasid).first().upvotes)
    # get the canvas string from the database
    canvasstring = Canvas.query.filter_by(id=canvasid).first().canvasstring
    return render_template("canvas.html", canvasstring=canvasstring, canvasid=canvasid, upvotenumber=upvotenumber)


# Socket.IO routes, used for real-time communication
@socketio.on("join") # upon user join
def join(json):
    data = dict(json)
    # make the signals specific to this canvas
    join_room(room=data["room"])
    socketio.emit("test", to=data["room"])

@socketio.on("pixel") # when the user places a pixel
def socket_pixel(json):
    data = dict(json)
    socketio.emit("pixel", data, to=data["room"])

@socketio.on("save") # saving the canvas
def save_canvas(json):
    data = dict(json)
    Canvas.query.filter_by(id=int(data["id"])).first().canvasstring = str(data["canvasstring"])
    db.session.commit()

@socketio.on("upvote")
def upvote(json):
    data = dict(json)
    new_upvote = UserUpvoteCanvas(data["id"], current_user.id)

