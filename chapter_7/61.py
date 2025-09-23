import pandas as pd
from collections import defaultdict

df_train = pd.read_csv("SST-2/train.tsv", sep="\t")
df_dev = pd.read_csv("SST-2/dev.tsv", sep="\t")

def text2bec(text:str) -> dict:
    bec = defaultdict(int)
    for token in text.split():
        bec[token] += 1
    return dict(bec)

df_train["feature"] = df_train["sentence"].apply(text2bec)
df_dev["feature"] = df_dev["sentence"].apply(text2bec)

train_data = df_train.apply(
    lambda x: {"text": x["sentence"], "label":str(x["label"]),"feature":x["feature"]},axis=1
).tolist()

print(train_data[0])

dev_data = df_dev.apply(
    lambda x: {"text": x["sentence"], "label":str(x["label"]),"feature":x["feature"]},axis=1
).tolist()

print(dev_data[0])
