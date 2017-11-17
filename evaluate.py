import poetrytools
import sys
import random

trainExamples = (("non_seuss_training_texts/daddy.txt", -1), ("non_seuss_training_texts/cloud.txt", -1), ("non_seuss_training_texts/troy.txt", -1), ("non_seuss_training_texts/another_sky.txt", -1), ("non_seuss_training_texts/dream.txt", -1), ("non_seuss_training_texts/road_not_taken.txt", -1), ("non_seuss_training_texts/when_sidewalk_ends.txt", -1),
("training_texts/fox_in_socks.txt", 1), ("training_texts/cat_in_the_hat.txt", 1), ("training_texts/green_eggs_and_ham.txt", 1), ("training_texts/hop_on_pop.txt", 1),
("training_texts/oh_the_places_you'll_go.txt", 1), ("training_texts/one_fish_two_fish_red_fish_blue_fish.txt", 1)
)
sight_set = set(line.strip() for line in open('sightwords.txt'))
weights = [random.uniform(0.0,1.0) for _ in xrange(4)]
eta = 0.05
numIters = 400

#returns 0 or 1 if seussian stanza, meter, and rhyme
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

#proportion of words from sight words list- 1st, 2nd, pre-k
def count_words(poem):
    sight_count = 0.0
    for word in poem:
        if word.lower() in sight_set:
            sight_count += 1
    sight_prop = sight_count / len(poem)
    return 1 if sight_prop >= 0.6 and sight_prop <= 0.9 else 0

#finds stanza, meter, rhyme_type, checks if in seussian patterns
def get_features(poem_str):
    poem = poetrytools.tokenize(poem_str)
    stanza, meter, rhyme_type = evaluate_poem(poem)

    #finds proportion of words that are sight words
    poem_str = poem_str.replace("\n", " ")
    poem_list = poem_str.split(" ")
    seussian_sight_prop = count_words(filter(str.isalnum, poem_list))

    features = [stanza, meter, rhyme_type, seussian_sight_prop] #for generated text
    return features

def classifier(x):
        dp = sum(i[0] * i[1] for i in zip(weights, x))
        print(dp)
        if dp > 0: return 1
        else: return -1

def sgd(feature, y):
        if len(feature) == 0: return 0
        hingeGradient = sum(i[0] * i[1] for i in zip(weights, feature)) * y
        if hingeGradient < 1:
            retVec = []
            for entry in feature:
                retVec.append(y*entry*-1)  #x_i * y
            return retVec
        return 0

def is_ascii(text):
    if isinstance(text, unicode):
        try:
            text.encode('ascii')
        except UnicodeEncodeError:
            return False
    else:
        try:
            text.decode('ascii')
        except UnicodeDecodeError:
            return False
    return True

for i in range(numIters):
    for x, y in trainExamples:
        poem_string = open(x, 'r').read()
        feature = get_features(poem_string)
        ret = sgd(feature, y)
        if ret != 0:
            for idx, entry in enumerate(weights):
                weights[idx] += (-1 * eta) * ret[idx]

poem_str = open(sys.argv[1], 'r').read()
# poem = poetrytools.tokenize(poem_str)
# print(poetrytools.guess_stanza_type(poem))
# print(poetrytools.guess_metre(poem))

# for char in poem_str:
#     print(is_ascii(char), char)
features = get_features(poem_str)
print(features)
print(classifier(features))
print(weights)
