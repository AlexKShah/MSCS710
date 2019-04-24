from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Metric(db.Model):
    pid = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    memory_percent = db.Column(db.String(255))
    cpu_percent = db.Column(db.String(255))
    num_threads = db.Column(db.String(255))
    name = db.Column(db.String(255))

    def __repr__(self):
        return '<Metric {}>'.format(self.body)
