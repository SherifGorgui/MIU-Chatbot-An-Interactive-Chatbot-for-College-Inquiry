import os

from sklearn.linear_model import SGDClassifier
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
#nltk.download('all')
from nltk.stem   import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import json
import pickle
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import *
import random


class Chatbot:

    __words=[]
    __classes = []
    __documents = []
    __ignore_words = ['?', '!']
    __data_file = open('dataset/intents.json', encoding = "utf8").read()
    __intents = json.loads(__data_file)

    def __init__(self):
        #to get all tags from json file (load every thing)
        for intent in self.__intents['intents']:
            for pattern in intent['patterns']:

                #tokenize each word
                w = nltk.word_tokenize(pattern)
                self.__words.extend(w)
                #add documents in the corpus
                self.__documents.append((w, intent['tag']))

                # add to our classes list
                if intent['tag'] not in self.__classes:
                    self.__classes.append(intent['tag'])
                    
                    

        # lemmaztize and lower each word and remove duplicates
        words = [lemmatizer.lemmatize(w.lower()) for w in self.__words if w not in self.__ignore_words]
        words = sorted(list(set(words)))
        # sort classes
        classes = sorted(list(set(self.__classes)))
        # documents = combination between patterns and intents
        print (len(self.__documents), "documents")
        # classes = intents
        print (len(classes), "classes", classes)
        # words = all words, vocabulary
        print (len(words), "unique lemmatized words", words)

        pickle.dump(words, open('C:/Users/Gorgui/Desktop/Chatbot/Chatbot v2.1/dataset/words.pkl', 'wb'))
        pickle.dump(classes, open('C:/Users/Gorgui/Desktop/Chatbot/Chatbot v2.1/dataset/classes.pkl', 'wb'))

        # create our training data
        training = []
        # create an empty array for our output
        output_empty = [0] * len(classes)
        # training set, bag of words for each sentence
        for doc in self.__documents:
            # initialize our bag of words
            bag = []
            # list of tokenized words for the pattern
            pattern_words = doc[0]
            # lemmatize each word - create base word, in attempt to represent related words
            pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]
            # create our bag of words array with 1, if word match found in current pattern
            for w in words:
                bag.append(1) if w in pattern_words else bag.append(0)
            
            # output is a '0' for each tag and '1' for current tag (for each pattern)
            output_row = list(output_empty)
            output_row[classes.index(doc[1])] = 1
            
            training.append([bag, output_row])
        # shuffle our features and turn into np.array
        random.shuffle(training)
        training = np.array(training, dtype=object)
        # create train and test lists. X - patterns, Y - intents
        train_x = list(training[:,0])
        train_y = list(training[:,1])
        print("Training data created")


        # Create model - 3 layers. First layer 128 neurons, second layer 64 neurons and 3rd output layer contains number of neurons
        # equal to number of intents to predict output intent with softmax
        model = Sequential()
        model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(64, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(len(train_y[0]), activation='softmax'))


        # Compile model. Stochastic gradient descent with Nesterov accelerated gradient gives good results for this model
        sgd = SGD(learning_rate=0.01, decay=1e-6, momentum=0.9, nesterov=True)
        model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
        #fitting and saving the model 
        hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
        model.save('C:/Users/Gorgui/Desktop/Chatbot/Chatbot v2.1/dataset/chatbot_model.h5', hist)
        print("model created") 
        print(model.summary())

