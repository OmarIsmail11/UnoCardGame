from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import cardsLoader

allCards = cardsLoader.loadCardsFromCSV()

cardOnTable = None
currentTurn = None
player1Name = None
player2Name = None
player1Cards = []
player2Cards = []
drawCount = 0
skipLabel = None

def displayCards(frame, playerCards, playCard_function):
    # Clears the frame and displays the player's cards as buttons.
    for widget in frame.winfo_children():
        widget.destroy()

    for card in playerCards:
        img = Image.open(card.imagePath) # Couldn't use tkinker PhotoImage() and used ImageTK.PhotoImage() instead as image needs resizing which is done by pillow library.
        img = img.resize((60, 80))
        img = ImageTk.PhotoImage(img)

        btn = Button(frame, image=img, bg="#0A662F", relief=FLAT, command=lambda c=card: playCard_function(c, playerCards, frame))
        btn.image = img  # Keep reference needed for tkinker garbage collector
        btn.pack(side=LEFT, padx=2) # No variable names for the buttons as after each loop packed into frame and tkinker handles this.

def checkIfCardCanBePlayed(card):
    global cardOnTable
    specialActionTypes = ["➕2️⃣", "🚫", "🔄"]
    wildCards = ["🌐", "🌐➕4️⃣"]
    cardCanBePlayed = False

    if card.type in wildCards:  # Wild cards can always be played
        cardCanBePlayed = True
    elif card.type in specialActionTypes:  # Action cards must match colour or type
        if (card.colour == cardOnTable.colour or card.type == cardOnTable.type):  # Allow same type regardless of colour
            cardCanBePlayed = True
    else:  # Numbered cards must match color or number
        if (card.colour == cardOnTable.colour or card.number == cardOnTable.number):
            cardCanBePlayed = True
    return cardCanBePlayed

def play_card(selectedCard, playerCards, frame):
    global cardOnTable, currentTurn, drawCount, skipLabel

    if currentTurn == player1Name and playerCards is not player1Cards:
        print("Not your turn!")
        return
    elif currentTurn == player2Name and playerCards is not player2Cards:
        print("Not your turn!")
        return

    # Clear skip label when the current player plays
    if skipLabel:
        skipLabel.destroy()
        skipLabel = None

    cardCanBePlayed = checkIfCardCanBePlayed(selectedCard)

    if cardCanBePlayed:
        print(f"Card {selectedCard.type} {selectedCard.colour} {selectedCard.number} played!")
        playerCards.remove(selectedCard)
        updatecardOnTable(selectedCard)
        displayCards(frame, playerCards, play_card)

        if selectedCard.type == "🌐":  # Wildcard
            newColour = chooseColour()
            selectedCard.colour = newColour
            updatecardOnTable(selectedCard)
            switch_turn()  # Normal turn switch
        elif selectedCard.type == "🌐➕4️⃣":  # Wild Draw Four
            newColour = chooseColour()
            selectedCard.colour = newColour
            updatecardOnTable(selectedCard)
            next_playerCards = player2Cards if currentTurn == player1Name else player1Cards
            next_frame = topDeckPlayerCardsFrame if currentTurn == player1Name else bottomDeckPlayerCardsFrame
            drawFour(next_playerCards, next_frame)  # Opponent draws 4

            switch_turn() # First switch just to write the skip turn label on top of opponent
            skipLabel = Label(window, text=f"{currentTurn} skips their turn!", font=("Arial", 12, "bold"), bg="#FF4444", fg="white", padx=5, pady=0)
            skipLabel.place(relx=0.9, rely=0.07, anchor="se")
            switch_turn()  # Skip the next player's turn (back to the original player)
        elif selectedCard.type == "➕2️⃣":  # Draw Two
            next_playerCards = player2Cards if currentTurn == player1Name else player1Cards
            next_frame = topDeckPlayerCardsFrame if currentTurn == player1Name else bottomDeckPlayerCardsFrame
            for _ in range(2):
                drawCard(next_playerCards, next_frame, is_action=True)
            switch_turn()
            skipLabel = Label(window, text=f"{currentTurn} skips their turn!", font=("Arial", 12, "bold"), bg="#FF4444", fg="white", padx=5, pady=0)
            skipLabel.place(relx=0.9, rely=0.07, anchor="se")
            switch_turn()
        elif selectedCard.type == "🚫":  # Skip
            switch_turn()
            skipLabel = Label(window, text=f"{currentTurn} skips their turn!", font=("Arial", 12, "bold"), bg="#FF4444", fg="white", padx=5, pady=0)
            skipLabel.place(relx=0.9, rely=0.07, anchor="se")
            switch_turn()
        elif selectedCard.type == "🔄":  # Reverse
            switch_turn()
            skipLabel = Label(window, text=f"{currentTurn} skips their turn!", font=("Arial", 12, "bold"), bg="#FF4444", fg="white", padx=5, pady=0)
            skipLabel.place(relx=0.9, rely=0.07, anchor="se")
            switch_turn()
        else:  # Normal cards (#️⃣)
            switch_turn()

        # Reset draw count when a card is played
        drawCount = 0

        checkWin()

    else:
        print("Invalid move! You can't play this card.")

def showGameOver(winner):
    gameOverWindow = Toplevel(window)
    gameOverWindow.title("Game Over!")
    icon = PhotoImage(file="images/unoLogo.png")
    gameOverWindow.iconphoto(False, icon)
    gameOverWindow.configure(bg="#222831")
    gameOverWindow.resizable(False, False)

    window_width = 300
    window_height = 250
    screen_width = gameOverWindow.winfo_screenwidth()
    screen_height = gameOverWindow.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    gameOverWindow.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Label for game over text
    Label(gameOverWindow, text="Game Over!", font=("Arial", 20, "bold"), fg="#FFD700", bg="#222831").pack(pady=10)

    # Winner label
    Label(gameOverWindow, text=f"{winner} Wins!", font=("Arial", 16, "bold"), fg="white", bg="#222831").pack(pady=5)

    img = Image.open("images/unoLogo.png")
    img = img.resize((150, 80))
    img = ImageTk.PhotoImage(img)
    Label(gameOverWindow, image=img, bg="#222831").pack(pady=5)
    gameOverWindow.image = img  # Keep reference to prevent garbage collection

    # Exit button
    Button(gameOverWindow, text="Exit", font=("Arial", 12, "bold"), bg="#FF3B3B", fg="white", relief=RAISED, bd=3, command=lambda: [window.quit(), gameOverWindow.destroy()]).pack(pady=10)

    gameOverWindow.transient(window)  # Make it a child of the main window
    gameOverWindow.grab_set()  # Make it modal (force interaction only with this window)
    window.wait_window(gameOverWindow)  # Wait until it closes
    window.destroy()

def checkWin():
    if len(player1Cards) == 0:
        showGameOver(player1Name)
    elif len(player2Cards) == 0:
        showGameOver(player2Name)

def drawCard(playerCards, frame, is_action=False):
    """Draws a single card and adds it to the player's deck, tracking manual draws."""
    global drawCount, currentTurn, skipLabel

    if allCards:
        card = random.choice(allCards)
        allCards.remove(card)
        playerCards.append(card)
        displayCards(frame, playerCards, play_card)

        # Increment draw count only for manual draws
        if not is_action:
            drawCount += 1
            print(f"Draw count: {drawCount}")
            if drawCount >= 2:
                if skipLabel:
                    skipLabel.destroy()
                next_player = currentTurn
                skipLabel = Label(window, text=f"{next_player} skips their turn!", font=("Arial", 12, "bold"), bg="#FF4444", fg="white", padx=5, pady=0)
                skipLabel.place(relx=0.9, rely=0.07, anchor="se")
                switch_turn()
                drawCount = 0
                print(f"{next_player} drew 2 cards from pile and skips their turn!")


def drawFour(playerCards, frame):
    """Draws four cards for Wild Draw Four."""
    for _ in range(4):
        if allCards:
            card = random.choice(allCards)
            allCards.remove(card)
            playerCards.append(card)
    displayCards(frame, playerCards, play_card)


def displaycardOnTable(tableFrame, card):
    """Displays the table card in the center frame."""
    img = Image.open(card.imagePath)
    img = img.resize((60, 80))
    img = ImageTk.PhotoImage(img)

    for widget in tableFrame.winfo_children():
        widget.destroy()

    cardOnTableLabel = Label(tableFrame, image=img, bg="#0A662F")
    cardOnTableLabel.image = img
    cardOnTableLabel.pack()


def updatecardOnTable(new_card):
    """Updates the table card to the played card."""
    global cardOnTable
    cardOnTable = new_card
    displaycardOnTable(tableFrame, cardOnTable)


def switch_turn():
    """Switches turn between player1 and player2."""
    global currentTurn, drawCount, skipLabel
    currentTurn = player2Name if currentTurn == player1Name else player1Name
    turnLabel.config(text=f"Current Turn: {currentTurn}")
    drawCount = 0


def chooseColour():
    colourWindow = Toplevel()
    colourWindow.title("Choose a Colour!")
    colourWindow.configure(bg="#03c6fc")  # Light blue background
    colourWindow.resizable(False, False)

    window_width = 250
    window_height = 220
    screen_width = colourWindow.winfo_screenwidth()
    screen_height = colourWindow.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    colourWindow.geometry(f"{window_width}x{window_height}+{x}+{y}")

    Label(colourWindow, text="Pick a Colour!", font=("Arial", 16, "bold"), bg="#03c6fc", fg="#ffffff").pack(pady=10)

    colours = [
        ("Red", "#FF0000"),
        ("Yellow", "#FFD700"),
        ("Green", "#008000"),
        ("Blue", "#0000FF")
    ]

    mapColourToEmoji = {
        "Green": "🟢",
        "Red": "🔴",
        "Blue": "🔵",
        "Yellow": "🟡"
    }

    chosenColour = StringVar(value="Red")

    # Frame for radio buttons
    radio_frame = Frame(colourWindow, bg="#03c6fc")
    radio_frame.pack()

    for colourName, textColour in colours:
        Radiobutton(radio_frame, text=colourName, variable=chosenColour, value=colourName,
                    font=("Arial", 12, "bold"), bg="#03c6fc", fg=textColour,
                    activebackground="#03c6fc", activeforeground=textColour,
                    selectcolor="white").pack(anchor=W, padx=10, pady=2)

    def submit_color():
        selectedColour = chosenColour.get()
        messagebox.showinfo("Colour Chosen", f"You chose {selectedColour}!")
        colourWindow.selectedColour = selectedColour
        colourWindow.destroy()

    Button(colourWindow, text="Submit", font=("Arial", 12, "bold"), bg="#FF1493", fg="white",
           relief=RAISED, bd=4, command=submit_color).pack(pady=5)

    colourWindow.selectedColour = None
    colourWindow.wait_window()
    return mapColourToEmoji[colourWindow.selectedColour]


def openMainScreen(player1, player2):
    global cardOnTable, currentTurn, player1Name, player2Name, player1Cards, player2Cards, turnLabel, tableFrame, topDeckPlayerCardsFrame, bottomDeckPlayerCardsFrame, window

    player1Name = player1
    player2Name = player2
    currentTurn = player1Name # By default player 1 starts

    window = Tk()
    window.title("Uno Card Game!")
    icon = PhotoImage(file="images/unoLogo.png")
    window.iconphoto(False, icon)
    window.configure(bg="#0A662F")

    window_width = 1200
    window_height = 600
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    player1Cards = []
    player2Cards = []

    # Top Deck (Player 2)
    topDeckFrame = Frame(window, background="#0A662F", height=80)
    topDeckFrame.pack(side=TOP, fill=X, pady=60)
    topDeckFrame.pack_propagate(False)
    Label(topDeckFrame, text=f"{player2Name}'s Deck", background="#34b1eb", foreground="white", width=15, font=("Arial", 16, "bold")).pack(side=LEFT, padx=5, fill=Y)
    global topDeckPlayerCardsFrame
    topDeckPlayerCardsFrame = Frame(topDeckFrame, background="#0A662F")
    topDeckPlayerCardsFrame.pack(side=RIGHT, fill=BOTH, expand=True)

    # Bottom Deck (Player 1)
    bottomDeckFrame = Frame(window, background="#0A662F", height=80)
    bottomDeckFrame.pack(side=BOTTOM, fill=X, pady=20)
    bottomDeckFrame.pack_propagate(False)
    Label(bottomDeckFrame, text=f"{player1Name}'s Deck", background="#34b1eb", foreground="white", width=15, font=("Arial", 16, "bold")).pack(side=LEFT, padx=5, fill=Y)
    global bottomDeckPlayerCardsFrame
    bottomDeckPlayerCardsFrame = Frame(bottomDeckFrame, background="#0A662F")
    bottomDeckPlayerCardsFrame.pack(side=RIGHT, fill=BOTH, expand=True)

    # Table Card
    cardOnTable = random.choice(allCards)
    while (cardOnTable.type in ["🌐➕4️⃣", "🌐"]): # Prevent wildcards to be the first card on table
        cardOnTable = random.choice(allCards)
    allCards.remove(cardOnTable)
    global tableFrame
    tableFrame = Frame(window, width=60, height=80, background="#0A662F")
    tableFrame.place(relx=0.5, rely=0.5, anchor=CENTER)
    displaycardOnTable(tableFrame, cardOnTable)

    # Turn Label
    global turnLabel
    turnLabel = Label(window, text=f"Current Turn: {currentTurn}", font=("Arial", 16, "bold"), bg="#42A5F5", fg="white", padx=10, pady=5)
    turnLabel.place(relx=0.5, rely=0.05, anchor=CENTER)

    # Initial card draw (7 cards each, not counted toward draw limit)
    for _ in range(7):
        drawCard(player1Cards, bottomDeckPlayerCardsFrame, is_action=True)
        drawCard(player2Cards, topDeckPlayerCardsFrame, is_action=True)

    # Draw Button
    drawButtonFrame = Frame(window, width=100, height=50, background="#0A662F")
    drawButtonFrame.place(relx=0.9, rely=0.5, anchor=CENTER)
    draw_button = Button(drawButtonFrame, text="Draw", font=("Arial", 14, "bold"), bg ="yellow", relief=RAISED,
                         command=lambda: drawCard(player1Cards if currentTurn == player1Name else player2Cards, bottomDeckPlayerCardsFrame if currentTurn == player1Name else topDeckPlayerCardsFrame))
    draw_button.pack()

    # Card Pile
    pile_image = Image.open("images/unoCardBack.png")
    pile_image = pile_image.resize((60, 80))
    pile_photo = ImageTk.PhotoImage(pile_image)
    pile_label = Label(window, image=pile_photo, bg="#0A662F")
    pile_label.image = pile_photo
    pile_label.place(relx=0.1, rely=0.5, anchor=CENTER)

    window.mainloop()

if __name__ == "__main__":
    openMainScreen("Player 1", "Player 2")