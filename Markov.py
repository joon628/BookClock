import os
import random
import json
from sutime import SUTime


class MarkOv:
    def __init__(self,state_size, min_length):
        self.trainString = ""
        self.source = ""
        self.state_size = state_size
        self.model = {}
        self.min_length = min_length
        self.resultText = ""


    def loadSent(self):
        with open('testJson.json') as json_data:
            time_data = json.load(json_data)

        trainstring = ""
        for indvData in time_data:
            for indvSent in time_data[indvData]:
                indvString = indvSent[0]
                trainstring = trainstring + indvString + " "
        self.trainString = trainstring

    def build_model(self):
        source = self.trainString.split()
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
            if i > min_length and text[-1][-1] == '.':
                break

        self.resultText = ' '.join(text)

    def initModel(self):
        self.loadSent()
        self.build_model()
        self.build_model()
        self.generate_text()

class sentWtime():
    # generate model until 10 sentence with ideal time sentence found (<10)
    # replace with desire time
    def __init__(self,state_size,min_length,desire_time):
        self.timeSent = []
        self.state_size = state_size
        self.min_length = min_length
        self.desireTime = desire_time
        self.desireTimeSent = []
        self.replacedTime = ""

    def buildModel(self):
        MRKV = MarkOv(self.state_size, self.min_length)
        MRKV.initModel()
        return MRKV.resultText

    def findTimeSent(self):
        sutime = SUTime(mark_time_ranges=False, include_range=False)
        while len(self.timeSent) < len(self.desireTime):
            resultTx = self.buildModel()
            resultTxArr = resultTx.split(".")
            for sent in resultTxArr:
                    parsed_sentence = sutime.parse(sent)
                    if parsed_sentence:
                        for ps_each in parsed_sentence:
                            if ps_each['type'] == 'TIME':
                                time_value_raw = ps_each['timex-value'].split('T')[1]
                                time_value = time_value_raw.split('-')[0]
                                if not time_value.isalpha() and time_value != "XX:XX":
                                    self.timeSent.append([sent,ps_each['text']])

    def replaceTime(self):
        """" Based on need time, generate time sentence accordingly"""
        self.findTimeSent()
        for i in range(len(self.desire_time)):
            replacedTime = self.timeSent[i][0].replace(self.timeSent[i][1], self.desire_time[i])
            self.desireTimeSent.append(replacedTime)

    def randCallSent(self,indvNeedTime):
        """ When sentence needed, randomly select from generated sentence """
        self.findTimeSent()
        randInt = random.randint(0,len(self.timeSent))
        print(randInt)
        print(self.timeSent[randInt])
        self.replacedTime  = self.timeSent[randInt][0].replace(self.timeSent[randInt][1],indvNeedTime)


if __name__ == "__main__":
    state_size = 3
    min_length = 20
    # desire_time = ["7:01","7:02","7:03","7:04","7:05","17:01","17:02","17:03","17:04","17:05"]
    desire_time = ["7:01","7:02","7:03"]

    SWT = sentWtime(state_size, min_length,desire_time)
    # SWT.replaceTime()
    SWT.randCallSent(desire_time[0])
    print(SWT.replacedTime)