import tkinter as tk
import math


class NimGame:
    def __init__(self):
        self.root = tk.Tk()
        self.user_score = self.ai_score = 0
        self.pile = 15
        self.user_turn = True
        self.ai_last_move = None
        self.setup_ui()

    def setup_ui(self):
        self.root.title("Nim Game")
        self.root.geometry("700x600")
        self.root.configure(bg='#2c3e50')

        # Main container
        main = tk.Frame(self.root, bg='#2c3e50')
        main.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Title
        tk.Label(main, text="NIM GAME", font=("Arial", 26, "bold"),
                 fg='white', bg='#2c3e50').pack(pady=(0, 15))

        # Score and status in one row
        info_frame = tk.Frame(main, bg='#2c3e50')
        info_frame.pack(fill=tk.X, pady=(0, 15))

        self.user_score_label = tk.Label(info_frame, text=f"You: {self.user_score}",
                                         font=("Arial", 16, "bold"), fg='#27ae60', bg='#2c3e50')
        self.user_score_label.pack(side=tk.LEFT)

        self.status_label = tk.Label(info_frame, text="Your Turn", font=("Arial", 14),
                                     fg='#f39c12', bg='#2c3e50')
        self.status_label.pack(side=tk.LEFT, expand=True)

        self.ai_score_label = tk.Label(info_frame, text=f"AI: {self.ai_score}",
                                       font=("Arial", 16, "bold"), fg='#e74c3c', bg='#2c3e50')
        self.ai_score_label.pack(side=tk.RIGHT)

        # Game canvas - larger for better stick display
        self.canvas = tk.Canvas(main, bg='#34495e', height=280)
        self.canvas.pack(fill=tk.X, pady=(0, 15))

        # AI move display
        self.ai_move_label = tk.Label(main, text="", font=("Arial", 12, "italic"),
                                      fg='#95a5a6', bg='#2c3e50', height=2)
        self.ai_move_label.pack(pady=(0, 10))

        # Action buttons in a compact row
        btn_frame = tk.Frame(main, bg='#2c3e50')
        btn_frame.pack(pady=(0, 15))

        self.buttons = []
        for i in range(1, 4):
            btn = tk.Button(btn_frame, text=f"Take {i}", font=("Arial", 11, "bold"),
                            bg='#3498db', fg='white', width=8, height=2,
                            command=lambda x=i: self.user_move(x))
            btn.pack(side=tk.LEFT, padx=8)
            self.buttons.append(btn)

        # Control buttons
        tk.Button(btn_frame, text="New Game", font=("Arial", 11, "bold"),
                  bg='#e74c3c', fg='white', width=8, height=2,
                  command=self.new_game).pack(side=tk.LEFT, padx=(20, 8))

        tk.Button(btn_frame, text="Exit", font=("Arial", 11, "bold"),
                  bg='#95a5a6', fg='white', width=8, height=2,
                  command=self.root.quit).pack(side=tk.LEFT, padx=8)

        self.update_display()

    def draw_sticks(self):
        self.canvas.delete("all")
        if self.pile <= 0:
            self.canvas.create_text(350, 140, text="No sticks remaining!",
                                    font=("Arial", 18, "bold"), fill='#e74c3c')
            return

        # Better spacing calculation
        cols = min(8, self.pile)  # Max 8 columns for better display
        rows = math.ceil(self.pile / cols)
        stick_w, stick_h = 15, 80
        spacing_x, spacing_y = 25, 20

        canvas_width = self.canvas.winfo_width() or 700
        total_width = cols * stick_w + (cols - 1) * spacing_x
        start_x = (canvas_width - total_width) // 2
        start_y = (280 - (rows * (stick_h + spacing_y))) // 2

        for i in range(self.pile):
            row, col = divmod(i, cols)
            x = start_x + col * (stick_w + spacing_x)
            y = start_y + row * (stick_h + spacing_y)

            # Draw stick with shadow effect
            self.canvas.create_rectangle(x+2, y+2, x + stick_w+2, y + stick_h+2,
                                         fill='#2c3e50', outline='')  # Shadow
            self.canvas.create_rectangle(x, y, x + stick_w, y + stick_h,
                                         fill='#d4a574', outline='#8b4513', width=2)

        # Stick count display
        self.canvas.create_text(350, 25, text=f"Sticks Remaining: {self.pile}",
                                font=("Arial", 16, "bold"), fill='white')

    def update_display(self):
        self.user_score_label.config(text=f"You: {self.user_score}")
        self.ai_score_label.config(text=f"AI: {self.ai_score}")

        # Update button states
        for i, btn in enumerate(self.buttons, 1):
            btn.config(state='normal' if self.pile >= i and self.user_turn else 'disabled',
                       bg='#3498db' if self.pile >= i and self.user_turn else '#95a5a6')

        self.status_label.config(
            text="Your Turn" if self.user_turn else "AI's Turn")

        # Update AI move display
        if self.ai_last_move:
            self.ai_move_label.config(
                text=f"AI's last move: Took {self.ai_last_move} stick{'s' if self.ai_last_move > 1 else ''}")
        else:
            self.ai_move_label.config(text="")

        self.root.after(10, self.draw_sticks)

    def user_move(self, sticks):
        if not self.user_turn or self.pile < sticks:
            return

        self.pile -= sticks
        self.user_turn = False
        self.check_game_end() or self.root.after(1000, self.ai_move)

    def ai_move(self):
        if self.pile <= 0:
            return

        # Optimal AI strategy
        move = next((i for i in [3, 2, 1] if self.pile >
                    i and (self.pile - i) % 4 == 0), 1)

        self.pile -= move
        self.ai_last_move = move
        self.user_turn = True
        self.check_game_end()

    def check_game_end(self):
        if self.pile <= 0:
            if self.user_turn:  # AI just moved and won
                self.ai_score += 1
                self.status_label.config(text="🤖 AI Wins! 🤖", fg='#e74c3c')
            else:  # User just moved and won
                self.user_score += 1
                self.status_label.config(text="🎉 You Win! 🎉", fg='#27ae60')

            self.root.after(2500, self.new_round)
            return True

        self.update_display()
        return False

    def new_round(self):
        self.pile = 15
        self.user_turn = True
        self.ai_last_move = None
        self.update_display()

    def new_game(self):
        self.user_score = self.ai_score = 0
        self.new_round()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    NimGame().run()
