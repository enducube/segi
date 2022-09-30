from app import app, socketio, db, login_manager
from flask import redirect, render_template, url_for, request
from app.models import Canvas, User, UserUpvoteCanvas, LoginForm
from flask_socketio import join_room, leave_room, rooms
from flask_login import login_user, logout_user, login_required, current_user
import json

# Flask login user loader,
# required to get interactions
# between flask login and the sqlalchemy stuff


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


# Flask routes, used to deliver the html templates
@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


# The register page, for users to make new accounts
@app.route("/register", methods=["GET", "POST"])
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
@app.route("/login", methods=["GET", "POST"])
def login():
    loginform = LoginForm()
    if loginform.validate_on_submit():
        user = User.query.filter_by(username=loginform.username.data).first()
        if user and user.check_password(loginform.password.data):
            login_user(user)
            return redirect("/")
    return render_template("login.html", form=loginform, reference="login")

@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")

# Profile page, where you can view a user's upvoted canvases
@app.route("/profile/<string:username>")
def profile(username):
    user = User.query.filter_by(username=username).first()
    return render_template("profile.html", user=user)


# Creating a new canvas
@app.route("/newcanvas", methods=["GET", "POST"])
def newcanvas():
    new_canvas = Canvas()
    new_canvas.canvasstring = ""
    db.session.add(new_canvas)
    db.session.commit()
    return redirect("/canvas/"+str(new_canvas.id))


# The actual canvas page
@app.route("/canvas/<int:canvasid>")
@login_required
def canvas(canvasid):
    upvoted = False
    the_canvas = Canvas.query.filter_by(id=canvasid).first()
    if the_canvas:  # check if the canvas exists
        if the_canvas in current_user.upvoted:
            upvoted = True
        upvotenumber = len(Canvas.query.filter_by(id=canvasid).first().upvotes)
        # get the canvas string from the database
        canvasstring = Canvas.query.filter_by(id=canvasid).first().canvasstring
        return render_template("canvas.html",
                               canvasstring=canvasstring,
                               canvasid=canvasid,
                               upvotenumber=upvotenumber,
                               upvoted=str(upvoted).lower())
    else:  # if the canvas doesn't exist, make a new one!
        new_canvas = Canvas(id=canvasid)
        new_canvas.canvasstring = ""
        db.session.add(new_canvas)
        db.session.commit()
        return redirect("/canvas/"+str(new_canvas.id))


# Socket.IO routes, used for real-time communication
@socketio.on("join")  # upon user join
def join(json):
    data = dict(json)
    # make the socket.io signals specific to this canvas
    join_room(room=data["room"])
    socketio.emit("test", to=data["room"])


@socketio.on("pixel")  # when the user places a pixel
def socket_pixel(json):
    data = dict(json)
    # emit the signal with the pixel data to everyone else on that canvas
    socketio.emit("pixel", data, to=data["room"])


@socketio.on("save")  # saving the canvas
def save_canvas(json):
    data = dict(json)
    canvas = Canvas.query.filter_by(id=int(data["id"])).first()
    canvas.canvasstring = str(data["canvasstring"])
    db.session.commit()


@socketio.on("upvote")  # when the canvas has been upvoted
def upvote(json):
    data = dict(json)
    new_upvote = UserUpvoteCanvas.insert((None, data["id"], current_user.id))
    db.session.execute(new_upvote)
    db.session.commit()
    data["upvotecount"] = len(db.session.query(UserUpvoteCanvas).filter_by(
        canvas_id=data["id"]).all())
    socketio.emit("upvoted", data, to=data["id"])


@socketio.on("unupvote")  # when the canvas has been unupvoted
def unupvote(json):
    data = dict(json)
    # get the upvote, and then execute a deletion
    # on the upvote previously made by the user
    the_upvote = db.session.query(UserUpvoteCanvas).filter_by(
        canvas_id=data["id"]).first()
    db.engine.execute(UserUpvoteCanvas.delete().where(
        UserUpvoteCanvas.c.id == the_upvote.id))
    data["upvotecount"] = len(db.session.query(UserUpvoteCanvas).filter_by(
        canvas_id=data["id"]).all())
    socketio.emit("unupvoted", data, to=data["id"])
