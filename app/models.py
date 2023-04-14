from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5

members = db.Table('followers',
    db.Column('member_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('club_id', db.Integer, db.ForeignKey('club.id'))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    joined = db.relationship(
        'User', secondary=members,
        primaryjoin=(members.c.member_id == id),
        secondaryjoin=(members.c.member_id == id),
        backref=db.backref('members', lazy='dynamic'), lazy='dynamic')


    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def join(self, user):
        if not self.is_member(user):
            self.joined.append(user)

    def unjoin(self, user):
        if self.is_member(user):
            self.joined.remove(user)

    def is_member(self, user):
        return self.members.filter(
            members.c.club_id == user.id).count() > 0

    def joined_clubs(self):
        return Club.query.join(
            members, (members.c.club_id == Club.user_id)).filter(
                members.c.member_id == self.id)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Club(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), index=True, unique=True)
    description = db.Column(db.String(300))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_name = db.Column(db.String(40))

    def __repr__(self):
        return '<{} Club>'.format(self.name)
