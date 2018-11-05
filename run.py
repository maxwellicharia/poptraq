import poptraq

app = poptraq.app
socket = poptraq.socketio

if __name__ == '__main__':
    socket.run(app, debug=True)
