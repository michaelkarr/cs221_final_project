import poetrytools
import sys
import random

weights = [0.7, -0.9999999999999999, 1.2, 0.30000000000000004]
sight_set = set(line.strip() for line in open('sightwords.txt'))

def evaluate_poem(poem):
    meter = poetrytools.guess_metre(poem)
    rhyme_type = poetrytools.guess_rhyme_type(poem)
    stanza = poetrytools.guess_stanza_type(poem)
    isSeussianStanza = isSeussianMeter = isSeussianRhyme = 0
    if stanza[1] == 'quatrains' or stanza[1] == 'sonnet':
        isSeussianStanza = 1
    if meter[3] == 'iambic trimeter' or meter[3] == 'iambic tetrameter' or meter[3] == 'anapestic tetrameter' or meter[3] == 'trochaic pentameter':
        isSeussianMeter = 1
    if rhyme_type[1] == 'seuss' or rhyme_type[1] == 'couplets' or rhyme_type[1]== 'alternate rhyme':
        isSeussianRhyme = 1
    return isSeussianStanza, isSeussianMeter, isSeussianRhyme

def count_words(poem):
    sight_count = 0.0
    for word in poem:
        if word.lower() in sight_set:
            sight_count += 1
    sight_prop = sight_count / len(poem)
    return 1 if sight_prop >= 0.6 and sight_prop <= 0.9 else 0

def predict(poem_str):
    poem = poetrytools.tokenize(poem_str)
    stanza, meter, rhyme_type = evaluate_poem(poem)

    #finds proportion of words that are sight words
    poem_str = poem_str.replace("\n", " ")
    poem_list = poem_str.split(" ")
    seussian_sight_prop = count_words(filter(str.isalnum, poem_list))

    features = [stanza, meter, rhyme_type, seussian_sight_prop] #for generated text
    classifier(features)

def classifier(x):
        dp = sum(i[0] * i[1] for i in zip(weights, x))
        if dp > 0: return {'seussian': '+'}
        else: return {'seussian': '-'}
