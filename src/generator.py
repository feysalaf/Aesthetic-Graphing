import time
import random
import json

data = []
def generateJson():

    d = random.randint(0,100)
    data.append({"Price":d,"Var":2*d})
    print(data[-1])
    with open('jsonPriceData', 'w') as fout:
        json.dump(data, fout)


for i in range(500):
    generateJson()
    time.sleep(1)
