import tkinter as tk
from tkinter import messagebox
import random

def get_word_list(file_name):
    with open(file_name, 'r') as file:
        return [line.strip().upper() for line in file if len(line.strip()) == 5]

word_list = get_word_list('Path\to\wordle_complete.txt')

def start_game():
    global word_to_guess, current_row, labels, guess_button, correct_letters
    word_to_guess = random.choice(word_list)
    current_row = 0
    correct_letters = set()  # Reset the correct letters
    for i in range(6):
        for j in range(5):
            labels[i][j].config(bg='white', text=' ')
    guess_button.config(state='normal')
    guess_var.set('')  # Clear the guess

    # Reset the keyboard colors
    for letter, button in keyboard_buttons.items():
        button.config(bg='white', fg='black')

def update_labels(guess):
    for i in range(5):
        if i < len(guess):
            labels[current_row][i].config(text=guess[i])
        else:
            labels[current_row][i].config(text=' ')

def update_letters_callback(*args):
    guess = guess_var.get().upper()
    if len(guess) > 5:  # Limit the length of the guess to 5 letters
        guess_var.set(guess[:5])
    else:
        update_labels(guess)

def check_guess(event=None):
    global current_row, word_to_guess
    guess = guess_var.get().upper()
    guess_var.set('')  # Clear the guess variable

    if len(guess) != 5 or guess not in word_list:
        messagebox.showerror("Error", "Invalid word. Please enter a five-letter word from the list.")
        return

    # Update the labels with the guess
    update_labels(guess)

    for i in range(5):
        if guess[i] == word_to_guess[i]:
            labels[current_row][i].config(bg="green", fg="white", text=guess[i])
            # Only change the color of the button if it's not already known to be correct
            if guess[i] not in correct_letters:
                keyboard_buttons[guess[i]].config(bg="green", fg="white")
            correct_letters.add(guess[i]) # Add the letter to the correct_letters set
        elif guess[i] in word_to_guess:
            labels[current_row][i].config(bg="yellow", fg="black", text=guess[i])
            # Only change the color of the button if it's not already known to be correct
            if guess[i] not in correct_letters:
                keyboard_buttons[guess[i]].config(bg="yellow", fg="black")
        else:
            labels[current_row][i].config(bg="gray", fg="black", text=guess[i])
            # Only change the color of the button if it's not already known to be correct
            if guess[i] not in correct_letters:
                keyboard_buttons[guess[i]].config(bg="gray", fg="black")

    if guess == word_to_guess:
        messagebox.showinfo("Congratulations!", "You guessed the word!")
        start_game()
    else:
        current_row += 1

    if current_row == 6:
        messagebox.showinfo("Game Over", f"You reached the max number of guesses. The word was: {word_to_guess}")
        start_game()

window = tk.Tk()
window.title('Wordle Game')

labels = [[tk.Label(window, width=5, height=2, bg='white', bd=1, relief='solid', font=("Helvetica", 24)) for _ in range(5)] for _ in range(6)]

for i in range(6):
    for j in range(5):
        labels[i][j].grid(row=i, column=j, padx=5, pady=5)

guess_var = tk.StringVar()
guess_var.trace('w', update_letters_callback)

guess_entry = tk.Entry(window, textvariable=guess_var, font=("Helvetica", 24))
guess_entry.grid(row=6, column=0, columnspan=5, sticky='we')

#Guess Button
guess_button = tk.Button(window, text='Guess', command=check_guess, height=2, width=10)
guess_button.grid(row=8, column=1, columnspan=1)

#Play Again Button
replay_button = tk.Button(window, text='Play Again', command=start_game, height=2, width=10)
replay_button.grid(row=8, column=3, columnspan=1)

window.bind('<Return>', check_guess) 

correct_letters = set()
keyboard_buttons = {}

# Virtual keyboard
keyboard_frame = tk.Frame(window)
keyboard_frame.grid(row=9, column=0, columnspan=5)

def press_key(key):
    guess_var.set(guess_var.get() + key)  # Add the letter to the guess variable

keyboard_layout = [
    'QWERTYUIOP',
    ' ASDFGHJKL',
    '  ZXCVBNM'
]

for y, row in enumerate(keyboard_layout):
    for x, letter in enumerate(row):
        if letter != ' ':
            keyboard_buttons[letter] = tk.Button(keyboard_frame, text=letter, font=("Helvetica", 20), command=lambda l=letter: press_key(l))
            keyboard_buttons[letter].grid(row=y, column=x, padx=5, pady=5)

start_game()
window.mainloop()



