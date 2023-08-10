import pandas as pd
import json


df = pd.read_json(r".\data\profils.json")

df = pd.concat([df.drop(['profils'], axis=1), df['profils'].apply(pd.Series)], axis=1)

df['sexe'] = "Homme"


a = df.to_dict(orient='records')
a = {"profils":a}

with open("./data/profils2.json", 'w', encoding='utf-8') as file:
    json.dump(a, file, ensure_ascii=False, indent=4)


