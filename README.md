# CS 221 Final Project - Michael Karr and Allison Tielking
Welcome to our final project read me! Here, we will explain what each folder of our project is supposed to do.

### Main Folder
#### evaluate.py

To run this program:
```bash
$ python evaluate.py
```
This program contains folders of the training texts and test texts. It will train the evaluator using SGD and then run through each test text to get the training and test error for our evaluator. You could modify this file to look at the evaluation of a specific .txt file as well.
#### min-char-rnn.py

This contains the vanilla implementation of our RNN. To run this program:
```bash
$ python min-char-rnn.py
```
This program will sample at every 100 cycles for 200 characters.
#### n-grams_baseline.py

This is our baseline implementation that uses n-grams to generate Seussian text.

### Poetry-Tools-Master

This holds our copy of the poetry tools library, which we edited to include checks for Seussian rhyme scheme and stanza that were not already part of the library. We specifically added anapestic tetrameter and seussian rhyme under the poetrytools/poetics.py folder.

### char-rnn-keras-master

This holds the current version of our model, the Keras multi-corpus RNN with a sequence length of 64. After doing research on various models from Github, we combined the best ideas into one program that we could understand. This code is written using Python 2, and you must install the [Keras](https://keras.io) deep learning library to run. To train the model with default settings: 
```bash
$ python train.py
```
To sample the model from the 100th epoch of training: 
```bash
$ python sample.py 100
```
The data folder holds all the network's training texts. A folder called logs will store a training_log after training locally.
### model_output

This stores the text samples from our various models, including ngrams, multi-corpus rnn, single corpus rnn, short sequence rnn, and vanilla.
### organizational

This holds our previous submissions, including a poster folder with all our figures and images of the poster, and our project proposal. 
### test_text

This holds our 15 test texts from 8 Seuss works and 7 non-Seuss works

### training_texts and non_seuss_training_texts

training_texts holds all our Seussian training texts, and non_seuss_training_texts holds all our non-Seussian training texts.
