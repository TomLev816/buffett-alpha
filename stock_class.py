import math
import numpy as np
import time

def zero_div_check(num, den, to_return=0):
    if den: return round(num / den, 4)
    else: return to_return

def check_nan(financial_data):
    if not isinstance(financial_data, str) and math.isnan(financial_data): 
        return 0
    return financial_data

class StockClass:
    def __init__(self, symbol, stock):
        self.ticker = symbol
        self.stock_info = stock
        self.prices = stock.history(period='1y', interval='1d', start=None, end=None)
        self.risk_free_rate = .0296

    def check_stock_history(self):
        if len(self.stock_info.history(period='5y', interval='3mo', start=None, end=None)) < 20:
            self.reason_not_included = 'Not long enough history'
            return False
        return True

    def check_stock_data(self):
        self.balance_sheets = self.stock_info.balance_sheet('a')
        self.income_statements = self.stock_info.income_statement('a', False)
        self.cash_flows = self.stock_info.cash_flow('a', False)
        if isinstance(self.balance_sheets, str) or isinstance(self.income_statements, str) or isinstance(self.cash_flows, str):
            self.reason_not_included = self.balance_sheets
            return False
        if len(self.balance_sheets) < 4 or len(self.income_statements) < 4 or len(self.cash_flows) < 4:
            self.reason_not_included = 'Not long enough history'
            time.sleep(16)
            return False
        return True

    def get_financial_data(self):
        self.get_balance_sheet_data()
        self.get_income_statment_data()
        self.get_cash_flow_data()
        self.get_profile_data()

    def check_for_more_data(self, statement, data_point, year):
        # LongTermDebt
        # TaxProvision
        # CostOfRevenue
        # CashAndCashEquivalents
        # import pdb; pdb.set_trace()

        if data_point == 'BasicAverageShares' and year == 'cy':
            return 1

        if data_point == 'OperatingExpense' and 'GeneralAndAdministrativeExpense' in statement:
            return check_nan(statement['GeneralAndAdministrativeExpense'])
            
        if data_point == 'CostOfRevenue' and 'InterestExpense' in statement:
            return check_nan(statement['InterestExpense'])

        if data_point == 'Depreciation' and 'DepreciationAndAmortization' in statement:
            return check_nan(statement['DepreciationAndAmortization'])

        return 0


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
        financial_data = 0
        if data_point in statement:
            financial_data = statement[data_point]
            financial_data =check_nan(financial_data)
            

        if financial_data == 0: 
            financial_data = self.check_for_more_data(statement, data_point, year)
            
        if financial_data == 0: 
            print(data_point + ' for ' + self.ticker + ' is zero.')
        
        text = data_point + '_' + year
        setattr(self, text, financial_data)
        
    def loop_data_points(self, statememt, data_points, year):
        for data_point in data_points:
            self.get_data_point(statememt, data_point, year)
        

    def get_income_statment_data(self):
        data_points = ['TotalRevenue', 'CostOfRevenue', 'NetIncome', 'TaxProvision', 'BasicAverageShares', 'OperatingExpense']
        income_statement = self.income_statements
        # import pdb; pdb.set_trace()
        self.income_statement_cy = income_statement.iloc[3]
        self.income_statement_1y = income_statement.iloc[2]
        self.income_statement_2y = income_statement.iloc[1]
        self.income_statement_3y = income_statement.iloc[0]
        self.loop_data_points(self.income_statement_cy, data_points, 'cy')
        self.loop_data_points(self.income_statement_1y, data_points, '1y')
        self.loop_data_points(self.income_statement_2y, data_points, '2y')
        self.loop_data_points(self.income_statement_3y, data_points, '3y')

    def get_cash_flow_data(self):
        data_points = ['Depreciation', 'CapitalExpenditure']
        cash_flow_statement = self.cash_flows
        self.cash_flow_cy = cash_flow_statement.iloc[3]
        self.cash_flow_1y = cash_flow_statement.iloc[2]
        self.cash_flow_2y = cash_flow_statement.iloc[1]
        self.cash_flow_3y = cash_flow_statement.iloc[0]

        self.loop_data_points(self.cash_flow_cy, data_points, 'cy')
        self.loop_data_points(self.cash_flow_3y, data_points, '3y')
    
    def get_balance_sheet_data(self):
        data_points = ['CommonStockEquity','TotalAssets','CurrentAssets','CashAndCashEquivalents','CurrentLiabilities','CurrentDebtAndCapitalLeaseObligation', 'LongTermDebt', 'TotalEquityGrossMinorityInterest']
        balance_sheet = self.balance_sheets
        self.balance_sheet_cy = balance_sheet.iloc[3]
        self.balance_sheet_1y = balance_sheet.iloc[2]
        self.balance_sheet_2y = balance_sheet.iloc[1]
        self.balance_sheet_3y = balance_sheet.iloc[0]

        self.loop_data_points(self.balance_sheet_cy, data_points, 'cy')
        self.loop_data_points(self.balance_sheet_1y, data_points, '1y')
        self.loop_data_points(self.balance_sheet_2y, data_points, '2y')
        self.loop_data_points(self.balance_sheet_3y, data_points, '3y')
        


    def det_profitability(self):
        working_capital = round(self.CurrentAssets_cy - self.CashAndCashEquivalents_cy -  self.CurrentLiabilities_cy + self.CurrentDebtAndCapitalLeaseObligation_cy   + self.TaxProvision_cy, 4)
        working_capital_2y = round(self.CurrentAssets_2y - self.CashAndCashEquivalents_2y - self.CurrentLiabilities_2y + self.CurrentDebtAndCapitalLeaseObligation_2y + self.TaxProvision_2y, 4)
        change_working_capital = working_capital - working_capital_2y
        self.gp_over_assets = zero_div_check((self.TotalRevenue_cy - self.CostOfRevenue_cy), self.TotalAssets_cy)
        self.roe = zero_div_check(self.NetIncome_cy, self.CommonStockEquity_cy)
        self.roa = zero_div_check(self.NetIncome_cy, self.TotalAssets_cy)
        self.cfoa = zero_div_check((self.NetIncome_cy + self.Depreciation_cy - change_working_capital - self.CapitalExpenditure_cy), self.TotalAssets_cy)
        self.low_acc = zero_div_check((self.Depreciation_cy - change_working_capital), self.TotalAssets_cy)
        self.gross_margin = zero_div_check((self.TotalRevenue_cy - self.CostOfRevenue_cy), self.TotalRevenue_cy)
        # print('Data for ' + self.ticker)
        # print('gp_over_assets- ' + str(self.gp_over_assets))
        # print('roe- ' + str(self.roe))
        # print('roa- ' + str(self.roa))
        # print('gross_margin- ' + str(self.gross_margin))
        # print('low_acc- ' + str(self.low_acc))
        # print('CFoA- ' + str(self.cfoa))
        # if self.ticker == 'AVXL':
        #     import pdb; pdb.set_trace()
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

        self.growth_gp_over_assets = zero_div_check((gross_profit_cy - gross_profit_3y), self.TotalAssets_3y)
        self.growth_roe = zero_div_check(( zero_div_check(self.NetIncome_cy, self.CommonStockEquity_cy) - zero_div_check(self.NetIncome_3y, self.CommonStockEquity_3y)), zero_div_check(self.NetIncome_3y, self.CommonStockEquity_3y))
        self.growth_roa = zero_div_check((zero_div_check(self.NetIncome_cy, self.TotalAssets_1y) - zero_div_check(self.NetIncome_3y, self.TotalAssets_3y)), zero_div_check(self.NetIncome_3y, self.TotalAssets_3y))
        self.growth_cfoa = zero_div_check((zero_div_check(cash_flow, self.TotalAssets_1y) - zero_div_check(cash_flow_3y, self.TotalAssets_3y)), zero_div_check(cash_flow_3y, self.TotalAssets_3y))
        self.growth_gross_margin = zero_div_check((zero_div_check((self.TotalRevenue_cy - self.CostOfRevenue_cy), self.TotalRevenue_cy) - zero_div_check((self.TotalRevenue_3y - self.CostOfRevenue_3y), self.TotalRevenue_3y)), zero_div_check((self.TotalRevenue_3y - self.CostOfRevenue_3y), self.TotalRevenue_3y))

        # print('growth_gp_over_assets: ' + str(self.growth_gp_over_assets))
        # print('growth_roe: ' + str(self.growth_roe))
        # print('growth_roa: ' + str(self.growth_roa))
        # print('growth_cfoa: ' + str(self.growth_cfoa))
        # print('growth_gross_margin: ' + str(self.growth_gross_margin))
        # print('')


    def det_payout(self):
        self.net_equity_issuance = 1 - zero_div_check(self.BasicAverageShares_1y, self.BasicAverageShares_2y, 1)
        self.net_payout_over_profits = zero_div_check((self.NetIncome_cy - (self.TotalEquityGrossMinorityInterest_cy - self.TotalEquityGrossMinorityInterest_3y)), (self.TotalRevenue_cy - self.CostOfRevenue_cy))
        self.net_debt_issuance = 1 - zero_div_check((self.CurrentDebtAndCapitalLeaseObligation_cy + self.LongTermDebt_cy), (self.CurrentDebtAndCapitalLeaseObligation_1y + self.LongTermDebt_1y), 1)

        # print('Payout for ' + self.ticker)
        # print('net_equity_issuance: ' + str(self.net_equity_issuance))
        # print('net_debt_issuance: ' + str(self.net_debt_issuance))
        # print('net_payout_over_profits: ' + str(self.net_payout_over_profits))

    def det_safty(self): 
        roe_cy = zero_div_check(self.NetIncome_cy, self.CommonStockEquity_cy)
        roe_1y = zero_div_check(self.NetIncome_1y, self.CommonStockEquity_1y)
        roe_2y = zero_div_check(self.NetIncome_2y, self.CommonStockEquity_2y)
        roe_3y = zero_div_check(self.NetIncome_3y, self.CommonStockEquity_3y)
        years = [roe_cy, roe_1y ,roe_2y, roe_3y]
        working_capital = round(self.CurrentAssets_cy - self.CashAndCashEquivalents_cy -  self.CurrentLiabilities_cy + self.CurrentDebtAndCapitalLeaseObligation_cy   + self.TaxProvision_cy, 4)
        ebit = self.TotalRevenue_cy - self.CostOfRevenue_cy - self.OperatingExpense_cy
        self.roe_std_3y = 1 - round(np.std(years), 4)
        self.leverage = 1 - (zero_div_check((self.LongTermDebt_cy + self.CurrentDebtAndCapitalLeaseObligation_cy), self.TotalAssets_cy))
        self.one_minus_beta = round(1 - self.beta, 4)
        self.altmans_z = zero_div_check(((1.2 * working_capital) + (1.4 * (self.NetIncome_cy - self.NetIncome_1y) ) + (3.3 * ebit) + (.6 * self.TotalEquityGrossMinorityInterest_cy) + (self.TotalRevenue_cy)),  self.TotalAssets_cy)
        # print('Safty for ' + self.ticker)
        # print('self.roe_std_3y: ' + str(self.self.roe_std_3y))
        # print('self.leverage: ' + str(self.self.leverage))
        # print('self.altmans_z: ' + str(self.altmans_z))
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


