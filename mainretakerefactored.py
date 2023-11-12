import random


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
        self.game_deck, self.top_card, self.split_card = self.build_and_shuffle_deck()
        self.discards = [self.top_card]
        self.current_color, self.card_value = self.split_card

        self.card_priority = {
            "Draw Two": 5,
            "Skip": 5,
            "Reverse": 5,
            "Wild Card": 10,
            "Wild Draw Four": 10
        }

    # Time Complexity of build_and_shuffle_deck(): O(1) on
    # initialization as the deck size remains constant.
    def build_and_shuffle_deck(self):
        game_deck = []

        for color in self.colors:
            for number in self.numbers:
                for _ in range(2):
                    if number == "0":
                        card = f"{color} {number}"
                    else:
                        card = f"{color} {number}"
                    game_deck.append(card)

            for special in self.specials:
                card = f"{color} {special}"
                game_deck.extend([card] * 2)

        for _ in range(4):
            game_deck.extend(self.wilds)

        random.shuffle(game_deck)
        top_card = game_deck.pop(0)

        while top_card.startswith("Wild") or top_card.split()[1] in self.specials:
            random.shuffle(game_deck)
            top_card = game_deck.pop(0)

        split_card = top_card.split()
        return game_deck, top_card, split_card

    # The draw_cards method pops cards from the deck, which has a time complexity of O(1) for each card drawn.
    # If you draw 'n' cards, the time complexity for drawing all of them is O(n).
    def draw_cards(self, num_cards):
        drawn_cards = []
        for _ in range(num_cards):
            drawn_cards.append(self.game_deck.pop(0))
        return drawn_cards

    # The valid_card method checks if there's a valid card in the player's hand, which requires
    # iterating through the player's hand (usually 7 cards).
    # So the time complexity is O(7) in the worst case, which simplifies to
    # O(1) since the number of cards in a player's hand is constant.
    def valid_card(self, color, value, player_hand):
        for card in player_hand:
            card_parts = card.split()
            if "Wild" in card or (len(card_parts) == 2 and (color == card_parts[0] or value == card_parts[1])):
                return True
        return False

    def suggest_best_card(self):
        valid_cards = [card for card in self.players[self.current_player] if self.valid_card(
            self.current_color, self.card_value, [card])]

        if not valid_cards:
            print("No valid cards to suggest.")
            return

        # Sort valid cards based on priority values
        sorted_cards = sorted(valid_cards, key=lambda x: self.card_priority.get(x.split()[1], 0), reverse=True)

        print("Suggested cards to play:")
        for i, card in enumerate(sorted_cards, start=1):
            print("{}. ".format(i), card)

    def current_hand(self):

        # The current_hand method iterates through the player's hand,
        # so the time complexity is O(n) as worst case, where n represents the total
        # number of cards the player currently has in their hand.
        # Best case would be O(1), where player has only a single card remaining.

        print(f"Player {self.current_player + 1} is now playing.")
        print("Your Current Hand:")
        print("......................")

        sorted_hand = sorted(self.players[self.current_player], key=lambda x: (x.split()[0], x.split()[1]))

        for i, card in enumerate(sorted_hand, start=1):
            print("{}. ".format(i), card)
        print(" ")

    def start_game(self):
        while self.num_players < 2 or self.num_players > 4:
            try:
                self.num_players = int(input("How Many People are playing: "))
                if not (2 <= self.num_players <= 4):
                    print("ERROR: Number of players invalid, please give a value of 2, up to 4.")
            except ValueError:
                print("ERROR: Please enter a valid integer.")

        self.number_of_players()

    # The number_of_players method initializes the game with 7 cards for each player,
    # which is O(num_players) in time complexity. Value is always between 2 and 4,
    # so the worst case and best case are effectively O(4) and O(2) respectively.
    def number_of_players(self):
        print(f"Starting game with {len(self.game_deck)} cards in deck.")
        for player in range(self.num_players):
            self.players[player] = self.draw_cards(7)
            print(f"Player {player + 1} initial cards: {self.players[player]}")

    # The play_turn method involves various conditional statements,
    # but in the worst case, it doesn't depend on the number of players or
    # cards in the deck. So, the time complexity is constant, O(1).
    def play_turn(self):
        self.current_hand()
        print("Top of pile:", self.discards[-1])

        if self.valid_card(self.current_color, self.card_value, self.players[self.current_player]):
            chosen_card = int(input("Please select a card to play or enter '0' to see suggestions: ")) - 1

            if chosen_card == -1:
                self.suggest_best_card()
                chosen_card = int(input("Please select a card to play: ")) - 1

            while not (0 <= chosen_card < len(self.players[self.current_player])) or not self.valid_card(
                    self.current_color, self.card_value, [self.players[self.current_player][chosen_card]]):
                chosen_card = int(input("Please choose a valid card to play: ")) - 1

            print("You have played", self.players[self.current_player][chosen_card])
            self.discards.append(self.players[self.current_player].pop(chosen_card))
        else:
            print(f"Player {self.current_player + 1} No cards are valid to play, please pick up from the pile.")
            self.players[self.current_player].extend(self.draw_cards(1))

        split_card = self.discards[-1].split()
        self.current_color, self.card_value = split_card

        if self.current_color == "Wild":
            for i, color in enumerate(self.colors, start=1):
                print(f"{i} {color}")
            color_update = int(input("What color would you like to change to: ")) - 1

            while color_update < 0 or color_update >= len(self.colors):
                color_update = int(input("Invalid Option Given. What color would you like to change to: ")) - 1

            self.current_color = self.colors[color_update]
            print("Colour has been changed to:", self.current_color)

            if self.card_value == "Draw Four":
                next_player = (self.current_player + self.direction) % self.num_players
                print(f"Player {next_player + 1} is drawing 4 more cards.")
                self.players[next_player].extend(self.draw_cards(4))

        if self.card_value == "Reverse":
            print("Direction of play has been reversed.")
            self.direction *= -1

        if self.card_value == "Skip":
            print("Next Player has been skipped.")
            self.current_player = (self.current_player + self.direction) % self.num_players

        if self.card_value == "Draw Two":
            next_player = (self.current_player + self.direction) % self.num_players
            print(f"Player {next_player + 1} is drawing 2 more cards.")
            self.players[next_player].extend(self.draw_cards(2))

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
            self.start_game()
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
