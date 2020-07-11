from api import app, jsonify, request
from yeelight import discover_bulbs, Bulb


@app.route('/getbulbs', methods=['GET'])
def get_yeelight():
    bulb = discover_bulbs()
    return jsonify({'data': bulb}), 200


@app.route('/switch', methods=['POST'])
def switch_yeelight():
    data = request.get_json()
    bulb = Bulb(data['ip'])
    bulb.toggle()
    return jsonify({'data': 'switched'}), 200
