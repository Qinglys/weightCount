from weight_count.src.exts import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50))
    remark = db.Column(db.String(100), default='')


class Weight(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'))
    weight = db.Column(db.Float)
    date = db.Column(db.Date)
