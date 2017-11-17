import random
import glob

ITERATION_LENGTH = 30
DIRECTORY = 'training_texts'
N_VALUE = 3

ngrams_dict = {}

# get all text files in directory
def get_files(directory):
    return glob.glob('{}/*.txt'.format(directory))

# read list of files 
def read_files(files):
    string_list = []
    for file in files:
        with open(file, 'r') as myfile:
            print 'reading {}.....'.format(file)
            data=myfile.read().replace('\n', ' ')
            string_list.append(data)
    return string_list

# generate n-grams dictionary to generate 
def n_gram(n, string_list):
    for text in string_list:
        split = text.split()
        for i in range(len(split) - n + 1):
            key = ' '.join(split[i : i + n - 1]).lower()
            if key not in ngrams_dict:
                ngrams_dict[key] = [split[i + n - 1].lower()]
            else:
                ngrams_dict[key].append(split[i + n - 1].lower())

# generates n-gram output from dictionary        
def generate_Ngram(iteration_length):
    text = random.choice(ngrams_dict.keys())
    fill_string = text
    for i in range(iteration_length):
        next_word = random.choice(ngrams_dict[text])
        fill_string += ' ' + next_word
        # special case for bigrams
        if " " in text:
            text = text[text.index(' ') + 1:] + ' ' + next_word
        else:
            text = next_word
    return fill_string

'''
MAIN OPERATIONS

Limitations: 
    - no word wrap
    - no line breaks
    - no rhyming
    - no syllabic counting
    - smart start/end
    - quotations and other context-specific punctuation
'''

files = get_files(DIRECTORY)
string_list = read_files(files)
n_gram(N_VALUE, string_list)
print 'Number of files analyzed: {}'.format(len(files))
print '{}-gram of length {} generated: '.format(N_VALUE, ITERATION_LENGTH)
print generate_Ngram(ITERATION_LENGTH)
