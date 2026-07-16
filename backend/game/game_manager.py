from backend.models.lobby import Lobby
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game import Game

class GameManager:
    _instance = None
    _initialized = False

    def __new__(cls: GameManager, *args, **kwargs):
        if cls._instance is None: 
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.active_games: dict[int, Game] = {}
            self.active_lobbies: dict[str, Lobby] = {}
            self._initialized = True
        

    def create_lobby(self, host_id, host_color, time_control) -> Lobby:
        pass

    def cancel_lobby(self, lobby_id, host_id):
        pass

    def join_lobby(self, lobby_id, player_id) -> Game:
        pass

    def get_game(self, game_id) -> Game | None:
        pass

    def get_game_for_player(self, player_id) -> Game | None:
        pass

    def end_game(self, game):
        pass

    def cleanup_stale_lobbies(self):
        pass

    def load_active_games_from_db(self):
        pass