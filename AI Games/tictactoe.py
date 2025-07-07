import tkinter as tk
from tkinter import messagebox
import math
import time
import threading

board = [' ' for _ in range(9)]
buttons = []
player_score = 0
computer_score = 0
player_first = True
current_turn = 'X'


def check_winner(b, player):
    combos = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    for combo in combos:
        if all(b[i] == player for i in combo):
            return True
    return False


def is_full(b):
    return ' ' not in b


def minimax(b, depth, alpha, beta, is_max):
    if check_winner(b, 'O'):
        return 1
    if check_winner(b, 'X'):
        return -1
    if is_full(b):
        return 0

    if is_max:
        max_eval = -math.inf
        for i in range(9):
            if b[i] == ' ':
                b[i] = 'O'
                eval = minimax(b, depth + 1, alpha, beta, False)
                b[i] = ' '
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
        return max_eval
    else:
        min_eval = math.inf
        for i in range(9):
            if b[i] == ' ':
                b[i] = 'X'
                eval = minimax(b, depth + 1, alpha, beta, True)
                b[i] = ' '
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
        return min_eval


def computer_move():

    time.sleep(0.5)
    best_score = -math.inf
    move = -1
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'
            score = minimax(board, 0, -math.inf, math.inf, False)
            board[i] = ' '
            if score > best_score:
                best_score = score
                move = i
    if move != -1:
        board[move] = 'O'
        buttons[move].config(text='O', state='disabled')
        check_game_over()


def click(pos):
    global current_turn
    if board[pos] == ' ' and current_turn == 'X':
        board[pos] = 'X'
        buttons[pos].config(text='X', state='disabled')
        current_turn = 'O'
        check_game_over()
        if not is_full(board):
            threading.Thread(target=run_computer_turn).start()


def run_computer_turn():
    global current_turn
    computer_move()
    current_turn = 'X'


def check_game_over():
    global player_score, computer_score
    if check_winner(board, 'X'):
        player_score += 1
        update_score()
        messagebox.showinfo("Game Over", "You win!")
        disable_board()
    elif check_winner(board, 'O'):
        computer_score += 1
        update_score()
        messagebox.showinfo("Game Over", "Computer wins!")
        disable_board()
    elif is_full(board):
        messagebox.showinfo("Game Over", "It's a draw!")
        disable_board()


def disable_board():
    for btn in buttons:
        btn.config(state='disabled')


def reset_game():
    global board, current_turn, player_first
    board = [' ' for _ in range(9)]
    for i in range(9):
        buttons[i].config(text=' ', state='normal')
    player_first = not player_first
    current_turn = 'X' if player_first else 'O'
    if current_turn == 'O':
        threading.Thread(target=run_computer_turn).start()


def update_score():
    score_label.config(
        text=f"You: {player_score}   Computer: {computer_score}")


root = tk.Tk()
root.title("Tic-Tac-Toe with Smart AI")

frame = tk.Frame(root)
frame.pack()

for i in range(9):
    btn = tk.Button(frame, text=' ', font=('Helvetica', 24), width=5, height=2,
                    command=lambda i=i: click(i))
    btn.grid(row=i//3, column=i % 3)
    buttons.append(btn)

score_label = tk.Label(root, text="You: 0   Computer: 0",
                       font=('Helvetica', 14))
score_label.pack(pady=5)

reset_btn = tk.Button(root, text="New Game", font=(
    'Helvetica', 12), command=reset_game)
reset_btn.pack(pady=5)


if current_turn == 'O':
    threading.Thread(target=run_computer_turn).start()

root.mainloop()
