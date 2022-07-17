import json
import time
from num2words import num2words
from sutime import SUTime
from gutenberg.acquire import load_etext
from gutenberg.cleanup import strip_headers
from nltk.tokenize import sent_tokenize
from ReadJSON import load_json, dictionaryToJson, populate_DF, create_sql, modify_json
import timeit
from concurrent.futures import ThreadPoolExecutor, as_completed


# from numba import jit, cuda

class Time_Text_Computation:
    def __init__(self):
        self.sentences = []
        self.currTitle = ""
        self.OuterBook = {}
        self.keywords = ["past", "-", "minutes", ":", "to", "o'clock", "noon", "midnight", "am", "pm", "P.M.", "A.M.", "after", "hours","half","quarter"]
        self.metaDF = load_json("modified_gutenMeta.json")
        self.bookIDs = self.metaDF.keys()

    def generate_number_text(self):
        temp = []
        for i in range(60):
            self.keywords.append(num2words(i))

    def get_id_range(self):
        booklength = len(self.metaDF.keys())
        print(booklength)

    def split_by_sentence(self,num):
        try:
            text = strip_headers(load_etext(num)).strip()
            sentences = text.replace("\r", " ").replace("\n"," ").replace("\t"," ").replace("’","'")
            self.currTitle = self.metaDF[num]['title'][0]
            with ThreadPoolExecutor() as executor:
                future = executor.submit(sent_tokenize, sentences)
            self.sentences = future.result()
        except:
            pass
    
    def check_for_time(self):
        sutime = SUTime(mark_time_ranges=False, include_range=False)
        for sentence in self.sentences:
            if any(word.lower() in sentence.lower() for word in self.keywords):
                parsed_sentence = sutime.parse(sentence)
            if parsed_sentence:
                for ps_each in parsed_sentence:
                    if ps_each['type'] == 'TIME':
                        time_value_raw = ps_each['timex-value'].split('T')[1]
                        time_value = time_value_raw.split('-')[0]
                        if not time_value.isalpha() and time_value != "XX:XX":
                            if time_value in self.OuterBook:
                                self.OuterBook[time_value].append([sentence, ps_each['text'],self.currTitle])
                            else:
                                self.OuterBook[time_value] = [[sentence, ps_each['text'], self.currTitle]]
    
                    
    def check_for_time_threaded(self):
        sutime = SUTime(mark_time_ranges=False, include_range=False)
        start_time = time.time()
        parsed_sentences = []
        with ThreadPoolExecutor(max_workers=50) as executor:
            for sentence in self.sentences:
                if any(word.lower() in sentence.lower() for word in self.keywords):
                    parsed_sentences.append(executor.submit(self.sutime_parse, sutime, sentence))
        for task in as_completed(parsed_sentences):
            sentence, individual_parsed_sentence = task.result()
            if individual_parsed_sentence:
                for ps_each in individual_parsed_sentence:
                    if ps_each['type'] == 'TIME':
                        time_value_raw = ps_each['timex-value'].split('T')[1]
                        time_value = time_value_raw.split('-')[0]
                        if not time_value.isalpha() and time_value != "XX:XX":
                            if time_value in self.OuterBook:
                                self.OuterBook[time_value].append([sentence, ps_each['text'],self.currTitle])
                            else:
                                self.OuterBook[time_value] = [[sentence, ps_each['text'], self.currTitle]]
                                
        print("--- %s seconds ---" % (time.time() - start_time))
                            
    def sutime_parse(self, sutime, sentence):
        parsed_sentence = sutime.parse(sentence)
        package = [sentence, parsed_sentence]
        return package
   
if __name__ == '__main__':
    TTC = Time_Text_Computation()
    TTC.generate_number_text()
    modify_json()
    
    booknum = 1
    testRange = TTC.bookIDs[:booknum]
    for i in testRange:
        try:
            TTC.split_by_sentence(i)
            TTC.check_for_time()
        except:
            pass
        print("Process: "+ str((i/booknum)*100) +" %")

    print("main")
    print(TTC.OuterBook.keys())
    for k, v in TTC.OuterBook.items():
        print(k, v)

    # dictionaryToJson(TTC.OuterBook)
    # df = populate_DF('./sample.json')
    # create_sql(df)

