import numpy as np
from yahooquery import Ticker
import stock_class

class AllStocksClass:
    def __init__(self, stock_list):
        self.ticker_list = stock_list
        self.stocks_as_classes = []
        self.all_stock_measures = ['gp_over_assets','roe','roa','cfoa','low_acc','gross_margin','growth_gp_over_assets','growth_roe','growth_roa','growth_cfoa','growth_gross_margin','net_equity_issuance','net_debt_issuance','net_payout_over_profits','leverage','one_minus_beta','roe_std_3y','altmans_z']
        self.all_factors = ['profitability_score','growth_score','payout_score','safty_score']
        self.z_score = ['z_score_sum']

        

    def calculate_all_factors(self):
        self.calculate_factors()
        self.calculate_scores(self.all_stock_measures)
        self.get_stock_factor_totals()
        self.calculate_scores(self.all_factors)
        self.calculate_total_z_scores()
        self.calculate_scores(self.z_score)

    def calculate_scores(self, factor_list):
        self.calculate_factor_mean_std(factor_list)
        self.calculate_z_scores(factor_list)

    def create_stock_class(self, stock):
        print('Getting data for ' + stock['ticker'])
        stock_as_class = stock_class.StockClass(stock['ticker'], stock['ticker_data'])
        stock_as_class.get_financial_data()
        return stock_as_class

    def get_stock_data(self):
        for ticker in self.ticker_list:
            data = {'ticker':ticker, 'ticker_data':Ticker(ticker)}
            stock_as_class = self.create_stock_class(data)
            self.stocks_as_classes.append(stock_as_class)
    
    def calculate_factors(self):
        for stock in self.stocks_as_classes:
            stock.calculate_factors()

    def calculate_factor_mean_std(self, factors):
        for factor in factors:
            factor_values = []
            for stock in self.stocks_as_classes:
                factor_values.append(getattr(stock, factor))
            mean = round(np.mean(factor_values), 4)
            std = round(np.std(factor_values), 4)
            factor_value = {'mean': mean, 'std': std}
            setattr(self, factor, factor_value)

    def calculate_z_scores(self, factors):
        for factor in factors:
            for stock in self.stocks_as_classes:
                factor_value = getattr(stock, factor)
                if factor_value == np.NaN:
                    print(stock.ticker + ' factor: ' + factor + ' is Nan')
                factor_mean_std = getattr(self, factor)
                stock_z_score = round((factor_value - factor_mean_std['mean']) / factor_mean_std['std'], 4)
                factor_name = factor + '_z_score'
                setattr(stock, factor_name, stock_z_score)

    def calculate_total_z_scores(self):
        for stock in self.stocks_as_classes:
            z_score_sum = 0
            for factor in self.all_factors:
                z_score_sum = z_score_sum + getattr(stock, factor)
            setattr(stock, 'z_score_sum', z_score_sum)

    def get_stock_factor_totals(self):
        for stock in self.stocks_as_classes:
            stock.calculate_factor_totals()

    def print_z_scores(self):
        factors = self.all_factors + self.z_score
        for factor in factors:
            print('Factor: ' + factor)
            for stock in self.stocks_as_classes:
                factor_name = factor + '_z_score'
                factor_value = getattr(stock, factor_name)
                print(stock.ticker + ': ' + str(round(factor_value, 4)))
