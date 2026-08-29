from classes.deck import Deck
class Table:
    def __init__(self, players):
        self.current_card = None
        self.direction = 'CW'
        self.turn=0
        self.players = players
        self.color=None
        self.deck = Deck()
    def start_game(self):
        for player in self.players:
            self.deck.add_user_deck(player)
        self.current_card = self.deck.draw_card()
        self.color = self.current_card.color
    def change_direction(self):
        if self.direction == 'CW':
            self.direction = 'CCW'
        else:
            self.direction = 'CW'
    def next_turn(self):
        if self.direction == 'CW':
            self.turn = (self.turn + 1) % len(self.players)
        else:
            self.turn = (self.turn - 1) % len(self.players)
    def skip_turn(self):
        if self.direction == 'CW':
            self.turn = (self.turn + 2) % len(self.players)
        else:
            self.turn = (self.turn - 2) % len(self.players)
    def color_change(self, new_color):
        self.color = new_color
    def add_card(self, card_quantity):
        if self.direction == 'CW':
            self.deck.add_card_to_user(self.players[(self.turn + 1) % len(self.players)], card_quantity)
        else:
            self.deck.add_card_to_user(self.players[(self.turn - 1) % len(self.players)], card_quantity)
        self.skip_turn()
    def play(self, card=None, color=None):
        if card is None:
            self.next_turn()
        else:
            self.current_card = card
            self.deck.remove_card(self.players[self.turn], card)
            if color is None:
                self.color = card.color
            else:
                self.color = color
            if card.type == "reverse":
                self.change_direction()
                self.next_turn()
            elif card.type == "skip":
                self.skip_turn()
            elif card.type == "draw_two":
                self.add_card(2)
            elif card.type == "wild_4" :
                self.add_card(4)
            elif card.type == "wild":
                self.next_turn()
    def no_playable_card(self):
        self.deck.add_card_to_user(self.players[self.turn], 1)
    def get_data(self):
        return {
            "current_card": {
                "color": self.current_card.color,
                "value": self.current_card.value,
                "type": self.current_card.type
            },
            "direction": self.direction,
            "turn": self.players[self.turn],
            "players": self.players,
            "color": self.color,
            "deck": {
                player: [
                    {
                        "color": card.color,
                        "value": card.value,
                        "type": card.type
                    }
                    for card in cards
                ]
                for player, cards in self.deck.user_decks.items()
            }
        }