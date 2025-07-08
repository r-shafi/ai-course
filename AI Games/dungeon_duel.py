import tkinter as tk
from tkinter import ttk
import random
import copy
import threading
import time

MAX_HP = 10
MIN_DAMAGE = 2
MAX_DAMAGE = 4
MIN_HEAL = 1
MAX_HEAL = 3
MAX_DEPTH = 2


class State:
    def __init__(self, player_hp=MAX_HP, ai_hp=MAX_HP, p_def=False, a_def=False, player_turn=True):
        self.player_hp = player_hp
        self.ai_hp = ai_hp
        self.player_defend = p_def
        self.ai_defend = a_def
        self.player_turn = player_turn

    def clone(self):
        return copy.deepcopy(self)

    def is_terminal(self):
        return self.player_hp <= 0 or self.ai_hp <= 0

    def evaluate(self):
        if self.ai_hp <= 0:
            return -100
        if self.player_hp <= 0:
            return 100
        score = self.ai_hp - self.player_hp
        if self.ai_defend:
            score += 1
        if self.player_defend:
            score -= 1
        return score


def apply_action(state, action):
    s = state.clone()
    dmg = random.randint(MIN_DAMAGE, MAX_DAMAGE)
    heal = random.randint(MIN_HEAL, MAX_HEAL)

    if s.player_turn:
        if action == 'attack':
            actual_dmg = dmg // 2 if s.ai_defend else dmg
            s.ai_hp -= actual_dmg
        elif action == 'defend':
            s.player_defend = True
        elif action == 'heal':
            s.player_hp = min(MAX_HP, s.player_hp + heal)
    else:
        if action == 'attack':
            actual_dmg = dmg // 2 if s.player_defend else dmg
            s.player_hp -= actual_dmg
        elif action == 'defend':
            s.ai_defend = True
        elif action == 'heal':
            s.ai_hp = min(MAX_HP, s.ai_hp + heal)

    s.player_turn = not s.player_turn
    if s.player_turn:
        s.player_defend = False
    else:
        s.ai_defend = False
    return s


def minimax(state, depth, maximizing):
    if depth == 0 or state.is_terminal():
        return state.evaluate(), None

    actions = ['attack', 'defend', 'heal']
    best = float('-inf') if maximizing else float('inf')
    best_action = None

    for action in actions:
        next_state = apply_action(state, action)
        val, _ = minimax(next_state, depth - 1, not maximizing)
        if maximizing:
            if val > best:
                best = val
                best_action = action
        else:
            if val < best:
                best = val
                best_action = action

    return best, best_action


class DungeonDuelGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("⚔️ Mini Dungeon Duel")
        self.root.geometry("600x500")
        self.root.configure(bg='#2c3e50')

        self.state = State()
        self.game_over = False
        self.ai_thinking = False

        self.setup_ui()
        self.update_display()

    def setup_ui(self):
        # Title
        title_label = tk.Label(self.root, text="⚔️ Mini Dungeon Duel ⚔️",
                               font=("Arial", 24, "bold"),
                               bg='#2c3e50', fg='#ecf0f1')
        title_label.pack(pady=20)

        # Game area frame
        game_frame = tk.Frame(self.root, bg='#34495e', relief='raised', bd=3)
        game_frame.pack(pady=10, padx=20, fill='both', expand=True)

        # Player section
        player_frame = tk.Frame(
            game_frame, bg='#3498db', relief='raised', bd=2)
        player_frame.pack(side='left', fill='both',
                          expand=True, padx=10, pady=10)

        tk.Label(player_frame, text="🧙‍♂️ YOU", font=("Arial", 16, "bold"),
                 bg='#3498db', fg='white').pack(pady=5)

        self.player_hp_label = tk.Label(player_frame, text="", font=("Arial", 14),
                                        bg='#3498db', fg='white')
        self.player_hp_label.pack(pady=5)

        self.player_status_label = tk.Label(player_frame, text="", font=("Arial", 12),
                                            bg='#3498db', fg='#ecf0f1')
        self.player_status_label.pack(pady=5)

        # AI section
        ai_frame = tk.Frame(game_frame, bg='#e74c3c', relief='raised', bd=2)
        ai_frame.pack(side='right', fill='both', expand=True, padx=10, pady=10)

        tk.Label(ai_frame, text="🤖 AI", font=("Arial", 16, "bold"),
                 bg='#e74c3c', fg='white').pack(pady=5)

        self.ai_hp_label = tk.Label(ai_frame, text="", font=("Arial", 14),
                                    bg='#e74c3c', fg='white')
        self.ai_hp_label.pack(pady=5)

        self.ai_status_label = tk.Label(ai_frame, text="", font=("Arial", 12),
                                        bg='#e74c3c', fg='#ecf0f1')
        self.ai_status_label.pack(pady=5)

        # Action log
        self.log_frame = tk.Frame(self.root, bg='#2c3e50')
        self.log_frame.pack(pady=10, padx=20, fill='x')

        tk.Label(self.log_frame, text="📜 Battle Log", font=("Arial", 12, "bold"),
                 bg='#2c3e50', fg='#ecf0f1').pack()

        self.log_text = tk.Text(self.log_frame, height=4, width=60,
                                bg='#34495e', fg='#ecf0f1', font=("Arial", 10),
                                state='disabled')
        self.log_text.pack(pady=5)

        # Action buttons
        button_frame = tk.Frame(self.root, bg='#2c3e50')
        button_frame.pack(pady=10)

        self.attack_btn = tk.Button(button_frame, text="⚔️ Attack",
                                    command=lambda: self.player_action(
                                        'attack'),
                                    font=("Arial", 12, "bold"), width=10, height=2,
                                    bg='#e74c3c', fg='white', activebackground='#c0392b')
        self.attack_btn.pack(side='left', padx=5)

        self.defend_btn = tk.Button(button_frame, text="🛡️ Defend",
                                    command=lambda: self.player_action(
                                        'defend'),
                                    font=("Arial", 12, "bold"), width=10, height=2,
                                    bg='#f39c12', fg='white', activebackground='#e67e22')
        self.defend_btn.pack(side='left', padx=5)

        self.heal_btn = tk.Button(button_frame, text="💚 Heal",
                                  command=lambda: self.player_action('heal'),
                                  font=("Arial", 12, "bold"), width=10, height=2,
                                  bg='#27ae60', fg='white', activebackground='#229954')
        self.heal_btn.pack(side='left', padx=5)

        # Reset button
        self.reset_btn = tk.Button(self.root, text="🔄 New Game",
                                   command=self.reset_game,
                                   font=("Arial", 12, "bold"), width=12, height=1,
                                   bg='#9b59b6', fg='white', activebackground='#8e44ad')
        self.reset_btn.pack(pady=10)

    def update_display(self):
        # Update HP bars with hearts
        player_hearts = "❤️" * self.state.player_hp + \
            "🖤" * (MAX_HP - self.state.player_hp)
        ai_hearts = "❤️" * self.state.ai_hp + "🖤" * (MAX_HP - self.state.ai_hp)

        self.player_hp_label.config(
            text=f"HP: {self.state.player_hp}/{MAX_HP}\n{player_hearts}")
        self.ai_hp_label.config(
            text=f"HP: {self.state.ai_hp}/{MAX_HP}\n{ai_hearts}")

        # Update status
        player_status = "🛡️ Defending" if self.state.player_defend else ""
        ai_status = "🛡️ Defending" if self.state.ai_defend else ""

        if self.ai_thinking:
            ai_status = "🤔 Thinking..."

        self.player_status_label.config(text=player_status)
        self.ai_status_label.config(text=ai_status)

        # Enable/disable buttons
        if self.game_over or not self.state.player_turn or self.ai_thinking:
            self.attack_btn.config(state='disabled')
            self.defend_btn.config(state='disabled')
            self.heal_btn.config(state='disabled')
        else:
            self.attack_btn.config(state='normal')
            self.defend_btn.config(state='normal')
            self.heal_btn.config(state='normal')

    def add_log(self, message):
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')

    def player_action(self, action):
        if self.game_over or not self.state.player_turn:
            return

        before_ai_hp = self.state.ai_hp
        before_player_hp = self.state.player_hp

        self.state = apply_action(self.state, action)

        # Log player action
        if action == 'attack':
            damage = before_ai_hp - self.state.ai_hp
            self.add_log(f"🧙‍♂️ You attack! AI takes {damage} damage! ⚔️")
        elif action == 'defend':
            self.add_log("🧙‍♂️ You brace for the next attack! 🛡️")
        elif action == 'heal':
            healing = self.state.player_hp - before_player_hp
            self.add_log(f"🧙‍♂️ You heal {healing} HP! 💚")

        self.update_display()

        if self.state.is_terminal():
            self.end_game()
        else:
            # AI turn
            self.ai_turn()

    def ai_turn(self):
        if self.game_over or self.state.player_turn:
            return

        self.ai_thinking = True
        self.update_display()

        # Run AI thinking in a separate thread
        thread = threading.Thread(target=self.ai_think_and_act)
        thread.start()

    def ai_think_and_act(self):
        # Simulate thinking time
        time.sleep(random.uniform(1.0, 2.5))

        # Get AI action
        _, ai_action = minimax(self.state, MAX_DEPTH, maximizing=True)

        # Execute on main thread
        self.root.after(0, self.execute_ai_action, ai_action)

    def execute_ai_action(self, ai_action):
        self.ai_thinking = False

        before_ai_hp = self.state.ai_hp
        before_player_hp = self.state.player_hp

        self.state = apply_action(self.state, ai_action)

        # Log AI action
        if ai_action == 'attack':
            damage = before_player_hp - self.state.player_hp
            self.add_log(f"🤖 AI attacks! You take {damage} damage! ⚔️")
        elif ai_action == 'defend':
            self.add_log("🤖 AI defends! 🛡️")
        elif ai_action == 'heal':
            healing = self.state.ai_hp - before_ai_hp
            self.add_log(f"🤖 AI heals {healing} HP! 💚")

        self.update_display()

        if self.state.is_terminal():
            self.end_game()

    def end_game(self):
        self.game_over = True
        self.update_display()

        if self.state.player_hp <= 0 and self.state.ai_hp <= 0:
            self.add_log("🤝 It's a draw! Both warriors fall!")
        elif self.state.player_hp <= 0:
            self.add_log("💀 You have been defeated! 😢")
        else:
            self.add_log("🎉 Victory! You have triumphed! 🏆")

    def reset_game(self):
        self.state = State()
        self.game_over = False
        self.ai_thinking = False

        # Clear log
        self.log_text.config(state='normal')
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state='disabled')

        self.add_log("🎮 New game started! Choose your action!")
        self.update_display()


def main():
    root = tk.Tk()
    game = DungeonDuelGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
