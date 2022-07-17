import os
import random
import json
from sutime import SUTime
import sqlite3
import re
import language_tool_python

from sqlite3 import OperationalError


class MarkOv:
    def __init__(self,state_size, min_length):
        self.trainString = ""
        self.source = ""
        self.state_size = state_size
        self.model = {}
        self.min_length = min_length
        self.resultText = ""

    def fixCaps(self,word):
        if word.isupper() and word != "I":
            word = word.lower()
        elif word[0].isupper():
            word = word.lower().capitalize()
        else:
            word = word.lower()
        return word

    def toHashKey(self,lst):
        return tuple(lst)

    # def loadSent(self):
    #     with open('testJson.json') as json_data:
    #         time_data = json.load(json_data)
    #
    #     trainstring = ""
    #     for indvData in time_data:
    #         for indvSent in time_data[indvData]:
    #             indvString = indvSent[0]
    #             trainstring = trainstring + indvString + " "
    #     self.trainString = trainstring

    def loadSentSQL(self):
        con = sqlite3.connect("time_database")
        cur = con.cursor()

        wordlist = []
        for row in cur.execute('SELECT * FROM time_database;'):
            wl = [self.fixCaps(w) for w in re.findall(r"[\w']+|[.,!?;]", row[1])]
            wordlist += wl
        self.trainString = wordlist


    def build_model(self):
        source = self.trainString
        for i in range(self.state_size, len(source)):
            current_word = source[i]
            previous_words = ' '.join(source[i-self.state_size:i])
            if previous_words in self.model:
                self.model[previous_words].append(current_word)
            else:
                self.model[previous_words] = [current_word]


    def generate_text(self):
        def get_new_starter():
            return random.choice([s.split(' ') for s in self.model.keys() if s[0].isupper()])
        text = get_new_starter()

        i = self.state_size
        while True:
            key = ' '.join(text[i-self.state_size:i])
            if key not in self.model:
                text += get_new_starter()
                i += 1
                continue

            next_word = random.choice(self.model[key])
            text.append(next_word)
            i += 1
            if i > self.min_length and text[-1][-1] == '.':
                break

        self.resultText = ' '.join(text)

    def initModel(self):
        self.loadSentSQL()
        self.build_model()
        self.build_model()
        self.generate_text()

class sentWtime():
    # generate model until 10 sentence with ideal time sentence found (<10)
    # replace with desire time
    def __init__(self,state_size,min_length,numOfSent):
        self.timeSent = []
        self.state_size = state_size
        self.min_length = min_length
        # self.desireTime = desire_time
        self.desireTimeSent = []
        self.replacedTime = ""
        self.numOfSent = numOfSent

    def buildModel(self):
        MRKV = MarkOv(self.state_size, self.min_length)
        MRKV.initModel()
        return MRKV.resultText

    def findTimeSent(self):
        sutime = SUTime(mark_time_ranges=False, include_range=False)
        tool = language_tool_python.LanguageToolPublicAPI('en-US')
        while len(self.timeSent) < self.numOfSent:
            resultTx = self.buildModel()
            resultTxArr = resultTx.split(".")
            print(resultTxArr)
            for sent in resultTxArr:
                print(sent)
                print(len(sent))
                if len(sent) > 20 or len(sent) < 400:
                    print("here")
                    parsed_sentence = sutime.parse(sent)
                    if parsed_sentence:
                        for ps_each in parsed_sentence:
                            if ps_each['type'] == 'TIME':
                                time_value_raw = ps_each['timex-value'].split('T')[1]
                                time_value = time_value_raw.split('-')[0]
                                if not time_value.isalpha() and time_value != "XX:XX":
                                    self.timeSent.append([tool.correct(sent),ps_each['text']])
        print("timeSent")
        print(self.timeSent)

    def replaceTime(self):
        """" Based on need time, generate time sentence accordingly"""
        self.findTimeSent()
        print(self.desireTime)
        for i in range(len(self.desireTime)):
            replacedTime = self.timeSent[i][0].replace(self.timeSent[i][1], self.desireTime[i])
            self.desireTimeSent.append(replacedTime)

    def randCallSent(self,indvNeedTime):
        """ When sentence needed, randomly select from generated sentence """
        self.findTimeSent()
        randInt = random.randint(0,len(self.timeSent))
        print(randInt)
        print(self.timeSent[randInt])
        self.replacedTime = self.timeSent[randInt][0].replace(self.timeSent[randInt][1],indvNeedTime)


if __name__ == "__main__":
    state_size = 2
    min_length = 20
    # desire_time = ["7:01","7:02","7:03","7:04","7:05","17:01","17:02","17:03","17:04","17:05"]
    desire_time = ["7:01","7:02","7:03"]
    numOfSent = 10

    SWT = sentWtime(state_size, min_length,numOfSent)
    SWT.findTimeSent()

    with open("data\markv.json", "w") as outfile:
        json.dump(SWT.timeSent, outfile)


    # MRK = MarkOv(state_size, min_length)
    # MRK.loadSentSQL()
    # print(MRK.trainString)