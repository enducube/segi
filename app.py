# SEGI (Super Eloquent Good Imagery) by enducube

from app import app, socketio

if __name__ == "__main__":
    print("google")
    socketio.run(app=app,host="0.0.0.0",port=80)