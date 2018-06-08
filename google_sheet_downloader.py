import requests
import time
import datetime
import csv

starttime=time.time()
YOUR_FILE_ID="1o6pGvAsk7PrSKXd6TN3J0SBwRLpVVmIPwXR9T5t2S-o"
#https://drive.google.com/open?id=1o6pGvAsk7PrSKXd6TN3J0SBwRLpVVmIPwXR9T5t2S-o
DELAY= 3 #3600
def start():
    print('started')

    response = requests.get('https://docs.google.com/spreadsheet/ccc?key='+YOUR_FILE_ID+'&output=csv')
    name_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    with open(name_time+'.csv', 'wb') as f:
        f.write(response.content)

    #response = requests.get('https://docs.google.com/spreadsheet/ccc?key='+YOUR_FILE_ID+'&output=tsv')
    #name_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    #with open(name_time+'.tsv', 'wb') as f:
    #    f.write(response.content)

    response = requests.get('https://docs.google.com/spreadsheet/ccc?key='+YOUR_FILE_ID+'&output=xlsx')
    name_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    with open(name_time+'.xlsx', 'wb') as f:
        f.write(response.content)

    print('downloaded')


def get_sheet():
    response = requests.get('https://docs.google.com/spreadsheet/ccc?key=' + YOUR_FILE_ID + '&output=csv')
    name_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    lines = [line.split(',') for line in response.text.split('\r\n')]
    keys = lines[0]
    data = []
    for l in range(1, len(lines)):
        trx = dict()
        for elem in range(len(lines[l])):
            trx[keys[elem]] = lines[l][elem]
        data.append(trx)
    # for i in data:
    #     print(i)
    return data



if __name__=="__main__":
    # start()
    # time.sleep(DELAY - ((time.time() - starttime) % DELAY))
    get_sheet()