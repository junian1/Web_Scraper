import Scraper as sp
import pandas as pd

# Can only do a maximum of 1000 at a time due to glassdoor limit
df = sp.get_jobs("data analyst", 1000, False)
df.to_csv("glassdoor_jobs.csv", index=False)

