import math
import numpy as np


class StockClass:
    def __init__(self, symbol, stock):
        self.ticker = symbol
        self.stock_info = stock
        self.prices = stock.history(period='1y', interval='1d', start=None, end=None) 
        self.risk_free_rate = .0296
        self.income_statement_cy = ''
        self.income_statement_1y = ''
        self.income_statement_2y = ''
        self.income_statement_3y = ''
        self.cash_flow_cy = ''
        self.cash_flow_1y = ''
        self.cash_flow_2y = ''
        self.cash_flow_3y = ''
        self.balance_sheet_cy = ''
        self.balance_sheet_1y = ''
        self.balance_sheet_2y = ''
        self.balance_sheet_3y = ''

    def get_financial_data(self):
        self.get_income_statment_data()
        self.get_cash_flow_data()
        self.get_balance_sheet_data()
        self.get_profile_data()
        self.check_data()

    def check_data(self):
        if self.TotalAssets_cy == 0:
            pass

    def get_profile_data(self):
        summary_detail = self.stock_info.summary_detail[self.ticker]
        key_stats = self.stock_info.key_stats[self.ticker]
        asset_profile = self.stock_info.asset_profile[self.ticker]

        data_list = [[summary_detail, 'beta'],[key_stats, 'sharesOutstanding'],[asset_profile, 'industry'],[asset_profile, 'sector']]
        for pair in data_list:
            if pair[1] in pair[0]:
                financial_data = pair[0][pair[1]]
            else:
                financial_data = 0
                print('No ' + pair[1] + ' for ' + self.ticker)
            setattr(self, pair[1], financial_data)

    def get_data_point(self,statement, data_point, year):
        if data_point in statement:
            financial_data = statement[data_point]
            if not isinstance(financial_data, str) and math.isnan(financial_data): 
                financial_data = 0
        else: 
            if data_point == 'CostOfRevenue' and 'InterestExpense' in statement:
                financial_data = statement['InterestExpense']
            else:
                print('No ' + data_point + ' for ' + self.ticker)
                financial_data = 0
        text = data_point + '_' + year
        setattr(self, text, financial_data)
        
    def loop_data_points(self, statememt, data_points, year):
        for data_point in data_points:
            self.get_data_point(statememt, data_point, year)
        

    def get_income_statment_data(self):
        income_statement = self.stock_info.income_statement('a')
        self.income_statement_cy = income_statement.tail(1).iloc[0]
        income_statement = self.stock_info.income_statement('a', False)
        self.income_statement_1y = income_statement.iloc[2]
        self.income_statement_2y = income_statement.iloc[1]
        self.income_statement_3y = income_statement.iloc[0]
        data_points = ['TotalRevenue', 'CostOfRevenue', 'NetIncome', 'TaxProvision', 'BasicAverageShares', 'OperatingExpense']
        self.loop_data_points(self.income_statement_cy, data_points, 'cy')
        self.loop_data_points(self.income_statement_1y, data_points, '1y')
        self.loop_data_points(self.income_statement_2y, data_points, '2y')
        self.loop_data_points(self.income_statement_3y, data_points, '3y')

    def get_cash_flow_data(self):
        cash_flow_statement = self.stock_info.cash_flow('a')
        self.cash_flow_cy = cash_flow_statement.tail(1).iloc[0]
        cash_flow_statement = self.stock_info.cash_flow('a', False)
        self.cash_flow_3y = cash_flow_statement.iloc[0]
        self.cash_flow_2y = cash_flow_statement.iloc[1]
        self.cash_flow_1y = cash_flow_statement.iloc[2]

        data_points = ['Depreciation', 'CapitalExpenditure']
        self.loop_data_points(self.cash_flow_cy, data_points, 'cy')
        self.loop_data_points(self.cash_flow_3y, data_points, '3y')
    
    def get_balance_sheet_data(self):
        balance_sheet = self.stock_info.balance_sheet('q')
        self.balance_sheet_cy = balance_sheet.tail(1).iloc[0]
        balance_sheet = self.stock_info.balance_sheet('a')
        self.balance_sheet_1y = balance_sheet.iloc[2]
        self.balance_sheet_2y = balance_sheet.iloc[1]
        self.balance_sheet_3y = balance_sheet.iloc[0]

        data_points = ['CommonStockEquity','TotalAssets','CurrentAssets','CashAndCashEquivalents','CurrentLiabilities','CurrentDebtAndCapitalLeaseObligation', 'LongTermDebt', 'TotalEquityGrossMinorityInterest']
        self.loop_data_points(self.balance_sheet_cy, data_points, 'cy')
        self.loop_data_points(self.balance_sheet_1y, data_points, '1y')
        self.loop_data_points(self.balance_sheet_2y, data_points, '2y')
        self.loop_data_points(self.balance_sheet_3y, data_points, '3y')
        


    def det_profitability(self):
        working_capital = round(self.CurrentAssets_cy - self.CashAndCashEquivalents_cy -  self.CurrentLiabilities_cy + self.CurrentDebtAndCapitalLeaseObligation_cy   + self.TaxProvision_cy, 4)
        working_capital_2y = round(self.CurrentAssets_2y - self.CashAndCashEquivalents_2y - self.CurrentLiabilities_2y + self.CurrentDebtAndCapitalLeaseObligation_2y + self.TaxProvision_2y, 4)
        change_working_capital = working_capital - working_capital_2y
        self.gp_over_assets = round((self.TotalRevenue_cy - self.CostOfRevenue_cy) / self.TotalAssets_cy, 4)
        self.roe = round(self.NetIncome_cy / self.CommonStockEquity_cy, 4)
        self.roa = round(self.NetIncome_cy / self.TotalAssets_cy, 4)
        self.cfoa = round((self.NetIncome_cy + self.Depreciation_cy - change_working_capital - self.CapitalExpenditure_cy) / self.TotalAssets_cy, 4)
        self.low_acc = round((self.Depreciation_cy - change_working_capital) / self.TotalAssets_cy, 4)
        self.gross_margin = round((self.TotalRevenue_cy - self.CostOfRevenue_cy) / (self.TotalRevenue_cy), 4)
        # self.profitability = round((self.gp_over_assets + self.roe + self.roa + self.gross_margin + self.low_acc + self.cfoa) / 6, 4)
        # print('gp_over_assets- ' + str(self.gp_over_assets))
        # print('roe- ' + str(self.roe))
        # print('roa- ' + str(self.roa))
        # print('gross_margin- ' + str(self.gross_margin))
        # print('low_acc- ' + str(self.low_acc))
        # print('CFoA- ' + str(self.cfoa))
        # print('profitability - ' + str(self.profitability))

    def det_growth(self):
        gross_profit_cy = (self.TotalRevenue_cy - self.CostOfRevenue_cy)            
        gross_profit_3y = (self.TotalRevenue_3y - self.CostOfRevenue_3y)
        working_capital = round(self.CurrentAssets_cy - self.CashAndCashEquivalents_cy -  self.CurrentLiabilities_cy + self.CurrentDebtAndCapitalLeaseObligation_cy   + self.TaxProvision_cy, 4)
        working_capital_2y = self.CurrentAssets_2y - self.CashAndCashEquivalents_2y - self.CurrentLiabilities_2y + self.CurrentDebtAndCapitalLeaseObligation_2y + self.TaxProvision_2y
        working_capital_3y = self.CurrentAssets_3y - self.CashAndCashEquivalents_3y - self.CurrentLiabilities_3y + self.CurrentDebtAndCapitalLeaseObligation_3y + self.TaxProvision_3y
        change_working_capital_cy = working_capital - working_capital_2y
        change_working_capital_3y = working_capital_2y - working_capital_3y
        cash_flow = self.NetIncome_cy + self.Depreciation_cy - change_working_capital_cy - self.CapitalExpenditure_cy
        cash_flow_3y = self.NetIncome_3y + self.Depreciation_3y - change_working_capital_3y - self.CapitalExpenditure_3y

        self.growth_gp_over_assets = round((gross_profit_cy - gross_profit_3y) / self.TotalAssets_3y, 4)
        self.growth_roe = round(((self.NetIncome_cy / self.CommonStockEquity_cy) - (self.NetIncome_3y / self.CommonStockEquity_3y)) / (self.NetIncome_3y / self.CommonStockEquity_3y), 4)
        self.growth_roa = round(((self.NetIncome_cy / self.TotalAssets_1y) - (self.NetIncome_3y / self.TotalAssets_3y)) / (self.NetIncome_3y / self.TotalAssets_3y), 4)
        self.growth_cfoa = round(((cash_flow / self.TotalAssets_1y) - (cash_flow_3y / self.TotalAssets_3y)) / (cash_flow_3y / self.TotalAssets_3y), 4)
        self.growth_gross_margin = round((((self.TotalRevenue_cy - self.CostOfRevenue_cy) / self.TotalRevenue_cy) - ((self.TotalRevenue_3y - self.CostOfRevenue_3y) / self.TotalRevenue_3y)) / ((self.TotalRevenue_3y - self.CostOfRevenue_3y) / self.TotalRevenue_3y), 4)

        # print('Growth for ' + self.ticker)
        # print('growth_gp_over_assets: ' + str(self.growth_gp_over_assets))
        # print('growth_roe: ' + str(self.growth_roe))
        # print('growth_roa: ' + str(self.growth_roa))
        # print('growth_cfoa: ' + str(self.growth_cfoa))
        # print('growth_gross_margin: ' + str(self.growth_gross_margin))


    def det_payout(self):
        self.net_equity_issuance = 1 - round(self.BasicAverageShares_1y / self.BasicAverageShares_2y,4)
        self.net_payout_over_profits = round((self.NetIncome_cy - (self.TotalEquityGrossMinorityInterest_cy - self.TotalEquityGrossMinorityInterest_3y)) / ((self.TotalRevenue_cy - self.CostOfRevenue_cy)),4)
        if self.CurrentDebtAndCapitalLeaseObligation_1y + self.LongTermDebt_1y > 0:
            self.net_debt_issuance = 1 - round((self.CurrentDebtAndCapitalLeaseObligation_cy + self.LongTermDebt_cy)/ (self.CurrentDebtAndCapitalLeaseObligation_1y + self.LongTermDebt_1y),4)
        else:
            self.net_debt_issuance = 1

        # print('Payout for ' + self.ticker)
        # print('net_equity_issuance: ' + str(self.net_equity_issuance))
        # print('net_debt_issuance: ' + str(self.net_debt_issuance))
        # print('net_payout_over_profits: ' + str(self.net_payout_over_profits))

    def det_safty(self): 
        roe_cy = round(self.NetIncome_cy / self.CommonStockEquity_cy, 4)
        roe_1y = round(self.NetIncome_1y / self.CommonStockEquity_1y, 4)
        roe_2y = round(self.NetIncome_2y / self.CommonStockEquity_2y, 4)
        roe_3y = round(self.NetIncome_3y / self.CommonStockEquity_3y, 4)
        years = [roe_cy, roe_1y ,roe_2y, roe_3y]
        working_capital = round(self.CurrentAssets_cy - self.CashAndCashEquivalents_cy -  self.CurrentLiabilities_cy + self.CurrentDebtAndCapitalLeaseObligation_cy   + self.TaxProvision_cy, 4)
        ebit = self.TotalRevenue_cy - self.CostOfRevenue_cy - self.OperatingExpense_cy
        self.roe_std_3y = 1 - round(np.std(years), 4)
        self.leverage = 1 - (round((self.LongTermDebt_cy + self.CurrentDebtAndCapitalLeaseObligation_cy) / self.TotalAssets_cy, 4))
        self.one_minus_beta = round(1 - self.beta, 4)
        self.altmans_z = round(((1.2 * working_capital) + (1.4 * (self.NetIncome_cy - self.NetIncome_1y) ) + (3.3 * ebit) + (.6 * self.TotalEquityGrossMinorityInterest_cy) + (self.TotalRevenue_cy)) / self.TotalAssets_cy, 4)
        # print('Safty for ' + self.ticker)
        # print('self.roe_std_3y: ' + str(self.self.roe_std_3y))
        # print('self.leverage: ' + str(self.self.leverage))
        # print('self.one_minus_beta: ' + str(self.self.one_minus_beta))
        return 

    def calculate_factor_totals(self):
        profitability = ['gp_over_assets','roe','roa','cfoa','low_acc','gross_margin']
        growth = ['growth_gp_over_assets','growth_roe','growth_roa','growth_cfoa','growth_gross_margin']
        payout = ['net_equity_issuance','net_debt_issuance','net_payout_over_profits']
        safty = ['leverage','one_minus_beta','roe_std_3y', 'altmans_z']
        factors = [['profitability', profitability], ['growth', growth], ['payout', payout], ['safty', safty]]
        for factor_obj in factors:
            factor_category = factor_obj[0]
            factor_array = factor_obj[1]
            factor_category_sum = 0
            factor_category_count = 0
            for factor in factor_array:
                factor_category_count = factor_category_count + 1
                factor_name = factor + '_z_score'
                factor_value = getattr(self, factor_name)
                factor_category_sum = factor_category_sum + factor_value
            factor_score_text = factor_category + '_score'
            setattr(self, factor_score_text, factor_category_sum)



    def calculate_factors(self):
        self.det_profitability()
        self.det_growth()
        self.det_payout()
        self.det_safty()


