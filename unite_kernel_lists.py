import os
import pandas as pd
import datetime as dt

LISTS_FOLDER = "./kernel_lists"
MERGED_LIST = "./kernels.csv"


all_refs = []
all_years = []
for filename in os.listdir(LISTS_FOLDER):
    path = os.path.join(LISTS_FOLDER, filename)
    try: 
        df = pd.read_csv(path)
        df.lastRunTime = pd.to_datetime(df.lastRunTime)        
        all_refs.append(df.ref)
        all_years.append(df.lastRunTime.dt.year)
        
    except AttributeError:
        continue
    except pd.errors.ParserError:
        print(filename)
        
all_refs = pd.concat(all_refs, ignore_index=True)
all_years = pd.concat(all_years, ignore_index=True)

df_new = pd.DataFrame()
df_new["ref"] = all_refs
df_new["year"] = all_years

df_new.drop_duplicates(inplace = True)
df_new.to_csv(MERGED_LIST)

print(df_new.shape)


# delete files from LISTS_FOLDER

for filename in os.listdir(LISTS_FOLDER):
    path = os.path.join(LISTS_FOLDER, filename)
    try:
        os.remove(path)
    except IsADirectoryError:
        continue