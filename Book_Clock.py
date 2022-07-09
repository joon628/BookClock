from ast import expr_context
from num2words import num2words
import re
import gutenbergpy.textget
from gutenberg.acquire import load_etext
from gutenberg.cleanup import strip_headers
import nltk
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
import pandas as pd
"""
To Do:

1. Grab Project Gutenberg and x number of texts (Pre Downloaded Files)


1a. Do I grab with downloaded files? V

1b. Do I download every time using the web?


2a. Regex Time representation phrases
2b. NLP Time representation phrasesq

3. Define each minute and corresponding text in hashmap 



4. Pull all text with the time correspondence from DB (Dump Search for all Time based Quotes)


split by sentence

4a. Do I search for each text every minute? 



4b. Do I download everything first and then run the file? V

5. Randomize selection tool for text dump 
6. Current Time display and output corresponding clock text  

"""

"""
Algorithm


Check sentence
If sentence does not have 
1. Number
2. Text style number 
3. The keywords noon and midnight

Then skip the sentence 

if it does, then run regex on the sentence



running regex 

1. does the sentence include any of the following?
    noon
    midnight
    afternoon
    morning
    am
    pm 
    evening

2. If so, run regex corresponding regex


"""

class Time_Text_Computation:
    def __init__(self):
        self.number_in_text = ""
        self.regex_dict = {
            #"past": re.compile(r"[^.]* ("+'|'.join(self.number_in_text)+r") past (?=("+'|'.join(self.number_in_text)+r")) [^.]*)", re.IGNORECASE),
            #"-": re.compile(r"[^.]* (?=("+'|'.join(self.number_in_text)+r")-(?=("+'|'.join(self.number_in_text)+r"))) [^.]*", re.IGNORECASE),
            #"minutes to": re.compile(r"[^.]* (?=("+'|'.join(self.number_in_text)+r") minutes to (?=("+'|'.join(self.number_in_text)+r")) [^.]*)", re.IGNORECASE),
            #":": re.compile(r"[^.]* ([01]?[0-9]|2[0-3]):[0-5][0-9][^.]*", re.IGNORECASE),
            "to" : re.compile(r".*("+self.number_in_text+") to ("+self.number_in_text+").*", re.IGNORECASE),
            "o'clock": re.compile(r".*("+self.number_in_text+") O'clock.*", re.IGNORECASE),
           # "afternoon":re.compile(r"[^.]* (?=("+'|'.join(self.number_in_text)+r") in the afternoon [^.]*)", re.IGNORECASE),
            #"morning":re.compile(r"[^.]* (?=("+'|'.join(self.number_in_text)+r") in the morning [^.]*)", re.IGNORECASE), #issues found
            #"am":  re.compile(r"[^.]* ([01]?[0-9]|2[0-3]):[0-5][0-9] am[^.]*", re.IGNORECASE),
            #"pm": re.compile(r"[^.]* ([01]?[0-9]|2[0-3]):[0-5][0-9] pm[^.]*", re.IGNORECASE),
            #"evening": re.compile(r"[^.]* (?=("+'|'.join(self.number_in_text)+r") in the evening [^.]*)", re.IGNORECASE)
        }
        self.sentences = []
   
    def generate_number_text(self):
        temp = []
        for i in range(20):
            temp.append(num2words(i)) 
        temp.append("half")
        temp.append("quarter")
        self.number_in_text = '|'.join(temp)
        print(self.number_in_text)
        
    def split_by_sentence(self,num):
        try:
            text = strip_headers(load_etext(num)).strip()
            sentences = text.replace("\r", " ").replace("\n"," ").replace("\t"," ").replace("’","'")
            self.sentences = sent_tokenize(sentences)
        except:
            pass
          
    def check_for_time(self):
        for sentence in self.sentences:
            if any(word.lower() in sentence for word in self.number_in_text):                
                for key in self.regex_dict:
                    if key in sentence:
                        if self.regex_dict[key].match(sentence):
                            m = self.regex_dict[key].match(sentence)
                            print(m.groups())
                            # print(key)
                            print(sentence)
                            
                        #if this matches figure out what it is 
class Book_Collection:
    pass

class Display:
    pass

if __name__ == "__main__":
    TTC = Time_Text_Computation()
    TTC.generate_number_text()
    #print('|'.join(TTC.number_in_text))
    
    
    for i in range (20,80):
        print(i)
        try:
            TTC.split_by_sentence(i)
            TTC.check_for_time()
        except:
            pass

        
