import tkinter as tk
from tkinter import messagebox


class NimGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Nim Game - User vs AI")

        self.user_score = 0
        self.ai_score = 0
        self.initial_pile = 15
        self.pile = self.initial_pile

        self.menu_frame = tk.Frame(root)
        self.menu_frame.pack(pady=20)

        self.start_button = tk.Button(
            self.menu_frame, text="Start Game", command=self.start_game)
        self.start_button.pack(pady=5)

        self.restart_button = tk.Button(
            self.menu_frame, text="Restart Game", command=self.restart_game)
        self.restart_button.pack(pady=5)

        self.exit_button = tk.Button(
            self.menu_frame, text="Exit", command=self.root.quit)
        self.exit_button.pack(pady=5)

        self.game_frame = tk.Frame(root)

    def start_game(self):
        self.menu_frame.pack_forget()
        self.game_frame.pack(pady=20)
        self.update_ui()

    def restart_game(self):
        self.pile = self.initial_pile
        self.update_ui()

    def update_ui(self):
        for widget in self.game_frame.winfo_children():
            widget.destroy()

        tk.Label(self.game_frame, text=f"Sticks Remaining: {self.pile}", font=(
            "Arial", 16)).pack(pady=10)
        tk.Label(self.game_frame, text=f"User Score: {self.user_score} | AI Score: {self.ai_score}", font=(
            "Arial", 12)).pack(pady=5)

        if self.pile == 0:
            return

        btn_frame = tk.Frame(self.game_frame)
        btn_frame.pack(pady=10)
        for i in [1, 2, 3]:
            if self.pile >= i:
                tk.Button(btn_frame, text=f"Take {i}", command=lambda x=i: self.user_move(
                    x)).pack(side=tk.LEFT, padx=5)

    def user_move(self, take):
        self.pile -= take
        if self.pile <= 0:
            self.user_score += 1
            messagebox.showinfo("Game Over", "You win!")
            self.pile = self.initial_pile
            self.update_ui()
            return
        self.root.after(500, self.ai_turn)

    def ai_turn(self):
        move = self.best_move(self.pile)
        self.pile -= move
        messagebox.showinfo("AI Move", f"AI takes {move} stick(s).")
        if self.pile <= 0:
            self.ai_score += 1
            messagebox.showinfo("Game Over", "AI wins!")
            self.pile = self.initial_pile
        self.update_ui()

    def minimax(self, pile, is_ai_turn):
        if pile == 0:
            return -1 if is_ai_turn else 1

        scores = []
        for move in [1, 2, 3]:
            if pile - move >= 0:
                scores.append(self.minimax(pile - move, not is_ai_turn))

        return max(scores) if is_ai_turn else min(scores)

    def best_move(self, pile):
        best_score = -float('inf')
        move = 1
        for m in [1, 2, 3]:
            if pile - m >= 0:
                score = self.minimax(pile - m, False)
                if score > best_score:
                    best_score = score
                    move = m
        return move


if __name__ == "__main__":
    root = tk.Tk()
    app = NimGame(root)
    root.mainloop()
