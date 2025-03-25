import csv
import Card

def loadCardsFromCSV():
    cards = []
    with open("Cards.csv", encoding="utf-8") as file:
        reader = csv.DictReader(file, fieldnames=["type", "colour", "number", "image_path"])
        next(reader)
        for row in reader:
            UnoCard = Card.Card(row["type"], row["colour"], row["number"], row["image_path"])
            cards.append(UnoCard)
    return cards