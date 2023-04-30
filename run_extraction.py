import os
import re
import json
import requests
import nltk
from sutime import SUTime
import sqlite3

# function to extract time expressions from a text using SUTime
def extract_time(sentence):
    try:
        sutime = SUTime(mark_time_ranges=True, include_range=True)
        time_expression = json.dumps(sutime.parse(sentence), sort_keys=True, indent=4)
        json_data = json.loads(time_expression)
        time_values = []
        for data in json_data:
            if data['type'] == 'TIME':
                time_values.append(data)
        return [sentence, time_values]
    except Exception as e:
        print(f"Error extracting time expressions from sentence: {sentence}")
        print(f"Error message: {str(e)}")
        return []

nltk.download('punkt') 
# open the book file and extract its text

def add_data():
    conn = sqlite3.connect('D:\\BookClockData\\timex.db')
    c = conn.cursor()
    for filename in os.listdir('D:\\BookClockData\\'):
        if filename.endswith(".txt"):
            # open file and process its contents
            with open(os.path.join('D:\\BookClockData\\', filename), "r") as f:
                book_text = f.read()
                sentences = nltk.sent_tokenize(book_text)
                # iterate over the sentences and extract time expressions
                for sentence in sentences:
                    input_data = extract_time(sentence)
                    if input_data[1] != []:
                        sentence = input_data[0]
                        timex_data = input_data[1]
                        for timex in timex_data:
                            text = timex['text']
                            timex_value = timex['timex-value']
                            typ = timex['type']
                            value = timex['value']
                            c.execute("INSERT INTO timex (sentence, text, 'timex-value', typ, value) VALUES (?, ?, ?, ?, ?)",
                                    (sentence, text, timex_value, typ, value))
    conn.commit()
    conn.close()
    
add_data()