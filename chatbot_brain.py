import nltk
import random
import os
from nltk import pos_tag
from nltk.tokenize import wordpunct_tokenize
import pdb


class Chatbot(object):

    def __init__(self, training_file="tell_tale_heart.txt"):
        self.training_file = training_file
        self.tri_lexicon = {}
        self.bi_lexicon = {}
        self.stop_puncts = ['.', '!', '?']
        self.puncts = [',', ';', ':', '"', "'", '-', '--', ",?"]

    def parse_training_input(self, text):
        while True:
            our_text = text.read(2048)
            if not our_text:
                break
            yield wordpunct_tokenize(our_text)

    def remove_non_final_punctuation(self, our_list):
        for i in our_list[:]:
            if i in self.puncts:
                our_list.remove(i)
        return our_list

    def tag_input(self, our_string):
        our_string = wordpunct_tokenize(our_string)
        return pos_tag(our_string)

    def fill_lexicon(self):
        f = open(self.training_file)
        for words in self.parse_training_input(f):
            words = self.remove_non_final_punctuation(words)
            for i in range(2, (len(words) - 2)):
                word_pair = "{} {}".format(words[i - 2], words[i - 1])
                first_word = str(words[i - 2])
                second_word = str(words[i - 1])
                next_word = words[i]
                if first_word not in self.bi_lexicon:
                    self.bi_lexicon[first_word] = [second_word]
                else:
                    self.bi_lexicon[first_word].append(second_word)
                if word_pair not in self.tri_lexicon:
                        self.tri_lexicon[word_pair] = [next_word]
                else:
                    self.tri_lexicon[word_pair].append(next_word)

    def i_filter_random(self, words):
        while True:
            seed = random.choice(words)
            if seed not in self.bi_lexicon:
                continue
            elif (seed in self.bi_lexicon) and (seed not in self.stop_puncts):
                return seed
            else:
                return "was"

    def o_filter_random(self, sentences):
        return str(random.choice(sentences))

    def generate_response(self, input_sent):
        #words = self.tag_input(input_sent)
        words = wordpunct_tokenize(input_sent)
        first_seed = self.i_filter_random(words)
        print "Given the seed: {}".format(first_seed)
        response_candidates = []
        while len(response_candidates) < 10:
            bad_sentence = False
            seed = first_seed
            candidate_sentence = [seed]
            while True:
                word_2 = None
                next_word = None
                while (not word_2) and (not next_word):
                    try:
                        word_2 = random.choice(self.bi_lexicon[seed])
                        bigram = "{} {}".format(seed, word_2)
                        next_word = random.choice(self.tri_lexicon[bigram])
                    except KeyError:
                        bad_sentence = True
                        break
                if bad_sentence:
                    break
                if word_2 not in self.stop_puncts:
                    candidate_sentence.append(word_2)
                bigram = "{} {}".format(word_2, next_word)
                seed = word_2
                if (next_word in self.stop_puncts) or (next_word not in self.bi_lexicon):
                    response_candidates.append(" ".join(candidate_sentence))
                    break
        return self.o_filter_random(response_candidates)

# def full_package():
#     gener

if __name__ == '__main__':
    bot = Chatbot()
    bot.fill_lexicon()
    print "Filled the lexicon!"
    print bot.generate_response("How are you doing?")
