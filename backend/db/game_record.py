import datetime 
from backend.app import db

class GameRecord(db.Model):
    __tablename__ = "games"
    game_id = db.Column(db.Integer, primary_key=True)
    white_user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=True)
    red_user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=True)

    status = db.Column(db.String, nullable=False, default="in_progress")
    result = db.Column(db.String, nullable=True)
    time_control = db.Column(db.JSON, nullable=True)
    moves = db.Column(db.Text, nullable=True, default="")

    created_at = db.Column(db.DateTime, nullable=False)
    started_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.datetime.now())
    finished_at = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"<Game {self.game_id} white: {self.white_user_id}, red: {self.red_user_id}, created at: {self.created_at}>"