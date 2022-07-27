from yahooquery import Ticker
import stock_class
import all_stocks_class
import pandas as pd

def get_ticker_symbols():
    df = pd.read_excel('master_list.xlsx', engine='openpyxl')
    # import pdb;pdb.set_trace()

    # ticker_list = ['goog', 'aapl', 'txn', 'msft', 'rick', 'cp', 'mco', 'uri', 'dhr']
    ticker_list = df['Symbol'].to_list()
    return ticker_list

def get_stock_data(ticker_list):
    stock_data = []
    for ticker in ticker_list:
        data = {'ticker':ticker, 'ticker_data':Ticker(ticker)}
        stock_data.append(data)
    return stock_data

def create_stock_classes(all_stock_data):
    stock_class_data = []
    for stock in all_stock_data:
        print('Getting data for ' + stock['ticker'])
        stock_as_class = stock_class.StockClass(stock['ticker'], stock['ticker_data'])
        stock_as_class.get_financial_data()
        stock_class_data.append(stock_as_class)
    return stock_class_data

def calculate_factors(stock_data):
    for stock in stock_data:
        stock.calculate_factors()

def run_script():
    ticker_list = get_ticker_symbols()
    all_data = all_stocks_class.AllStocksClass(ticker_list)
    all_data.get_all_the_data()

run_script()