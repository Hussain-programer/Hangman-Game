import tkinter as tk
import random
from word_list import word_list

class HangmanGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Hangman Game")
        self.master.geometry("900x750")
        self.master.configure(bg="Cyan")
        self.word_list = word_list
        self.secret_word = self.choose_secret_word()
        self.correct_guesses = set()
        self.incorrect_guesses = set()
        self.attempts_left = 7
        self.initialize_gui()
    def initialize_gui(self):
        button_bg = "#4a7a8c"
        button_fg = "white"
        button_font = ("Helvetica", 12, "bold")
        self.hangman_canvas = tk.Canvas(self.master, width=300, height=300, bg="#C0C0C0")
        self.hangman_canvas.pack(pady=20)
        self.word_display = tk.Label(
            self.master,
            text="_ " * len(self.secret_word),
            font=("Helvetica", 30),
            bg="light cyan",
        )
        self.word_display.pack(pady=(40, 20))
        self.reset_button = tk.Button(
            self.master,
            text="Reset Game",
            command=self.reset_game,
            width=20,
            height=2,
            bg=button_bg,
            fg=button_fg,
            font=button_font,
        )
        self.reset_button.pack(pady=(10, 0))
        self.buttons_frame = tk.Frame(self.master)
        self.buttons_frame.pack(pady=20)
        self.setup_alphabet_buttons()
    def setup_alphabet_buttons(self):
        button_bg = "#808080"
        button_fg = "#C0C0C0"
        button_font = ("Helvetica", 12, "bold")
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        lower_row = alphabet[26:]
        upper_row = alphabet[:26]
        lower_frame = tk.Frame(self.buttons_frame)
        lower_frame.pack()
        upper_frame = tk.Frame(self.buttons_frame)
        upper_frame.pack()
        self.buttons = {}  # dictionary to store the buttons
        for letter in upper_row:
            button = tk.Button(
                upper_frame,
                text=letter,
                command=lambda l=letter: self.guess_letter(l),
                width=2,
                height=1,
                bg=button_bg,
                fg=button_fg,
                font=button_font,
                relief="flat",
                highlightthickness=0,
                bd=0
            )
            button.pack(side="left", padx=2, pady=2)
            self.buttons[letter] = button  # store the button in the dictionary
        for letter in lower_row:
            button = tk.Button(
                lower_frame,
                text=letter,
                command=lambda l=letter: self.guess_letter(l),
                width=2,
                height=1,
                bg=button_bg,
                fg=button_fg,
                font=button_font,
            )
            button.pack(side="left", padx=2, pady=2)
            self.buttons[letter] = button  # store the button in the dictionary
    def guess_letter(self, letter):
        if letter in self.secret_word:
            self.buttons[letter].config(bg="#00FF00")  # change to green if correct
        else:
            self.buttons[letter].config(bg="#FF0000")  # change to red if incorrect
    def choose_secret_word(self):
        return random.choice(self.word_list)
    def update_hangman_canvas(self):
        self.hangman_canvas.delete("all")
        stages = [
            self.draw_head,
            self.draw_body,
            self.draw_left_arm,
            self.draw_right_arm,
            self.draw_left_leg,
            self.draw_right_leg,
            self.draw_face,
        ]
        for i in range(len(self.incorrect_guesses)):
            if i < len(stages):
                stages[i]()
    def draw_head(self):
        self.hangman_canvas.create_oval(125, 50, 185, 110, outline="black")
    def draw_body(self):
        self.hangman_canvas.create_line(155, 110, 155, 170, fill="black")
    def draw_left_arm(self):
        self.hangman_canvas.create_line(155, 130, 125, 150, fill="black")
    def draw_right_arm(self):
        self.hangman_canvas.create_line(155, 130, 185, 150, fill="black")
    def draw_left_leg(self):
        self.hangman_canvas.create_line(155, 170, 125, 200, fill="black")
    def draw_right_leg(self):
        self.hangman_canvas.create_line(155, 170, 185, 200, fill="black")
    def draw_face(self):
        self.hangman_canvas.create_line(140, 70, 150, 80, fill="white")
        self.hangman_canvas.create_line(160, 70, 170, 80, fill="white")
        self.hangman_canvas.create_arc(
            140, 85, 170, 105, start=0, extent=-180, fill="white"
        )
    def guess_letter(self, letter):
        if letter in self.secret_word and letter not in self.correct_guesses:
            self.correct_guesses.add(letter)
        elif letter not in self.incorrect_guesses:
            self.incorrect_guesses.add(letter)
            self.attempts_left -= 1
            self.update_hangman_canvas()
        self.update_word_display()
        self.check_game_over()
    def update_word_display(self):
        displayed_word = " ".join(
        [
                letter if letter in self.correct_guesses else "_"
                for letter in self.secret_word
            ]
        )
        self.word_display.config(text=displayed_word)
    def check_game_over(self):
        if set(self.secret_word).issubset(self.correct_guesses):
            self.display_game_over_message("Congratulations, you've won!")
        elif self.attempts_left == 0:
            self.display_game_over_message(
                f"Game over! The word was: {self.secret_word}"
            )
    def display_game_over_message(self, message):
        stylish_font = ("Arial", 18, "italic")
        button_bg = "#4a7a8c"
        button_fg = "white"
        button_font = ("Helvetica", 12, "bold")
        self.reset_button.pack_forget()
        self.buttons_frame.pack_forget()
        self.game_over_label = tk.Label(
            self.master, text=message, font=stylish_font, fg="#C0C0C0", bg="#007FFF"
    )
        self.game_over_label.pack(pady=(10, 20))
        if not hasattr(self, "restart_button"):
            self.restart_button = tk.Button(
            self.master,
            text="Restart Game",
            command=self.reset_game,
            width=20,
            height=2,
            bg=button_bg,
            fg=button_fg,
            font=button_font,
        )
        self.restart_button.pack(pady=(10, 20))
    def reset_game(self):
        self.secret_word = self.choose_secret_word()
        self.correct_guesses = set()
        self.incorrect_guesses = set()
        self.attempts_left = 7
        num_revealed_letters = 2  # you can adjust this number as needed
        revealed_letters = random.sample(self.secret_word, num_revealed_letters)
        self.correct_guesses.update(revealed_letters)
        self.word_display['text'] = " ".join([letter if letter in self.correct_guesses else "_" for letter in self.secret_word])
        self.update_hangman_canvas() 
        self.hangman_canvas.delete("all")
        self.update_word_display()
        for frame in self.buttons_frame.winfo_children():
            for button in frame.winfo_children():
                button.configure(state=tk.NORMAL)
        self.reset_button.pack(pady=(10, 0))
        if hasattr(self, "game_over_label") and self.game_over_label.winfo_exists():
            self.game_over_label.pack_forget()
        if hasattr(self, "restart_button") and self.restart_button.winfo_exists():
            self.restart_button.pack_forget()
        self.buttons_frame.pack()
def main():
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()
if __name__ == "__main__":
    main()