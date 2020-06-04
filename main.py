import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import datetime
from src import GetRate as gt
from time import sleep
from matplotlib.animation import FuncAnimation

rate_vals = []
date_vals = []

def AnimateLatest(i,key):
    """For animating rate for real time.

    Arguments:
        i {[integer]} -- [number of calls?, it counts how many times it is called]
        key {[string]} -- [Key for ExchangeRate currency, EUR to KEY]
    """
    print(type(i))
    print(i)
    latest = gt.GetLatestRate(key)
    now = datetime.datetime.now().replace(microsecond=0)    #time without micro second
    latestval = latest['rates'][key]
    rate_vals.append(latestval)
    date_vals.append(now)
    plt.cla()
    plt.plot_date(date_vals, rate_vals, marker="o", linestyle="-")
    for x,y in zip(date_vals,rate_vals):
        label = "{rate}".format(rate=y)
        plt.annotate(label,(x,y))



def StrToDateTime(array):
    """Changes datetime objects to string objects, so we can use them at our matplotlib plots.

    Arguments:
        array {[Array]} -- [List of dates.]

    Returns:
        [Array] -- [Returns a string array.]
    """
    date_array = []
    for i in array:
        date = datetime.datetime.strptime(i['date'], "%Y-%m-%d")
        date_array.append(date)
    return date_array

def GetValuesFromList(array, key):
    """[Gets values from dictionary and returns them as a list, to use at plot.]

    Arguments:
        array {[dict]} -- [Dict we get from ]
        key {[string]} -- [Key for ExchangeRate currency, EUR to KEY]

    Returns:
        [array] -- [Array of values to show on plot.]
    """
    vals = []
    for i in array:
        vals.append(i['rates'][key])
    return vals


def run():
    
    key = 'USD'
    plt.tight_layout()
    pltm  = plt.figure(1)
    ax = pltm.add_subplot(111)
    ax.set_title('EUR/USD Exchange Rate')
    ax.set_xlabel('Date')
    ax.set_ylabel('Exchange Rate')
    monthly = gt.GetMonthlyRate(key)
    values = GetValuesFromList(monthly,key)
    dates  = StrToDateTime(monthly)
    plt.plot_date(dates,values, linestyle="-", marker="o", label="EUR/USD")
    plt.legend(loc="upper left")
    for x,y in zip(dates,values):
        label = "{:.2f}".format(y)
        plt.annotate(label,(x,y))
    pltm.show()
    # bu kısımda aylık kısmı çıkarmış oluyoruz 
    # güncel kısma geçiş

    pltl = plt.figure(2)
    ax2 = pltl.add_subplot(111)
    ax2.set_title('EUR/USD Exchange Rate')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Exchange Rate')
    #şuan kullandığım figür üzerinden animatelatest fonksiyonunu 2000 ms interval ile güncelliyorum
    anim = FuncAnimation(plt.gcf(), AnimateLatest, interval=2000, fargs=(key,))
    
    pltl.show() 
    plt.show()
        
            
  
    

if __name__ == "__main__":
    run()