from classes.card import Card
class Deck:
    def __init__(self):
        self.cards = []
        self.deck=[]
        self.user_decks={}
        self.gen_deck()
        self.shuffle()
    def add_user_deck(self, player_id):
        self.user_decks[player_id] = []
        for _ in range(7):
            self.user_decks[player_id].append(self.draw_card())
    def add_card_to_user(self, player_id, cards):
        for _ in range(cards):
            card = self.draw_card()
            self.user_decks[player_id].append(card)
    def gen_deck(self):
        color= ["red", "green", "blue", "yellow"]
        for c in color:
            self.cards.append(Card(c, 0, "number"))
            for i in range(1, 10):
                self.cards.append(Card(c, i, "number"))
                self.cards.append(Card(c, i, "number"))
            self.cards.append(Card(c, 20, "skip"))
            self.cards.append(Card(c, 20, "skip"))
            self.cards.append(Card(c, 50, "reverse"))   
            self.cards.append(Card(c, 50, "reverse"))   
            self.cards.append(Card(c, 70, "draw_two"))   
            self.cards.append(Card(c, 70, "draw_two"))   
        for i in range(4):
            self.cards.append(Card("black", 100, "wild"))
            self.cards.append(Card("black", 200, "wild_4"))
    def deck_redo(self):
        self.deck = self.cards.copy()
        for player_id in self.user_decks:
            for card in self.user_decks[player_id]:
                self.deck.remove(card)
    def shuffle(self):
        import random
        self.deck =self.cards.copy()
        random.shuffle(self.deck)
    def draw_card(self):
        if len(self.deck) == 0:
            self.deck_redo()
            self.shuffle()
        return self.deck.pop() 
    def remove_card(self, player_id, card):
        self.user_decks[player_id].remove(card)
