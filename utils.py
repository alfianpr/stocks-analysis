import json
import pandas as pd
import requests
import os
from bs4 import BeautifulSoup
import re
from decimal import Decimal

# Scrape requirements
def scrape_finance(TYPE, SYMBOL):
    global params, req

    ENDPOINT = "https://exodus.stockbit.com/findata-view/company/financial"

    with open('cred.txt') as f:
        Auth = f.readlines()

    headers = {
        "Authorization" : Auth[0]
    }

    params = {
        "symbol" : SYMBOL,
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
def scrape_data(TYPE, SYMBOL):
    header_elements = scrape_finance(TYPE, SYMBOL).find_all("table")[0].find("tr")
    data_elements = scrape_finance(TYPE, SYMBOL).find_all("table")[0].find_all("tr")[1:]

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
def scrape_key(TYPE, SYMBOL):
    header_elements_2 = scrape_finance(TYPE, SYMBOL).find_all("table")[1].find("tr")
    data_elements_2 = scrape_finance(TYPE, SYMBOL).find_all("table")[1].find_all("tr")[1:]

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

def calculate_dcf(G15, G610, TGR, DR, average_free_cash_flow, share_outstanding, net_debt):
    E_1_5 = average_free_cash_flow*(G15+1)**5
    E_6_10 = E_1_5*(G610+1)**5
    Eterminal = E_6_10*(1+TGR)/(DR-TGR)
    F10 = E_6_10/(1+DR)**10

    lst_E15 = []
    for i in range(5):
        n = i+1
        lst_E15.append(average_free_cash_flow*(G15+1)**n)
    lst_E610 = []
    for i in range(5):
        n = i+1
        lst_E610.append(E_1_5*(G610+1)**n)

    tot_E_list = lst_E15+lst_E610 #+[float(Eterminal)]

    lst_Fn = []
    for i in range(10):
        n = i + 1
        lst_Fn.append(tot_E_list[i]/(1+DR)**n)

    Fn_Terminal = Eterminal/(1+DR)**10
    tot_Fn = sum(lst_Fn+[float(Fn_Terminal)])
    return round((tot_Fn - net_debt)/share_outstanding, 2)