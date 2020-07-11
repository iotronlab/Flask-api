from api import app, jsonify, request, make_response, socketio, emit
from functools import wraps
from flask_jwt_extended import (jwt_required, get_jwt_identity)
import datetime

from models import *


@app.route('/')
def index():
    return jsonify({'data': {'msg': 'Smart Hub Available.', 'name': 'Smart Hub'}}), 200


@app.route('/devices', methods=['GET'])
@jwt_required
def get_devices():
    current_user = get_jwt_identity()
    user = Users.query.filter_by(public_id=current_user).first()
    if not user:
        return jsonify({'message': 'User not Found'}), 404
    devices = user.owned_devices
    shared = user.shared_devices
    if not devices and not shared:
        return jsonify({'message': 'No devices found'}), 404
    output = []
    shareddevice = []
    rooms = []
    for device in devices:
        device_data = {}
        room_data = {}
        device_data['id'] = device.id
        device_data['name'] = device.device_name
        device_data['status'] = device.status
        device_data['room'] = device.room_id
        output.append(device_data)
        room = device.room

        if (len(rooms) < 1):
            room_data['id'] = room.id
            room_data['name'] = room.name
            rooms.append(room_data)
        else:
            present = False
            for item in rooms:
                if item['id'] == room.id:
                    present = True
            if present == False:
                room_data['id'] = room.id
                room_data['name'] = room.name
                rooms.append(room_data)

    for device in shared:
        device_data = {}
        room_data = {}
        device_data['id'] = device.id
        device_data['name'] = device.device_name
        device_data['status'] = device.status
        device_data['room'] = device.room_id
        shareddevice.append(device_data)
        room = device.room

        if (len(rooms) < 1):
            room_data['id'] = room.id
            room_data['name'] = room.name
            rooms.append(room_data)
        else:
            present = False
            for item in rooms:
                if item['id'] == room.id:
                    present = True
            if present == False:
                room_data['id'] = room.id
                room_data['name'] = room.name
                rooms.append(room_data)

    return jsonify({'devices': output, 'rooms': rooms, 'shared': shareddevice}), 200


@app.route('/devices/<id>', methods=['GET'])
def get_one_device(id):
    device = Devices.query.filter_by(id=id).first()
    if not device:
        return jsonify({'message': 'No Device Found'})

    device_data = {}
    device_data['id'] = device.id
    device_data['name'] = device.device_name
    device_data['status'] = device.status

    return jsonify(device_data)


@app.route('/rooms/<id>', methods=['GET'])
def get_room_devices(id):
    room = Rooms.query.filter_by(id=id).first()
    if not room:
        return jsonify({'message': 'Room not Found'})
    room_data = {}
    room_data['id'] = room.id
    room_data['name'] = room.name
    devices = room.room_devices
    output = []
    for device in devices:
        device_data = {}
        device_data['id'] = device.id
        device_data['name'] = device.device_name
        device_data['status'] = device.status
        output.append(device_data)

    return jsonify({'room': room_data, 'devices': output})


@app.route('/devices', methods=['POST'])
@jwt_required
def add_devices():
    current_user = get_jwt_identity()

    user = Users.query.filter_by(public_id=current_user).first()
    if not user:
        return jsonify({'message': 'User not Found'}), 404
    data = request.get_json()

    room = Rooms.query.filter_by(name=data['room']).first()
    if not room:
        new_room = Rooms(name=data['room'])
        db.session.add(new_room)
        db.session.commit()
    room = Rooms.query.filter_by(name=data['room']).first()
    new_device = Devices(
        device_name=data['name'], status=False, room_id=room.id, owner_id=user.id)
    db.session.add(new_device)
    db.session.commit()
    return jsonify({'message': 'successfully added'}), 200


@app.route('/devices/update', methods=['PATCH'])
@jwt_required
def update_device():
    data = request.get_json()
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
    socketio.emit('socketUpdate', {'data': device_data}, broadcast=True), 200
    return jsonify(device_data), 200
