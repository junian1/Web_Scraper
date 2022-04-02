import pandas as pd


path = 'glassdoor_jobs_da.csv'
df = pd.read_csv(path)

# Remove rating from company_name
df.Company_Name = df.Company_Name.apply(lambda x: x.split("\n")[0])

# Clean salary data separately
df.Salary_Estimate = df.Salary_Estimate
dfsal = df[(df.Salary_Estimate != '-1')&(df.Salary_Estimate.notna())]
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


# Clean rating
dfrate = df[df.Rating != -1]

# Clean founded year
dfyear = df[df.Founded != -1]
dfyear['Duration'] = 2022 - df.Founded

# Clean company type
dftype = df[(df.Type != '-1')&(df.Type != 'Unknown')].astype('str')
dftype['IsPrivate'] = dftype.Type.apply(lambda x: 1 if 'Private' in x else 0)


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
df['jd_excel'] = df.Job_Description.apply(lambda x: 1 if 'excel' in x.lower() else 0)
df['jd_ml'] = df.Job_Description.apply(lambda x: 1 if 'machine learning' in x.lower() else 0)
df['jd_ds'] = df.Job_Description.apply(lambda x: 1 if 'data science' in x.lower() else 0)


# Add Rank, 0 = null, 1 = intern, 2 = junior, 3 = senior, 4 = manager, 5 = director
intern = ['intern']
junior = ['junior','jr','jnr','fresh','graduate','entry']
senior = ['senior','sr','snr','special','expert']
manager = ['manager','mgr','mngr','lead']
director = ['director','chief','head']

df.loc[df['Job_Title'].str.lower().str.contains('|'.join(intern)), 'Rank'] = 1
df.loc[df['Job_Title'].str.lower().str.contains('|'.join(junior)), 'Rank'] = 2 
df.loc[df['Job_Title'].str.lower().str.contains('|'.join(senior)), 'Rank'] = 3
df.loc[df['Job_Title'].str.lower().str.contains('|'.join(manager)), 'Rank'] = 4
df.loc[df['Job_Title'].str.lower().str.contains('|'.join(director)), 'Rank'] = 5
df.loc[df.Rank.isna(), 'Rank'] = 0

df[['Min_Salary','Max_Salary']] = dfsal[['Min_Salary','Max_Salary']]
df['Rate'] = dfrate['Rating']
df[['Min_Size','Max_Size']] = dfsize[['Min_Size','Max_Size']] 
df['Duration'] = dfyear['Duration']
df['IsPrivate'] = dftype['IsPrivate']

df.to_csv('glassdoor_job_clean.csv')
