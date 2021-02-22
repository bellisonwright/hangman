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

    def __init__(self, dictionary_array, print_outputs=True, difficulty="easy", end_screen_spacing=1):
        '''
        :param dictionary_array: np array, wordlist scraped from Oxford Dictionary of English
        :param print_outputs: True/False, should outputs of each game be printed
        :param difficulty: "easy" or "hard", 11 attempts or 7 attempts
        :param end_screen_spacing: int,
        '''
        self.dictionary = dictionary_array
        self.print_outputs = print_outputs
        self.difficulty = difficulty

        self.start_gallows_at = 0
        if self.difficulty == "hard":
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
        if self.print_outputs:
            os.system('cls||clear')
            print("\n\n{}".format(self.pictures[0]))
            print("\nWord to guess: "+" ".join(self.blanks))
            print("Incorrect guesses: None")
        while not self.has_lost_game and not self.is_word_guessed:
            game.one_go(input("\nGuess a letter: "))

    def autorun(self, num_runs=10000, word_length=None, strategy="random"):
        lang_freq = ["e", "t", "a", "o", "i", "n", "s", "r", "h", "l", "d", "c", "u", "m", "f", "p", "g", "w", "y", "b", "v", "k", "x", "j", "q", "z"]
        dict_freq = ["e", "a", "r", "i", "o", "t", "n", "s", "l", "c", "u", "d", "p", "m", "h", "g", "b", "f", "y", "w", "k", "v", "x", "z", "j", "q"]
        self.print_outputs = False
        success_counter = 0
        for i in range(num_runs):
            dict_index = randrange(len(dictionary))
            game.__init__(self.dictionary,difficulty=self.difficulty, print_outputs=False)
            game.initialise(str(dictionary[dict_index]))
            while not self.has_lost_game and not self.is_word_guessed:
                if strategy == "random":
                    letter_index = randrange(26)
                    if self.alphabet[letter_index] not in self.guessed_letters:
                        game.one_go(self.alphabet[letter_index])
                elif strategy == "language frequency":
                    letter = lang_freq[len(self.guessed_letters)]
                    game.one_go(letter=letter)
                elif strategy == "dictionary frequency":
                    letter = dict_freq[len(self.guessed_letters)]
                    game.one_go(letter=letter)
            if self.is_word_guessed:
                success_counter += 1
            if i % int(num_runs/20) == int(num_runs/20)-1:
                # print("#{}:\t{},\t{}/{}\tletters guessed correctly ({}%).".format(i+1, self.word_to_guess, len(self.word_to_guess)-self.blanks.count("_"), len(self.word_to_guess), round(100*(len(self.word_to_guess)-self.blanks.count("_"))/len(self.word_to_guess))).expandtabs(20))
                print("#{}:\t{:20} {}{}/{}{}letters guessed correctly ({}%).".format(i+1, self.word_to_guess+",", len(self.word_to_guess)-self.blanks.count("_"), " "*(2-len(str(len(self.word_to_guess)-self.blanks.count("_")))), len(self.word_to_guess), " "*(3-len(str(len(self.word_to_guess)))), round(100*(len(self.word_to_guess)-self.blanks.count("_"))/len(self.word_to_guess))))
        return success_counter, num_runs

if __name__ == "__main__":
    print("\n" * 100)
    os.system('cls||clear')

    difficulty_level = "easy"
    if "h" in input("Easy or hard mode? [E/h] ").lower():
        difficulty_level = "hard"
    mode = input("Pick a mode:\n\n1. Single player\n2. Multiplayer\n3. Autorun (computer vs computer)\n\n[1/2/3]: ").lower()
    print("Loading dictionary...", end=" ", flush=True)
    import_csv = pd.read_csv("dictionary.csv", usecols=[0], header=None, names=["Words"])
    dictionary = np.array(import_csv[~import_csv.Words.str.contains(r'[^a-z]', na=False)]).ravel()
    print("Done.\n")
    if "2" in mode:
        while True:
            game = Hangman(dictionary, difficulty=difficulty_level)
            game.play_real_time()
            if "y" not in input("\nPlay again? [y/N] ").lower():
                break
    elif "1" in mode:
        while True:
            game = Hangman(dictionary, difficulty=difficulty_level)
            word_index = randrange(len(dictionary))
            game.play_word(dictionary[word_index])
            if "y" not in input("\nPlay again? [y/N] ").lower():
                break
    elif "3" in mode:
        game = Hangman(dictionary, difficulty=difficulty_level)
        strat_key = {"1": "random", "2": "language frequency", "3": "dictionary frequency", "4": "all"}
        strat = strat_key[input("Choose a strategy:\n\n1. Random\n2. By language frequency\n3. By dictionary frequency\n4. All\n\n[1/2/3/4]: ")]
        n = input("How many runs? (default is 10000) ")
        if n == "":
            n = 10000
        if strat != "all":
            results = game.autorun(int(n), strategy=strat)
            print("Computer was successful in {} out of {} games ({}%) using the {} strategy.".format(results[0], results[1], round(100*results[0]/results[1], 2), strat))
        else:
            for i in range(3):
                results = game.autorun(int(n), strategy=strat_key[str(i+1)])
                print("Computer was successful in {} out of {} games ({}%) using the {} strategy.\n\n".format(results[0], results[1], round(100*results[0]/results[1], 2), strat))



