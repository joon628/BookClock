from asyncore import read
from number2words import num2words
import re
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
    past
    -
    minute after
    :
    to 
    O'clock
    noon
    midnight
    afternoon
    morning
    am
    pm 
    evening

2. If so, run regex corresponding regex


"""



def split_by_sentence(directory):
    with open(directory) as f:
        sentences = f.split(".")
    return sentences





            
            
            
class Time_Text_Computation:
    def __init__(self):
        self.number_in_text = []
        self.regex_dict = {
            "past": re.compile(r"(?=("+'|'.join(self.number_in_text)+r") past (?=("+'|'.join(self.number_in_text)+r"))", re.IGNORECASE),
            "-": re.compile(r"(?=("+'|'.join(self.number_in_text)+r")-(?=("+'|'.join(self.number_in_text)+r"))", re.IGNORECASE),
            "minute after": re.compile(r"(?=("+'|'.join(self.number_in_text)+r") minute after (?=("+'|'.join(self.number_in_text)+r"))", re.IGNORECASE),
            ":": re.compile(r"[0-9]+:[0-9]+", re.IGNORECASE),
            "to" : re.compile(r"(?=("+'|'.join(self.number_in_text)+r") to (?=("+'|'.join(self.number_in_text)+r"))", re.IGNORECASE):,
            "O'clock":, 
            "noon":,
            "midnight":,
            "afternoon":,
            "morning":,
            "am":,
            "pm":,
            "evening":
        }
        
    def generate_number_text(self):
        for i in range(60):
            self.number_in_text.append(num2words(i), to = 'ordinal') 
    
    def check_for_time(self):
        for sentence in sentences:
            if number in sentence or text_number in sentence or ["noon","midnight"] in sentence:
                for key in self.regex_dict:
                    if key in sentence:
                        self.regex_dict[key].match(sentence)
                        #if this matches figure out what it is 
     
    def regex_time_expression(self): 
        

        
        
        return past.match(input)
        
     




class Book_Collection:
    pass

class Display:
    pass