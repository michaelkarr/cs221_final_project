import poetrytools
import sys

def evaluate_poem(poem):
    # meter = poetrytools.guess_metre(poem)
    # rhyme_type = poetrytools.guess_rhyme_type(poem)
    # stanza = poetrytools.guess_stanza_type(poem)
    # return stanza, meter, rhyme_type
    poetrytools.guess_form(poem, verbose=True)
#pass in generated poem as string

poem_str = open(sys.argv[1], 'r').read()
poem = poetrytools.tokenize(poem_str)
evaluate_poem(poem)
# stanza, meter, rhyme_type = evaluate_poem(poem)
# print(stanza, meter, rhyme_type)
