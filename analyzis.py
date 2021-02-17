import os
from shutil import copyfile

import pandas as pd

f = f'./cases/HistoryFiles/history_def.csv'

num_top = 30

df = pd.read_csv(f, header=0)

df = df.drop_duplicates(subset=['ananlytics_ob0']).sort_values(by='obj0').head(num_top)

if not os.path.exists('./cases/exported'):
    os.mkdir('./cases/exported')
ind = 0
for i, d in df.iterrows():
    uid = d['local_id']
    obj = -eval(d['ananlytics_ob0'])[0]
    print(uid)
    copyfile(f"./cases/models/{uid}.mph", f"./cases/exported/{ind}_{uid}_{round(float(obj), 4)}.mph")
    copyfile(f"./cases/tmp/{obj}.png", f"./cases/exported/{ind}_{uid}_{round(float(obj), 4)}.png")
    ind += 1
