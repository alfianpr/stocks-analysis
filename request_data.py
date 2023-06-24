import json
import pandas as pd
import random
import re
import requests
import time
import numpy as np
from datetime import date
import os
import time
import sys
from bs4 import BeautifulSoup

headers = {
    "Authorization" : "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjU3MDc0NjI3LTg4MWItNDQzZC04OTcyLTdmMmMzOTNlMzYyOSIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7InVzZSI6IkFsZmlhbnByOTkiLCJlbWEiOiJhbGZpYW5wcmF0YW1hQGhvdG1haWwuY29tIiwiZnVsIjoiQWxmaWFuIFByYXRhbWEiLCJzZXMiOiJWM2RJY3NGNXVBOFVubFE2IiwiZHZjIjoiIiwidWlkIjo2NjAyODF9LCJleHAiOjE2ODc2NzYzNzYsImlhdCI6MTY4NzU4OTk3NiwiaXNzIjoiU1RPQ0tCSVQiLCJqdGkiOiIyZTljYTJkZC0wNWJmLTRjOTYtYmE5MS1iMThlZDdmYjUyYTgiLCJuYmYiOjE2ODc1ODk5NzZ9.tOyHLRdUqQhyo8d-yTd2pKfCsT58ELzHPFTo_qOZJRnPSiXiQM-F7-xlHevf8fy7WrptSmyd6m3MLU_sCmLWtE34V6D4Jk39u7tUbUIVJfiuYbsDA9ANUl4Ldg1_m0RszxtqDA0i4xL8VAHhjcACjXsnnApVVA8eze1-ugiwQDnAmo98gms_JCV69n2iIKsTCwUaf-Z2wIrTGEztS2n5IvPO-3PNU-78gsHI3tRNld4PI_HxvPoIrACM_xQZM8eef2JJVivic54kWLqHaGnZuPR2hxM41KWUIDx4TSYiDPbBE65IGo7y8_zVlhai5ahqvo5uBmuHK9z7kBmZxBlH0Q"
}

params = {
    "symbol" : "BBCA",
    "data_type" : 1,
    "report_type" : 1,
    "statement_type": 1
}

scrape = requests.get("https://exodus.stockbit.com/findata-view/company/financial", params=params, headers=headers)

print(scrape.status_code)

df_0 = scrape.json()
df_1 = pd.json_normalize(df_0)
df_2 = json.loads(pd.Series.to_json(df_1))
df_3 = pd.DataFrame(df_2)
df_3["data.html_report"].to_csv(f"{params['symbol']}.csv", index=False, header=False)

os.rename(f"{params['symbol']}.csv", f"{params['symbol']}.html")

data = []
list_header = []
soup = BeautifulSoup(open(f"{params['symbol']}.html"),'html.parser')
header = soup.find_all("table")[0].find("tr")

for items in header:
    try:
        list_header.append(items.get_text())
    except:
        continue

# for getting the data
HTML_data = soup.find_all("table")[0].find_all("tr")[1:]
 
for element in HTML_data:
    sub_data = []
    for sub_element in element:
        try:
            sub_data.append(sub_element.get_text())
        except:
            continue
    data.append(sub_data)


dataFrame = pd.DataFrame(data = data, columns = list_header)
dataFrame.to_csv(f"clean_{params['symbol']}.csv")