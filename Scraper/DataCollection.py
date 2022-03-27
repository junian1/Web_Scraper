import Scrape as sp
import pandas as pd

df = sp.get_jobs("data analyst", 1000, False)
df.to_csv("glassdoor_jobs.csv", index=False)

