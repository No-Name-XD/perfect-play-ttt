import tkinter as tk

GAME = ["-"] * 9

WIN = [
    [0,1,2],[3,4,5],[6,7,8],
    [0,3,6],[1,4,7],[2,5,8],
    [0,4,8],[2,4,6]
]

# -------- LOGIC -------- #

def check(player):
    for combo in WIN:
        if all(GAME[i] == player for i in combo):
            return True
    return False

def draw():
    return "-" not in GAME

def empty():
    return [i for i in range(9) if GAME[i] == "-"]


# -------- Purrfect win/draw strategy -------- #

def bot():
    # win
    for i in empty():
        GAME[i] = "X"
        if check("X"):
            return
        GAME[i] = "-"

    # block
    for i in empty():
        GAME[i] = "O"
        if check("O"):
            GAME[i] = "X"
            return
        GAME[i] = "-"

    # opposite corners
    if GAME[4] == "O":
        if GAME[0] == "X" and GAME[8] == "-":
            GAME[8] = "X"
            return
        if GAME[2] == "X" and GAME[6] == "-":
            GAME[6] = "X"
            return
        if GAME[6] == "X" and GAME[2] == "-":
            GAME[2] = "X"
            return
        if GAME[8] == "X" and GAME[0] == "-":
            GAME[0] = "X"
            return

    # center
    if GAME[4] == "-":
        GAME[4] = "X"
        return

    # corners
    for i in [0,2,6,8]:
        if GAME[i] == "-":
            GAME[i] = "X"
            return

    # edges
    for i in [1,3,5,7]:
        if GAME[i] == "-":
            GAME[i] = "X"
            return


# -------- ui ig -------- #

def update_buttons():
    for i in range(9):
        buttons[i]["text"] = GAME[i]

        if GAME[i] == "X":
            buttons[i]["fg"] = "#ff4d4d"
        elif GAME[i] == "O":
            buttons[i]["fg"] = "#4da6ff"
        else:
            buttons[i]["fg"] = "white"


def click(i):
    # prevent clicking filled / finished game
    if GAME[i] != "-" or check("X") or check("O"):
        return

    # human move
    GAME[i] = "O"
    update_buttons()

    # check win
    if check("O"):
        status.set("You did something fishy didn't you? CHEATER!")
        return

    if draw():
        status.set("Won't lemme win and won't win yourself 😒")
        return

    # bot turn
    status.set("My turn boi...")
    root.after(400, bot_turn)


def bot_turn():
    bot()
    update_buttons()

    # check win
    if check("X"):
        status.set("YOU LOOOSEE!! HAHAHA!!")
        return

    if draw():
        status.set("Won't lemme win and won't win yourself 😒")
        return

    status.set("Your Turn")


def reset():
    global GAME
    GAME = ["-"] * 9

    # bot starts first
    GAME[0] = "X"

    update_buttons()
    status.set("Your Turn")


# -------- WINDOW -------- #

root = tk.Tk()
root.title("Unbeatable Tic Tac Toe 😈")
root.geometry("400x550")
root.configure(bg="#1e1e1e")
root.resizable(False, False)

status = tk.StringVar()
status.set("Your Turn")

# Title
title = tk.Label(root,
                 text="Tic Tac Toe",
                 font=("Arial", 20, "bold"),
                 bg="#1e1e1e",
                 fg="white")
title.pack(pady=10)

# Board
frame = tk.Frame(root, bg="#1e1e1e")
frame.pack()

buttons = []

# Status label
status_label = tk.Label(root,
                        textvariable=status,
                        font=("Arial", 16, "bold"),
                        bg="#1e1e1e",
                        fg="#00ffcc")
status_label.pack(pady=15)


for i in range(9):
    btn = tk.Button(frame,
                    text="-",
                    font=("Arial", 28, "bold"),
                    width=4,
                    height=2,
                    bg="#2d2d2d",
                    fg="white",
                    activebackground="#3c3c3c",
                    relief="flat",
                    command=lambda i=i: click(i))

    btn.grid(row=i//3, column=i%3, padx=5, pady=5)
    buttons.append(btn)

# Restart button
restart_btn = tk.Button(root,
                        text="Restart",
                        font=("Arial", 12, "bold"),
                        bg="#007acc",
                        fg="white",
                        relief="flat",
                        command=reset)
restart_btn.pack(pady=10)

# Start game (bot first move)
GAME[0] = "X"
update_buttons()

root.mainloop()
