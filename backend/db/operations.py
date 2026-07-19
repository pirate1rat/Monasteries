import datetime

from backend.db.game_record import GameRecord
from backend.db.user import User
from backend.app import db
from backend.models.enums import PlayerColor, GameStatus

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from backend.game.game import Game

# USER
def create_user(username: str, email: str, password: str) -> User:
    new_user = User(
        username=username,
        email=email,
        password=password
    )

    db.session.add(new_user)
    db.session.commit()
    return new_user

def username_exists(username: str) -> bool:
    return db.session.query(User).filter_by(username=username).first() is not None

def email_exists(email: str) -> bool:
    return db.session.query(User).filter_by(email=email).first() is not None

def get_user_by_id(user_id: int) -> User | None:
    return db.session.get(User, user_id)

def get_user_by_email(email: str) -> User | None:
    return db.session.query(User).filter_by(email=email).first()

def update_ranking(user_id: int, new_ranking: int) -> bool:
    user = db.session.get(User, user_id)
    if user is None:
        return False
    
    user.ranking = new_ranking
    db.session.commit()
    return True

# GAMERECORD
def save_game(game: "Game"):
    game_record: GameRecord = db.session.get(GameRecord, game.game_id)

    if game_record is None:
        new_game_record = GameRecord(
            white_user_id=game.players.inverse[PlayerColor.WHITE],
            red_user_id=game.players.inverse[PlayerColor.RED],
            status=game.status,
            result=game.result,
            time_control=game.time_control,
            moves=game.get_moves_string(),
            created_at=game.started_at,
            finished_at=None,
        )

        db.session.add(new_game_record)
    else:
        game_record.moves = game.get_moves_string()
        game_record.status = game.status.value
        game_record.result = game.result.value if game.result else None
        game_record.finished_at = game.finished_at if game.status == GameStatus.FINISHED else None
    
    db.session.commit()

def get_game_record_by_id(game_id: int) -> GameRecord | None:
    return db.session.get(GameRecord, game_id)

def get_active_games() -> list[GameRecord] | None:
    return db.session.query(GameRecord).filter_by(status="in_progress").all()

def get_game_records_for_player(player_id: int) -> list[GameRecord] | None:
    return db.session.query(GameRecord).filter(
        (GameRecord.white_user_id == player_id) or
        (GameRecord.red_user_id == player_id)
    ).all()