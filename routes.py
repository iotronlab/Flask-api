from api import jwt, app, jsonify, request, make_response
from functools import wraps
from flask_jwt_extended import (jwt_required)
import datetime

from models import *


@app.route('/')
def index():
    return jsonify({'data': {'msg': 'Smart Hub Available.', 'name': 'Smart Hub'}}), 200


@app.route('/devices', methods=['GET'])
@jwt_required
def get_devices():
    devices = Devices.query.all()
    output = []
    for device in devices:
        device_data = {}
        device_data['id'] = device.id
        device_data['name'] = device.device_name
        device_data['status'] = device.status
        output.append(device_data)

    return jsonify({'devices': output})


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
def add_devices():
    data = request.get_json()
    new_device = Devices(device_name=data['name'], status=False)
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
