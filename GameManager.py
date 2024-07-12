import Card
import csv
import emoji
with open("Cards.csv", encoding="utf-8") as file:
    reader = csv.DictReader(file, fieldnames=["type", "colour", "number"])
    AllCards = []
    for row in reader:
        UnoCard = Card.Card(row["type"],row["colour"],row["number"])
        AllCards.append(UnoCard)

print(AllCards[1:])


