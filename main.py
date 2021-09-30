import tkinter as tk
import random
from functools import partial

class Memory(tk.Tk):
    def __init__(self):
        super().__init__()
        self.cards = [tk.PhotoImage(file='images/square.png'), tk.PhotoImage(file='images/circle.png'),
                      tk.PhotoImage(file='images/heart.png'), tk.PhotoImage(file='images/octagon.png'),
                      tk.PhotoImage(file='images/star.png')] * 2

        random.seed()
        random.shuffle(self.cards)

        self.turn = 0
        self.flipped = []
        self.facing = [False] * len(self.cards)
        self.back_img = tk.PhotoImage(file='images/back.png')
        self.turns = 0

        self.init_ui()
    def init_ui(self):
        self.title('Memory')
        card_frame = tk.Frame()

        self.cards_btn = [tk.Button(card_frame, image=self.back_img, command=partial(self.pick_card, i)) for i in range(len(self.cards))]

        for i, card in enumerate(self.cards_btn):
            c = i % 5
            r = (i - c) // 5
            card.grid(row=r, column=c)

        card_frame.pack()

        self.new_btn = tk.Button(self, text='New game', command=self.reset)
        self.new_btn.pack()

        self.turns_lbl = tk.Label(self, text='Turns: 0')
        self.turns_lbl.pack()

    def reset(self):
        random.shuffle(self.cards)
        self.turn = 0

        self.flipped = []
        self.facing = [False] * len(self.cards)

        self.change_all_facedown_state(tk.NORMAL)

        self.turns = 0
        self.update_turns_lbl()

        for card in self.cards_btn:
            card.config(image=self.back_img)

    def flip_card(self, i):
        if self.facing[i]:
            self.cards_btn[i].config(image=self.back_img)
            self.facing[i] = False
        else:
            self.cards_btn[i].config(image=self.cards[i])

    def pick_card(self, button_i):
        self.flip_card(button_i)
        self.flipped.append(button_i)
        self.facing[button_i] = True
        self.cards_btn[button_i].config(state=tk.DISABLED)

        if self.turn == 1:
            self.turns += 1
            self.update_turns_lbl()

            self.change_all_facedown_state(tk.DISABLED)
            if self.cards[self.flipped[0]] == self.cards[self.flipped[1]]:
                self.change_all_facedown_state(tk.NORMAL)
                self.flipped.clear()
            else:
                self.after(1000, lambda: self.flip_card(self.flipped[0]))
                self.after(1000, lambda: self.flip_card(self.flipped[1]))
                self.after(1000, lambda: self.change_all_facedown_state(tk.NORMAL))
                self.after(1000, self.flipped.clear)

        # if self.has_won():
        #     self.after(1000, self.reset)

        self.turn += 1
        self.turn %= 2

    def has_won(self):
        return False not in self.facing

    def change_all_facedown_state(self, state):
        for i, b in enumerate(self.cards_btn):
            if not self.facing[i]:
                b.config(state=state)

    def update_turns_lbl(self):
        self.turns_lbl.config(text=f'Turns: {self.turns}')

if __name__ == '__main__':
    game = Memory()
    game.mainloop()