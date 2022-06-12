from app import app, socketio, db
from flask import redirect, render_template, url_for, request
from app.models import Canvas
import json
# Flask routes, used to deliver the html templates
@app.route("/",methods=["GET", "POST"])
def index():
    new_canvas = Canvas()
    new_canvas.canvasstring = ""
    db.session.add(new_canvas)
    db.session.commit()
    #print(new_canvas.canvasstring, new_canvas.id)
    return redirect("/canvas/"+str(new_canvas.id))

# The actual canvas page
@app.route("/canvas/<int:canvasid>")
def canvas(canvasid):
    canvasstring = Canvas.query.filter_by(id=canvasid).first().canvasstring
    #print(canvasstring)
    return render_template("canvas.html", canvasstring=canvasstring, canvasid=canvasid)


# Socket.IO routes, used for real-time communication

@socketio.on("connection")
def socket_cool():
    pass
    #socketio.emit("yort", broadcast=True)

@socketio.on("pixel")
def socket_pixel(json):
    data = dict(json)
    socketio.emit("pixel", data, broadcast=True)

@socketio.on("save")
def save_canvas(json):
    data = dict(json)
    Canvas.query.filter_by(id=int(data["id"])).first().canvasstring = str(data["canvasstring"])
    db.session.commit()