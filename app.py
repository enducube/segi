# SEGI by enducube
# A real-time drawing canvas application powered by Flask, SQLAlchemy, and Socket.IO

from app import app, socketio

if __name__ == "__main__":
    print("google")
    socketio.run(app=app,host="0.0.0.0",port=80)