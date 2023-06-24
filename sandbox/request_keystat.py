import json
import pandas as pd
import random
import re
import requests
import time
import numpy as np
from datetime import date
import html_to_json

headers = {
    "Authorization" : "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7InVzZSI6IkFsZmlhbnByOTkiLCJlbWEiOiJhbGZpYW5wcmF0YW1hQGhvdG1haWwuY29tIiwiZnVsIjoiQWxmaWFuIFByYXRhbWEiLCJzZXMiOiJvNndYTGJRYTVhYUc3ZnZmIiwiZHZjIjoiIiwidWlkIjo2NjAyODF9LCJleHAiOjE2ODc0MTU5NjYsImlhdCI6MTY4NzMyOTU2NiwiaXNzIjoiU1RPQ0tCSVQiLCJqdGkiOiJlNTliMzNiOC02MTQxLTQ0ZjAtYmZkYy1kYzg1MDRjMDJhNjEiLCJuYmYiOjE2ODczMjk1NjZ9.aM6tOCRI8lwd-r5PPRVmyE3bFCCHSSjarYcfxPTLQJk"
}


scrape = requests.get("https://exodus.stockbit.com/keystats/ratio/v1/BBCA", headers=headers)

print(scrape.status_code)

df_0 = scrape.json()
df_1 = pd.json_normalize(df_0)
df_2 = json.loads(pd.Series.to_json(df_1["data.closure_fin_items_results"]))
df_3 = pd.DataFrame(df_2)

df_4 = df_3["0"]
# df_4 = df_3.explode("data.closure_fin_items_results")
# df_5 = pd.DataFrame(df_4)

print(df_4)
# df_3.to_csv("test.csv")
# print(df_4)
# df_3 = df_2["0"]

# df_4 = html_to_json.convert(df_3)
# df_5 = df_4["div"]
# df_6 = pd.DataFrame(df_5)
# df_7 = df_6["div"][0]

# df_8 = pd.DataFrame(df_7)

# df_9 = df_8["div"]
# df_10 = pd.DataFrame(df_9)
# df_11 = df_10["div"][1]
# df_12 = pd.DataFrame(df_11)
# df_13 = df_12["div"][0]
# df_14 = pd.DataFrame(df_13)
# df_15 = df_14["table"][0]
# df_16 = pd.DataFrame(df_15)
# df_17 = df_16["tbody"][0]
# df_18 = pd.DataFrame(df_17)
# df_19 = df_18["tr"][0]
# df_20 = pd.DataFrame(df_19)
# # print (df_12)
# # df_10 = pd.DataFrame(df_9)

# df_20.to_csv("test.csv")