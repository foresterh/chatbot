import nltk
import random
import os
from nltk import pos_tag
from nltk.tokenize import wordpunct_tokenize

from trainbot import Trainbot
import input_filters
import output_filters


class Chatbot(Trainbot):

    def __init__(self, training_file=u"tell_tale_heart.txt"):
        super(Chatbot, self).__init__(training_file=u"tell_tale_heart.txt")
        self.training_file = training_file
        # self.funct_dict = {"filter_content": input_filters.filter_content,
        #                   "filter_length_words": input_filters.filter_length_words,
        #                   "filter_content_priority": input_filters.filter_content_priority}

    def i_filter_random(self, words, lexicon=None):
        u"""Return randomly selected, non-punctuation word from words."""
        count = 0
        while count < len(words):
            seed = random.choice(words)
            if (seed in self.bi_lexicon) and (seed not in self.stop_puncts):
                return seed
            count += 1
        return u"What a funny thing to say!"

    def o_filter_random(self, sentences):
        u"""Return randomly selected sentence from sentecnces"""
        return random.choice(sentences)

    def _create_chains(self, pair, size=10):
        u"""Return list of markov generated strings spawned from the seed."""
        candidates = []
        w_1 = pair[0]
        w_2 = pair[1]
        while len(candidates) < size:
            word_1, word_2 = w_1, w_2
            candidate = [word_1, word_2]
            pair = u"{} {}".format(word_1, word_2)
            done = False
            while not done:
                try:
                    next_word = random.choice(self.tri_lexicon[pair])
                    candidate.append(next_word)
                    word_1, word_2 = word_2, next_word
                    pair = u"{} {}".format(word_1, word_2)
                except KeyError:
                    candidates.append(" ".join(candidate))
                    done = True
                if next_word in self.stop_puncts:
                    candidates.append(" ".join(candidate))
                    done = True
        return candidates

    def _pair_seed(self, seed):
        word_1 = seed
        word_2 = None
        while word_2 is None:
            try:
                next_ = random.choice(self.bi_lexicon[seed])
                if next_ not in self.stop_puncts:
                    word_2 = next_
                    pair = [word_1, word_2]
            except KeyError:
                continue
        return pair

    def _chain_filters(self, strings, filters):
        u"""Return a list of strings that satisfiy the requirements of all filters.

        Expects: A list of filter functions.
        Returns: A list of strings.
        """
        return self._filter_recursive(strings, filters)

    def _filter_recursive(self, strings, filters):
        u"""Return list of strings or call the next filter function."""
        if filters == []:
            return strings
        else:
            return self._filter_recursive(filters[0](strings), filters[1:])

    # def apply_i_filter(self, filter_, seeds):
    #     lexicon = self.bi_lexicon
    #     if filter_ == "filter_content":
    #         return input_filters.filter_content(seeds)
    #     elif filter_ == "small_talk":
    #         return input_filters.filter_small_talk(seeds, lexicon)
    #     elif filter_ == "length":
    #         return input_filters.filter_length_words(seeds)
    #     elif filter_ == "content_priority":
    #         return input_filters.filter_content_priority(seeds)
    #     else:
    #         return seeds

    def apply_o_filter(self, filter_, chains):
        if filter_ == u"filter_length":
            return output_filters.filter_length(chains)
        if filter_ == u"filter_pos":
            return output_filters.filter_pos(chains)
        else:
            return chains

    def compose_response(
            self,
            input_sent,
            input_key=None,
            output_filter=None,
            ):
        u"""Return a response sentence based on the input."""
        # Tokenize input
        seeds = wordpunct_tokenize(input_sent)
        # Select seed based on input filter
        if input_key:
            print u"Input filter: {}".format(input_key)
            seeds = input_filters.input_funcs[input_key](seeds)
            if isinstance(seeds, basestring):
                return seeds
        # Randomly pick a seed from the returned possibilities.
        print seeds
        seed = self.i_filter_random(seeds)
        if seed == u"What a funny thing to say!":
            return seed
        # Create chains
        pair = self._pair_seed(seed)
        chains = self._create_chains(pair)
        # Return output of filter
        if output_filter != "default":
            print u"Output filter: {}".format(output_filter)
            filtered = output_filters.funct_dict[output_filter](chains)
        else:
            output = chains
        if len(filtered) > 0:
            output = self.o_filter_random(filtered)
        else:
            output = u"I'm not sure what to say about that."

        print "Here comes my output!"
        return output

if __name__ == u'__main__':
    bot = Chatbot(training_file="Doctorow.txt")
    bot.fill_lexicon()
    print u"Filled the lexicon!"
    print bot.compose_response(
        u"My beautiful carriage is red and blue and it hums while I drive it!",
        u"Content Filter",
        u"filter_NN_VV"
        )
