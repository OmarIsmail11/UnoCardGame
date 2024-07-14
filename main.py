from Card import Card
from os import system
from GameManager import GameManager
def main():
    Game = GameManager()
    Game.ReadCSVFile()
    Game.PrintTutorial()
    input("Press enter to continue: ")
    system("cls||clear")
    Player1Name, Player2Name = Game.StartGame()
    system("cls||clear")
    Game.PlayGame()

if __name__ == "__main__":
    main()