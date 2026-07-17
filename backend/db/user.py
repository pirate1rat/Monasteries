import datetime
from backend.app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(12), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    ranking = db.Column(db.Integer, default=500, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.datetime.now())

    def __repr__(self):
        return f"<User {self.user_id} name: {self.username}, ranking: {self.ranking}, created at: {self.created_at}>"
    
    def get_id(self):
        return str(self.user_id)