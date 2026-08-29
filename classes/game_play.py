from classes.uno_table import Table
class Game():
    def __init__(self, lobby_id, players):
        self.lobby_id = lobby_id
        self.table = Table(players)
    def start_game(self):
        self.table.start_game()
        return self.table.get_data()
