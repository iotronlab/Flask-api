from api import app, socketio, emit, send



@socketio.on('message')
def handle_my_custom_event(message):
    print('received msg:' + message)

@socketio.on('update')
def handle_my_custom_event(json):
    print('received json:' + str(json))