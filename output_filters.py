import nltk
from nltk import pos_tag
from nltk.tokenize import wordpunct_tokenize
from collections import OrderedDict

funct_dict = OrderedDict({})

grammar1 = nltk.parse_cfg("""
    Sent  -> NP VP | NP VP END
    NP -> Det Nom | PropN | Det NP | N | PR
    Nom -> Adj Nom | N
    VP -> V Adj | V NP | V S | V NP PP | V Prep NP | V
    PP -> Prep NP

    PropN -> 'NNP' | 'NNPS'
    Det -> 'DT'
    N -> 'NN' | 'NNS'
    Adj  -> 'JJ' | 'JJR' |  'JJS'
    V ->  'VB'  | 'VBD' | 'VBG' | 'VBN' | 'VBP' | 'VBZ'
    Prep -> 'TO' | 'IN'
    CC -> 'CC'
    PR -> 'PRP' | 'PRP$'
    RB -> 'RB' | 'RBR' | 'RBS'
    END -> '.' | '?' | '!'
    """)


def add_func_to_dict(name=None):
    def wrapper(func):
        function_name = name
        if function_name is None:
            function_name = func.__name__
        funct_dict[function_name] = func
        return func
    return wrapper


@add_func_to_dict("No Filter Selected")
def no_o_filter_selected(sentences):
    return sentences


@add_func_to_dict("Length Filter")
def filter_length(sentences, wordcount=8):
    u"""Return every sentence that has a length <= wordcount.

    Takes in a list of sentences and returns a reduced list,
    that contains only sentences with less than or equal to <wordcount>
    words.
    """
    output_sentences = []
    for sentence in sentences[:]:
        sentence = sentence.split()
        if len(sentence) <= wordcount:
            output_sentences.append(" ".join(sentence))
    return output_sentences


@add_func_to_dict("Part of Speech Filter")
def filter_pos(sentences):
    """Takes in a list of sentences and returns a reduced list,

    that contains only sentences that contain the necessarry pos."""
    content_pos = ['VB', 'NN', 'JJ']
    output_sentences = []
    for sentence in sentences:
        words = wordpunct_tokenize(sentence)
        tagged = pos_tag(words)
        for word, pos in tagged:
            if pos[:2] in content_pos:
                output_sentences.append(sentence)
                break
    return output_sentences


@add_func_to_dict("Noun-Verb Filter")
def filter_NN_VV(sentences):
    """Takes in a list of sentences and returns a reduced list of
    sentences that have at least one noun followed somewhere by at least
    one verb.
    """
    output_sentences = []
    for sentence in sentences:
        words = wordpunct_tokenize(sentence)
        tagged = pos_tag(words)
        has_noun = False
        for word, tag in tagged:
            if tag[:2] == "NN":
                has_noun = True
            if has_noun and tag[:2] == "VB":
                output_sentences.append(sentence)
                break
    return output_sentences


@add_func_to_dict("Syntactic Filter")
def syntactic_filter(sentences):
    """Filters responses through part of speech tagging and
    recursive structure lookup."""
    output_sentences = []
    print "Before syntax filter there were " + str(len(sentences)) + " sentences."
    for sentence in sentences:
        print sentence + "\n"
        tokens = nltk.tokenize.wordpunct_tokenize(sentence)
        posTagged = nltk.pos_tag(tokens)

        justTags = []
        for word, tag in posTagged:
            justTags.append(tag)

        rd_parser = nltk.RecursiveDescentParser(grammar1)
        try:
            if len(rd_parser.nbest_parse(justTags)) > 0:
                output_sentences.append(sentence)
        except ValueError:
            pass
    print "After the syntax filter there were " + str(len(output_sentences)) + " sentences."
    return output_sentences
