import poetrytools
import sys

#returns 0 or 1 if seussian stanza, meter, and rhyme
def evaluate_poem(poem):
    meter = poetrytools.guess_metre(poem)
    rhyme_type = poetrytools.guess_rhyme_type(poem)
    stanza = poetrytools.guess_stanza_type(poem)
    isSeussianStanza = isSeussianMeter = isSeussianRhyme = 0
    if stanza[1] == 'quatrains':
        isSeussianStanza = 1
    if meter[3] == 'iambic trimeter' or meter[3] == 'iambic tetrameter' or meter[3] == 'anapestic tetrameter':
        isSeussianMeter = 1
    if rhyme_type[1] == 'seuss' or rhyme_type[1] == 'couplets' or rhyme_type[1]== 'alternate rhyme':
        isSeussianRhyme = 1
    return isSeussianStanza, isSeussianMeter, isSeussianRhyme

#proportion of words from sight words list- 1st, 2nd, pre-k
def count_words(poem):
    sight_count = 0.0
    for word in poem:
        if word.lower() in sight_set:
            sight_count += 1
    sight_prop = sight_count / len(poem)
    return 1 if sight_prop >= 0.6 and sight_prop <= 0.9 else 0

#finds stanza, meter, rhyme_type, checks if in seussian patterns
poem_str = open(sys.argv[1], 'r').read()
poem = poetrytools.tokenize(poem_str)
stanza, meter, rhyme_type = evaluate_poem(poem)

#finds proportion of words that are sight words
sight_set = set(line.strip() for line in open('sightwords.txt'))
poem_str = poem_str.replace("\n", " ")
poem_list = poem_str.split(" ")
seussian_sight_prop = count_words(filter(str.isalnum, poem_list))

#weights_vector starts as all 1
features = [stanza, meter, rhyme_type, seussian_sight_prop]
print(features)
