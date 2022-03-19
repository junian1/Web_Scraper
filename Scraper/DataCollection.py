import Scrape as sp
import pandas as pd

df = sp.get_jobs("data scientist", 5, False)
df.to_csv("glassdoor_jobs.csv", index=False)

