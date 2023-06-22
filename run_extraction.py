import os
import re
import json
import requests
import nltk
from sutime import SUTime
import sqlite3
from tqdm import tqdm
import signal


# class TimeoutError(Exception):
#     pass

# def timeout(seconds=100, error_message=os.strerror(errno.ETIME)):
#     def decorator(func):
#         def _handle_timeout(signum, frame):
#             raise TimeoutError(error_message)

#         def wrapper(*args, **kwargs):
#             signal.signal(signal.SIGALRM, _handle_timeout)
#             signal.alarm(seconds)
#             try:
#                 result = func(*args, **kwargs)
#             finally:
#                 signal.alarm(0)
#             return result

#         return wraps(func)(wrapper)

#     return decorator

class extraction:
    def __init__(self):
        nltk.download('punkt') 
        
# function to extract time expressions from a text using SUTime
    def extract_time(self, sentence):
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

    
    # open the book file and extract its text

    def continue_or_new_addition(self):
        conn = sqlite3.connect('D:\\BookClockData\\timex.db')
        c = conn.cursor()

        c.execute(f"PRAGMA table_info(timex)")
        columns = [column[1] for column in c.fetchall()]

        # Generate the query to delete duplicate rows
        sql_query = f'''
            DELETE FROM timex 
            WHERE ROWID NOT IN (
                SELECT MIN(ROWID)
                FROM timex
                GROUP BY "{'", "'.join(columns)}"
            )
        '''
        c.execute(sql_query)
        conn.commit()

        if len(c.execute("SELECT * FROM timex").fetchall()) != 0:
            sql_query = c.execute(f"SELECT book FROM timex")
            last_book = sql_query.fetchall()[-1][0]
            #for all books that come after the last book, last sentence
            list_of_books = list(os.listdir('D:\\BookClockData\\'))
            for i, book in enumerate(list_of_books):
                if book.split("&")[0] == last_book and book.endswith('.txt'):
                    list_of_books = list_of_books[i:]
            for filename in list_of_books:
                self.insert_data(filename, conn, c)
        else:
            for filename in tqdm(os.listdir('D:\\BookClockData\\')):
                self.insert_data(filename, conn, c)
        
        conn.close()

    def insert_data(self, filename, conn, c):
        print(filename)
        if filename.endswith(".txt"):
            # open file and process its contents
            book = filename.split("&")[0]
            author = filename.split("&")[1].replace(".txt", "")
            with open(os.path.join('D:\\BookClockData\\', filename), "r") as f:
                book_text = f.read()
                sentences = nltk.sent_tokenize(book_text)
                # iterate over the sentences and extract time expressions
                for sentence in sentences:
                    input_data = self.extract_time(sentence)
                    if input_data[1] != []:
                        sentence = input_data[0]
                        timex_data = input_data[1]
                        for timex in timex_data:
                            text = timex['text']
                            timex_value = timex['timex-value']
                            typ = timex['type']
                            value = timex['value']
                            c.execute("INSERT INTO timex (book, author, sentence, text, 'timex-value', typ, value) VALUES (?, ? ,?, ?, ?, ?, ?)",
                                    (book, author, sentence, text, timex_value, typ, value))
                    conn.commit()

e = extraction()  
e.continue_or_new_addition()