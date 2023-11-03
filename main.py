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
            UNO_Deck.append(wild)


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

    for player in range(Num_Players):
        Players.append(draw_cards(7, Game_Deck))

    return Players, Game_Deck

def current_hand(Current_Player, Players_Hand):
    print("Player {}".format(Current_Player + 1), "is now playing.")
    print("Your Current Hand:")
    print("......................")
    i = 1
    for card in Players_Hand:
        print(i, card)
        i = i+1
    print(" ")

    return

def valid_card(color, value, Players_Hand):

    for card in Players_Hand:

        if "Wild" in card:
            return True

        elif color in card or value in card:
            return True

    return False


def start_game():
    global Game_Deck
    global Discards
    global CardValue
    global Current_Color
    global Player_Number
    global Players

    Players = []

    Discards = []

    Game_Deck = build_UNO_Deck()
    Game_Deck = shuffle_UNO_Deck(Game_Deck)

    Player_Number = int(input("How Many People are playing: "))

    while Player_Number < 2 or Player_Number > 4:
        Player_Number = int(input("ERROR: Number of players invalid, please give a value of 2, up until 4: "))

    Players, Game_Deck = number_of_players(Player_Number, Game_Deck)

    Discards.append(Game_Deck.pop(0))
    splitCard = Discards[0].split(" ", 1)
    Current_Color = splitCard[0]

    if Current_Color != "Wild":
        CardValue = splitCard[1]

    else:
        CardValue = "Any"


while Playing:
    Players = []

    PlayerTurn = 0

    current_hand(PlayerTurn, Players[PlayerTurn])

    print("Top of pile: {}".format(Discards[-1]))

    if valid_card(Current_Color, CardValue, Players[PlayerTurn]):
        ChosenCard = int(input("Please select a card to play: "))
        while not valid_card(Current_Color, CardValue, [Players[PlayerTurn][ChosenCard - 1]]):
            ChosenCard = int(input("Please choose a valid card to play: "))

        print("You have played {}".format(Players[PlayerTurn][ChosenCard - 1]))

        Discards.append(Players[PlayerTurn].pop(ChosenCard - 1))

    else:
        print("No cards available are valid to play, please pick up from pile.")
        Players[PlayerTurn].extend(draw_cards(1, Game_Deck))
    print(" ")

    PlayerTurn += 1

    if PlayerTurn == Player_Number:
        PlayerTurn = 0

    elif PlayerTurn < 0:
        PlayerTurn = Player_Number - 1






Current_Player = 1

start_game()