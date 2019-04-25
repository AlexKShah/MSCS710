from app import db

class Metric(db.Model):
    cpu_percent = db.Column(db.String(255))
    memory_percent = db.Column(db.String(255))
    name = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    num_threads = db.Column(db.String(255))
    pid = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return '<Metric {}>'.format(self.body)
