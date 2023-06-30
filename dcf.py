import json
import pandas as pd
import requests
import os
from bs4 import BeautifulSoup
import argparse
import re
from decimal import Decimal

# Configuration
'''
This variable has purpose to scrape financial report type.
List option : income_statement, balance_sheet, cash_flow
'''
TYPE_FREE_CASH_FLOW = "cash_flow"
TYPE_SHARE_OUTSTANDING = "income_statement"
TYPE_NET_DEBT_LEVEL = "balance_sheet"

# Convert configuration
match TYPE_FREE_CASH_FLOW:
    case "income_statement":
        CONV_FREE_CASH_FLOW = 1
    case "balance_sheet":
        CONV_FREE_CASH_FLOW = 2
    case "cash_flow":
        CONV_FREE_CASH_FLOW = 3

match TYPE_SHARE_OUTSTANDING:
    case "income_statement":
        CONV_SHARE_OUTSTANDING = 1
    case "balance_sheet":
        CONV_SHARE_OUTSTANDING = 2
    case "cash_flow":
        CONV_SHARE_OUTSTANDING = 3

match TYPE_NET_DEBT_LEVEL:
    case "income_statement":
        CONV_NET_DEBT_LEVEL = 1
    case "balance_sheet":
        CONV_NET_DEBT_LEVEL = 2
    case "cash_flow":
        CONV_NET_DEBT_LEVEL = 3

# Get user input configuration
parser = argparse.ArgumentParser(description="stocks analysis")
parser.add_argument("-n", help="input the company name")
args = parser.parse_args()

# Scrape requirements
def scrape_finance(TYPE):
    global params, req

    ENDPOINT = "https://exodus.stockbit.com/findata-view/company/financial"

    with open('cred.txt') as f:
        Auth = f.readlines()

    headers = {
        "Authorization" : Auth[0]
    }

    params = {
        "symbol" : args.n,
        "data_type" : 1,
        "report_type" : TYPE,
        "statement_type": 2
    }

    req = requests.get(ENDPOINT, params=params, headers=headers)

    df_0 = req.json()
    df_1 = pd.json_normalize(df_0)
    df_2 = json.loads(pd.Series.to_json(df_1))
    df_3 = pd.DataFrame(df_2)
    df_3["data.html_report"].to_csv(f"data/{params['symbol']}_{TYPE}.csv", index=False, header=False)
    os.rename(f"data/{params['symbol']}_{TYPE}.csv", f"data/{params['symbol']}_{TYPE}.html")
    return BeautifulSoup(open(f"data/{params['symbol']}_{TYPE}.html"),'html.parser')

# scrape the main data
def scrape_data(TYPE):
    header_elements = scrape_finance(TYPE).find_all("table")[0].find("tr")
    data_elements = scrape_finance(TYPE).find_all("table")[0].find_all("tr")[1:]

    # for getting the header
    list_header = []
    for i in header_elements:
        try:
            list_header.append(i.get_text())
        except:
            continue

    # for getting the data
    data = []
    for i in data_elements:
        sub_data = []
        for j in i:
            try:
                sub_data.append(j.get_text())
            except:
                continue
        data.append(sub_data)

    # clean the data
    clean_list_header = [i for i in list_header if i != " "]

    clean_data = []
    for i in range(0, len(data)):
        clean_data.append([j for j in data[i] if j != " "])

    dataFrame = pd.DataFrame(data = clean_data, columns = clean_list_header)
    dataFrame.to_csv(f"data/clean_{params['symbol']}_{TYPE}_data.csv")
    return dataFrame

# scrape key ratio
def scrape_key(TYPE):
    header_elements_2 = scrape_finance(TYPE).find_all("table")[1].find("tr")
    data_elements_2 = scrape_finance(TYPE).find_all("table")[1].find_all("tr")[1:]

    list_header_2 = []
    for i in header_elements_2:
        try:
            list_header_2.append(i.get_text())
        except:
            continue

    # for getting the data
    data_2 = []
    for i in data_elements_2:
        sub_data_2 = []
        for j in i:
            try:
                sub_data_2.append(j.get_text())
            except:
                continue
        data_2.append(sub_data_2)

    # clean the data
    clean_list_header_2 = [i for i in list_header_2 if i != " "]

    clean_data_2 = []
    for i in range(0, len(data_2)):
        clean_data_2.append([j for j in data_2[i] if j != " "])

    dataFrame_2 = pd.DataFrame(data = clean_data_2, columns = clean_list_header_2)
    dataFrame_2.to_csv(f"data/clean_{params['symbol']}_{TYPE}_keyratio.csv")
    return dataFrame_2

# df_fcf_data = scrape_data(CONV_FREE_CASH_FLOW)
df_fcf_key = scrape_key(CONV_FREE_CASH_FLOW)
df_so_key = scrape_key(CONV_SHARE_OUTSTANDING)
df_nd_key = scrape_key(CONV_NET_DEBT_LEVEL)

def Average(lst):
    return sum(lst) / len(lst)

def text_to_num(text):
        d = {'K': 3, 'M': 6, 'B': 9}
        if text[-1] in d:
            num, magnitude = text[:-1], text[-1]
            return Decimal(num) * 10 ** d[magnitude]
        else:
            return Decimal(text)

# Extract metrics
def metrics(metrics, dataframe, average):
    fcf = dataframe.loc[dataframe["In Million"] == f"{metrics}"].reset_index()
    fcf_2 = fcf[fcf.columns[-average:]].replace(",", "", regex=True)
    list_fcf = fcf_2.loc[0, :].values.flatten().tolist()
    regex_3 = []
    for i in list_fcf:
        regex = re.sub(r'[(]', '-', i)
        regex_2 = re.sub(r'[)]', '', regex)
        regex_3.append(regex_2)
    regex_4 = [int(float(text_to_num(s))) for s in regex_3]
    average_fcf = Average(lst = regex_4)
    return average_fcf


average_free_cash_flow = metrics(metrics="Free cash flow (Annual)", dataframe=df_fcf_key, average=3)
share_outstanding = metrics(metrics="Share Outstanding", dataframe=df_so_key, average=1)
net_debt = metrics(metrics="Net Debt (Annual)", dataframe=df_nd_key, average=3)

if __name__ == "__main__":
    if req.status_code == 200:
        print("Data received")
        try:
            print("Average free cash flow in the last 3 years: ", average_free_cash_flow)
        except:
            print("Can't get the financial data")
        try:
            print("Share Outstanding: ", share_outstanding)
        except:
            print("Can't get the financial data")
        try:
            print("Total Net Debt: ", net_debt)
        except:
            print("Can't get the financial data")
    else:
        print("can't connect, please fix the credential")