from api import app, db

subs = db.Table('subs',
                db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                db.Column('device_id', db.Integer, db.ForeignKey('devices.id'))
                )


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))

    # one-to-many relationship
    owned_devices = db.relationship('Devices', backref='owner')
    # many-to-many relationship
    user_devices = db.relationship(
        'Devices', secondary=subs, backref=db.backref('subscribers', lazy='dynamic'))


class Rooms(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    # one-to-many relationship
    room_devices = db.relationship('Devices', backref='room')


class Devices(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    device_name = db.Column(db.String(50))
    status = db.Column(db.Boolean)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'))
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
