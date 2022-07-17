import time
from datetime import datetime
import json
import random
import sqlite3
from ReadJSON import load_json
from Mrk2 import genTimeSent


class ClockRun:
    def __init__(self, timeData, mrkvSent):
        self.timeData = timeData
        self.mrkvSent = mrkvSent

    def renewMrk(self):
        self.mrkvSent = genTimeSent(50)

    def runMain(self):
        curr = ""
        while True:
            now = datetime.now()
            if now == "0:0":
                self.renewMrk()
            while curr != now.minute:
                if now.minute < 10:
                    nowString = str(now.hour) + ":0" + str(now.minute)
                else:
                    nowString = str(now.hour) + ":" + str(now.minute)

                if nowString in self.timeData.keys():
                    print(nowString)
                    print("true")
                    selectInt = random.randint(0, len(self.timeData[nowString]))
                    print(self.timeData[nowString][selectInt])
                else:
                    print(nowString)
                    self.randCallSent(nowString)
                curr = now.minute
                time.sleep(1)

    def randCallSent(self,indvNeedTime):

        randInt = random.randint(0,len(self.mrkvSent)-1)
        replacedTime  = self.mrkvSent[0][randInt].replace(self.mrkvSent[1][randInt],indvNeedTime)
        print(replacedTime)


if __name__ == "__main__":
    mrkvSent = load_json('markv.json')

    con = sqlite3.connect("time_database")
    cur = con.cursor()
    time_data = {}
    for row in cur.execute('SELECT * FROM time_database;'):
        if row[0] in time_data.keys():
            time_data[row[0]].append(row[1:])
        else:
            time_data[row[0]] = [row[1:]]


    CR = ClockRun(time_data,mrkvSent)
    CR.runMain()

