"""
 SEGI by enducube
 A real-time drawing canvas application powered
 by Flask, SQLAlchemy, and Socket.IO


 MAKE SURE TO RUN pip install -r requirements.txt
"""

from app import app, socketio

if __name__ == "__main__":
    print("enducube's SEGI Canvas running on http://localhost/")
    socketio.run(app=app, host="0.0.0.0", port=80)
