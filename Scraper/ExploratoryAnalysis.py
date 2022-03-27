import numpy as np 
import pandas as pd
import re


path = 'glassdoor_jobs_da.csv'
df = pd.read_csv(path)

# Remove rating from company_name
df.Company_Name = df.Company_Name.apply(lambda x: x.split("\n")[0])

# Clean salary data separately
dfsal = df[df.Salary_Estimate!= '-1']
dfnosal = df[df.Salary_Estimate== '-1']

# Clean salary estimate into min salary and max salary, if only 1 value available, then min salary = max salary
dfsal.Salary_Estimate = dfsal.Salary_Estimate.apply(lambda x: x.split('(')[0])
dfsal.Salary_Estimate = dfsal.Salary_Estimate.apply(lambda x: x.replace('K','000').replace('MYR',''))
dfsal['Min_Salary'] = dfsal.Salary_Estimate.apply(lambda x: int(x.split('-')[0]))
dfsal['Max_Salary'] = dfsal.Salary_Estimate.apply(lambda x: int(x.split('-')[-1]))

# Clean size data
df.Size = df.Size.astype('str')
dfsize = df[(df.Size != '-1')&(df.Size != 'Unknown')&(df.Size != 'nan')]
dfnosize = df[df.Size == '-1']

# Split size into 2 columns, min size and max size, if only 1 value is available, then min size = max size
dfsize.Size = dfsize.Size.apply(lambda x: x.replace('Employees','').replace('to','-').replace('+',''))
dfsize['Min_Size'] = dfsize.Size.apply(lambda x: int(x.split('-')[0]))
dfsize['Max_Size'] = dfsize.Size.apply(lambda x: int(x.split('-')[-1]))


# Search through JD for specific skillset
df['jd_python'] = df.Job_Description.apply(lambda x: 1 if 'python' in x.lower() else 0)
df['jd_r'] = df.Job_Description.apply(lambda x: 1 if 'r studio' in x.lower() else 0)
df['jd_sql'] = df.Job_Description.apply(lambda x: 1 if 'sql' in x.lower() else 0)
df['jd_nosql'] = df.Job_Description.apply(lambda x: 1 if 'nosql' in x.lower() else 0)
df['jd_mongo'] = df.Job_Description.apply(lambda x: 1 if 'mongo' in x.lower() else 0)
df['jd_tableau'] = df.Job_Description.apply(lambda x: 1 if 'tableau' in x.lower() else 0)
df['jd_bi'] = df.Job_Description.apply(lambda x: 1 if 'power bi' in x.lower() else 0)
df['jd_panda'] = df.Job_Description.apply(lambda x: 1 if 'panda' in x.lower() else 0)
df['jd_numpy'] = df.Job_Description.apply(lambda x: 1 if 'numpy' in x.lower() else 0)
df['jd_spss'] = df.Job_Description.apply(lambda x: 1 if 'spss' in x.lower() else 0)
df['jd_stats'] = df.Job_Description.apply(lambda x: 1 if 'statistic' in x.lower() else 0)
df['jd_psych'] = df.Job_Description.apply(lambda x: 1 if 'psychology' in x.lower() else 0)
df['jd_ml'] = df.Job_Description.apply(lambda x: 1 if 'machine learning' in x.lower() else 0)
df['jd_ds'] = df.Job_Description.apply(lambda x: 1 if 'data science' in x.lower() else 0)
df['jd_exp'] = df.Job_Description.apply(lambda x: 1 if 'experiment' in x.lower() else 0)
df['jd_rdm'] = df.Job_Description.apply(lambda x: 1 if 'random' in x.lower() else 0)
df['jd_remote'] = df.Job_Description.apply(lambda x: 1 if 'remote' in x.lower() else 0)






