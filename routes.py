from api import app, jsonify, request, make_response
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
    shares = user.shared_devices
    if not devices and not shares:
        return jsonify({'message': 'No devices found'}), 404
    output = []
    shared = []
    rooms = []
    for device in devices:
        device_data = {}
        device_data['id'] = device.id
        device_data['name'] = device.device_name
        device_data['status'] = device.status
        device_data['room'] = device.room_id
        output.append(device_data)
        room = Rooms.query.filter_by(id=device.room_id).first()
        room_data = {}
        room_data['id'] = room.id
        room_data['name'] = room.name
        rooms.append(room_data)

    return jsonify({'devices': output, 'rooms': rooms})


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
    return jsonify({'message': 'success'})


@app.route('/devices/<id>', methods=['PUT'])
def update_device(id):
    device = Devices.query.filter_by(id=id).first()
    if not device:
        return jsonify({'message': 'No Device Found'})

    # device.status = !device.status
    return jsonify(device)
