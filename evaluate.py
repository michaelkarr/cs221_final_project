import poetrytools
import sys

#returns 0 or 1 if seussian stanza, meter, and rhyme
def evaluate_poem(poem):
    meter = poetrytools.guess_metre(poem)
    rhyme_type = poetrytools.guess_rhyme_type(poem)
    stanza = poetrytools.guess_stanza_type(poem)
    isSeussianStanza = isSeussianMeter = isSeussianRhyme = False
    if stanza[1] == 'quatrains':
        isSeussianStanza = True
    if meter[3] == 'iambic trimeter' or meter[3] == 'iambic tetrameter' or meter[3] == 'anapestic tetrameter':
        isSeussianMeter = True
    if rhyme_type[1] == 'seuss' or rhyme_type[1] == 'couplets' or rhyme_type[1]== 'alternate rhyme':
        isSeussianRhyme = True
    return isSeussianStanza, isSeussianMeter, isSeussianRhyme

#proportion of words from sight words list- 1st, 2nd, pre-k
def count_words(poem):
    sight_count = 0.0
    for word in poem:
        if word.lower() in sight_set:
            sight_count += 1
    return sight_count / len(poem)

#finds stanza, meter, rhyme_type, checks if in seussian patterns
poem_str = open(sys.argv[1], 'r').read()
poem = poetrytools.tokenize(poem_str)
stanza, meter, rhyme_type = evaluate_poem(poem)

#finds proportion of words that are sight words
sight_set = set(line.strip() for line in open('sightwords.txt'))
poem_str = poem_str.replace("\n", " ")
poem_list = poem_str.split(" ")
sight_prop = count_words(filter(str.isalnum, poem_list))