import argparse
import os
import json
import sys

import numpy as np

from model import build_model, save_weights

DATA_DIR = './data'
LOG_DIR = './logs'

# constans for diversity promotion
BATCH_SIZE = 16
SEQ_LENGTH = 64

# manipulate training files
class TrainLogger(object):
	def __init__(self, file):
		self.file = os.path.join(LOG_DIR, file)
		self.epochs = 0
		with open(self.file, 'w') as f:
			f.write('epoch,loss,acc\n')

	def add_entry(self, loss, acc):
		self.epochs += 1
		s = '{},{},{}\n'.format(self.epochs, loss, acc)
		with open(self.file, 'a') as f:
			f.write(s)

# build dictionaries for consistent dimension for LSTM and embedding
def read_batches(T, vocab_size):
	length = T.shape[0]
	batch_chars = length / BATCH_SIZE

	for start in range(0, batch_chars - SEQ_LENGTH, SEQ_LENGTH):
		X = np.zeros((BATCH_SIZE, SEQ_LENGTH))
		Y = np.zeros((BATCH_SIZE, SEQ_LENGTH, vocab_size))
		for batch_idx in range(0, BATCH_SIZE):
			for i in range(0, SEQ_LENGTH):
				X[batch_idx, i] = T[batch_chars * batch_idx + start + i]
				Y[batch_idx, i, T[batch_chars * batch_idx + start + i + 1]] = 1
		yield X, Y

def train(text1, text2, epochs=100, save_freq=10):
	# clean input
	text1 = unicode(text1, errors='ignore')
	text2 = unicode(text2, errors='ignore')

	# create character index dictinaries
	char_to_idx1 = { ch: i for (i, ch) in enumerate(sorted(list(set(text1)))) }
	char_to_idx2 = { ch: i for (i, ch) in enumerate(sorted(list(set(text2)))) }

	# store dicts in files
	with open(os.path.join(DATA_DIR, 'char_to_idx1.json'), 'w') as f1:
		json.dump(char_to_idx1, f1)

	with open(os.path.join(DATA_DIR, 'char_to_idx2.json'), 'w') as f2:
		json.dump(char_to_idx2, f2)

	# create reverse dictionaries
	idx_to_char1 = { i: ch for (ch, i) in char_to_idx1.items() }
	idx_to_char2 = { i: ch for (ch, i) in char_to_idx2.items() }

	vocab_size = len(char_to_idx1)

	# build model with loss and optimization metrics
	model = build_model(BATCH_SIZE, SEQ_LENGTH, vocab_size)
	model.summary()
	model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

	# separate training into two texts
	T1 = np.asarray([char_to_idx1[c] for c in text1], dtype=np.int32)
	T2 = np.asarray([char_to_idx2[c] for c in text2], dtype=np.int32)

	# steps_per_epoch = (len(text2) / BATCH_SIZE - 1) / SEQ_LENGTH
	log = TrainLogger('training_log.csv')

	# train the network
	for epoch in range(epochs):
		print '\nEpoch {}/{}'.format(epoch + 1, epochs)

		losses, accs = [], []

		# start training on non-seuss text, switch to Seuss in transfer 
		#	learning after 15 epochs
		if epoch < 15:
			for i, (X, Y) in enumerate(read_batches(T1, vocab_size)):
				loss, acc = model.train_on_batch(X, Y)
				# print logs for every batch
				print 'Batch {}: loss = {}, acc = {}'.format(i + 1, loss, acc)
				losses.append(loss)
				accs.append(acc)
		else:
			for i, (X, Y) in enumerate(read_batches(T2, vocab_size)):
				loss, acc = model.train_on_batch(X, Y)
				print 'Batch {}: loss = {}, acc = {}'.format(i + 1, loss, acc)
				losses.append(loss)
				accs.append(acc)

		log.add_entry(np.average(losses), np.average(accs))

		# save checkpoint data to file
		if (epoch + 1) % save_freq == 0:
			save_weights(epoch + 1, model)
			print 'Saved checkpoint to', 'weights.{}.h5'.format(epoch + 1)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Train the model on some text.')
	parser.add_argument('--input', default='all_seuss.txt', help='name of the text file to train from')
	parser.add_argument('--epochs', type=int, default=100, help='number of epochs to train for')
	parser.add_argument('--freq', type=int, default=10, help='checkpoint save frequency')
	args = parser.parse_args()

	if not os.path.exists(LOG_DIR):
		os.makedirs(LOG_DIR)

	model = train(open(os.path.join(DATA_DIR, "non_seuss.txt")).read(), open(os.path.join(DATA_DIR, "all_seuss.txt")).read(), args.epochs, args.freq)
