from tkinter import *
import mainScreen

def start_game():
    player1_name = entry_p1.get().strip()
    player2_name = entry_p2.get().strip()

    if player1_name == "" or player2_name == "":
        label_error.config(text="Please enter both names!", fg="red")
        return

    start_window.destroy()

    mainScreen.openMainScreen(player1_name, player2_name)

start_window = Tk()
start_window.title("Welcome!")
icon = PhotoImage(file="images/unoLogo.png")
start_window.iconphoto(False, icon)
start_window.configure(bg="#0A662F")

window_width = 300
window_height = 220

screen_width = start_window.winfo_screenwidth()
screen_height = start_window.winfo_screenheight()

x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)

start_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# UI Elements
Label(start_window, text="Player 1 Name:", font=("Arial", 12), bg="#0A662F", fg="white").pack(pady=(10, 2))
entry_p1 = Entry(start_window, font=("Arial", 12))
entry_p1.pack(pady=(2, 10))

Label(start_window, text="Player 2 Name:", font=("Arial", 12), bg="#0A662F", fg="white").pack(pady=(10, 2))
entry_p2 = Entry(start_window, font=("Arial", 12))
entry_p2.pack(pady=(2, 10))

label_error = Label(start_window, text="", font=("Arial", 10), bg="#0A662F")
label_error.pack(pady=(5, 2))

Button(start_window, text="Start Game", font=("Arial", 12, "bold"), command=start_game,bg="#FF3B3B", fg="white", relief=RAISED, bd=3).pack(pady=5)

start_window.mainloop()
