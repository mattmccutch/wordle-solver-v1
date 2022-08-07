__author__ = "<your name>"
__organization__ = "COSC343/AIML402, University of Otago"
__email__ = "<your e-mail>"

from os import remove
import random
from stat import FILE_ATTRIBUTE_SPARSE_FILE


class WordleAgent():
    """
        A class that encapsulates the code dictating the
        behaviour of the Wordle playing agent

        ...

        Attributes
        ----------
        dictionary : list
            a list of valid words for the game
        letter : list
            a list containing valid characters in the game
        word_length : int
            the number of letters per guess word
        num_guesses : int
            the max. number of guesses per game
        mode: str
            indicates whether the game is played in 'easy' or 'hard' mode

        Methods
        -------
        AgentFunction(percepts)
            Returns the next word guess given state of the game in percepts
        """

    def __init__(self, dictionary, letters, word_length, num_guesses, mode):
        """
        :param dictionary: a list of valid words for the game
        :param letters: a list containing valid characters in the game
        :param word_length: the number of letters per guess word
        :param num_guesses: the max. number of guesses per game
        :param mode: indicates whether the game is played in 'easy' or 'hard' mode
        """

        self.dictionary = dictionary
        self.letters = letters
        self.word_length = word_length
        self.num_guesses = num_guesses
        self.mode = mode
        self.green_guesses = []
        self.orange_guesses = []
        self.grey_guesses = []
        self.previous_guesses = []
        self.guess_counter = 0
        self.letter_indexes = []
        self.letter_states = []

    def AgentFunction(self, percepts):
        """Returns the next word guess given state of the game in percepts

        :param percepts: a tuple of three items: guess_counter, letter_indexes, and letter_states;
                 guess_counter is an integer indicating which guess this is, starting with 0 for initial guess;
                 letter_indexes is a list of indexes of letters from self.letters corresponding to
                             the previous guess, a list of -1's on guess 0;
                 letter_states is a list of the same length as letter_indexes, providing feedback about the
                             previous guess (conveyed through letter indexes) with values of 0 (the corresponding
                             letter was not found in the solution), -1 (the correspond letter is found in the
                             solution, but not in that spot), 1 (the corresponding letter is found in the solution
                             in that spot).
        :return: string - a word from self.dictionary that is the next guess
        """

        # This is how you extract three different parts of percepts.
        self.guess_counter, self.letter_indexes, self.letter_states = percepts

        if self.guess_counter == 0:
            self.green_guesses = []
            self.orange_guesses = []
            self.grey_guesses = []
            self.previous_guesses = []
            return self.dictionary[random.randrange(len(self.dictionary))]
        else:
            potential_words = self.get_potential_words()
            best_words = self.best_words(potential_words)
            if len(best_words) > 0:
                return best_words[random.randrange(len(best_words))]
            elif len(potential_words) > 0:
                return potential_words[random.randrange(len(potential_words))]
            else:
                return self.dictionary[random.randrange(len(self.dictionary))]

    def fill_states(self):
        for i in range(0, len(self.letter_indexes)):
            guessed_char = self.letters[self.letter_indexes[i]]
            if self.letter_states[i] == 1:
                if [guessed_char, i] not in self.green_guesses:
                    self.green_guesses.append([guessed_char, i])
            if self.letter_states[i] == 0:
                if [guessed_char, i] not in self.grey_guesses:
                    self.grey_guesses.append([guessed_char, i])
            if self.letter_states[i] == -1:
                if [guessed_char, i] not in self.orange_guesses:
                    self.orange_guesses.append([guessed_char, i])

    def get_potential_words(self):
        self.fill_states()
        potential_words = []
        for word in self.dictionary:
            add_word = True
            for g_guess in self.green_guesses:
                green_char = g_guess[0]
                green_index = g_guess[1]
                if word[green_index] != green_char:
                    add_word = False
            for o_guess in self.orange_guesses:
                orange_char = o_guess[0]
                orange_index = o_guess[1]
                if word[orange_index] == orange_char:
                    add_word = False
                if orange_char not in word:
                    add_word = False
            for gr_guess in self.grey_guesses:
                grey_char = gr_guess[0]
                grey_index = gr_guess[1]
                if word[grey_index] == grey_char:
                    add_word = False
            if add_word == True:
                potential_words.append(word)
        return potential_words

    def fill_frequencies(self, potential_words):
        freqs = {}
        word_chars = []
        for word in potential_words:
            for i in range(len(word)):
                if word[i] not in word_chars:
                    word_chars.append(word[i])
        for letter in word_chars:
            char_freqs = [0] * len(self.letter_indexes)
            for word in potential_words:
                for i in range(0, len(self.letter_indexes)):
                    if word[i] == letter:
                        char_freqs[i] += 1
                freqs.update({letter: char_freqs})
        return freqs

    def best_words(self, potential_words):
        freqs = self.fill_frequencies(potential_words)
        max_chars = [0] * len(self.letter_indexes)
        max_chars_size = [0] * len(self.letter_indexes)
        for freq in freqs:
            for i in range(len(freqs[freq])):
                if freqs[freq][i] > max_chars_size[i]:
                    max_chars_size[i] = freqs[freq][i]
                    max_chars[i] = freq
        word_scores = []
        for word in potential_words:
            word_score = 0
            for i in range(len(max_chars)):
                if max_chars[i] == word[i]:
                    word_score += max_chars_size[i]
            word_scores.append([word, word_score])

        threshold = 0
        green_is = []
        for guess in self.green_guesses:
            index = guess[1]
            green_is.append(index)
        for i in range(len(max_chars_size)):
            if i not in green_is:
                threshold += max_chars_size[i]
        best_words = []
        for score in word_scores:
            if score[1] >= threshold:
                best_words.append(score[0])

        return best_words
