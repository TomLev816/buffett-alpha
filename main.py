from yahooquery import Ticker
import stock_class
import all_stocks_class
import pandas as pd

def get_ticker_symbols():
    df = pd.read_excel('master_list.xlsx', engine='openpyxl')
    ticker_list = df['Ticker'].to_list()

    # ticker_list = ['goog', 'aapl', 'txn', 'msft', 'rick', 'cp', 'mco', 'uri', 'dhr']
    return ticker_list

def create_stock_class(stock):
    print('Getting data for ' + stock['ticker'])
    stock_as_class = stock_class.StockClass(stock['ticker'], stock['ticker_data'])
    return stock_as_class

def get_stock_data(ticker_list, all_stocks):
    for ticker in ticker_list:
        data = {'ticker':ticker, 'ticker_data':Ticker(ticker)}
        stock_as_class = create_stock_class(data)
        all_stocks.add_stock_as_class(stock_as_class)
        # self.stocks_as_classes.append(stock_as_class)

def run_script():
    all_stocks = all_stocks_class.AllStocksClass()
    ticker_list = get_ticker_symbols()
    get_stock_data(ticker_list, all_stocks)
    all_stocks.calculate_all_factors()
    all_stocks.print_z_scores()
    all_stocks.print_to_excel()

    import pdb; pdb.set_trace()


run_script()