import os
from flask import request, session
from flask import jsonify, render_template
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import nltk
from nltk.stem import WordNetLemmatizer

import pickle
import numpy as np
from keras.models import load_model
from models.chatbot_train import Chatbot
from datetime import datetime

from models.question_answer_data import QuestionAnswer


import json
import random

class QAController:
    __intents = json.loads(open('C:/Users/Gorgui/Desktop/Chatbot/Chatbot v2.1/dataset/intents.json', encoding="utf8").read())
    __words = pickle.load(open('C:/Users/Gorgui/Desktop/Chatbot/Chatbot v2.1/dataset/words.pkl', 'rb'))
    __classes = pickle.load(open('C:/Users/Gorgui/Desktop/Chatbot/Chatbot v2.1/dataset/classes.pkl', 'rb'))

    __lemmatizer = WordNetLemmatizer()
    __model = load_model('C:/Users/Gorgui/Desktop/Chatbot/Chatbot v2.1/dataset/chatbot_model.h5')

    __question_answer = QuestionAnswer()
    def __init__(self):
        self.__chatbot = Chatbot()

    def __clean_up_sentence(self, sentence):
        # tokenize the pattern - split words into array
        sentence_words = nltk.word_tokenize(sentence)
        # stem each word - create short form for word
        sentence_words = [self.__lemmatizer.lemmatize(word.lower()) for word in sentence_words]
        return sentence_words

    # return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

    def __bow(self, sentence, words, show_details=True):
        # tokenize the pattern
        sentence_words = self.__clean_up_sentence(sentence)
        # bag of words - matrix of N words, vocabulary matrix
        bag = [0]*len(words)  
        for s in sentence_words:
            for i,w in enumerate(words):
                if w == s: 
                    # assign 1 if current word is in the vocabulary position
                    bag[i] = 1
                    if show_details:
                        print ("found in bag: %s" % w)
        return(np.array(bag))

    def __predict_class(self, sentence, model):
        # filter out predictions below a threshold
        p = self.__bow(sentence, self.__words,show_details=False)
        res = model.predict(np.array([p]))[0]
        ERROR_THRESHOLD = 0.25
        results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
        # sort by strength of probability
        results.sort(key=lambda x: x[1], reverse=True)
        return_list = []
        for r in results:
            return_list.append({"intent": self.__classes[r[0]], "probability": str(r[1])})
        return return_list

    def __getResponse(self, ints, intents_json):
        try:
            tag = ints[0]['intent']
            list_of_intents = intents_json['intents']
            for i in list_of_intents:
                if(i['tag']== tag):
                    result = random.choice(i['responses'])
                    break
        except IndexError:
            result ="I Don't understand,Plase elaborate"
        return result

    def __chatbot_response(self, msg):
        print(msg)
        ints = self.__predict_class(msg, self.__model)
        res = self.__getResponse(ints, self.__intents)
        return res

    def __send(self, msg):
        if msg != '':
            ques = msg.split(",")
            for x in ques:
                res = self.__chatbot_response(x)
                resstr = str(res)
                print(resstr)
                link = resstr.split(",")
                for y in link:
                    print(y)
                    if ("http" in y):
                        return y
                    else:
                        return resstr



    def send_msg(self):
        if request.method == 'POST':
            # datetime object containing current date and time
            now = datetime.now()
            # dd/mm/YY H:M:S
            date_time = now.strftime("%d/%m/%Y %H:%M:%S")
            print("date and time =", date_time)	    
            question = request.form['msg']
            answer = self.__send(question)
            user_id = session['id']
            self.__question_answer.insert_data(user_id, question, answer, date_time)
            return jsonify({'answer': answer})