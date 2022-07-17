from codecs import ignore_errors
import json
from ReadJSON import load_json, dictionaryToJson
import time
import pandas as pd
import random
import sqlite3

class BookClock:
    def __init__(self,time):
        with open("./sample.json") as json_data:
            self.json = json.load(json_data)
        #self.time = time
        self.out = ""
        self.DF = ""
        
    def randomize_output(self):
        quote_selection = self.DF[self.time]
        self.out = quote_selection.sample()
        
    def quality_check(self):
        pass
    
    def highlight_text(self):
        pass
    
    def populate_DF(self):
        df = pd.DataFrame(columns = ['time', 'sentence', 'highlight', 'title'])
        for key in self.json:
            for value in self.json[key]:
                temp = {'time': key,'sentence':value[0], 'highlight':value[1],'title':value[2]}
                df2 = pd.DataFrame.from_dict([temp])
                df = pd.concat([df,df2])  
        self.DF = df
    
    def create_sql(self):
        conn = sqlite3.connect('time_database')
        df = self.DF
        df.to_sql('time_database', conn, if_exists='replace', index = False)
 
if __name__ == '__main__':
    # t = time.localtime()
    # current_time = time.strftime("%H:%M", t)
    bookclock = BookClock("9:30")
    bookclock.populate_DF()
    bookclock.create_sql()
    # out = bookclock.out
    print(bookclock.DF)