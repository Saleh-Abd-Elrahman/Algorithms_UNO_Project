from collections import deque
import random


class Card:
    def __init__(self, value, color):
        self.value = value
        self.color = color

    def effect(self, game):
        pass


class ReverseCard(Card):
    def __init__(self, color):
        super().__init__("Reverse", color)

    def effect(self, game):
        game.direction *= -1
        print("Direction of play has been reversed.")


class SkipCard(Card):
    def __init__(self, color):
        super().__init__("Skip", color)

    def effect(self, game):
        game.current_player = (game.current_player + game.direction) % game.num_players
        print("Next Player has been skipped.")


class DrawTwoCard(Card):
    def __init__(self, color):
        super().__init__("Draw Two", color)

    def effect(self, game):
        next_player = (game.current_player + game.direction) % game.num_players
        print(f"Player {next_player + 1} is drawing 2 more cards.")

        # Draw the cards for the next player only once
        game.players[next_player].extend(game.draw_cards(2))

        # Skip the next player's turn
        game.current_player = (game.current_player + game.direction) % game.num_players


class UNOGame:
    def __init__(self, num_players):
        self.num_players = num_players
        self.colors = ["Red", "Green", "Yellow", "Blue"]
        self.numbers = [str(i) for i in range(10)]
        self.specials = ["Draw Two", "Skip", "Reverse"]
        self.wilds = ["Wild Card", "Wild Draw Four"]
        self.players = [[] for _ in range(num_players)]
        self.current_player = 0
        self.direction = 1
        self.game_deck, top_card = self.build_and_shuffle_deck()
        self.discards = deque([top_card])
        self.current_color, self.card_value = top_card.color, top_card.value

        for player in range(self.num_players):
            self.players[player] = self.draw_cards(7)
            print(f"Player {player + 1} initial cards: {self.players[player]}")

    # rest of the code remains the same
    def current_hand(self):
        print(f"Player {self.current_player + 1} is now playing.")
        print("Your Current Hand:")
        print("......................")
        for i, card in enumerate(self.players[self.current_player], start=1):
            print("{}. ".format(i), card.color, card.value)
        print(" ")

    def number_of_players(self):
        print(f"Starting game with {len(self.game_deck)} cards in deck.")


    def build_and_shuffle_deck(self):
        game_deck = deque()

        for color in self.colors:
            for number in self.numbers:
                for _ in range(2):
                    if number == "0":
                        card = Card(number, color)
                    else:
                        card = Card(number, color)
                    game_deck.append(card)

            for special in self.specials:
                card = Card(special, color)
                game_deck.extend([card] * 2)

        for _ in range(4):
            game_deck.extend([Card("Wild", "Wild")] * 1)

        random.shuffle(game_deck)
        top_card = game_deck.popleft()

        while top_card.value == "Wild" or top_card.value in self.specials:
            random.shuffle(game_deck)
            top_card = game_deck.popleft()

        return game_deck, top_card

    def draw_cards(self, num_cards):
        drawn_cards = [self.game_deck.popleft() for _ in range(num_cards)]
        return drawn_cards

    def valid_card(self, color, value, player_hand):
        for card in player_hand:
            if card.value == value or card.color == color or card.value in self.specials or card.value == "Wild":
                return True
        return False

    def play_turn(self):
        self.current_hand()

        if self.discards[-1].value == "Wild" and self.discards[-1].color == "Wild":
            print("Top of pile: Wild Card")
        else:
            print("Top of pile:", self.discards[-1].color, self.discards[-1].value)

        if self.valid_card(self.current_color, self.card_value, self.players[self.current_player]):
            chosen_card = int(input("Please select a card to play: ")) - 1

            while not (0 <= chosen_card < len(self.players[self.current_player])) or not self.valid_card(
                    self.current_color, self.card_value, [self.players[self.current_player][chosen_card]]):
                chosen_card = int(input("Please choose a valid card to play: ")) - 1

            played_card = self.players[self.current_player][chosen_card]
            print("You have played", played_card.color, played_card.value)
            self.discards.append(self.players[self.current_player].pop(chosen_card))

            # Check if the played card is a Draw Two card
            if played_card.value == "Draw Two":
                next_player = (self.current_player + self.direction) % self.num_players
                print(f"Player {next_player + 1} is drawing 2 more cards.")
                self.players[next_player].extend(self.draw_cards(2))

            # Update the current color and value after playing a card
            self.current_color, self.card_value = played_card.color, played_card.value

        else:
            print(f"Player {self.current_player + 1} No cards available are valid to play, please pick up from the pile.")
            drawn_card = self.draw_cards(1)[0]
            print("You have drawn", drawn_card.color, drawn_card.value)
            self.players[self.current_player].append(drawn_card)

            # Update the current color and value after drawing a card
            self.current_color, self.card_value = drawn_card.color, drawn_card.value

        if self.current_color == "Wild":
            for i, color in enumerate(self.colors, start=1):
                print(f"{i} {color}")
            color_update = int(input("What color would you like to change to: ")) - 1

            while color_update < 0 or color_update >= len(self.colors):
                color_update = int(input("Invalid Option Given. What color would you like to change to: ")) - 1

            self.current_color = self.colors[color_update]
            print("Colour has been changed to:", self.current_color)

            if self.card_value == "Wild Draw Four":
                next_player = (self.current_player + self.direction) % self.num_players
                print(f"Player {next_player + 1} is drawing 4 more cards.")
                self.players[next_player].extend(self.draw_cards(4))

        if self.card_value == "Reverse":
            ReverseCard(self.current_color).effect(self)

        if self.card_value == "Skip":
            SkipCard(self.current_color).effect(self)

        if self.card_value == "Draw Two":
            DrawTwoCard(self.current_color).effect(self)

        if len(self.players[self.current_player]) == 0:
            winner = "Player {}".format(self.current_player + 1)
            print("Game Over")
            print(winner)
            return

        self.current_player = (self.current_player + self.direction) % self.num_players

        if self.current_player < 0:
            self.current_player = self.num_players - 1

    # The play_game method consists of a loop where the game is played.
    # The loop continues indefinitely until the game ends. The time complexity depends on
    # how long the game is played.
    def play_game(self):
        while True:
            self.number_of_players()
            self.play_turn()


if __name__ == "__main__":
    num_players = None
    while num_players is None:
        try:
            num_players = int(input("How Many People are playing: "))
            if not (2 <= num_players <= 4):
                print("ERROR: Number of players invalid, please give a value of 2, up until 4.")
                num_players = None
        except ValueError:
            print("ERROR: Please enter a valid integer.")

    uno_game = UNOGame(num_players)
    uno_game.play_game()
