import os

ngrams_dict = {}

def N_gram(n, string_list):
    for text in string_list:
        split = text.split()
        for i in range(len(split) - n + 1):
            key = ' '.join(split[i : i + n - 1]).lower()
            if key not in ngrams_dict:
                ngrams_dict[key] = [split[i + n - 1]]
            else:
                ngrams_dict[key].append(split[i + n - 1])

string_list = ["hello HOW are you doing today"]
N_gram(2, string_list)
print ngrams_dict
