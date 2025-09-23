import pandas as pd
import pickle
from collections import defaultdict

# モデルとベクトライザーの読み込み
with open("SST-2/logistic_model.pkl", "rb") as f:
    clf = pickle.load(f)
with open("SST-2/vectorizer.pkl", "rb") as f:
    vec = pickle.load(f)

# 検証データの読み込み
df_dev = pd.read_csv("SST-2/dev.tsv", sep="\t")

#textを特徴ベクトルに変換する関数
def text2vec(text:str) -> dict:
    bec = defaultdict(int)
    for token in text.split():
        bec[token] += 1
    return dict(bec)

df_dev["feature"] = df_dev["sentence"].apply(text2vec)
X_dev = vec.transform([d["feature"] for d in df_dev.to_dict(orient="records")])

pred = clf.predict(X_dev[0])
pred_nbr = pred.tolist()

if pred_nbr[0] == 1:
    print("Positive")
else:
    print("Negative")

if pred_nbr[0] == df_dev["label"][0]:
    print("match")
else:
    print("not match")