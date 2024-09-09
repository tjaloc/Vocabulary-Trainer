"""TK-INTER VOCABULARY TRAINER

Based on lesson/ day 31 of "100 days of code - Python Bootcamp"
"""

from tkinter import *
import pandas as pd

BACKGROUND_COLOR = "#B1DDC6"
WORDS_TO_LEARN_ORIGINAL = 'data/french_words.csv'
WORDS_TO_LEARN = 'data/words_to_learn.csv'

to_learn = None
current_card = None

# ------------------------- CSV DATA ------------------------- #
# If we have started to learn and therefore have a reduced list
# of words left to learn WORDS_TO_LEARN will be used else the
# original/ full list.

try:
    to_learn = pd.read_csv(WORDS_TO_LEARN)
except FileNotFoundError:
    to_learn = pd.read_csv(WORDS_TO_LEARN_ORIGINAL)

# ------------------------ FUNCTIONS ------------------------ #
def next_card():
    """Chose a random item from vocabulary data frame. Display the word in the first language.
     After 3 seconds show the translation on back of the flash card.
    """
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = to_learn.sample()
    canvas.itemconfig(card_bgd, image=card_front)
    canvas.itemconfig(card_lang, text='French', fill='black')
    canvas.itemconfig(card_word, text=current_card['French'].item(), fill='black')
    flip_timer = window.after(3000, func=flip_card)

def flip_card():
    """Display translation on the back of the flash card.
    """
    canvas.itemconfig(card_bgd, image=card_back)
    canvas.itemconfig(card_lang, text='English', fill='white')
    canvas.itemconfig(card_word, text=current_card['English'].item(), fill='white')

def is_known():
    """Remove known terms from the WORDS_TO_LEARN vocabulary.
    """
    global to_learn
    to_learn = to_learn.drop(index=current_card.index)
    to_learn.to_csv(WORDS_TO_LEARN, index=False)
    next_card()


# ---------------------------- GUI ---------------------------- #
window = Tk()
window.title('Flashy')
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)
flip_timer = window.after(3000, flip_card)

# create elements
canvas = Canvas(window, bg=BACKGROUND_COLOR, width=800, height=526, highlightthickness=0)
card_front = PhotoImage(file='images/card_front.png')
card_back = PhotoImage(file='images/card_back.png')
card_bgd = canvas.create_image(415, 263, image=card_front, anchor='center')
card_lang = canvas.create_text(400, 150, text='', font=('Verdana', 40, 'italic'))
card_word = canvas.create_text(400, 263, text='', font=('Verdana', 50, 'bold'))
canvas.grid(row=0, column=0, columnspan=2)

btn_unknown_img = PhotoImage(file='images/wrong.png')
btn_unknown = Button(image=btn_unknown_img, highlightthickness=0, command=next_card)
btn_unknown.grid(row=1, column=0)

btn_known_img = PhotoImage(file='images/right.png')
btn_known = Button(image=btn_known_img, highlightthickness=0, command=is_known)
btn_known.grid(row=1, column=1)

# -------------------- RUN VOCABULARY TEST --------------------- #
if __name__ == '__main__':
    next_card()
    window.lift()
    window.mainloop()
