from num2words import num2words
import re
from gutenberg.acquire import load_etext
from gutenberg.cleanup import strip_headers
import nltk
from nltk.tokenize import sent_tokenize


class Gutenberg:
    def __init__(self):
        self.book_sentences = []
        
    def get_text(self, book_id):
        text = strip_headers(load_etext(book_id)).strip()
        self.book_sentences = sent_tokenize(text)
    
class Generate_Time:
    def __init__(self):
        self.time_stamp = []
        self.text = ["one", "two", "three", "four", "five", "six", "seven", "eight","nine","ten", "eleven", "twelve", "thirteen", "fourteen", "quarter", "sixteen","seventeen", "eighteen", "nineteen", "twenty", "twenty-one","twenty-two", "twenty-three", "twenty-four", "twentyfive"," twenty-six", "twenty-seven", "twenty-eight", "twenty-nine", "half"]
  
    def text_time_generator(self, h, m):
        """
        Args:
            h (_int_): hours
            m (_int_): minutes

        Returns:
            str: the corresponding type of time in text form, such as "fifteen minutes to ten"
        """
        op = ""    
        if (m == 0):
            op = self.text[h - 1] + " o' clock"
        elif (m == 30):
            op = self.text[m - 1]+ " past " + self.text[h - 1]
        elif (m == 1):
            op = self.text[m - 1] + " minute past " + self.text[h - 1]
            #minute after
        elif (m == 15):
            op = self.text[m - 1]+ " past " + self.text[h - 1]
        elif (m < 30):
            op = self.text[m - 1] + " minutes past " + self.text[h - 1]
            #minutes after
        elif (m==45):
            op = "quarter to " + self.text[h]
        else:
            op =self. text[(60 - m)-1] + " minutes to " + self.text[h]
        return op
    
    def time_dash_generator(self, h, m):
        return str(num2words(h))+"-"+str(num2words(m))
        
    def time_num_generator(self, h, m):
        if (m < 10):
            m = "0"+str(m)
        return str(h)+":"+str(m)
    
    def create(self):
        for h in range(1,12):
            for m in range(0,60):
                self.time_stamp.append(self.text_time_generator(h, m))
                self.time_stamp.append(self.time_dash_generator(h, m))
                self.time_stamp.append(self.time_num_generator(h, m))
                
if __name__ == "__main__":
    time_sample = Generate_Time()
    time_sample.create()
    print(time_sample.time_stamp)
    
    g = Gutenberg()
    for i in range(1,500):
        g.get_text(i)
        print(g.book_sentences)
        for time_stamp in time_sample.time_stamp:
            print(time_stamp)
            for sentence in g.book_sentences:
                if time_stamp in sentence:
                    print("FOUND",time_stamp)
                else:
                    print("None")
        
    
            
    
        
    
                
    