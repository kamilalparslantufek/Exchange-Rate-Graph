import json
import requests
import sys
import time
from datetime import date,timedelta
import pandas as pd
import numpy as np
### BU KISIMDA DÖVİZ DEĞERİNİ GERİ DÖNDÜRÜYORUZ
def GetLatestRate(key):
    """Returns data for exchangerate

    Arguments:
        key {[string]} -- [Key for ExchangeRate currency, EUR to KEY]

    Returns:
        [type] -- [description]
    """
    url = CreateJsonForSingleLatest(key)
    response = requests.get(url)
    data = json.loads(response.text)                #PARSELAMAK İÇİN VAR
    value = data                     #PARSELAYARAK KEY'İN DEĞERİNİ ALIYORUZ
    print(type(value))
    return value                                    #TEK KUR DEĞERİ

#API BENİ KISITLADIĞI İÇİN 5 GÜNLÜK BİR KISIMDAN ALIYORUZ
#(5 günlük almamın sebeplerinden biri sadece 1000 get ile sınırlı olmam)
#AYLIK DEĞER DÖNÜYOR

def GetMonthlyRate(key):  
    """Gets values for each 5 day in last month, cause API limits us for only 1000 requests per day.
    

    Arguments:
        key {[String]} -- [Key for ExchangeRate currency, EUR to KEY.]

    Returns:
        [Array] -- [Returns an array of values for each 5 day in last month.]
    """
    date_base = date.today() - timedelta(days=1)
    date_array = np.array([date_base - timedelta(days=i*5) for i in range(6)])
    date_array = date_array[::-1]
    ##api sınırladırlamalı olduğu için bir döngünün içinde
    #bu array'in içindeki tarihlerin değerlerini alıp onu geri döndüreceğiz
    value_array = []
    for sdate in date_array:
        url = CreateJsonForMonthly(key, sdate)
        val = RequestForMonthly(url, key)
        value_array.append(val)
    return value_array

def RequestForMonthly(url, key):
    """[Makes a request to API with created URL.]

    Arguments:
        url {[string]} -- [url to make request from api.]
        key {[string]} -- [Key for ExchangeRate currency, EUR to KEY.]

    Returns:
        [dictionary] -- [returns response text dict of request.]
    """
    response = requests.get(url)
    data = json.loads(response.text)
    value = data
    return value
    
def CreateJsonForSingleLatest(symbol):
    """[Creates URL for request]

    Arguments:
        symbol {[string]} -- [Key for ExchangeRate currency, EUR to KEY.]

    Returns:
        [string] -- [URL]
    """
    #urlbase = "http://data.fixer.io/api/latest"
    apikey = open("token.txt", "r").read()
    #URL = urlbase + "?access_key=" + apikey + "&symbols=" + symbol
    url ="http://data.fixer.io/api/latest?access_key={apikey}&symbols={symbol}".format(apikey=apikey, symbol=symbol)
    return url

def CreateJsonForMonthly(symbol, sdate):
    """[Summary]
    Creates request URL for monthly ExchangeRate(only 6 day intervals cause we have limited requests per day.)
    Arguments:
        symbol {[string]} -- [Key for ExchangeRate currency, EUR to KEY]
        sdate {[datetime.date]} -- [dates for monthly]

    Returns:
        [string] -- [URL]
    """
    print(type(sdate))
    #URL = "http://data.fixer.io/api/"
    apikey = open("token.txt", "r").read()
    #URL = URL + str(sdate) + "?access_key=" + apikey + "&symbols=" + symbol
    url = "http://data.fixer.io/api/{date}?access_key={apikey}&symbols={symbol}".format(date=str(sdate), apikey=apikey,symbol=symbol)
    return url