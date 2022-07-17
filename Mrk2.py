import re
import random
import sqlite3
from sutime import SUTime
import json
import language_tool_python
import os
from ReadJSON import write_json


tempMapping = {}

mapping = {}

starts = []

def fixCaps(word):
    if word.isupper() and word != "I":
        word = word.lower()
    elif word [0].isupper():
        word = word.lower().capitalize()
    else:
        word = word.lower()
    return word

def toHashKey(lst):
    return tuple(lst)

def wordlist():
    con = sqlite3.connect("time_database")
    cur = con.cursor()

    wordlist = []
    for row in cur.execute('SELECT * FROM time_database;'):
        wl = [fixCaps(w) for w in re.findall(r"[\w']+|[.,!?;]", row[1])]
        wordlist += wl
    return wordlist


def addItemToTempMapping(history, word):
    global tempMapping
    while len(history) > 0:
        first = toHashKey(history)
        if first in tempMapping:
            if word in tempMapping[first]:
                tempMapping[first][word] += 1.0
            else:
                tempMapping[first][word] = 1.0
        else:
            tempMapping[first] = {}
            tempMapping[first][word] = 1.0
        history = history[1:]

def buildMapping(wordlist, markovLength):
    global tempMapping
    starts.append(wordlist [0])
    for i in range(1, len(wordlist) - 1):
        if i <= markovLength:
            history = wordlist[: i + 1]
        else:
            history = wordlist[i - markovLength + 1 : i + 1]
        follow = wordlist[i + 1]
        if history[-1] == "." and follow not in ".,!?;":
            starts.append(follow)
        addItemToTempMapping(history, follow)
    for first, followset in tempMapping.items():
        total = sum(followset.values())
        mapping[first] = dict([(k, v / total) for k, v in followset.items()])

def next(prevList):
    sum = 0.0
    retval = ""
    index = random.random()
    while toHashKey(prevList) not in mapping:
        prevList.pop(0)
    for k, v in mapping[toHashKey(prevList)].items():
        sum += v
        if sum >= index and retval == "":
            retval = k
    return retval

def genSentence(markovLength):
    curr = random.choice(starts)
    sent = curr.capitalize()
    prevList = [curr]
    while (curr not in "."):
        curr = next(prevList)
        prevList.append(curr)
        if len(prevList) > markovLength:
            prevList.pop(0)
        if (curr not in ".,!?;"):
            sent += " "
        sent += curr
    return sent


def genTimeSent(numOfSent):
    buildMapping(wordlist(), 2)
    sutime = SUTime(mark_time_ranges=False, include_range=False)
    tool = language_tool_python.LanguageToolPublicAPI('en-US')
    timeSent = []
    while len(timeSent) < numOfSent:
        sent = genSentence(2)
        if len(sent) < 30 or len(sent) > 400:
            continue
        parsed_sentence = sutime.parse(sent)
        if parsed_sentence:
            ps_each = parsed_sentence[0]
            if ps_each['type'] == 'TIME':
                time_value_raw = ps_each['timex-value'].split('T')[1]
                time_value = time_value_raw.split('-')[0]
                if not time_value.isalpha() and time_value != "XX:XX":
                    timeSent.append([tool.correct(tool.correct(sent)), ps_each['text']])
    return timeSent


if __name__ == "__main__":
    timeSent = genTimeSent(50)
    # write_json(timeSent, 'markv.json')

