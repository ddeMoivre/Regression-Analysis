#   * Collect historical financial data from internet
#   * Create time series data matrix: Data
#         Closing prices on stocks (BAC, GE, JDSU, XOM)
#         Closing values of indexes (SP500)
#         Yields on constant maturity US rates/bonds (3MO, 1YR, 5YR, 10 YR)
#         Closing price on crude oil spot price

import pandas as pd
import pandas_datareader.data as web
import datetime

#   Stock Price Data from Yahoo
#      Apply pandas_datareader.data  function
#         web.DataReader
#
#          Returns historical data for any symbol at the website
#          http://finance.yahoo.com
#
#     Set start and end date for collection in YYYYMMDD (numeric) format
start = datetime.datetime(2011,10,15)
end = datetime.datetime(2021,10,15)

# Collect historical data for S&P 500 Index
SP500 = web.DataReader("^GSPC", 'yahoo', start, end)

#Collect historical data for 3 stocks
GE = web.DataReader("GE", 'yahoo', start, end)
BAC = web.DataReader("BAC", 'yahoo', start, end)
XOM = web.DataReader("XOM", 'yahoo', start, end)

# Each stock has four colomns: High, Low, Open, Close, Volume  and Adj Close

# Federal Reserve Economic Data (FRED) from the St. Louis Federal Reserve

# Series name | Description
#
# DGS3MO      | 3-Month Treasury, constant maturity rate
# DGS1        | 1-Year Treasury, constant maturity rate
# DGS5        | 5-Year Treasury, constant maturity rate
# DGS10       | 10-Year Treasury, constant maturity rate
#
# DAAA        | Moody's Seasoned Aaa Corporate Bond Yield
# DBAA        | Moody's Seasoned Baa Corporate Bond Yield
#
# DCOILWTICO  | Crude Oil Prices: West Text Intermediate (WTI) - Cushing, Oklahoma

DGS3MO = web.DataReader("DGS3MO",'fred', start, end)
DGS1 = web.DataReader("DGS1",'fred', start, end)
DGS5 = web.DataReader("DGS5",'fred', start, end)
DGS10 = web.DataReader("DGS10",'fred', start, end)
DAAA = web.DataReader("DAAA",'fred', start, end)
DBAA = web.DataReader("DBAA",'fred', start, end)
DCOILWTICO = web.DataReader("DCOILWTICO",'fred', start, end)

# Each object is a 1-column matrix with time series data
# The column-name is the same as the object name

#   Merge data series together
# Create data frame with all FRED series from 2011/10/15 on

fred = pd.concat([DGS3MO, DGS1, DGS5, DGS10, DAAA,
                    DBAA, DCOILWTICO], axis=1)

# Merge the closing prices for the stock market data series
yahoo = pd.concat([SP500['Close'], GE['Close'], BAC['Close'], XOM['Close']], axis=1)
yahoo.columns = ["SP500", "GE", "BAC", "XOM"]

# Merge the yahoo and Fred data together
data0 = pd.concat([yahoo, fred], axis=1)

# Subset out days when SP500 is not missing (not == NA)
data00 = data0[data0['SP500'].notnull()]

print(data00.isna().sum())

# Remaining missing values are for interest rates and the crude oil spot price
#   There are days when the stock market is open but the bond market and/or commodities market
#   is closed
# For the rates and commodity data, replace NAs with previoius non-NA values

data = data00.fillna(method='ffill')

print(data.isna().sum())

# Transform to data frame
data = pd.DataFrame(data)

data.to_csv('data.csv')
