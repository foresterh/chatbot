import chatbot_brain

stock = u"What a funny thing to say!"


def test_initialize_bot():
    bot = chatbot_brain.Chatbot()
    assert len(bot.tri_lexicon) == 0
    assert len(bot.bi_lexicon) == 0


def test_fill_lexicon():
    bot = chatbot_brain.Chatbot()
    bot.fill_lexicon()
    assert len(bot.tri_lexicon) > 0
    assert len(bot.bi_lexicon) > 0


def test_compose_response():
    bot = chatbot_brain.Chatbot()
    output = bot.compose_response(input_sent="How are you doing?")
    assert "," not in output[0]
    for sentence in output:
        assert "." not in sentence[:-1]


def test_i_filter_random_empty_words():
    u"""Assert an empty string is not found in the default lexicon."""
    bot = chatbot_brain.Chatbot()
    words = [""]
    assert bot.i_filter_random(words) == stock


def test_i_filter_random_words_not_in_lexicon():
    u"""Assert that if all words are not in lexicon the default is returned."""
    bot = chatbot_brain.Chatbot()
    words = ["moose", "bear", "eagle"]
    lexicon = {"car": "mercedes", "boat": "sail", "train": "track"}
    assert bot.i_filter_random(words, lexicon) == stock

# untested methods:
# i_filter_random
# o_filter_random
# _create_chains
# _pair_seed
# _chain_filters
# _filter_recursive
