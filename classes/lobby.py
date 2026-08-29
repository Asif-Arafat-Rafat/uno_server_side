class Lobby:

    def __init__(self, code):
        self.code = code
        self.players = {}

    def add_player(self, player_id):
        self.players[player_id] = {
            "connected": True
        }

    def remove_player(self, player_id):
        del self.players[player_id]

    def player_count(self):
        return len(self.players)