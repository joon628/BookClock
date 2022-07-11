import json
from num2words import num2words
from sutime import SUTime
from gutenberg.acquire import load_etext
from gutenberg.cleanup import strip_headers
from nltk.tokenize import sent_tokenize
from numba import cuda,jit

class Time_Text_Computation:
    def __init__(self):
        self.numbers_in_text = ""
        self.sentences = []
        self.keywords = ["past","-", "minute after", ":", "to", "o'clock", "noon", "midnight", "am", "pm"]
     
    def generate_number_text(self):
        temp = []
        for i in range(20):
            temp.append(num2words(i))
        temp.append("half")
        temp.append("quarter")
        self.numbers_in_text = temp

    def split_by_sentence(self,num):
        try:
            text = strip_headers(load_etext(num)).strip()
            sentences = text.replace("\r", " ").replace("\n"," ").replace("\t"," ").replace("’","'")
            self.sentences = sent_tokenize(sentences)
        except:
            pass
    
    
    def check_for_time(self):
        for sentence in self.sentences:
            if any(word.lower() in sentence for word in self.numbers_in_text):
                for key in self.keywords:
                    if key in sentence:
                        print(sentence)
                        self.run_sutime(sentence)
                        
    @jit(forceobj=True)
    def run_sutime(self,sentence):
        sutime = SUTime(mark_time_ranges=True, include_range=True)
        print(json.dumps(sutime.parse(sentence), sort_keys=True, indent=4))

        
        
        
if __name__ == '__main__':
    TTC = Time_Text_Computation()
    TTC.generate_number_text()
    for i in range (20,30):
        print(i)
        try:
            TTC.split_by_sentence(i)
            TTC.check_for_time()
        except:
            pass







     