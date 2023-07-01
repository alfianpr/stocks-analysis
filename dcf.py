import argparse
from utils import scrape_key, metrics, calculate_dcf

# Asumption configuration
growth_rate_year_5_10 = 0.12
growth_rate_year_5_10 = 0.09
discount_rate = 0.09
terminal_growth_rate = 0.02

# Scrape_configuration
'''
This variable has purpose to scrape financial report type.
List option : income_statement, balance_sheet, cash_flow
'''
TYPE_FREE_CASH_FLOW = "cash_flow"
TYPE_SHARE_OUTSTANDING = "income_statement"
TYPE_NET_DEBT_LEVEL = "balance_sheet"

# Convert configuration
match TYPE_FREE_CASH_FLOW:
    case "cash_flow":
        CONV_FREE_CASH_FLOW = 3

match TYPE_SHARE_OUTSTANDING:
    case "income_statement":
        CONV_SHARE_OUTSTANDING = 1

match TYPE_NET_DEBT_LEVEL:
    case "balance_sheet":
        CONV_NET_DEBT_LEVEL = 2

parser = argparse.ArgumentParser(description="stocks analysis")
parser.add_argument("-n", help="input the company name")
args = parser.parse_args()

df_fcf_key = scrape_key(CONV_FREE_CASH_FLOW, args.n)
df_so_key = scrape_key(CONV_SHARE_OUTSTANDING, args.n)
df_nd_key = scrape_key(CONV_NET_DEBT_LEVEL, args.n)

average_free_cash_flow = metrics(metrics="Free cash flow (Annual)", dataframe=df_fcf_key, average=3)
share_outstanding = metrics(metrics="Share Outstanding", dataframe=df_so_key, average=1)
net_debt = metrics(metrics="Net Debt (Annual)", dataframe=df_nd_key, average=1)

intrinsic = calculate_dcf(G15 = growth_rate_year_5_10, 
                          G610 = growth_rate_year_5_10, 
                          TGR = terminal_growth_rate, 
                          DR = discount_rate, 
                          average_free_cash_flow = average_free_cash_flow, 
                          share_outstanding = share_outstanding, 
                          net_debt = net_debt)

if __name__ == "__main__":
    print("Data received")
    try:
        print(f"The intrinsic value of {args.n} using DCF method is:", "\nRp", intrinsic)
    except:
        print("Can't get the financial data")
    print("################# Key financial report ####################")
    try:
        print("Average free cash flow in the last 3 years:", "Rp", average_free_cash_flow)
    except:
        print("Can't get the financial data")
    try:
        print("Share Outstanding:", "Rp", share_outstanding)
    except:
        print("Can't get the financial data")
    try:
        print("Total Net Debt:", "Rp", net_debt)
    except:
        print("Can't get the financial data")