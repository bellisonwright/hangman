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
    '''
    Game of hangman.
    '''
    def __init__(self, dictionary_array, print_outputs=True, pictures=None):
        '''
        :param dictionary_array: dictionary, scraped from Oxford Dictionary of English
        :param print_outputs: True/False, should outputs of each game be printed
        :param pictures: ASCII graphics for hangman figure in a list
        '''
        self.dictionary = dictionary_array
        self.print_outputs = print_outputs
        self.pictures = pictures if pictures else ['\n\n\n\n\n\n\n         ', '\n\n       \n       \n       \n       \n       \n=========', '\n       \n      |\n      |\n      |\n      |\n      |\n=========', '\n  +---+\n      |\n      |\n      |\n      |\n      |\n=========', '\n  +---+\n     \\|\n      |\n      |\n      |\n      |\n=========', '\n  +---+\n  |  \\|\n      |\n      |\n      |\n      |\n=========', '\n  +---+\n  |  \\|\n  O   |\n      |\n      |\n      |\n=========', '\n  +---+\n  |  \\|\n  O   |\n  |   |\n      |\n      |\n=========', '\n  +---+\n  |  \\|\n  O   |\n /|   |\n      |\n      |\n=========', '\n  +---+\n  |  \\|\n  O   |\n /|\\  |\n      |\n      |\n=========', '\n  +---+\n  |  \\|\n  O   |\n /|\\  |\n /    |\n      |\n=========', '\n  +---+\n  |  \\|\n  O   |\n /|\\  |\n / \\  |\n      |\n=========']

        self.incorrect_letters = []
        self.guessed_letters = []
        self.alphabet = list(string.ascii_lowercase)
        self.letters_left = self.alphabet
        self.is_word_guessed = False
        self.has_lost_game = False
        self.word_to_guess = None
        self.blanks = None

    def initialise(self, word_to_guess):
        self.word_to_guess = word_to_guess.lower()
        self.blanks = ["_" for i in range(len(self.word_to_guess))]

    def print_update(self):
        if not self.has_lost_game:
            print(self.pictures[len(self.incorrect_letters)])
        else:
            print(self.pictures[-1])
        print(" ".join(self.blanks))
        if len(self.incorrect_letters) > 0:
            print("Incorrect guesses:", " ".join([i.upper() for i in self.incorrect_letters]))

    def one_go(self, letter):
        letter = letter.lower()
        if letter in self.alphabet:
            if letter not in self.guessed_letters:
                self.guessed_letters.append(letter)
                if letter in self.word_to_guess and not self.has_lost_game:
                    for i in [i for i, j in enumerate(self.word_to_guess) if j == letter]:
                        self.blanks[i] = letter.upper()
                    if "_" in self.blanks:
                        if self.print_outputs:
                            print("\n\n\nWell done, \'{}\' is correct!".format(letter.upper()))
                            self.print_update()
                    else:
                        self.is_word_guessed = True
                        if self.print_outputs:
                            print("\n\n\nCongratulations, you win!\nThe word was \'{}\'.".format(self.word_to_guess.upper()))
                            self.print_update()
                elif letter not in self.word_to_guess and not self.has_lost_game:
                    self.incorrect_letters.append(letter)
                    if len(self.incorrect_letters) < len(self.pictures)-1:
                        if self.print_outputs:
                            print("\n\n\nUnlucky, \'{}\' is incorrect...".format(letter.upper()))
                            self.print_update()
                    else:
                        self.has_lost_game = True
                        if self.print_outputs:
                            print("\n\n\nUnlucky, \'{}\' is incorrect... and you lose.\nThe word was \'{}\'.".format(letter.upper(), self.word_to_guess.upper()))
                            self.print_update()
                else:
                    if self.print_outputs:
                        print("\n\n\nYou already lost...")


            else:
                if self.print_outputs:
                    print("{} has already been tried. Please try another letter.".format(letter))
        else:
            if self.print_outputs:
                print("{} is not a letter. Please try again.".format(letter))

    def iterate(self, strategy="random"):
        self.letters_left = self.alphabet
        while not self.is_word_guessed and not self.has_lost_game:
            if strategy == "random":
                letter = self.letters_left[randrange(len(self.letters_left))]
                self.one_go(letter)
                if letter in self.letters_left:
                    self.letters_left.remove(letter)

    def play_real_time(self):
        word_to_guess = None
        input_new_word_to_guess = True
        while input_new_word_to_guess:
            word_to_guess = input("Please choose a word: ")
            if word_to_guess in dictionary:
                input_new_word_to_guess = False
            else:
                while True:
                    warning_input = input("\nAre you sure? \'{}\' doesn't look like a real word... [Y/n] ".format(word_to_guess))
                    if warning_input == "" or "y" in warning_input or "Y" in warning_input:
                        input_new_word_to_guess = False
                        break
                    elif "n" in warning_input or "N" in warning_input:
                        break
                    else:
                        print("I didn't understand that... Please type either \'Y\' or \'Y\'.")
        self.initialise(word_to_guess)
        print("\n"*100)
        print(self.pictures[0])
        print(" ".join(self.blanks))
        while not self.has_lost_game and not self.is_word_guessed:
            game.one_go(input("\nGuess a letter: "))


if __name__ == "__main__":
    print("Loading...", end=" ", flush=True)
    import_csv = pd.read_csv("dictionary.csv", usecols=[0], header=None, names=["Words"])
    dictionary = np.array(import_csv[~import_csv.Words.str.contains(r'[^a-z]', na=False)]).ravel()
    print("Done.\n")
    pictures11 = ['\n\n\n\n\n\n\n         ', '\n\n       \n       \n       \n       \n       \n=========', '\n       \n      |\n      |\n      |\n      |\n      |\n=========', '\n  +---+\n      |\n      |\n      |\n      |\n      |\n=========', '\n  +---+\n     \\|\n      |\n      |\n      |\n      |\n=========', '\n  +---+\n  |  \\|\n      |\n      |\n      |\n      |\n=========', '\n  +---+\n  |  \\|\n  O   |\n      |\n      |\n      |\n=========', '\n  +---+\n  |  \\|\n  O   |\n  |   |\n      |\n      |\n=========', '\n  +---+\n  |  \\|\n  O   |\n /|   |\n      |\n      |\n=========', '\n  +---+\n  |  \\|\n  O   |\n /|\\  |\n      |\n      |\n=========', '\n  +---+\n  |  \\|\n  O   |\n /|\\  |\n /    |\n      |\n=========', '\n  +---+\n  |  \\|\n  O   |\n /|\\  |\n / \\  |\n      |\n=========']
    pictures7 = pictures11[5:]

    game = Hangman(dictionary)
    game.play_real_time()



