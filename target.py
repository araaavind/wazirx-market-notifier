import requests
import json
import datetime
from tkinter import *
import time
import re
import pprint
url = "https://api.wazirx.com/api/v2/tickers"
def get_tickers(coin):
    response = requests.get(url)
    data = response.text
    # pprint.pprint(data)
    market = json.loads(data)
    ticker = []
    first = market[coin]['last']
    ticker.append(first)
    second = market['usdtinr']['low']
    ticker.append(second)
    return ticker

def setup_gui(coin, window, vals, change):
    window.wm_title("Target Value Alert")
    date_time = datetime.datetime.now().strftime("%A %d %B %Y at %H:%M:%S")
    str_date_time = "On " + str(date_time)

    if(re.search("inr", coin)):
        coin_name = coin[:-3].upper()
        l1 = Label(window, text="Current Value of "+coin_name)
        l1.grid(row = 0, column = 0)

        l2 = Label(window, text=str_date_time)
        l2.grid(row=1, column=0)

        l4 = Label(window, text="INR: "+'%0.3f'%vals[1])
        l4.grid(row=2, column=0)

        if change[1] == "red":
            l6 = Label(window, text=change[0], fg="red")
        elif change[1] == "green":
            l6 = Label(window, text=change[0], fg="green")
        else:
            l6 = Label(window, text=coin_name+" is stable.", fg="blue")
        l6.grid(row=3, column=0)
       
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        
        xpos = screen_width - 1540
        ypos = screen_height - 225
        window.geometry("204x120+" + str(xpos) + "+" + str(ypos))
        
        return window


    else:
        coin_name = coin[:-4].upper()
        l1 = Label(window, text="Current Value of "+coin_name)
        l1.grid(row = 0, column = 0)

        l2 = Label(window, text=str_date_time)
        l2.grid(row=1, column=0)

        l3 = Label(window, text="USDT: "+'%0.3f'%vals[0])
        l3.grid(row=2, column=0)

        l4 = Label(window, text="INR: "+'%0.3f'%vals[1])
        l4.grid(row=3, column=0)

        if change[1] == "red":
            l6 = Label(window, text=change[0], fg="red")
        elif change[1] == "green":
            l6 = Label(window, text=change[0], fg="green")
        else:
            l6 = Label(window, text=coin_name+" is stable.", fg="blue")
        l6.grid(row=4, column=0)

        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        
        xpos = screen_width - 1540
        ypos = screen_height - 225
        window.geometry("204x120+" + str(xpos) + "+" + str(ypos))
        
        return window

def computeData(coin):
    if(re.search("inr", coin)):
        tkrs = get_tickers(coin)
        inr = float(tkrs[0])
        return [0, inr]
    else:
        tkrs = get_tickers(coin)
        usdt = float(tkrs[0])
        inr = float(tkrs[0]) * float(tkrs[1])
        return [usdt, inr]

def analyse(coin, target):
    window = Tk()
    values = computeData(coin)
    change = ["stable", 'blue']
    window = setup_gui(coin, window, values, change)
    window.update()
    time.sleep(5)
    window.destroy()
    flag = 1
    while True:        
        values = computeData(coin)
        if (values[1] >= target and flag == 1):
            flag = 0
            window = Tk()
            change = ["The value has gone above "+str(target), 'green']
            window = setup_gui(coin, window, values, change)
            window.update()
            window.lift()
            window.attributes('-topmost', True)
            time.sleep(5)
            window.destroy()
            continue
        elif (values[1] <= target and flag == 0):
            flag = 1
            window = Tk()
            change = ["The value has gone below "+str(target), 'red']
            window = setup_gui(coin, window, values, change)
            window.update()
            window.lift()
            window.attributes('-topmost', True)
            time.sleep(5)
            window.destroy()
            continue

def main():
    coin = 'xlminr'
    target = 27.5
    analyse(coin, target)

if __name__ == '__main__':
    main()
