import requests
import json
import datetime
from tkinter import *
import time
import re
url = "https://api.wazirx.com/api/v2/tickers"
def get_tickers(coin):
    response = requests.get(url)
    data = response.text
    market = json.loads(data)
    ticker = []
    first = market[coin]['last']
    ticker.append(first)
    second = market['usdtinr']['low']
    ticker.append(second)
    return ticker

def setup_gui(coin, window, vals, change):
    window.wm_title("WRX/USDT")
    date_time = datetime.datetime.now().strftime("%A %d %B %Y at %H:%M:%S")
    str_date_time = "On " + str(date_time)

    if(re.search("inr", coin)):
        coin_name = coin[:-3].upper()
        l1 = Label(window, text="Current Value of "+coin_name)
        l1.grid(row = 1, column = 0)

        l2 = Label(window, text=str_date_time)
        l2.grid(row=0, column=0)

        #l3 = Label(window, text="USDT: "+'%0.5f'%vals[0])
        #l3.grid(row=2, column=0)

        l4 = Label(window, text="INR: "+'%0.5f'%vals[1])
        l4.grid(row=2, column=0)

        l5 = Label(window, text="You own: " + str(vals[2]) + " volumes of " + coin_name)
        l5.grid(row=3, column=0)

        if change[1] == "red":
            l6 = Label(window, text="Your Portfolio lost Rs. " + '%0.4f'%float(change[0]), fg="red")
        elif change[1] == "green":
            l6 = Label(window, text="Your Portfolio gained Rs. " + '%0.4f'%float(change[0]), fg="green")
        else:
            l6 = Label(window, text="Your Portfolio is stable", fg="blue")
        l6.grid(row=4, column=0)

        l7 = Label(window, text="Total Portfolio Value: "+'%0.4f'%vals[3])
        l7.grid(row=5, column=0)
       
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        
        xpos = screen_width - 1540
        ypos = screen_height - 225
        window.geometry("202x140+" + str(xpos) + "+" + str(ypos))
        
        return window


    else:
        coin_name = coin[:-4].upper()
        l1 = Label(window, text="Current Value of "+coin_name)
        l1.grid(row = 1, column = 0)

        l2 = Label(window, text=str_date_time)
        l2.grid(row=0, column=0)

        l3 = Label(window, text="USDT: "+'%0.5f'%vals[0])
        l3.grid(row=2, column=0)

        l4 = Label(window, text="INR: "+'%0.5f'%vals[1])
        l4.grid(row=3, column=0)

        l5 = Label(window, text="You own: " + str(vals[2]) + " volumes of " + coin_name)
        l5.grid(row=4, column=0)

        if change[1] == "red":
            l6 = Label(window, text="Your Portfolio lost Rs. " + '%0.4f'%float(change[0]), fg="red")
        elif change[1] == "green":
            l6 = Label(window, text="Your Portfolio gained Rs. " + '%0.4f'%float(change[0]), fg="green")
        else:
            l6 = Label(window, text="Your Portfolio is stable", fg="blue")
        l6.grid(row=5, column=0)

        l7 = Label(window, text="Total Portfolio Value: "+'%0.4f'%vals[3])
        l7.grid(row=6, column=0)

        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        
        xpos = screen_width - 1540
        ypos = screen_height - 225
        window.geometry("202x150+" + str(xpos) + "+" + str(ypos))
        
        return window

def computeData(coin, volume):
    if(re.search("inr", coin)):
        tkrs = get_tickers(coin)
        inr = float(tkrs[0])
        vol = volume;
        portfolio_val = float(inr*vol)
        return [0, inr, vol, portfolio_val]
    else:
        tkrs = get_tickers(coin)
        usdt = float(tkrs[0])
        inr = float(tkrs[0]) * float(tkrs[1])
        vol = volume;
        portfolio_val = float(inr*vol)
              
        return [usdt, inr, vol, portfolio_val]

def analyse(coin, volume):
    window = Tk()
    values = computeData(coin, volume)
    last_pv = values[3]
    change = ["stable", 'blue']
    window = setup_gui(coin, window, values, change)
    window.update()
    time.sleep(5)
    window.destroy()
    while True:        
        values = computeData(coin, volume)
        if (values[3] >= last_pv + 0.01):
            window = Tk()
            change = [str(values[3] - last_pv), 'green']
            last_pv = values[3]
            window = setup_gui(coin, window, values, change)
            window.update()
            window.lift()
            window.attributes('-topmost', True)
            time.sleep(5)
            window.destroy()
            continue
        elif (values[3] <= last_pv - 0.01):
            window = Tk()
            change = [str(last_pv-values[3]), 'red']
            last_pv = values[3]
            window = setup_gui(coin, window, values, change)
            window.update()
            window.lift()
            window.attributes('-topmost', True)
            time.sleep(5)
            window.destroy()
            continue

def main():
    coin = 'xlminr'
    volume = 1377.9
    analyse(coin, float(volume))

if __name__ == '__main__':
    main()
