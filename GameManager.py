import Card
import csv
import random

class GameManager:
    def __init__(self):
        self._Player1Name = ""
        self._Player2Name = ""
        self._Player1Deck = []
        self._Player2Deck = []
        self._AllCards = []
        self._CardOnTable = Card.Card("","","")

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
        CardOnTable = random.choice(self._AllCards)
        self._AllCards.remove(CardOnTable)
        while len(self._Player1Deck) != 0 and len(self._Player2Deck) != 0:
            #Player 1's Turn
            print(f"{self._Player1Name}'s turn !")
            GameManager.PrintDeck(self, self._Player1Name)
            print(f"Card on Table: {CardOnTable}")
            PlayOrDraw = input("Do you want to play or draw a card (P/D): ")
            while (PlayOrDraw != "P" and PlayOrDraw != "D"):
                PlayOrDraw = input("Invalid, please re-enter !\nDo you want to play or draw a card (P/D): ")
            match PlayOrDraw:
                case "P":
                    CardToPlayIndex = int(input("Please enter the number of card you want to play: "))
                    while CardToPlayIndex <= 0 or CardToPlayIndex > len(self._Player1Deck):
                        CardToPlayIndex = int(input("Invalid, Please re-enter the number of card you want to play: "))
                    CardToPlay = self._Player1Deck[CardToPlayIndex-1]
                    if CardToPlay._type == "#️⃣":
                        if CardOnTable._type == "#️⃣" and (CardToPlay._colour == CardOnTable._colour or CardToPlay._number == CardOnTable._number):
                            GameManager.PlayCard(self, self._Player1Name, CardToPlay)
                            GameManager.PrintDeck(self, self._Player1Name)
                            print(self.CardOnTable)
                            return
                    
                    

    def PlayCard(self, player, card):
        match player:
            case self._Player1Name:
                self._Player1Deck.remove(card)
                self._CardOnTable = card
                return
            case self._Player2Name:
                self._Player2Deck.remove(card)
                self._CardOnTable = card
                return
