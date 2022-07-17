import time
from datetime import datetime
import json
import random

class ClcokRun:
    def __init__(self, timeData):
        self.timeData = timeData

    def runMain(self):
        curr = ""
        while True:
            now = datetime.now()
            while curr != now.minute:
                if now.minute < 10:
                    nowString = str(now.hour) + ":0" + str(now.minute)
                else:
                    nowString = str(now.hour) + ":" + str(now.minute)

                if nowString in self.timeData.keys():
                    selectInt = random.randint(0, len(self.timeData[nowString]))
                    print(self.timeData[nowString][selectInt])
                else:
                    print(nowString)
                curr = now.minute
                time.sleep(1)


if __name__ == "__main__":
    with open('testJson.json') as json_data:
        time_data = json.load(json_data)
    CR = ClcokRun(time_data)
    CR.runMain()
