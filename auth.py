from api import app, db, jwt, jsonify, request, make_response, cors
from flask_jwt_extended import (
    jwt_required, create_access_token,
    get_jwt_identity, get_raw_jwt
)
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from models import Users


blacklist = set()


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist


@app.route('/signup', methods=['POST'])
def add_user():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    data = request.get_json()

    user = Users.query.filter_by(email=data['email']).first()
    if user:
        return jsonify({'msg': "email already exists. Kindly Login."}), 403

    hashpassword = generate_password_hash(data['password'], method='sha256')
    new_user = Users(public_id=str(
        uuid.uuid4()), name=data['name'], email=data['email'], password=hashpassword)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'msg': 'New user created. Login to continue.'}), 200


@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    if not email:
        return make_response({'msg': 'email missing'}, 401, {'WWW-Authenticate': 'Basic realm="email missing"'})
    if not password:
        return make_response({'msg': 'password missing'}, 401, {'WWW-Authenticate': 'Basic realm="password missing"'})
    user = Users.query.filter_by(email=email).first()

    if not user:
        return make_response({'msg': 'User not Found'}, 401, {'WWW-Authenticate': 'Basic realm="User not found"'})
    if check_password_hash(user.password, password):
        # Identity can be any data that is json serializable
        access_token = create_access_token(identity=user.public_id)
        return jsonify({'msg': 'successfully logged in', 'token': access_token}), 200
    return make_response({'msg': 'Incorrect Credentials'}, 401, {'WWW-Authenticate': 'Basic realm="Incorrect credentials"'})


@app.route('/userdetails', methods=['GET'])
@jwt_required
def get_user():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()

    user = Users.query.filter_by(public_id=current_user).first()
    if not user:
        return jsonify({'message': 'User not Found'}), 404

    user_data = {}
    user_data['name'] = user.name
    user_data['email'] = user.email

    return jsonify({'data': user_data}), 200


# Endpoint for revoking the current users access token
@app.route('/logout', methods=['DELETE'])
@jwt_required
def logout():
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)
    return jsonify({"msg": "Successfully logged out"}), 200
