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


# -------- MINIMAX -------- #

def minimax(is_maximizing, depth=0):
    if check("X"):
        return 10 - depth
    if check("O"):
        return depth - 10
    if draw():
        return 0

    if is_maximizing:
        best = -100
        for i in empty():
            GAME[i] = "X"
            score = minimax(False, depth+1)
            GAME[i] = "-"
            best = max(score, best)
        return best
    else:
        best = 100
        for i in empty():
            GAME[i] = "O"
            score = minimax(True, depth+1)
            GAME[i] = "-"
            best = min(score, best)
        return best


def best_move():
    best_score = -100
    move = None

    for i in empty():
        GAME[i] = "X"
        score = minimax(False)
        GAME[i] = "-"

        if score > best_score:
            best_score = score
            move = i

    return move


def bot():
    move = best_move()
    if move is not None:
        GAME[move] = "X"


# -------- UI -------- #

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
    if GAME[i] != "-" or check("X") or check("O"):
        return

    # human move
    GAME[i] = "O"
    update_buttons()

    if check("O"):
        status.set("You win! 😳")
        return

    if draw():
        status.set("It's a draw 😐")
        return

    status.set("AI thinking...")
    root.after(300, bot_turn)


def bot_turn():
    bot()
    update_buttons()

    if check("X"):
        status.set("AI wins 😈")
        return

    if draw():
        status.set("It's a draw 😐")
        return

    status.set("Your turn")


def reset():
    global GAME
    GAME = ["-"] * 9

    # AI starts first (optional)
    bot()
    update_buttons()

    status.set("Your turn")


# -------- WINDOW -------- #

root = tk.Tk()
root.title("Minimax Tic Tac Toe 🤖")
root.geometry("400x550")
root.configure(bg="#1e1e1e")
root.resizable(False, False)

status = tk.StringVar()
status.set("Your turn")

# Title
title = tk.Label(root,
                 text="Tic Tac Toe (Minimax AI)",
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

# Start game
bot()  # AI starts first
update_buttons()

root.mainloop()
