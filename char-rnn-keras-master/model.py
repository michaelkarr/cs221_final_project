import os

import numpy as np
from keras.models import Sequential, model_from_json
from keras.layers import LSTM, Dropout, TimeDistributed, Dense, Activation, Embedding

MODEL_DIR = './model'

# save model weights into file
def save_weights(epoch, model):
	if not os.path.exists(MODEL_DIR):
		os.makedirs(MODEL_DIR)
	model.save_weights(os.path.join(MODEL_DIR, 'weights.{}.h5'.format(epoch)))

# build model from weights
def load_weights(epoch, model):
	model.load_weights(os.path.join(MODEL_DIR, 'weights.{}.h5'.format(epoch)))
	return model

# create model
def build_model(batch_size, seq_len, vocab_size):
	model = Sequential()
	# creating an embedding for LSTMs
	model.add(Embedding(vocab_size, 512, batch_input_shape=(batch_size, seq_len)))

	# add three chained state LSTMs with dropout of 20%
	# return_sequences must be true when stacking LSTMs to ensure they all receive
	#	same dimensionality for input
	# need states to access hidden layers easily
	for i in range(3):
		model.add(LSTM(256, return_sequences=True, stateful=True))
		model.add(Dropout(0.2))

	model.add(TimeDistributed(Dense(vocab_size)))
	model.add(Activation('softmax'))
	return model

if __name__ == '__main__':
	model = build_model(16, 64, 50)
	model.summary()
