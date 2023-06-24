import json
import pandas as pd
import requests
import os
from bs4 import BeautifulSoup

headers = {
    "Authorization" : "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjU3MDc0NjI3LTg4MWItNDQzZC04OTcyLTdmMmMzOTNlMzYyOSIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7InVzZSI6IkFsZmlhbnByOTkiLCJlbWEiOiJhbGZpYW5wcmF0YW1hQGhvdG1haWwuY29tIiwiZnVsIjoiQWxmaWFuIFByYXRhbWEiLCJzZXMiOiJWM2RJY3NGNXVBOFVubFE2IiwiZHZjIjoiIiwidWlkIjo2NjAyODF9LCJleHAiOjE2ODc2NzYzNzYsImlhdCI6MTY4NzU4OTk3NiwiaXNzIjoiU1RPQ0tCSVQiLCJqdGkiOiIyZTljYTJkZC0wNWJmLTRjOTYtYmE5MS1iMThlZDdmYjUyYTgiLCJuYmYiOjE2ODc1ODk5NzZ9.tOyHLRdUqQhyo8d-yTd2pKfCsT58ELzHPFTo_qOZJRnPSiXiQM-F7-xlHevf8fy7WrptSmyd6m3MLU_sCmLWtE34V6D4Jk39u7tUbUIVJfiuYbsDA9ANUl4Ldg1_m0RszxtqDA0i4xL8VAHhjcACjXsnnApVVA8eze1-ugiwQDnAmo98gms_JCV69n2iIKsTCwUaf-Z2wIrTGEztS2n5IvPO-3PNU-78gsHI3tRNld4PI_HxvPoIrACM_xQZM8eef2JJVivic54kWLqHaGnZuPR2hxM41KWUIDx4TSYiDPbBE65IGo7y8_zVlhai5ahqvo5uBmuHK9z7kBmZxBlH0Q"
}

params = {
    "symbol" : "BBCA",
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

# scrape key ratio
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