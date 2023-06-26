import json
import pandas as pd
import requests
import os
from bs4 import BeautifulSoup
import argparse

parser = argparse.ArgumentParser(description="stocks analysis")
parser.add_argument("-n", help="input the company name")
args = parser.parse_args()

with open('cred') as f:
    Auth = f.readlines()

headers = {
    "Authorization" : Auth[0]
}

params = {
    "symbol" : args.n,
    "data_type" : 1,
    "report_type" : 3,
    "statement_type": 2
}

scrape = requests.get("https://exodus.stockbit.com/findata-view/company/financial", params=params, headers=headers)

print(scrape.status_code)

df_0 = scrape.json()
df_1 = pd.json_normalize(df_0)
df_2 = json.loads(pd.Series.to_json(df_1))
df_3 = pd.DataFrame(df_2)
df_3["data.html_report"].to_csv(f"data/{params['symbol']}.csv", index=False, header=False)
os.rename(f"data/{params['symbol']}.csv", f"data/{params['symbol']}.html")

soup = BeautifulSoup(open(f"data/{params['symbol']}.html"),'html.parser')

# scrape the main data
def scrape_data():
    header_elements = soup.find_all("table")[0].find("tr")
    data_elements = soup.find_all("table")[0].find_all("tr")[1:]

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
    dataFrame.to_csv(f"data/clean_{params['symbol']}_data.csv")
    return dataFrame

# scrape key ratio
def scrape_key():
    header_elements_2 = soup.find_all("table")[1].find("tr")
    data_elements_2 = soup.find_all("table")[1].find_all("tr")[1:]

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
    dataFrame_2.to_csv(f"data/clean_{params['symbol']}_keyratio.csv")
    return dataFrame_2

df_data = scrape_data()
df_key = scrape_key()

def Average(lst):
    return sum(lst) / len(lst)

# Extract metrics
def metrics(metrics):
    fcf = df_key.loc[df_key["In Million"] == f"{metrics}"].reset_index()
    fcf_2 = fcf[fcf.columns[-3:]].replace(",", "", regex=True).replace(" ", "", regex=True).replace("B", "000000000", regex=True)
    list_fcf = fcf_2.loc[0, :].values.flatten().tolist()
    list_fcf_int = [int(s) for s in list_fcf]
    average_fcf = Average(lst = list_fcf_int)
    return average_fcf

print(df_data)

print(df_key)

print(metrics(metrics="Free cash flow (Annual)"))