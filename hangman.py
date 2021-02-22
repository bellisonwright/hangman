#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 16:12:53 2021

@author: bertie
"""

import pandas as pd
import numpy as np
import string
from random import randrange

class Hangman():
    def __init__(self, dictionary, print_outputs=True, pictures=['\n\n\n\n\n\n\n         ', '\n\n       \n       \n       \n       \n       \n=========', '\n       \n      |\n      |\n      |\n      |\n      |\n=========', '\n  +---+\n      |\n      |\n      |\n      |\n      |\n=========', '\n  +---+\n     \\|\n      |\n      |\n      |\n      |\n=========', '\n  +---+\n  |  \\|\n      |\n      |\n      |\n      |\n=========', '\n  +---+\n  |  \\|\n  O   |\n      |\n      |\n      |\n=========', '\n  +---+\n  |  \\|\n  O   |\n  |   |\n      |\n      |\n=========', '\n  +---+\n  |  \\|\n  O   |\n /|   |\n      |\n      |\n=========', '\n  +---+\n  |  \\|\n  O   |\n /|\\  |\n      |\n      |\n=========', '\n  +---+\n  |  \\|\n  O   |\n /|\\  |\n /    |\n      |\n=========', '\n  +---+\n  |  \\|\n  O   |\n /|\\  |\n / \\  |\n      |\n=========']):
        self.dictionary = dictionary
        self.pictures = pictures
        self.print_outputs = print_outputs
    
    def initialise(self, word_to_guess):
        self.word_to_guess = word_to_guess.lower()
        print("Guessing {}.".format(self.word_to_guess))
        self.incorrect_count = 0
        self.guessed_letters = []
        self.alphabet = list(string.ascii_lowercase)
        self.is_word_guessed = False
        self.blanks = ["_" for i in range(len(self.word_to_guess))]
        
    def one_go(self, letter):
        letter = letter.lower()
        if letter in self.alphabet:
            if letter not in self.guessed_letters:
                self.guessed_letters.append(letter)
                if letter in self.word_to_guess:
                    if self.print_outputs == True:
                        print("Well done, {} is correct!".format(letter))
                        print(self.pictures[self.incorrect_count])
                        print("testing",[i for i, l in enumerate(self.word_to_guess) if l == letter])
                        for i in [i for i, l in enumerate(self.word_to_guess) if l == letter]:
                            # print("test",i,l)
                            self.blanks[i] = letter.upper()
                        print(" ".join(self.blanks))
                else:
                    self.incorrect_count += 1
                    if self.print_outputs == True:
                        print("Unlucky, {} is incorrect...".format(letter))
                        print(self.pictures[self.incorrect_count])
                        print(" ".join(self.blanks))
                    
            else:
                if self.print_outputs == True:
                    print("{} has already been tried. Please try another letter.".letter)
        else:
            if self.print_outputs == True:
                print("{} is not a letter. Please try again.".letter)

    def iterate(self, strategy="random"):
        self.letters_left = self.alphabet
        while self.is_word_guessed == False:
            if strategy == "random":
                letter = self.letters_left[randrange(len(self.letters_left))]
                self.one_go(letter)
                if letter in self.letters_left:
                    self.letters_left.remove(letter)









if __name__ == "__main__":
    import_csv = pd.read_csv("dictionary.csv",usecols=[0],header=None,names=["Words"])
    dictionary = np.array(import_csv[~import_csv.Words.str.contains(r'[^a-z]',na=False)]).ravel()
    pictures11 = ['\n\n\n\n\n\n\n         ', '\n\n       \n       \n       \n       \n       \n=========', '\n       \n      |\n      |\n      |\n      |\n      |\n=========', '\n  +---+\n      |\n      |\n      |\n      |\n      |\n=========', '\n  +---+\n     \\|\n      |\n      |\n      |\n      |\n=========', '\n  +---+\n  |  \\|\n      |\n      |\n      |\n      |\n=========', '\n  +---+\n  |  \\|\n  O   |\n      |\n      |\n      |\n=========', '\n  +---+\n  |  \\|\n  O   |\n  |   |\n      |\n      |\n=========', '\n  +---+\n  |  \\|\n  O   |\n /|   |\n      |\n      |\n=========', '\n  +---+\n  |  \\|\n  O   |\n /|\\  |\n      |\n      |\n=========', '\n  +---+\n  |  \\|\n  O   |\n /|\\  |\n /    |\n      |\n=========', '\n  +---+\n  |  \\|\n  O   |\n /|\\  |\n / \\  |\n      |\n=========']
    pictures7 = pictures11[5:]
    
    game = Hangman(dictionary)
    game.initialise("Hello")
    game.one_go("h")
    game.one_go("f")
    game.one_go("g")
    game.one_go("k")
    game.one_go("l")