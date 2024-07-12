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
    
    def ReadCSVFile(self):
        with open("Cards.csv", encoding="utf-8") as file:
            reader = csv.DictReader(file, fieldnames=["type", "colour", "number"])
            for row in reader:
                UnoCard = Card.Card(row["type"],row["colour"],row["number"])
                self._AllCards.append(UnoCard)
           
    def StartGame(self):
        print("==========================# Welcome to UNO PvP #===========================")
        print("Rules:\n     1)Each player starts with a deck of 7 cards\n     2)First to finish his deck of cards wins!")
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
                print(f"{self._Player1Name}'s Deck:{self._Player1Deck}")
                return
            case self._Player2Name:
                print(f"{self._Player2Name}' Deck:\n{self._Player2Deck}")
                return
        

