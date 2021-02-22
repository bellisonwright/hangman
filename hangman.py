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
import os


class Hangman():
    '''
    Game of hangman.
    '''
    outputs_dict = {
        "correct": "Well done, \'{letter}\' is correct!",
        "won": "Congratulations, you win!\nThe word was \'{word}\'.",
        "incorrect": "Unlucky, \'{letter}\' is incorrect...",
        "lost": "Unlucky, \'{letter}\' is incorrect... and you just lost.\nThe word was \'{word}\', and you got {correct_letters} out of {total_letters} letters ({percent_score}%).",
        "already lost": "You already lost...",
        "already tried": "\'{letter}\' has already been guessed. Please choose another letter.",
        "not a letter": "\'{letter}\' is not a letter. Please try again."
    }
    length_of_picture = 12

    def __init__(self, dictionary_array, print_outputs=True, mode="easy", end_screen_spacing=1):
        '''
        :param dictionary_array: np array, wordlist scraped from Oxford Dictionary of English
        :param print_outputs: True/False, should outputs of each game be printed
        :param mode: "easy" or "hard", 11 attempts or 7 attempts
        :param end_screen_spacing: int,
        '''
        self.dictionary = dictionary_array
        self.print_outputs = print_outputs

        self.start_gallows_at = 0
        if mode == "hard":
            self.start_gallows_at = 5
        self.pictures = []
        with open("gallows.txt", "r") as f:
            current_element = ""
            for num, line in enumerate(f):
                if num % self.length_of_picture != self.length_of_picture-1:
                    current_element += line
                else:
                    self.pictures.append(current_element)
                    current_element = ""
        self.pictures = self.pictures[self.start_gallows_at:]

        self.incorrect_letters = []
        self.guessed_letters = []
        self.alphabet = list(string.ascii_lowercase)
        self.letters_left = self.alphabet
        self.is_word_guessed = False
        self.has_lost_game = False
        self.word_to_guess = None
        self.blanks = None
        self.end_screen = []

    def initialise(self, word_to_guess):
        self.word_to_guess = word_to_guess.lower()
        self.blanks = ["_" for i in range(len(self.word_to_guess))]

    def create_end_screen(self, result, spacing=0):
        file_name = "gallows.txt"
        strings_to_add = []
        with open("you-{}.txt".format(result), "r") as f:
            for line in f:
                strings_to_add.append(line)
        with open(file_name, 'r') as f:
            current_element = ""
            for num, line in enumerate(f.readlines()[(len(self.incorrect_letters)+self.start_gallows_at)*self.length_of_picture:(len(self.incorrect_letters)+self.start_gallows_at+1)*self.length_of_picture]):
                if num % len(strings_to_add) != len(strings_to_add)-1:
                    current_element += line[:-1] + spacing*" " + strings_to_add[num % len(strings_to_add)]
                else:
                    current_element += line[:-1] + spacing*" " + strings_to_add[num % len(strings_to_add)]
                    self.end_screen.append(current_element)
                    current_element = ""

    def print_update(self, letter, message, valid_guess=True):
        if self.print_outputs:
            print("\n" + "".join(["━" for i in range(43)]) + "\n")
            if valid_guess:
                os.system('cls||clear')
            print(self.outputs_dict[message].format(letter=letter.upper(), word=self.word_to_guess.upper(), correct_letters=len(self.word_to_guess)-self.blanks.count("_"), total_letters=len(self.word_to_guess), percent_score=round(100*(len(self.word_to_guess)-self.blanks.count("_"))/len(self.word_to_guess))))
            if valid_guess:
                if not self.has_lost_game and not self.is_word_guessed:
                    print("\n{}".format(self.pictures[len(self.incorrect_letters)]))
                    print("\nWord to guess: "+" ".join(self.blanks))
                elif self.is_word_guessed:
                    self.create_end_screen("win", 2)
                    print(self.end_screen[0])
                    print("Word to guess: "+" ".join(self.blanks))
                elif self.has_lost_game:
                    self.create_end_screen("lose", 2)
                    print(self.end_screen[0])
                    print("Word to guess: "+" ".join(self.word_to_guess.upper()))

                if len(self.incorrect_letters) > 0:
                    print("Incorrect guesses:", " ".join([i.upper() for i in self.incorrect_letters]))
                else:
                    print("Incorrect guesses: None")

    def one_go(self, letter):
        letter = letter.lower()
        if letter in self.alphabet:
            if letter not in self.guessed_letters:
                self.guessed_letters.append(letter)
                if letter in self.word_to_guess and not self.has_lost_game:
                    for i in [i for i, j in enumerate(self.word_to_guess) if j == letter]:
                        self.blanks[i] = letter.upper()
                    if "_" in self.blanks:
                        self.print_update(letter, "correct")
                    else:
                        self.is_word_guessed = True
                        self.print_update(letter, "won")
                elif letter not in self.word_to_guess and not self.has_lost_game:
                    self.incorrect_letters.append(letter)
                    if len(self.incorrect_letters) < len(self.pictures)-1:
                        self.print_update(letter, "incorrect")
                    else:
                        self.has_lost_game = True
                        self.print_update(letter, "lost")
                else:
                    self.print_update(letter, "already lost", False)
            else:
                self.print_update(letter, "already tried", False)
        else:
            self.print_update(letter, "not a letter", False)

    def iterate(self, strategy="random"):
        self.letters_left = self.alphabet
        while not self.is_word_guessed and not self.has_lost_game:
            if strategy == "random":
                letter = self.letters_left[randrange(len(self.letters_left))]
                self.one_go(letter)
                if letter in self.letters_left:
                    self.letters_left.remove(letter)

    def play_real_time(self):
        while True:
            word_to_guess = input("Please choose a word: ")
            if word_to_guess in dictionary:
                break
            else:
                os.system('cls||clear')
                warning_input = input("\nAre you sure? \'{}\' doesn't look like a real word... [Y/n] ".format(word_to_guess))
                if "n" not in warning_input.lower():
                    break
        self.initialise(word_to_guess)
        print("\n" * 100)
        os.system('cls||clear')
        print("\n\n{}".format(self.pictures[0]))
        print("\nWord to guess: "+" ".join(self.blanks))
        print("Incorrect guesses: None")
        while not self.has_lost_game and not self.is_word_guessed:
            game.one_go(input("\nGuess a letter: "))

    def play_word(self, word_to_guess):
        self.initialise(word_to_guess)
        os.system('cls||clear')
        print("\n\n{}".format(self.pictures[0]))
        print("\nWord to guess: "+" ".join(self.blanks))
        print("Incorrect guesses: None")
        while not self.has_lost_game and not self.is_word_guessed:
            game.one_go(input("\nGuess a letter: "))


if __name__ == "__main__":
    print("Loading...", end=" ", flush=True)
    import_csv = pd.read_csv("dictionary.csv", usecols=[0], header=None, names=["Words"])
    dictionary = np.array(import_csv[~import_csv.Words.str.contains(r'[^a-z]', na=False)]).ravel()
    print("Done.\n")

    mode = "easy"
    if "h" in input("Easy or hard mode? [E/h] ").lower():
        mode = "hard"
    game = Hangman(dictionary, mode=mode)
    if "s" not in input("Single player or multiplayer? [s/M] ").lower():
        while True:
            game.play_real_time()
            if "y" not in input("\nPlay again? [y/N] ").lower():
                break
    else:
        while True:
            word_index = randrange(len(dictionary))
            game.play_word(dictionary[word_index])
            if "y" not in input("\nPlay again? [y/N] ").lower():
                break


