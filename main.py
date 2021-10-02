import tkinter as tk
from tkinter import messagebox
import random
from functools import partial
from pygame import mixer
import os
from PIL import Image, ImageTk


class Memory(tk.Tk):
    def __init__(self):
        super().__init__()

        directory = 'images/shapes/'
        self.cards = [ImageTk.PhotoImage(Image.open(directory+os.fsdecode(f)).resize((128, 128))) for f in os.listdir(os.fsencode(directory))] * 2

        self.audio = Audio()

        self.turn = 0
        self.flipped = []
        self.facing_up = [False] * len(self.cards)
        self.back_img = tk.PhotoImage(file='images/back.png')
        self.turns = 0
        self.my_font = ('tkDefaultFont', 18)
        self.run = True
        self.waiting = False

        random.seed()
        random.shuffle(self.cards)

        self.init_ui()

    def init_ui(self):
        self.title('Memory')
        self.geometry('705x690')
        self.bg='#3F88C5'
        self.config(bg=self.bg)

        self.win_lbl = tk.Label(self, text='Pick a card', bg=self.bg, fg='white', font=self.my_font)
        self.win_lbl.pack(padx=5, pady=5)

        card_frame = tk.Frame(self, bg='#3F88C5')

        self.cards_btn = [tk.Button(card_frame, image=self.back_img, bd=0, command=partial(self.pick_card, i)) for i in range(len(self.cards))]

        for i, card in enumerate(self.cards_btn):
            c = i % 5
            r = (i - c) // 5
            card.grid(row=r, column=c, padx=5, pady=5)

        card_frame.pack()

        bottom_frame = tk.Frame(self, bg='#3F88C5', width=705, height=100)
        bottom_frame.pack_propagate(False)

        new_btn = tk.Button(bottom_frame, text='New game', bg='#E94F37', fg='white', font=self.my_font, command=self.reset)
        new_btn.pack(side=tk.RIGHT, padx=10, pady=10)

        self.turns_lbl = tk.Label(bottom_frame, font=self.my_font, bg=self.bg, fg='white', text='Turns: 0')
        self.turns_lbl.pack(side=tk.LEFT, padx=10, pady=10)

        bottom_frame.pack()

        menubar = tk.Menu(self)

        deckmenu = tk.Menu(menubar, tearoff=0)
        deckmenu.add_radiobutton(label="Shapes", command=lambda: self.change_deck('shapes'))
        deckmenu.add_radiobutton(label="Shrek", command=lambda: self.change_deck('shrek'))
        deckmenu.add_radiobutton(label='Star Wars Prequels', command=lambda: self.change_deck('prequels'))
        deckmenu.add_radiobutton(label='Marvel Heroes', command=lambda: self.change_deck('marvelheroes'))
        deckmenu.add_radiobutton(label='Marvel Villains', command=lambda: self.change_deck('marvelvillains'))
        menubar.add_cascade(label="Deck", menu=deckmenu)
        self.config(menu=menubar)

        print(self.winfo_height(), self.winfo_width())

    def reset(self):
        if self.run:
            again = messagebox.askyesno(title='Memory', message='Are you sure you want to reset the game?')
            if not again:
                return

        self.run = True
        self.waiting = False
        self.win_lbl.config(text='Pick a card')
        random.shuffle(self.cards)
        self.turn = 0

        self.flipped = []
        self.facing_up = [False] * len(self.cards)

        self.turns = 0
        self.update_turns_lbl()

        for card in self.cards_btn:
            card.config(image=self.back_img)

    def flip_card(self, i):
        if self.facing_up[i]:
            self.cards_btn[i].config(image=self.back_img)
            self.facing_up[i] = False
        else:
            self.cards_btn[i].config(image=self.cards[i])

    def pick_card(self, button_i):
        if self.facing_up[button_i] or self.waiting:
            return

        self.flip_card(button_i)
        self.flipped.append(button_i)
        self.facing_up[button_i] = True

        if self.turn == 1:
            if self.cards[self.flipped[0]] == self.cards[self.flipped[1]]:
                if not self.has_won():
                    self.audio.correct.play()

                self.flipped.clear()
            else:
                self.audio.incorrect.play()

                self.waiting = True

                self.turns += 1
                self.update_turns_lbl()

                self.after(2000, self.no_match)

        if self.has_won():
            self.audio.win.play()
            self.turns += 1
            self.update_turns_lbl()
            self.run = False
            self.win_lbl.config(text='You win')

        self.turn += 1
        self.turn %= 2

    def no_match(self):
        self.flip_card(self.flipped[0])
        self.flip_card(self.flipped[1])
        self.flipped.clear()
        self.waiting = False

    def has_won(self):
        return False not in self.facing_up

    def update_turns_lbl(self):
        self.turns_lbl.config(text=f'Turns: {self.turns}')

    def change_deck(self, deck):
        directory = f'images/{deck}/'

        self.cards = [ImageTk.PhotoImage(Image.open(directory+os.fsdecode(f)).resize((128, 128))) for f in os.listdir(os.fsencode(directory))] * 2
        self.reset()


class Audio:
    def __init__(self):
        mixer.init()
        self.win = mixer.Sound('audio/youWin.wav')
        self.correct = mixer.Sound('audio/correct.wav')
        self.incorrect = mixer.Sound('audio/incorrect.wav')
        self.all_sounds = (self.win, self.correct, self.incorrect)


if __name__ == '__main__':
    game = Memory()
    game.mainloop()