import numpy as np
import nltk
import logging
from nltk.stem.porter import PorterStemmer
from src.core.settings.logging import LOGGING_NAME_CORE


log = logging.getLogger(LOGGING_NAME_CORE)

try:
    nltk.data.find('tokenizers/punkt')
    log.debug("tokenizers/punkt init")
except LookupError:
    nltk.download('punkt')


class NLTKUtils():
    stemmer = PorterStemmer()

    def tokenize(self, sentence):
        """
        split sentence into array of words/tokens
        a token can be a word or punctuation character, or number
        """
        return nltk.word_tokenize(sentence)

    def stem(self, word):
        """
        stemming = find the root form of the word
        examples:
        words = ["organize", "organizes", "organizing"]
        words = [stem(w) for w in words]
        -> ["organ", "organ", "organ"]
        """
        return self.stemmer.stem(word.lower())

    def bag_of_words(self, tokenized_sentence, words):
        """
        return bag of words array:
        1 for each known word that exists in the sentence, 0 otherwise
        example:
        sentence = ["hello", "how", "are", "you"]
        words = ["hi", "hello", "I", "you", "bye", "thank", "cool"]
        bog   = [  0 ,    1 ,    0 ,   1 ,    0 ,    0 ,      0]
        """
        # stem each word
        sentence_words = [self.stem(word) for word in tokenized_sentence]
        # initialize bag with 0 for each word
        bag = np.zeros(len(words), dtype=np.float32)
        for idx, w in enumerate(words):
            if w in sentence_words:
                bag[idx] = 1

        return bag
