import random
import time

Game_Deck = []
Players = []
Discards = []
CardValue = ""
Current_Color = ""
Player_Number = 0


def build_UNO_Deck():
    colors = ["Red", "Green", "Yellow", "Blue"]
    numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    specials = ["Draw Two", "Skip", "Reverse"]
    wilds = ["Wild Card", "Wild Draw Four"]

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

    return UNO_Deck


def shuffle_UNO_Deck(UNO_Deck):
    for cardPos in range(len(UNO_Deck)):
        randPos = random.randint(0, 107)
        UNO_Deck[cardPos], UNO_Deck[randPos] = UNO_Deck[randPos], UNO_Deck[cardPos]
    return UNO_Deck


def draw_cards(NumCards, GameDeck):
    Drawn_Cards = []

    for i in range(NumCards):
        Drawn_Cards.append(GameDeck.pop(0))
    return Drawn_Cards


def number_of_players(Num_Players, GameDeck):
    for player in range(Num_Players):
        Players.append(draw_cards(7, GameDeck))


def current_hand(Current_Player):
    print("Player {}".format(Current_Player + 1), "is now playing.")
    print("Your Current Hand:")
    print("......................")
    i = 1
    for card in Players[Current_Player]:
        print(i, card)
        i = i + 1
    print(" ")


def valid_card(color, value, Players_Hand):
    for card in Players_Hand:
        card_color, card_value = card.split(" ", 1)
        if "Wild" in card:
            return True
        elif color == card_color or value == card_value:
            return True
    return False


def start_game():
    global Game_Deck, Discards, CardValue, Current_Color, Player_Number, Players
    Discards = []
    Game_Deck = build_UNO_Deck()
    Game_Deck = shuffle_UNO_Deck(Game_Deck)

    while Player_Number is None or Player_Number < 2 or Player_Number > 4:
        try:
            Player_Number = int(input("How Many People are playing: "))
            if not (2 <= Player_Number <= 4):
                print("ERROR: Number of players invalid, please give a value of 2, up until 4.")
        except ValueError:
            print("ERROR: Please enter a valid integer.")


    number_of_players(Player_Number, Game_Deck)

    top_card = Game_Deck.pop(0)

    # add code here to check whether top card is special or wild and to remove if the case
    
    Discards.append(top_card)
    split_card = top_card.split(" ", 1)
    Current_Color = split_card[0]

    if Current_Color != "Wild":
        CardValue = split_card[1]
    else:
        CardValue = "Any"


start_game()
Direction = 1
PlayerTurn = 0

while True:
    colors = ["Red", "Green", "Yellow", "Blue"]
    current_hand(PlayerTurn)
    print("Top of pile: {}".format(Discards[-1]))

    if valid_card(Current_Color, CardValue, Players[PlayerTurn]):
        ChosenCard = int(input("Please select a card to play: "))
        while not valid_card(Current_Color, CardValue, [Players[PlayerTurn][ChosenCard - 1]]):
            ChosenCard = int(input("Please choose a valid card to play: "))

        print("You have played {}".format(Players[PlayerTurn][ChosenCard - 1]))
        Discards.append(Players[PlayerTurn].pop(ChosenCard - 1))


    else:
        print("Player {}".format(Players[PlayerTurn]), "No cards available are valid to play, please pick up from the pile.")
        Players[PlayerTurn].extend(draw_cards(1, Game_Deck))

    print(" ")

    splitCard = Discards[-1].split(" ", 1)
    Current_Color = splitCard[0]

    if len(splitCard) == 1:
        CardValue = "Any"

    else:
        CardValue = splitCard[1]


    if Current_Color == "Wild":
        for i in range(len(colors)):
            print("{} {}".format(i+1, colors[i]))
        Color_Update = int(input("What color would you like to change to: "))

        while Color_Update < 1 or Color_Update > 4:
            Color_Update = int(input("Invalid Option Given. What color would you like to change to: "))

        Current_Color = colors[Color_Update - 1]

        if CardValue == "Draw Four":
            print("Player", PlayerTurn + 2, "is drawing 4 more cards.")
            Players[PlayerTurn + Direction].extend(draw_cards(4, Game_Deck))

    if CardValue == "Reverse":
        print("Direction of play has been reversed.")
        Direction = Direction * -1

    if CardValue == "Skip":
        print("Next Player has been skipped.")
        PlayerTurn += Direction

    if CardValue == "Draw Two":
        print("Player", PlayerTurn + 2, "is drawing 2 more cards.")
        Players[PlayerTurn + Direction].extend(draw_cards(2, Game_Deck))


    PlayerTurn += Direction

    if PlayerTurn >= Player_Number:
        PlayerTurn = 0
    elif PlayerTurn < 0:
        PlayerTurn = Player_Number - 1
