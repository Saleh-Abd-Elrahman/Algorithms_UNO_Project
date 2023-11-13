import random
from collections import deque

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def pop(self, index):
        if index == 0:
            data = self.head.data
            self.head = self.head.next
            return data
        else:
            current = self.head
            for _ in range(index - 1):
                current = current.next
            data = current.next.data
            current.next = current.next.next
            return data

    def __iter__(self):
        current = self.head
        while current:
            yield current.data
            current = current.next

class UNOGame:
    def __init__(self, num_players):
        self.colors = ["Red", "Green", "Yellow", "Blue"]
        self.num_players = num_players
        self.numbers = [str(i) for i in range(10)]
        self.specials = ["Draw Two", "Skip", "Reverse"]
        self.wilds = ["Wild Card", "Wild Draw Four"]
        self.players = [LinkedList() for _ in range(num_players)]
        self.current_player = 0
        self.direction = 1

        self.game_deck = deque()
        for color in self.colors:
            for number in self.numbers:
                for _ in range(2):
                    if number == "0":
                        card = f"{color} {number}"
                    else:
                        card = f"{color} {number}"
                    self.game_deck.append(card)
            for special in self.specials:
                card = f"{color} {special}"
                self.game_deck.extend([card] * 2)
        for _ in range(4):
            self.game_deck.extend(self.wilds)
        random.shuffle(self.game_deck)
        self.top_card = self.game_deck.popleft()
        while self.top_card.startswith("Wild") or self.top_card.split()[1] in self.specials:
            self.top_card = self.game_deck.popleft()
        self.split_card = self.top_card.split(maxsplit=1)

        # Change players to a list of linked lists
        self.players = [LinkedList() for _ in range(num_players)]
        self.current_player = 0
        self.direction = 1
        self.discards = [self.top_card]
        self.current_color, self.card_value = self.split_card

        self.card_priority = {
            "Draw Two": 5,
            "Skip": 5,
            "Reverse": 5,
            "Wild Card": 10,
            "Wild Draw Four": 10
        }

    def draw_cards(self, num_cards):
        drawn_cards = []
        for _ in range(num_cards):
            drawn_cards.append(self.game_deck.popleft())
        return drawn_cards

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

    def handle_seven_rule(self):
        print("Seven Rule Activated! You can swap hands with another player.")
        target_player = int(input("Choose a player to swap hands with (1 to {}): ".format(self.num_players))) - 1

        while not (0 <= target_player < self.num_players) or target_player == self.current_player:
            target_player = int(
                input("Invalid option. Choose a different player (1 to {}): ".format(self.num_players))) - 1

        self.players[self.current_player], self.players[target_player] = (
            self.players[target_player],
            self.players[self.current_player],
        )

    def handle_zero_rule(self):
        print("Zero Rule Activated! All players pass their hands to the next player in the direction of play.")
        self.current_player = (self.current_player + self.direction) % self.num_players

        for i in range(self.num_players):
            next_player = (self.current_player + self.direction) % self.num_players
            self.players[self.current_player], self.players[next_player] = (
                self.players[next_player],
                self.players[self.current_player],
            )
            self.current_player = next_player

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

            while not (0 <= chosen_card < len(self.players[self.current_player])):
                chosen_card = int(input("Please choose a valid card to play: ")) - 1

            played_card = self.players[self.current_player].pop(chosen_card)

            if played_card.split()[1] == "7":
                self.handle_seven_rule()

            if played_card.split()[1] == "0":
                self.handle_zero_rule()

            print("You have played", played_card)
            self.discards.append(played_card)

        else:
            print(f"Player {self.current_player + 1} No cards are valid to play, please pick up from the pile.")
            drawn_card = self.draw_cards(1)
            print("You have drawn:", drawn_card[0])
            drawn_card = drawn_card[0]
            if self.valid_card(self.current_color, self.card_value, [drawn_card]):
                self.players[self.current_player].append(drawn_card)
            else:
                print("The drawn card is not a valid play.")

        split_card = self.discards[-1].split(maxsplit=1)
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