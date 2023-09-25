import random

def build_UNO_Deck():

    colors = ["Red", "Green", "Yellow", "Blue"]
    numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    specials = ["Draw Two", "Skip", "Reverse"]
    wilds = ["Wild", "Wild Draw Four"]

    UNO_Deck = []

    for color in colors:
        for number in numbers:
            New_Card = "{} {}".format(color, number)
            UNO_Deck.append(New_Card)
            if number != 0:
                UNO_Deck.append(New_Card)

        for special in specials:
            New_Card = "{} {}".format(color, special)
            UNO_Deck.append(New_Card)
            if number != 0:
                UNO_Deck.append(New_Card)

        for i in range(4):
            for wild in wilds:
                New_Card = "{} {}".format(color, wild)
                UNO_Deck.append(New_Card)


    print(UNO_Deck)
    return UNO_Deck

def shuffle_UNO_Deck(UNO_Deck):
    for cardPos in range(len(UNO_Deck)):
        randPos = random.randint(0, 107)
        UNO_Deck[cardPos], UNO_Deck[randPos] = UNO_Deck[randPos], UNO_Deck[cardPos]
    return UNO_Deck

def draw_cards(NumCards):

    Drawn_Cards = []

    for i in range(NumCards):
        Drawn_Cards.append(Game_Deck.pop(0))
    return Drawn_Cards

def number_of_players(Num_Players):

    Players = []

    for player in range(Num_Players):
        Players.append(draw_cards(7))

    return Players

def start_game():
    return

Game_Deck = build_UNO_Deck()
Game_Deck = shuffle_UNO_Deck(Game_Deck)

Players = number_of_players(4)
print(Players)