import Card
import csv

with open("Cards.csv") as file:
    reader = csv.DictReader(file, fieldnames=["type", "colour", "number"])
    AllCards = []
    for row in reader:
        UnoCard = Card.Card(row["type"],row["colour"],row["number"])
        AllCards.append(UnoCard)

print(AllCards)
    

