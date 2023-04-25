from datetime import datetime
from hashlib import md5
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

membership = db.Table(
    'membership',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('club_id', db.Integer, db.ForeignKey('club.id'))
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    grade = db.Column(db.Integer)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    joined = db.relationship(
        'Club', secondary=membership,
        backref=db.backref('memership', lazy='dynamic'), viewonly=True, lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Club(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), index=True, unique=True)
    description = db.Column(db.String(300))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_name = db.Column(db.String(40))
    members = db.relationship('User', secondary=membership, backref=db.backref(
    'membership', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<{} Club>'.format(self.name)

    def join(self, user):
        if not self.is_joined(user):
            self.members.append(user)

    def unjoin(self, user):
        if self.is_joined(user):
            self.members.remove(user)

    def is_joined(self, user):
        return self.members.filter(
            membership.c.user_id == user.id).count() > 0
