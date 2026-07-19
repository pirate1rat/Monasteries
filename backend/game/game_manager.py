import datetime
import time
import random
from uuid import uuid4, UUID

from backend.models.lobby import Lobby
from backend.models.time_control import TimeControl
from backend.models.enums import PlayerColor, GameResult
from backend.game.game import Game

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game import Game

LOBBY_TIMEOUT_MINUTES = 15

OPPOSITE: dict[PlayerColor, PlayerColor] = {
    PlayerColor.WHITE: PlayerColor.RED,
    PlayerColor.RED: PlayerColor.WHITE,
}

class GameManager:
    _instance = None
    _initialized = False

    def __new__(cls: GameManager, *args, **kwargs):
        if cls._instance is None: 
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, socketio):
        if not self._initialized:
            self._socketio = socketio

            self.active_games: dict[int, "Game"] = {}
            self.active_lobbies: dict[UUID, Lobby] = {}
            self._next_game_id: int = 1
            self._initialized = True
        
    def create_lobby(self, host_id: int, host_color: PlayerColor, time_control: TimeControl) -> Lobby:
        new_lobby_uuid = uuid4()
        new_lobby =  Lobby(
            new_lobby_uuid,
            host_id, 
            host_color,
            time_control,
            datetime.datetime.now()
        )
        self.active_lobbies[new_lobby_uuid] = new_lobby
        return new_lobby

    def cancel_lobby(self, lobby_id: UUID, host_id) -> bool:
        """
        Returns False if lobby doesn't exist
        """

        lobby = self.active_lobbies.get(lobby_id)
        if lobby is None:
            return False
        del self.active_lobbies[lobby_id]
        return True
    
    def create_game(self, white_id: int, red_id: int, time_control: TimeControl) -> "Game":
        self._next_game_id += 1

        return Game(
            self._next_game_id,
            white_id,
            red_id,
            time_control
        )

    def join_lobby(self, lobby_id, player_id) -> "Game" | None:
        """
        Pairs the player with the host, creates a Game, and removes the lobby. 
        Returns None if the lobby does not exist or if the player tries to join 
        their own lobby.
        """

        lobby = self.active_lobbies.get(lobby_id)
        if lobby_id is None: 
            return None

        if lobby.host_color == PlayerColor.NEUTRAL:
            host_color = random.choice([PlayerColor.WHITE, PlayerColor.RED])
        else:
            host_color = lobby.host_color
        
        if host_color == PlayerColor.WHITE:
            white_id, red_id = lobby.host_id, player_id
        else:
            white_id, red_id = player_id, lobby.host_id

        game = self.create_game(white_id, red_id, lobby.time_control)
        self.active_games[game.game_id] = game
        del self.active_lobbies[lobby.lobby_id]

        return game

    def get_game(self, game_id) -> "Game" | None:
        return self.active_games[game_id]

    def get_game_for_player(self, player_id) -> Game | None:
        for game in self.active_games.values():
            if player_id in game.players.keys(): return game
        
        return None

    def cleanup_stale_lobbies(self):
        """
        Removes lobbies older than LOBBY_TIMEOUT_MINUTES. Returns a list of removed 
        lobby IDs (for notifying clients if needed).
        """

        cutoff = datetime.datetime.now() - datetime.timedelta(minutes=LOBBY_TIMEOUT_MINUTES)
        stale = [l_id for l_id, lobby in self.active_lobbies.items() if lobby.created_at < cutoff]
        for l_id in stale:
            del self.active_lobbies[l_id]
        return stale

    def handle_disconnect(self, game_id: int, player_id: int) -> bool:
        """
        Starts the disconnection timer. The on_timeout callback calls end_game
        and emits an event through Socket.IO — Game does not do this itself.
        Returns False if the game does not exist.
        """

        game = self.get_game(game_id)
        if game is None:
            return False

        def on_timeout(gid: int, result: GameResult):
            self.end_game(gid)
            #TODO

        game.on_player_disconnect(player_id, on_timeout)
        return True

    def handle_reconnect(self, game_id: int, player_id: int) -> bool:
        """
        Return False if game doesn't exist
        """

        game = self.get_game(game_id)
        if game is None:
            return False
        game.on_player_reconnect(player_id)
        return True

    def end_game(self, game_id: int) -> bool:
        game = self.active_games.get(game_id, None)
        if game is None:
            return False
        #TODO saves to db

        return True

    def load_active_games_from_db(self):
        #TODO
        pass