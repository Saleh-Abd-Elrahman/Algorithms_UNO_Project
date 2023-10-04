import random


class Card:
    def __init__(self, color, value):
        self.colors = color
        self.value = value


class Player:
    def __init__(self, id):
        self.id = id
        self.hand = []

    def draw(self, deck, num=1):
        for _ in range(num):
            self.hand.append(deck.pop_card())

    def play_card(self, index):
        return self.hand.pop(index)


class UnoGame:
    def __init__(self, num_players):
        self.num_players = num_players
        self.deck = self.build_deck()
        self.players = self.init_players()
        self.current_player_index = 0
        self.direction = 1
        self.discards = []
        random.shuffle(self.deck)

    def build_deck(self):
        colors = ["Red", "Green", "Yellow", "Blue"]
        numbers = list(range(10)) + ["Draw Two", "Skip", "Reverse"]
        wilds = ["Wild Card", "Wild Draw Four"]
        return [Card(color, value) for color in colors for value in numbers] \
            + [Card("", wild) for wild in wilds for _ in range(4)]

    def pop_card(self):
        return self.deck.pop()

    def init_players(self):
        return [Player(i) for i in range(self.num_players)]

    def play(self):
        # draw initial card
        self.discards.append(self.pop_card())
        # game loop
        while True:
            current_player = self.players[self.current_player_index]
            print("Current Player:", current_player.id)
            print("Top card:", self.discards[-1].colors, self.discards[-1].value)
            valid_card_indices = [i for i, card in enumerate(current_player.hand)
                                  if self.is_valid_play(card)]
            if valid_card_indices:
                # player chooses a valid card
                card_index = self.choose_card(valid_card_indices)
                self.discards.append(current_player.play_card(card_index))
                print("Player played:", self.discards[-1].colors, self.discards[-1].value)
            else:
                # player must draw a card
                current_player.draw(self)
            self.next_player()

    def is_valid_play(self, card):
        top_discard = self.discards[-1]
        return card.colors == top_discard.colors or card.value == top_discard.value

    def choose_card(self, valid_card_indices):
        return valid_card_indices[0]

    def next_player(self):
        def next_player(self):
            self.current_player = (self.current_player + 2) % len(self.players)


if __name__ == "__main__":
    game = UnoGame(4)
    game.play()
