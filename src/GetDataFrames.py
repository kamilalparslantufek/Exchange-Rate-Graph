from RateOperations import GetRate as gr
import pandas as pd


def GetMonthlyRateDataFrame(key):
    """Returns dataframe from json.

    Arguments:
        key {[string]} -- [key for exchange rate EUR to Key value.]

    Returns:
        [DataFrame] -- [Returns dataframe object made from json.]
    """
    dd = pd.DataFrame.from_dict(gr.GetMonthlyRate(key))
    dd = dd[::-1]
    return dd


def GetLatestRateDataFrame(key):
    """same as above function"""
    dd = pd.DataFrame.from_dict(gr.GetLatestRate(key))
    return dd