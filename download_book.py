import os
from urllib import request
import re
from bs4 import BeautifulSoup
import requests 

def text_from_gutenberg(title, author, url):
    # Convert inputs to lowercase
    title = title.lower()
    author = author.lower()
   
    # Check if the file is stored locally
    
    directory = "D:\\BookClockData\\"
    title = title.replace(" ","_")
    title = re.sub(r'[^\w\s]', '', title)
    author = author.replace(" ","_")
    author = re.sub(r'[^\w\s]', '', author)
    bookname = title + "&" + author
    filename = directory + bookname + ".txt"
    print(filename)
    if os.path.isfile(filename) and os.stat(filename).st_size != 0:
            print("{title} file already exists".format(title=title))

    else:
        print("{title} file does not already exist. Grabbing from Project Gutenberg".format(title=title))
        response = request.urlopen(url)
        raw = response.read().decode('utf-8-sig')
        print("Saving {title} file".format(title=title))
        with open(filename, 'w') as outfile:
            outfile.write(find_beginning_and_end(title, author, raw))  
                

def find_beginning_and_end(title, author, raw):
    '''
    This function serves to find the text within the raw data provided by Project Gutenberg
    '''
    
    start_regex = '\*\*\*\s?START OF TH(IS|E) PROJECT GUTENBERG EBOOK.*\*\*\*'
    draft_start_position = re.search(start_regex, raw)
    begining = draft_start_position.end()

    if re.search(title.lower(), raw[draft_start_position.end():].lower()):
        title_position = re.search(title.lower(), raw[draft_start_position.end():].lower())
        begining += title_position.end()
        # If the title is present, check for the author's name as well
        if re.search(author.lower(), raw[draft_start_position.end() + title_position.end():].lower()):
            author_position = re.search(author.lower(), raw[draft_start_position.end() + title_position.end():].lower())
            begining += author_position.end()
    
    end_regex = 'end of th(is|e) project gutenberg ebook'
    end_position = re.search(end_regex, raw.lower())

    text = raw[begining:end_position.start()]
    
    return text

def get_title_and_author(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    bibrec_table = soup.find('table', {'class': 'bibrec'})
    try:
        title = soup.find('td', {'itemprop': 'headline'}).text.strip()
    except:
        title  = "No title"
    try:
        author = soup.find('a', {'itemprop': 'creator'}).text.strip()
    except:
        author  = "No author"
    
    return title, author

def loop():
    for i in range(30341):
        url = f"https://www.gutenberg.org/ebooks/{i+40001}"
        title, author = get_title_and_author(url)
        if title == "No title":
            continue
        url = f'http://www.gutenberg.org/cache/epub/{i+40001}/pg{i+40001}.txt'
        try:
            text_from_gutenberg(title, author, url)
        except:
            pass
loop()