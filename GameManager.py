import Card
import csv
import random
from os import system
from pyfiglet import Figlet

class GameManager:
    def __init__(self):
        self._Player1Name = ""
        self._Player2Name = ""
        self._Player1Deck = []
        self._Player2Deck = []
        self._AllCards = []
        self._CardOnTable = Card.Card("","","")
        self._WildCardColour = ""
        self._Player1SkipsTurn = False
        self._Winner = ""

    @property
    def Player1Name(self):
        return self._Player1Name
    
    @Player1Name.setter
    def Player1Name(self, name):
        self._Player1Name = name

    @property
    def Player2Name(self):
        return self._Player2Name
    
    @Player2Name.setter
    def Player2Name(self, name):
        self._Player2Name = name

    @property
    def AllCards(self):
        return self._AllCards
    
    @property
    def Player1Deck(self):
        return self._Player1Deck
    
    @property
    def Player2Deck(self):
        return self._Player2Deck
    
    @property
    def CardOnTable(self):
        return self._CardOnTable
    
    @property
    def WildCardColour(self):
        return self._WildCardColour
    
    @property
    def Player1SkipsTurn(self):
        return self._Player1SkipsTurn

    @property
    def Winner(self):
        return self._Winner
        
    def ReadCSVFile(self):
        with open("Cards.csv", encoding="utf-8") as file:
            reader = csv.DictReader(file, fieldnames=["type", "colour", "number"])
            next(reader)
            for row in reader:
                UnoCard = Card.Card(row["type"],row["colour"],row["number"])
                self._AllCards.append(UnoCard)

    def PrintTutorial(self):
        print("==========================# Welcome to UNO PvP #===========================")
        print("Rules:")
        print(f"1) Match the cards: Players take turn to play a card from their deck that matches the top card of the discard pile by color or number") 
        print(f"2) Action cards: Use Skip, Reverse, Draw Two, Wild, and Wild Draw Four cards for special effects ( These have no numbers on them to match with ).")
        print(f"3) Draw if no match: Draw a card from the draw pile if you can't play a matching card; play if possible, otherwise pass")
        print(f"4) Win by playing all cards: The first player to get rid of all their cards wins the game")
        print(f"\nCards' Symbols:")
        print(f"- All cards consist of three parts as following (type of card, colour, number).")
        print(f"1) Normal Card: {self._AllCards[30]} -> Normal Card with the yellow colour and the number 6")
        print(f"2) Skip Card: {self._AllCards[84]} -> Skip Card with the red colour")
        print(f"3) Reverse Card: {self._AllCards[82]} -> Reverse Card with the blue colour")
        print(f"4) Draw 2 Card: {self._AllCards[96]} -> Draw 2 Card with the green colour")
        print(f"5) WildCard: {self._AllCards[102]} -> WildCard")
        print(f"6) Draw 4 WildCard: {self._AllCards[105]} -> Draw 4 WildCard")
        print("\nHow to play the cards:")
        print("1) Normal Card: You match the either the colour or the number with the card on discard pile, otherwise can't be played.")
        print("2) Skip Card: You match only with the colour. Skips the other player's turn.")
        print("3) Reverse Card: You match only with the colour. Reverses the turns which results in the same action as the skip card as this a 2 player game.")
        print("4) Draw 2 Card: You match only with the colour. Makes opponent draw 2 cards and skips their turn.")
        print("5) WildCard: If you have this consider yourself lucky as this card doesn't need to be matched and when played lets you choose what colour the opponent should play.")
        print("6) Draw 4 WildCard: This is the most powerful card in the game ! Has same wildcard traits + opponent draws 4 cards and skips his turn.")
        print("\nHow to use the program:")
        print("-To play a card enter the number of card in your deck. ex: Deck[Card1,Card2,Card3] if you want to play card 2 enter 2")
        print("-In each turn program asks you if you want to play or draw a card.\n\n")

    def StartGame(self):
        self._Player1Name = input("Player 1 please enter your name : ")
        self._Player2Name = input("Player 2 please enter your name: ")
        for _ in range(7):
            GameManager.DrawCard(self, self._Player1Name)
            GameManager.DrawCard(self, self._Player2Name)
        return self._Player1Name, self._Player2Name   

    def DrawCard(self, player):
        card = random.choice(self._AllCards)
        self._AllCards.remove(card)
        match player:
            case self._Player1Name:
                self._Player1Deck.append(card)
                return
            case self._Player2Name:
                self._Player2Deck.append(card)
                return

    def PrintDeck(self, player):
        match player:
            case self._Player1Name:
                print(f"{self._Player1Name}'s Deck:\n{self._Player1Deck}")
                return
            case self._Player2Name:
                print(f"{self._Player2Name}' Deck:\n{self._Player2Deck}")
                return
        
    def PlayGame(self):
        self._CardOnTable = random.choice(self._AllCards[:75])
        self._AllCards.remove(self._CardOnTable)
        while len(self._Player1Deck) != 0 and len(self._Player2Deck) != 0:
            if len(self._Player1Deck) == 0:
                break
            if len(self._Player2Deck) == 0:
                break
            #Player 1's Turn
            if self._Player1SkipsTurn == False:
                print(f"{self._Player1Name}'s turn !")
                GameManager.PrintDeck(self, self._Player1Name)
                print(f"Card on Table: {self._CardOnTable}")
                PlayerCanPlay = GameManager.CheckIfPlayerCanPlay(self, self._Player1Name, self._Player1Deck)
                match PlayerCanPlay:
                    case True:
                        CardToPlayIndex = int(input("Please enter the number of card you want to play: "))
                        while CardToPlayIndex <= 0 or CardToPlayIndex > len(self._Player1Deck):
                            CardToPlayIndex = int(input("Invalid Number ! Please re-enter the number of card you want to play: "))
                        CardToPlay = self._Player1Deck[CardToPlayIndex-1]
                        CardCanBePlayed = GameManager.CheckIfCardCanBePlayed(self, CardToPlay)
                        while not CardCanBePlayed:
                            CardToPlayIndex = int(input("Invalid Card ! Please re-enter the number of card you want to play: "))
                            CardToPlay = self._Player1Deck[CardToPlayIndex-1]
                            CardCanBePlayed = GameManager.CheckIfCardCanBePlayed(self, CardToPlay)
                        GameManager.PlayCard(self, CardToPlay, self._Player1Name)
                        SkipCard, ReverseCard, Draw2Card, WildCardColour, Draw4WildCardColour = GameManager.GetActionDetails(self, CardToPlay)
                        #check if ReverseCard or SkipCard as both behave the same
                        if SkipCard == True or ReverseCard == True:
                            #skip opponent's turn
                            print(f"{self._Player2Name} will skip his turn !\n\n")
                            continue
                        #check if Draw2Card
                        elif Draw2Card == True:
                            #opponent draws two cards and skips his turn
                            GameManager.DrawCard(self, self._Player2Name)
                            GameManager.DrawCard(self, self._Player2Name)
                            #skip opponent's turn
                            print(f"{self._Player2Name} will skip his turn !\n\n")
                            continue
                        elif WildCardColour != None:
                            match WildCardColour:
                                case "R":
                                    self._CardOnTable._colour = "🔴"
                                case "G":
                                    self._CardOnTable._colour = "🟢"
                                case "B":
                                    self._CardOnTable._colour = "🔵"
                                case "Y":
                                    self._CardOnTable._colour = "🟡"
                            print("After choosing colour:")
                            print("After playing card:")
                            GameManager.PrintDeck(self, self._Player1Name)
                            print(f"Card on Table: {self._CardOnTable}\n\n")
                        elif Draw4WildCardColour != None:
                            GameManager.DrawCard(self, self._Player2Name)
                            GameManager.DrawCard(self, self._Player2Name)
                            GameManager.DrawCard(self, self._Player2Name)
                            GameManager.DrawCard(self, self._Player2Name)
                            match Draw4WildCardColour:
                                case "R":
                                    self._CardOnTable._colour = "🔴"
                                case "G":
                                    self._CardOnTable._colour = "🟢"
                                case "B":
                                    self._CardOnTable._colour = "🔵"
                                case "Y":
                                    self._CardOnTable._colour = "🟡"
                            print("After choosing colour:")
                            print("After playing card:")
                            GameManager.PrintDeck(self, self._Player1Name)
                            print(f"Card on Table: {self._CardOnTable}\n\n")
                            #skip opponent's turn
                            print(f"{self._Player2Name} will skip his turn !\n\n")
                            continue
                    case False:
                            GameManager.DrawCard(self, self._Player1Name)
                            print("You have no valid cards in deck therefore you drew a card.")
                            print("After Drawing card:")
                            GameManager.PrintDeck(self, self._Player1Name)
                            print(f"Card on Table: {self._CardOnTable}")
                            PlayerCanPlay = GameManager.CheckIfPlayerCanPlay(self, self._Player1Name, self._Player1Deck)
                            if not PlayerCanPlay:
                                print("\n\nThere are no valid cards to play so you need to draw another card and skip turn.")
                                GameManager.DrawCard(self, self._Player1Name)
                                print("After Drawing card:")
                                GameManager.PrintDeck(self, self._Player1Name)
                                print(f"Card on Table: {self._CardOnTable}\n\n")
                            else:
                                CardToPlayIndex = int(input("Please enter the number of card you want to play: "))
                                while CardToPlayIndex <= 0 or CardToPlayIndex > len(self._Player1Deck):
                                    CardToPlayIndex = int(input("Invalid Number ! Please re-enter the number of card you want to play: "))
                                CardToPlay = self._Player1Deck[CardToPlayIndex-1]
                                CardCanBePlayed = GameManager.CheckIfCardCanBePlayed(self, CardToPlay)
                                while not CardCanBePlayed:
                                    CardToPlayIndex = int(input("Invalid Card ! Please re-enter the number of card you want to play: "))
                                    CardToPlay = self._Player1Deck[CardToPlayIndex-1]
                                    CardCanBePlayed = GameManager.CheckIfCardCanBePlayed(self, CardToPlay)
                                GameManager.PlayCard(self, CardToPlay, self._Player1Name)
                                SkipCard, ReverseCard, Draw2Card, WildCardColour, Draw4WildCardColour = GameManager.GetActionDetails(self, CardToPlay)
                                #check if ReverseCard or SkipCard as both behave the same
                                if SkipCard == True or ReverseCard == True:
                                    #skip opponent's turn
                                    print(f"{self._Player2Name} will skip his turn !\n\n")
                                    continue
                                #check if Draw2Card
                                elif Draw2Card == True:
                                    #opponent draws two cards and skips his turn
                                    GameManager.DrawCard(self, self._Player2Name)
                                    GameManager.DrawCard(self, self._Player2Name)
                                    #skip opponent's turn
                                    print(f"{self._Player2Name} will skip his turn !\n\n")
                                    continue
                                elif WildCardColour != None:
                                    match WildCardColour:
                                        case "R":
                                            self._CardOnTable._colour = "🔴"
                                        case "G":
                                            self._CardOnTable._colour = "🟢"
                                        case "B":
                                            self._CardOnTable._colour = "🔵"
                                        case "Y":
                                            self._CardOnTable._colour = "🟡"
                                    print("After choosing colour:")
                                    print("After playing card:")
                                    GameManager.PrintDeck(self, self._Player1Name)
                                    print(f"Card on Table: {self._CardOnTable}\n\n")
                                elif Draw4WildCardColour != None:
                                    GameManager.DrawCard(self, self._Player2Name)
                                    GameManager.DrawCard(self, self._Player2Name)
                                    GameManager.DrawCard(self, self._Player2Name)
                                    GameManager.DrawCard(self, self._Player2Name)
                                    match Draw4WildCardColour:
                                        case "R":
                                            self._CardOnTable._colour = "🔴"
                                        case "G":
                                            self._CardOnTable._colour = "🟢"
                                        case "B":
                                            self._CardOnTable._colour = "🔵"
                                        case "Y":
                                            self._CardOnTable._colour = "🟡"
                                    print("After choosing colour:")
                                    print("After playing card:")
                                    GameManager.PrintDeck(self, self._Player1Name)
                                    print(f"Card on Table: {self._CardOnTable}")
                                    #skip opponent's turn
                                    print(f"{self._Player2Name} will skip his turn !\n\n")
                                    continue
            self._Player1SkipsTurn = False
            #Player 2's Turn
            if len(self._Player1Deck) == 0:
                break
            if len(self._Player2Deck) == 0:
                break
            print(f"{self._Player2Name}'s turn !")
            GameManager.PrintDeck(self, self._Player2Name)
            print(f"Card on Table: {self._CardOnTable}")
            PlayerCanPlay = GameManager.CheckIfPlayerCanPlay(self, self._Player2Name, self._Player2Deck)
            match PlayerCanPlay:
                case True:
                    CardToPlayIndex = int(input("Please enter the number of card you want to play: "))
                    while CardToPlayIndex <= 0 or CardToPlayIndex > len(self._Player2Deck):
                        CardToPlayIndex = int(input("Invalid Number ! Please re-enter the number of card you want to play: "))
                    CardToPlay = self._Player2Deck[CardToPlayIndex-1]
                    CardCanBePlayed = GameManager.CheckIfCardCanBePlayed(self, CardToPlay)
                    while not CardCanBePlayed:
                        CardToPlayIndex = int(input("Invalid Card ! Please re-enter the number of card you want to play: "))
                        CardToPlay = self._Player2Deck[CardToPlayIndex-1]
                        CardCanBePlayed = GameManager.CheckIfCardCanBePlayed(self, CardToPlay)
                    GameManager.PlayCard(self, CardToPlay, self._Player2Name)
                    SkipCard, ReverseCard, Draw2Card, WildCardColour, Draw4WildCardColour = GameManager.GetActionDetails(self, CardToPlay)
                    #check if ReverseCard or SkipCard as both behave the same
                    if SkipCard == True or ReverseCard == True:
                        #skip opponent's turn
                        self._Player1SkipsTurn = True
                        print(f"{self._Player1Name} will skip his turn !\n\n")
                        continue
                    #check if Draw2Card
                    elif Draw2Card == True:
                        #opponent draws two cards and skips his turn
                        GameManager.DrawCard(self, self._Player1Name)
                        GameManager.DrawCard(self, self._Player1Name)
                        self._Player1SkipsTurn = True
                        #skip opponent's turn
                        print(f"{self._Player1Name} will skip his turn !\n\n")
                        continue
                    elif WildCardColour != None:
                        match WildCardColour:
                            case "R":
                                self._CardOnTable._colour = "🔴"
                            case "G":
                                self._CardOnTable._colour = "🟢"
                            case "B":
                                self._CardOnTable._colour = "🔵"
                            case "Y":
                                self._CardOnTable._colour = "🟡"
                        print("After choosing colour:")
                        print("After playing card:")
                        GameManager.PrintDeck(self, self._Player2Name)
                        print(f"Card on Table: {self._CardOnTable}")
                    elif Draw4WildCardColour != None:
                        GameManager.DrawCard(self, self._Player1Name)
                        GameManager.DrawCard(self, self._Player1Name)
                        GameManager.DrawCard(self, self._Player1Name)
                        GameManager.DrawCard(self, self._Player1Name)
                        match Draw4WildCardColour:
                            case "R":
                                self._CardOnTable._colour = "🔴"
                            case "G":
                                self._CardOnTable._colour = "🟢"
                            case "B":
                                self._CardOnTable._colour = "🔵"
                            case "Y":
                                self._CardOnTable._colour = "🟡"
                        print("After choosing colour:")
                        print("After playing card:")
                        GameManager.PrintDeck(self, self._Player2Name)
                        print(f"Card on Table: {self._CardOnTable}")
                        #skip opponent's turn
                        self._Player1SkipsTurn = True
                        print(f"{self._Player1Name} will skip his turn !\n\n")
                        continue
                      
                case False:
                        print("You have no valid cards in deck therefore you drew a card.")
                        GameManager.DrawCard(self, self._Player2Name)
                        print("After Drawing card:")
                        GameManager.PrintDeck(self, self._Player2Name)
                        print(f"Card on Table: {self._CardOnTable}")
                        PlayerCanPlay = GameManager.CheckIfPlayerCanPlay(self, self._Player2Name, self._Player2Deck)
                        if not PlayerCanPlay:
                            print("There are no valid cards to play so you need to draw another card and skip turn.")
                            GameManager.DrawCard(self, self._Player2Name)
                            print("After Drawing card:")
                            GameManager.PrintDeck(self, self._Player2Name)
                        else:
                            CardToPlayIndex = int(input("Please enter the number of card you want to play: "))
                            while CardToPlayIndex <= 0 or CardToPlayIndex > len(self._Player2Deck):
                                CardToPlayIndex = int(input("Invalid Number ! Please re-enter the number of card you want to play: "))
                            CardToPlay = self._Player2Deck[CardToPlayIndex-1]
                            CardCanBePlayed = GameManager.CheckIfCardCanBePlayed(self, CardToPlay)
                            while not CardCanBePlayed:
                                CardToPlayIndex = int(input("Invalid Card ! Please re-enter the number of card you want to play: "))
                                CardToPlay = self._Player2Deck[CardToPlayIndex-1]
                                CardCanBePlayed = GameManager.CheckIfCardCanBePlayed(self, CardToPlay)
                            GameManager.PlayCard(self, CardToPlay, self._Player1Name)
                            SkipCard, ReverseCard, Draw2Card, WildCardColour, Draw4WildCardColour = GameManager.GetActionDetails(self, CardToPlay)
                            #check if ReverseCard or SkipCard as both behave the same
                            if SkipCard == True or ReverseCard == True:
                                #skip opponent's turn
                                self._Player1SkipsTurn = True
                                print(f"{self._Player1Name} will skip his turn !\n\n")
                                continue
                            #check if Draw2Card
                            elif Draw2Card == True:
                                #opponent draws two cards and skips his turn
                                GameManager.DrawCard(self, self._Player1Name)
                                GameManager.DrawCard(self, self._Player1Name)
                                #skip opponent's turn
                                self._Player1SkipsTurn = True
                                print(f"{self._Player1Name} will skip his turn !\n\n")
                                continue
                            elif WildCardColour != None:
                                match WildCardColour:
                                    case "R":
                                        self._CardOnTable._colour = "🔴"
                                    case "G":
                                        self._CardOnTable._colour = "🟢"
                                    case "B":
                                        self._CardOnTable._colour = "🔵"
                                    case "Y":
                                        self._CardOnTable._colour = "🟡"
                                print("After choosing colour:")
                                print("After playing card:")
                                GameManager.PrintDeck(self, self._Player2Name)
                                print(f"Card on Table: {self._CardOnTable}")
                            elif Draw4WildCardColour != None:
                                GameManager.DrawCard(self, self._Player1Name)
                                GameManager.DrawCard(self, self._Player1Name)
                                GameManager.DrawCard(self, self._Player1Name)
                                GameManager.DrawCard(self, self._Player1Name)
                                match Draw4WildCardColour:
                                    case "R":
                                        self._CardOnTable._colour = "🔴"
                                    case "G":
                                        self._CardOnTable._colour = "🟢"
                                    case "B":
                                        self._CardOnTable._colour = "🔵"
                                    case "Y":
                                        self._CardOnTable._colour = "🟡"
                                print("After choosing colour:")
                                print("After playing card:")
                                GameManager.PrintDeck(self, self._Player2Name)
                                print(f"Card on Table: {self._CardOnTable}")
                                #skip opponent's turn
                                self._Player1SkipsTurn = True
                                print(f"{self._Player1Name} will skip his turn !\n\n")
                                continue            
        if len(self._Player1Deck) == 0:
            GameManager.DisplayWinner(self, self._Player1Name)
        if len(self._Player2Deck) == 0:
            GameManager.DisplayWinner(self, self._Player2Name)                

    def UpdatePile(self, player, card):
        match player:
            case self._Player1Name:
                if card in self._Player1Deck:
                    self._Player1Deck.remove(card)
                self._CardOnTable = card
                return
            case self._Player2Name:
                if card in self._Player2Deck:
                    self._Player2Deck.remove(card)
                self._CardOnTable = card
                return
            
    def CheckIfCardCanBePlayed(self, CardToPlay):
        if CardToPlay._type == "#️⃣":
            if self._CardOnTable._type == "#️⃣" and (CardToPlay._colour == self._CardOnTable._colour or CardToPlay._number == self._CardOnTable._number):
                return True
            elif self._CardOnTable._type == "🔄" and (CardToPlay._colour == self._CardOnTable._colour):
                return True
            elif self._CardOnTable._type == "🚫" and (CardToPlay._colour == self._CardOnTable._colour):
                return True
            elif self._CardOnTable._type == "➕2️⃣" and (CardToPlay._colour == self._CardOnTable._colour):
                return True
            elif self._CardOnTable._type == "🌐" and (CardToPlay._colour == self._CardOnTable._colour):
                return True
            elif self._CardOnTable._type == "🌐➕4️⃣" and (CardToPlay._colour == self._CardOnTable._colour):
                return True
            else:
                return False
        elif CardToPlay._type == "🔄":
            if self._CardOnTable._type == "#️⃣" and CardToPlay._colour == self._CardOnTable._colour:
                return True  
            elif self._CardOnTable._type == "🔄":
                return True
            elif self._CardOnTable._type == "🚫" and (CardToPlay._colour == self._CardOnTable._colour):
                return True
            elif self._CardOnTable._type == "➕2️⃣" and (CardToPlay._colour == self._CardOnTable._colour):
                return True
            elif self._CardOnTable._type == "🌐" and (CardToPlay._colour == self._CardOnTable._colour):
                return True
            elif self._CardOnTable._type == "🌐➕4️⃣" and (CardToPlay._colour == self._CardOnTable._colour):
                return True
            else:
                return False
        elif CardToPlay._type == "🚫":
            if self._CardOnTable._type == "#️⃣" and CardToPlay._colour == self._CardOnTable._colour:
                return True  
            elif self._CardOnTable._type == "🔄" and CardToPlay._colour == self._CardOnTable._colour:
                return True
            elif self._CardOnTable._type == "🚫":
                return True
            elif self._CardOnTable._type == "➕2️⃣" and (CardToPlay._colour == self._CardOnTable._colour):
                return True
            elif self._CardOnTable._type == "🌐" and (CardToPlay._colour == self._CardOnTable._colour):
                return True
            elif self._CardOnTable._type == "🌐➕4️⃣" and (CardToPlay._colour == self._CardOnTable._colour):
                return True
            else:
                return False
        elif CardToPlay._type == "➕2️⃣":
            if self._CardOnTable._type == "#️⃣" and CardToPlay._colour == self._CardOnTable._colour:
                return True  
            elif self._CardOnTable._type == "🔄" and CardToPlay._colour == self._CardOnTable._colour:
                return True
            elif self._CardOnTable._type == "🚫" and CardToPlay._colour == self._CardOnTable._colour:
                return True
            elif self._CardOnTable._type == "➕2️⃣":
                return True
            elif self._CardOnTable._type == "🌐" and (CardToPlay._colour == self._CardOnTable._colour):
                return True
            elif self._CardOnTable._type == "🌐➕4️⃣":
                return True
            else:
                return False
        elif CardToPlay._type == "🌐":
                return True 
        elif CardToPlay._type == "🌐➕4️⃣":
                return True

    def CheckIfPlayerCanPlay(self, player, PlayerDeck):
        match player:
            case self._Player1Name:
                NumberOfCardsCanBePlayed = 0
                for Card in self._Player1Deck:
                    if GameManager.CheckIfCardCanBePlayed(self, Card):
                        NumberOfCardsCanBePlayed += 1
                if NumberOfCardsCanBePlayed == 0:
                    return False
                else:
                    return True
            case self._Player2Name:
                NumberOfCardsCanBePlayed = 0
                for Card in self._Player2Deck:
                    if GameManager.CheckIfCardCanBePlayed(self, Card):
                        NumberOfCardsCanBePlayed += 1
                if NumberOfCardsCanBePlayed == 0:
                    return False
                else:
                    return True

            
    def PlayCard(self, CardToPlay, player):
        match player:
            case self._Player1Name:
                if CardToPlay._type == "#️⃣":
                    if self._CardOnTable._type == "#️⃣" and (CardToPlay._colour == self._CardOnTable._colour or CardToPlay._number == self._CardOnTable._number):
                        GameManager.UpdatePile(self, self._Player1Name, CardToPlay)
                        print("\nAfter playing card:")
                        GameManager.PrintDeck(self, self._Player1Name)
                        print(f"Card on Table: {self._CardOnTable}\n\n")
                    elif self._CardOnTable._type == "🔄" and (CardToPlay._colour == self._CardOnTable._colour):
                        GameManager.UpdatePile(self, self._Player1Name, CardToPlay)
                        print("\nAfter playing card:")
                        GameManager.PrintDeck(self, self._Player1Name)
                        print(f"Card on Table: {self._CardOnTable}\n\n")
                    elif self._CardOnTable._type == "🚫" and (CardToPlay._colour == self._CardOnTable._colour):
                        GameManager.UpdatePile(self, self._Player1Name, CardToPlay)
                        print("\nAfter playing card:")
                        GameManager.PrintDeck(self, self._Player1Name)
                        print(f"Card on Table: {self._CardOnTable}\n\n")
                    elif self._CardOnTable._type == "➕2️⃣" and (CardToPlay._colour == self._CardOnTable._colour):
                        GameManager.UpdatePile(self, self._Player1Name, CardToPlay)
                        print("\nAfter playing card:")
                        GameManager.PrintDeck(self, self._Player1Name)
                        print(f"Card on Table: {self._CardOnTable}\n\n")
                    elif self._CardOnTable._type == "🌐" and (CardToPlay._colour == self._CardOnTable._colour):
                        GameManager.UpdatePile(self, self._Player1Name, CardToPlay)
                        print("\nAfter playing card:")
                        GameManager.PrintDeck(self, self._Player1Name)
                        print(f"Card on Table: {self._CardOnTable}\n\n")
                    elif self._CardOnTable._type == "🌐➕4️⃣" and (CardToPlay._colour == self._CardOnTable._colour):
                        GameManager.UpdatePile(self, self._Player1Name, CardToPlay)
                        print("\nAfter playing card:")
                        GameManager.PrintDeck(self, self._Player1Name)
                        print(f"Card on Table: {self._CardOnTable}\n\n")
                    else:
                        print("Invalid card! Please retry.")
                elif CardToPlay._type == "🔄":
                    if self._CardOnTable._type == "#️⃣" and CardToPlay._colour == self._CardOnTable._colour:
                        GameManager.UpdatePile(self, self._Player1Name, CardToPlay)
                        print("\nAfter playing card:")
                        GameManager.PrintDeck(self, self._Player1Name)
                        print(f"Card on Table: {self._CardOnTable}\n\n")  
                    elif self._CardOnTable._type == "🔄":
                        GameManager.UpdatePile(self, self._Player1Name, CardToPlay)
                        print("\nAfter playing card:")
                        GameManager.PrintDeck(self, self._Player1Name)
                        print(f"Card on Table: {self._CardOnTable}\n\n")
                    elif self._CardOnTable._type == "🚫" and (CardToPlay._colour == self._CardOnTable._colour):
                        GameManager.UpdatePile(self, self._Player1Name, CardToPlay)
                        print("\nAfter playing card:")
                        GameManager.PrintDeck(self, self._Player1Name)
                        print(f"Card on Table: {self._CardOnTable}\n\n")
                    elif self._CardOnTable._type == "➕2️⃣" and (CardToPlay._colour == self._CardOnTable._colour):
                        GameManager.UpdatePile(self, self._Player1Name, CardToPlay)
                        print("\nAfter playing card:")
                        GameManager.PrintDeck(self, self._Player1Name)
                        print(f"Card on Table: {self._CardOnTable}\n\n")
                    elif self._CardOnTable._type == "🌐" and (CardToPlay._colour == self._CardOnTable._colour):
                        GameManager.UpdatePile(self, self._Player1Name, CardToPlay)
                        print("\nAfter playing card:")
                        GameManager.PrintDeck(self, self._Player1Name)
                        print(f"Card on Table: {self._CardOnTable}\n\n")
                    elif self._CardOnTable._type == "🌐➕4️⃣" and (CardToPlay._colour == self._CardOnTable._colour):
                        GameManager.UpdatePile(self, self._Player1Name, CardToPlay)
                        print("\nAfter playing card:")
                        GameManager.PrintDeck(self, self._Player1Name)
                        print(f"Card on Table: {self._CardOnTable}\n\n")
                    else:
                        print("Invalid card! Please retry.")
                elif CardToPlay._type == "🚫":
                    if self._CardOnTable._type == "#️⃣" and CardToPlay._colour == self._CardOnTable._colour:
                        GameManager.UpdatePile(self, self._Player1Name, CardToPlay)
                        print("\nAfter playing card:")
                        GameManager.PrintDeck(self, self._Player1Name)
                        print(f"Card on Table: {self._CardOnTable}\n\n")  
                    elif self._CardOnTable._type == "🔄" and CardToPlay._colour == self._CardOnTable._colour:
                        GameManager.UpdatePile(self, self._Player1Name, CardToPlay)
                        print("\nAfter playing card:")
                        GameManager.PrintDeck(self, self._Player1Name)
                        print(f"Card on Table: {self._CardOnTable}\n\n")
                    elif self._CardOnTable._type == "🚫":
                        GameManager.UpdatePile(self, self._Player1Name, CardToPlay)
                        print("\nAfter playing card:")
                        GameManager.PrintDeck(self, self._Player1Name)
                        print(f"Card on Table: {self._CardOnTable}\n\n")
                    elif self._CardOnTable._type == "➕2️⃣" and (CardToPlay._colour == self._CardOnTable._colour):
                        GameManager.UpdatePile(self, self._Player1Name, CardToPlay)
                        print("\nAfter playing card:")
                        GameManager.PrintDeck(self, self._Player1Name)
                        print(f"Card on Table: {self._CardOnTable}\n\n")
                    elif self._CardOnTable._type == "🌐" and (CardToPlay._colour == self._CardOnTable._colour):
                        GameManager.UpdatePile(self, self._Player1Name, CardToPlay)
                        print("\nAfter playing card:")
                        GameManager.PrintDeck(self, self._Player1Name)
                        print(f"Card on Table: {self._CardOnTable}\n\n")
                    elif self._CardOnTable._type == "🌐➕4️⃣" and (CardToPlay._colour == self._CardOnTable._colour):
                        GameManager.UpdatePile(self, self._Player1Name, CardToPlay)
                        print("\nAfter playing card:")
                        GameManager.PrintDeck(self, self._Player1Name)
                        print(f"Card on Table: {self._CardOnTable}\n\n")
                    else:
                        print("Invalid card! Please retry.")
                elif CardToPlay._type == "➕2️⃣":
                    if self._CardOnTable._type == "#️⃣" and CardToPlay._colour == self._CardOnTable._colour:
                        GameManager.UpdatePile(self, self._Player1Name, CardToPlay)
                        print("\nAfter playing card:")
                        GameManager.PrintDeck(self, self._Player1Name)
                        print(f"Card on Table: {self._CardOnTable}\n\n")  
                    elif self._CardOnTable._type == "🔄" and CardToPlay._colour == self._CardOnTable._colour:
                        GameManager.UpdatePile(self, self._Player1Name, CardToPlay)
                        print("\nAfter playing card:")
                        GameManager.PrintDeck(self, self._Player1Name)
                        print(f"Card on Table: {self._CardOnTable}\n\n")
                    elif self._CardOnTable._type == "🚫" and CardToPlay._colour == self._CardOnTable._colour:
                        GameManager.UpdatePile(self, self._Player1Name, CardToPlay)
                        print("\nAfter playing card:")
                        GameManager.PrintDeck(self, self._Player1Name)
                        print(f"Card on Table: {self._CardOnTable}\n\n")
                    elif self._CardOnTable._type == "➕2️⃣":
                        GameManager.UpdatePile(self, self._Player1Name, CardToPlay)
                        print("\nAfter playing card:")
                        GameManager.PrintDeck(self, self._Player1Name)
                        print(f"Card on Table: {self._CardOnTable}\n\n")
                    elif self._CardOnTable._type == "🌐" and (CardToPlay._colour == self._CardOnTable._colour):
                        GameManager.UpdatePile(self, self._Player1Name, CardToPlay)
                        print("\nAfter playing card:")
                        GameManager.PrintDeck(self, self._Player1Name)
                        print(f"Card on Table: {self._CardOnTable}\n\n")
                    elif self._CardOnTable._type == "🌐➕4️⃣" and (CardToPlay._colour == self._CardOnTable._colour):
                        GameManager.UpdatePile(self, self._Player1Name, CardToPlay)
                        print("\nAfter playing card:")
                        GameManager.PrintDeck(self, self._Player1Name)
                        print(f"Card on Table: {self._CardOnTable}\n\n")
                    else:
                        print("Invalid card! Please retry.")
                elif CardToPlay._type == "🌐":
                        GameManager.UpdatePile(self, self._Player1Name, CardToPlay)  
                elif CardToPlay._type == "🌐➕4️⃣":
                        GameManager.UpdatePile(self, self._Player1Name, CardToPlay)
            case self._Player2Name:
                if CardToPlay._type == "#️⃣":
                    if self._CardOnTable._type == "#️⃣" and (CardToPlay._colour == self._CardOnTable._colour or CardToPlay._number == self._CardOnTable._number):
                        GameManager.UpdatePile(self, self._Player2Name, CardToPlay)
                        print("\nAfter playing card:")
                        GameManager.PrintDeck(self, self._Player2Name)
                        print(f"Card on Table: {self._CardOnTable}\n\n")
                    elif self._CardOnTable._type == "🔄" and (CardToPlay._colour == self._CardOnTable._colour):
                        GameManager.UpdatePile(self, self._Player2Name, CardToPlay)
                        print("\nAfter playing card:")
                        GameManager.PrintDeck(self, self._Player2Name)
                        print(f"Card on Table: {self._CardOnTable}\n\n")
                    elif self._CardOnTable._type == "🚫" and (CardToPlay._colour == self._CardOnTable._colour):
                        GameManager.UpdatePile(self, self._Player2Name, CardToPlay)
                        print("\nAfter playing card:")
                        GameManager.PrintDeck(self, self._Player2Name)
                        print(f"Card on Table: {self._CardOnTable}\n\n")
                    elif self._CardOnTable._type == "➕2️⃣" and (CardToPlay._colour == self._CardOnTable._colour):
                        GameManager.UpdatePile(self, self._Player2Name, CardToPlay)
                        print("\nAfter playing card:")
                        GameManager.PrintDeck(self, self._Player2Name)
                        print(f"Card on Table: {self._CardOnTable}\n\n")
                    elif self._CardOnTable._type == "🌐" and (CardToPlay._colour == self._CardOnTable._colour):
                        GameManager.UpdatePile(self, self._Player2Name, CardToPlay)
                        print("\nAfter playing card:")
                        GameManager.PrintDeck(self, self._Player2Name)
                        print(f"Card on Table: {self._CardOnTable}\n\n")
                    elif self._CardOnTable._type == "🌐➕4️⃣" and (CardToPlay._colour == self._CardOnTable._colour):
                        GameManager.UpdatePile(self, self._Player2Name, CardToPlay)
                        print("\nAfter playing card:")
                        GameManager.PrintDeck(self, self._Player2Name)
                        print(f"Card on Table: {self._CardOnTable}\n\n")
                    else:
                        print("Invalid card! Please retry.")
                elif CardToPlay._type == "🔄":
                    if self._CardOnTable._type == "#️⃣" and CardToPlay._colour == self._CardOnTable._colour:
                        GameManager.UpdatePile(self, self._Player2Name, CardToPlay)
                        print("\nAfter playing card:")
                        GameManager.PrintDeck(self, self._Player2Name)
                        print(f"Card on Table: {self._CardOnTable}\n\n")  
                    elif self._CardOnTable._type == "🔄":
                        GameManager.UpdatePile(self, self._Player2Name, CardToPlay)
                        print("\nAfter playing card:")
                        GameManager.PrintDeck(self, self._Player2Name)
                        print(f"Card on Table: {self._CardOnTable}\n\n")
                    elif self._CardOnTable._type == "🚫" and (CardToPlay._colour == self._CardOnTable._colour):
                        GameManager.UpdatePile(self, self._Player2Name, CardToPlay)
                        print("\nAfter playing card:")
                        GameManager.PrintDeck(self, self._Player2Name)
                        print(f"Card on Table: {self._CardOnTable}\n\n")
                    elif self._CardOnTable._type == "➕2️⃣" and (CardToPlay._colour == self._CardOnTable._colour):
                        GameManager.UpdatePile(self, self._Player2Name, CardToPlay)
                        print("\nAfter playing card:")
                        GameManager.PrintDeck(self, self._Player2Name)
                        print(f"Card on Table: {self._CardOnTable}\n\n")
                    elif self._CardOnTable._type == "🌐" and (CardToPlay._colour == self._CardOnTable._colour):
                        GameManager.UpdatePile(self, self._Player2Name, CardToPlay)
                        print("\nAfter playing card:")
                        GameManager.PrintDeck(self, self._Player2Name)
                        print(f"Card on Table: {self._CardOnTable}\n\n")
                    elif self._CardOnTable._type == "🌐➕4️⃣" and (CardToPlay._colour == self._CardOnTable._colour):
                        GameManager.UpdatePile(self, self._Player2Name, CardToPlay)
                        print("\nAfter playing card:")
                        GameManager.PrintDeck(self, self._Player2Name)
                        print(f"Card on Table: {self._CardOnTable}\n\n")
                    else:
                        print("Invalid card! Please retry.")
                elif CardToPlay._type == "🚫":
                    if self._CardOnTable._type == "#️⃣" and CardToPlay._colour == self._CardOnTable._colour:
                        GameManager.UpdatePile(self, self._Player2Name, CardToPlay)
                        print("\nAfter playing card:")
                        GameManager.PrintDeck(self, self._Player2Name)
                        print(f"Card on Table: {self._CardOnTable}\n\n")  
                    elif self._CardOnTable._type == "🔄" and CardToPlay._colour == self._CardOnTable._colour:
                        GameManager.UpdatePile(self, self._Player2Name, CardToPlay)
                        print("\nAfter playing card:")
                        GameManager.PrintDeck(self, self._Player2Name)
                        print(f"Card on Table: {self._CardOnTable}\n\n")
                    elif self._CardOnTable._type == "🚫":
                        GameManager.UpdatePile(self, self._Player2Name, CardToPlay)
                        print("\nAfter playing card:")
                        GameManager.PrintDeck(self, self._Player2Name)
                        print(f"Card on Table: {self._CardOnTable}\n\n")
                    elif self._CardOnTable._type == "➕2️⃣" and (CardToPlay._colour == self._CardOnTable._colour):
                        GameManager.UpdatePile(self, self._Player2Name, CardToPlay)
                        print("\nAfter playing card:")
                        GameManager.PrintDeck(self, self._Player2Name)
                        print(f"Card on Table: {self._CardOnTable}\n\n")
                    elif self._CardOnTable._type == "🌐" and (CardToPlay._colour == self._CardOnTable._colour):
                        GameManager.UpdatePile(self, self._Player2Name, CardToPlay)
                    elif self._CardOnTable._type == "🌐➕4️⃣" and (CardToPlay._colour == self._CardOnTable._colour):
                        GameManager.UpdatePile(self, self._Player2Name, CardToPlay)
                    else:
                        print("Invalid card! Please retry.")
                elif CardToPlay._type == "➕2️⃣":
                    if self._CardOnTable._type == "#️⃣" and CardToPlay._colour == self._CardOnTable._colour:
                        GameManager.UpdatePile(self, self._Player2Name, CardToPlay)
                        print("\nAfter playing card:")
                        GameManager.PrintDeck(self, self._Player2Name)
                        print(f"Card on Table: {self._CardOnTable}\n\n")  
                    elif self._CardOnTable._type == "🔄" and CardToPlay._colour == self._CardOnTable._colour:
                        GameManager.UpdatePile(self, self._Player2Name, CardToPlay)
                        print("\nAfter playing card:")
                        GameManager.PrintDeck(self, self._Player2Name)
                        print(f"Card on Table: {self._CardOnTable}\n\n")
                    elif self._CardOnTable._type == "🚫" and CardToPlay._colour == self._CardOnTable._colour:
                        GameManager.UpdatePile(self, self._Player2Name, CardToPlay)
                        print("\nAfter playing card:")
                        GameManager.PrintDeck(self, self._Player2Name)
                        print(f"Card on Table: {self._CardOnTable}\n\n")
                    elif self._CardOnTable._type == "➕2️⃣":
                        GameManager.UpdatePile(self, self._Player2Name, CardToPlay)
                        print("\nAfter playing card:")
                        GameManager.PrintDeck(self, self._Player2Name)
                        print(f"Card on Table: {self._CardOnTable}\n\n")
                    elif self._CardOnTable._type == "🌐" and (CardToPlay._colour == self._CardOnTable._colour):
                        GameManager.UpdatePile(self, self._Player2Name, CardToPlay)
                        print("\nAfter playing card:")
                        GameManager.PrintDeck(self, self._Player2Name)
                        print(f"Card on Table: {self._CardOnTable}\n\n")
                    elif self._CardOnTable._type == "🌐➕4️⃣" and (CardToPlay._colour == self._CardOnTable._colour):
                        GameManager.UpdatePile(self, self._Player2Name, CardToPlay)
                        print("\nAfter playing card:")
                        GameManager.PrintDeck(self, self._Player2Name)
                        print(f"Card on Table: {self._CardOnTable}\n\n")
                    else:
                        print("Invalid card! Please retry.")
                elif CardToPlay._type == "🌐":
                        GameManager.UpdatePile(self, self._Player2Name, CardToPlay) 
                elif CardToPlay._type == "🌐➕4️⃣":
                        GameManager.UpdatePile(self, self._Player2Name, CardToPlay)

    def DisplayWinner(self, player):
        figlet = Figlet()
        figlet.setFont(font = "slant")
        match player:
            case self._Player1Name:
                Text = f"UNO !!!\n{self._Player1Name} Wins !"
                print(figlet.renderText(Text))
            case self._Player2Name:
                Text = f"UNO !!!\n{self._Player2Name} Wins !"
                print(figlet.renderText(Text))


    def GetActionDetails(self, CardToPlay):
        if CardToPlay._type == "#️⃣":
            SkipCard = None
            ReverseCard = None
            WildCardColour = None
            Draw2Card = None
            Draw4WildCardColour = None
        elif CardToPlay._type == "🔄":
            SkipCard = None
            ReverseCard = True
            WildCardColour = None
            Draw2Card = None
            Draw4WildCardColour = None
        elif CardToPlay._type == "🚫":
            SkipCard = True
            ReverseCard = None
            WildCardColour = None
            Draw2Card = None
            Draw4WildCardColour = None
        elif CardToPlay._type == "➕2️⃣":
            SkipCard = None
            ReverseCard = None
            WildCardColour = None
            Draw2Card = True
            Draw4WildCardColour = None
        elif CardToPlay._type == "🌐":
            WildCardColour = input("Enter the colour you want for the wildcard (R/G/B/Y): ")
            while WildCardColour not in ["R", "G", "B", "Y"]:
                WildCardColour = input("Enter the colour you want for the wildcard (R/G/B/Y): ")
            SkipCard = None
            ReverseCard = None
            Draw2Card = None
            Draw4WildCardColour = None
        elif CardToPlay._type == "🌐➕4️⃣":
            Draw4WildCardColour = input("Enter the colour you want for the wildcard (R/G/B/Y): ")
            while Draw4WildCardColour not in ["R", "G", "B", "Y"]:
                Draw4WildCardColour = input("Enter the colour you want for the wildcard (R/G/B/Y): ")
            SkipCard = None
            ReverseCard = None
            Draw2Card = None
            WildCardColour = None
        return SkipCard, ReverseCard, Draw2Card, WildCardColour, Draw4WildCardColour
            