from backend import app
from backend.instances import socketio

app = app.create_app()

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)