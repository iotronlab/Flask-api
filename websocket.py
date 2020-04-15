from api import app, socketio, emit, send, db, jsonify
from models import *


@socketio.on('message')
def handleMessage(message):
    print('received msg:' + message)


@socketio.on('update')
def handleJSON(json):
    data = json['data']
    device = Devices.query.filter_by(id=data['id']).first()
    if not device:
        return jsonify({'message': 'No Device Found'})
    device.status = data['status']
    db.session.add(device)
    db.session.commit()
    device_data = {}
    device_data['id'] = device.id
    device_data['name'] = device.device_name
    device_data['status'] = device.status
    send(device_data, broadcast=True)
    print(device_data)
