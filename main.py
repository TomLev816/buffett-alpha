from yahooquery import Ticker
import stock_class
import all_stocks_class
import pandas as pd

def get_ticker_symbols():
    df = pd.read_excel('master_list.xlsx', engine='openpyxl')
    ticker_list = df['Symbol'].to_list()

    # ticker_list = ['goog', 'aapl', 'txn', 'msft', 'rick', 'cp', 'mco', 'uri', 'dhr']
    return ticker_list

def run_script():
    ticker_list = get_ticker_symbols()
    all_data = all_stocks_class.AllStocksClass(ticker_list)
    all_data.get_stock_data()
    all_data.calculate_all_factors()
    all_data.print_z_scores()
    import pdb; pdb.set_trace()


run_script()