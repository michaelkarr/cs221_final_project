import argparse
import os
import json
import sys

import numpy as np

from model import build_model, load_weights

DATA_DIR = './data'

# sample the most recent model
def sample(epoch, header, num_chars):
	# get the character dictionary and build the character-index dict
	with open(os.path.join(DATA_DIR, 'char_to_idx2.json')) as f:
		char_to_idx2 = json.load(f)
	idx_to_char2 = { i: ch for (ch, i) in char_to_idx2.items() }
	vocab_size = len(char_to_idx2)

	model = build_model(1, 1, vocab_size)
	load_weights(epoch, model)

	# header implementation if needed
	sampled = [char_to_idx2[c] for c in header]
	for c in header[:-1]:
		batch = np.zeros((1, 1))
		batch[0, 0] = char_to_idx2[c]
		model.predict_on_batch(batch)

	# sample until parameter
	for i in range(num_chars):
		batch = np.zeros((1, 1))
		if sampled:
			batch[0, 0] = sampled[-1]
		else:
			batch[0, 0] = np.random.randint(vocab_size)
		result = model.predict_on_batch(batch).ravel()
		sample = np.random.choice(range(vocab_size), p=result)
		sampled.append(sample)

	print ''.join(idx_to_char2[c] for c in sampled)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Sample some text from the trained model.')
	parser.add_argument('epoch', type=int, help='epoch checkpoint to sample from')
	parser.add_argument('--seed', default='', help='initial seed for the generated text')
	parser.add_argument('--len', type=int, default=512, help='number of characters to sample (default 512)')
	args = parser.parse_args()

	print sample(args.epoch, args.seed, args.len)
