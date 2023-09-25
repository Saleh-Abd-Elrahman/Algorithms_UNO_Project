import random
import time

Game_Deck =[]

Playing = True

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

def draw_cards(NumCards, GameDeck):

    Drawn_Cards = []

    for i in range(NumCards):
        Drawn_Cards.append(Game_Deck.pop(0))
    return Drawn_Cards

def number_of_players(Num_Players, Game_Deck):

    Players = []

    for player in range(Num_Players):
        Players.append(draw_cards(7, Game_Deck))

    return Players, Game_Deck

def current_hand(Current_Player, Players_Hand):
    print("Player {}".format(Current_Player + 1), "is now playing.")
    print("Your Current Hand:")
    print("......................")
    for card in Players_Hand:
        i = 1
        print(i, card)
        i = i+1
    print(" ")

    return

def valid_card():

    return
def start_game():
    global Game_Deck

    while Playing:

        Discards = []

        PlayerTurn = 0

        Game_Deck = build_UNO_Deck()
        Game_Deck = shuffle_UNO_Deck(Game_Deck)

        Player_Number = int(input("How Many People are playing: "))

        while Player_Number < 2 or Player_Number > 4:
            Player_Number = int(input("ERROR: Number of players invalid, please give a value of 2, up until 4: "))

        Players, Game_Deck = number_of_players(Player_Number, Game_Deck)

        Discards.append(Game_Deck.pop(0))

        print(Players)

        current_hand(PlayerTurn, Players[PlayerTurn])

        print("Top of pile: {}".format(Discards[-1]))


        return

    return


Current_Player = 1

start_game()