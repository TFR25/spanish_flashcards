import random
from tkinter import *
import pandas as pd

BACKGROUND_COLOR = "#B1DDC6"
FONT_NAME = "Ariel"

df_dict = {}

try:
    df = pd.read_csv("./data/study.csv")
except FileNotFoundError:
    df = pd.read_csv("./data/Spanish_English_Flashcard_Data.csv")
    df_dict = df.to_dict(orient="records")
else:
    df_dict = df.to_dict(orient="records")


def new_word():
    """a new word is generated every 3 seconds"""
    global flashcard, timer
    window.after_cancel(timer)  # reset timer
    flashcard = random.choice(df_dict)
    canvas.itemconfig(card_title, text="Spanish", fill="black")
    canvas.itemconfig(card_word, fill="black", text=flashcard["Spanish"].lower())
    canvas.itemconfig(canvas_image, image=card_front)
    timer = window.after(3000, func=flip_card)


def flip_card():
    """card is flipped displaying the answer after 3 seconds"""
    canvas.itemconfig(canvas_image, image=card_back)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=flashcard["English"].lower(), fill="white")


def remove_word():
    """word is removed if checkmark button pressed, indicating player knows the word and its translation."""
    df_dict.remove(flashcard)
    new_df_dict = pd.DataFrame(df_dict)
    new_df_dict.to_csv("./data/study.csv", index=False)
    new_word()


window = Tk()
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
window.title("Spanish Flashcards")

flashcard = {}
timer = window.after(3000, func=flip_card)

# define images
card_front = PhotoImage(file="./images/card_front.png")
card_back = PhotoImage(file="./images/card_back.png")
correct_button = PhotoImage(file="./images/right.png")
incorrect_button = PhotoImage(file="./images/wrong.png")


canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

canvas_image = canvas.create_image(400, 263, image=card_front)

card_title = canvas.create_text(400, 150, text="", font=(FONT_NAME, 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=(FONT_NAME, 60, "bold"))

right_button = Button(image=correct_button, highlightthickness=0, relief=GROOVE, command=remove_word)
right_button.grid(row=1, column=0, padx=50, pady=50)

wrong_button = Button(image=incorrect_button, highlightthickness=0, relief=GROOVE, command=new_word)
wrong_button.grid(row=1, column=1, padx=50, pady=50)

new_word()

window.mainloop()
