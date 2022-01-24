from db import db


class UserModel(db.Model):
    __tablename__ = "mst_user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    password = db.Column(db.String(30))

    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password

    def json(self):
        return {"username": self.username, "password": self.password}
    
    @classmethod
    def find_by_username(cls, username):
        # SELECT * FROM items WHERE username=username LIMIT 1
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def find_by_username_pass(cls, username, password):
        # SELECT * FROM items WHERE username=username and password=password LIMIT 1
        return cls.query.filter_by(username=username, password=password).first()
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()