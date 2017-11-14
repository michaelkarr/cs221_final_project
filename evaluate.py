import poetrytools
import sys

def evaluate_poem(poem):
    meter = poetrytools.guess_metre(poem)
    rhyme_type = poetrytools.guess_rhyme_type(poem)
    stanza = poetrytools.guess_stanza_type(poem)
    return stanza[1], meter[3], rhyme_type[1]
#pass in generated poem as string

poem_str = open(sys.argv[1], 'r').read()
poem = poetrytools.tokenize(poem_str)
stanza, meter, rhyme_type = evaluate_poem(poem)
isSeussianStanza = isSeussianMeter = isSeussianRhyme = False
if stanza == 'quatrains':
    isSeussianStanza = True
if meter == 'iambic trimeter' or meter == 'iambic tetrameter' or meter == 'anapestic tetrameter':
    isSeussianMeter = True
if rhyme_type == 'seuss' or rhyme_type == 'couplets' or rhyme_type == 'alternate rhyme':
    isSeussianRhyme = True
print(isSeussianStanza, isSeussianMeter, isSeussianRhyme)
