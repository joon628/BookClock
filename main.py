import json
import time
from venv import create
from num2words import num2words
from sutime import SUTime
from gutenberg.acquire import load_etext
from gutenberg.cleanup import strip_headers
from nltk.tokenize import sent_tokenize
from ReadJSON import load_json, dictionaryToJson, populate_DF, create_sql
import timeit

# from numba import jit, cuda

class Time_Text_Computation:
    def __init__(self):
        self.numbers_in_text = ""
        self.sentences = []
        self.currTitle = ""
        self.OuterBook = {}
        self.keywords = ["past","-", "minute after", ":", "to", "o'clock", "noon", "midnight", "am", "pm"]
        self.metaDF = load_json()
        self.bookIDs = self.metaDF.keys()

    def generate_number_text(self):
        temp = []
        for i in range(20):
            temp.append(num2words(i))
        temp.append("half")
        temp.append("quarter")
        self.numbers_in_text = temp

    def get_id_range(self):
        booklength = len(self.metaDF.keys()) # 15942
        print(booklength)

    def split_by_sentence(self,num):
        try:
            text = strip_headers(load_etext(num)).strip()
            sentences = text.replace("\r", " ").replace("\n"," ").replace("\t"," ").replace("’","'")
            self.currTitle = self.metaDF[num]['title'][0]
            print(self.currTitle)
            self.sentences = sent_tokenize(sentences)
        except:
            pass
    
    def check_for_time(self):
        sutime = SUTime(mark_time_ranges=False, include_range=False)
        for sentence in self.sentences:
            parsed_sentence = sutime.parse(sentence)
            if parsed_sentence:
                for ps_each in parsed_sentence:
                    if ps_each['type'] == 'TIME':
                        time_value = ps_each['timex-value'].split('T')[1]
                        if not time_value.isalpha() or not "XX:XX":
                            print(sentence)
                            print(time_value)
                            print(ps_each['text'])
                            print(self.currTitle)
                            print()
                            if time_value in self.OuterBook:
                                self.OuterBook[time_value].append([sentence, ps_each['text'],self.currTitle])
                            else:
                                self.OuterBook[time_value] = [[sentence, ps_each['text'], self.currTitle]]
    
                             
if __name__ == '__main__':
    TTC = Time_Text_Computation()
    # TTC.generate_number_text()
    testRange = TTC.bookIDs[:100]
    for i in testRange:
        try:
            TTC.split_by_sentence(i)
            TTC.check_for_time()
          
        except:
            pass

    print("main")
    print(TTC.OuterBook.keys())
    for k, v in TTC.OuterBook.items():
        print(k, v)
    dictionaryToJson(TTC.OuterBook)
    df = populate_DF('./sample.json')
    create_sql(df)

