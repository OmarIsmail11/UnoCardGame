from Card import Card
import os
from GameManager import GameManager
def main():
    Game = GameManager()
    Game.ReadCSVFile()
    Game.PrintTutorial()
    input("Press enter to continue: ")
    os.system("cls||clear")
    Player1Name, Player2Name = Game.StartGame()
    Game.PlayGame()

    # Game.DrawCard(Player1Name)
    # Game.DrawCard(Player1Name)
    # Game.PrintDeck(Player1Name)
    # print(len(Game._AllCards))

if __name__ == "__main__":
    main()