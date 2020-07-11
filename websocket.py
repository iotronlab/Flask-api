from api import app, socketio, emit, send, db, jsonify
from models import *


@socketio.on('message')
def handleMessage(message):
    print('received msg:' + message)

    
@socketio.on('connectdevice')
def handleMessage():
    send('received msg')



@socketio.on('update')
def handle_json(json):
    data = json['data']
    device = Devices.query.filter_by(id=data['id']).first()
    if not device:
        socketio.send('Device not found')
    device.status = data['status']
    db.session.add(device)
    db.session.commit()
    device_data = {}
    device_data['id'] = device.id
    device_data['name'] = device.device_name
    device_data['status'] = device.status
    socketio.emit('updatedDevice', {'device':device_data}, broadcast=True)
    print(device_data)
