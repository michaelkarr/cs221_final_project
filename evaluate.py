import poetrytools
import sys
import random
from textblob import TextBlob

trainExamples = (("non_seuss_training_texts/daddy.txt", -1), ("non_seuss_training_texts/cloud.txt", -1), ("non_seuss_training_texts/troy.txt", -1), ("non_seuss_training_texts/another_sky.txt", -1), ("non_seuss_training_texts/dream.txt", -1), ("non_seuss_training_texts/road_not_taken.txt", -1), ("non_seuss_training_texts/when_sidewalk_ends.txt", -1),
("training_texts/fox_in_socks.txt", 1), ("training_texts/cat_in_the_hat.txt", 1), ("training_texts/green_eggs_and_ham.txt", 1), ("training_texts/hop_on_pop.txt", 1),
("training_texts/oh_the_places_you'll_go.txt", 1), ("training_texts/one_fish_two_fish_red_fish_blue_fish.txt", 1)
)
testExamples = (("test_text/brown.txt", 1), ("test_text/eulalie.txt", -1), ("test_text/foot.txt", 1), ("test_text/horton.txt", 1), ("test_text/turtle.txt", 1), ("test_text/wocket.txt", 1), ("test_text/shakespeare.txt", -1), ("test_text/cummings.txt", -1), ("test_text/kaur.txt", -1), ("test_text/reeves.txt", -1), ("test_text/eggs.txt", 1),
("test_text/catback.txt", 1), ("test_text/power.txt", -1), ("test_text/marvin.txt", 1), ("test_text/hatch.txt", 1))
sight_set = set(line.strip() for line in open('sightwords.txt'))
weights = [0] * 4
eta = 0.1
numIters = 200

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

    # analysis = TextBlob(poem_str)
    # if analysis.sentiment.polarity > 0:
    #     sentiment = 1
    # elif analysis.sentiment.polarity == 0:
    #     sentiment = 0
    # else:
    #     sentiment = -1

    features = [stanza, meter, rhyme_type, seussian_sight_prop] #for generated text
    return features

def classifier(x): #dot product of weight and feature vector, returns classification
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

def is_ascii(text): #checks if each character has an ascii encoding, used to clean up test/training text
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

for i in range(numIters): #sgd to optimize training weights
    for x, y in trainExamples:
        poem_string = open(x, 'r').read()
        feature = get_features(poem_string)
        ret = sgd(feature, y)
        if ret != 0:
            for idx, entry in enumerate(weights):
                weights[idx] += (-1 * eta) * ret[idx]

error = 0
#8 seuss test, #7 non-seuss test -> 3/8 seuss error, 2/7 seuss
for x, y in testExamples: #gets test error
    poem_string = open(x, 'r').read()
    feature = get_features(poem_string)
    print(x, feature)
    if classifier(feature) != y:
        error += 1
print(1.0 * error / len(testExamples))
