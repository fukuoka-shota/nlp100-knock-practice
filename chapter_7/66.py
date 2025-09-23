from sklearn.metrics import confusion_matrix
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

# print(X_dev.shape)
# print(X_dev.shape[0])

prediction = []
reference = []

for i in range(X_dev.shape[0]):
    pred = clf.predict(X_dev[i])
    pred_nbr = pred.tolist()[0]
    prediction.append(pred_nbr)

s_dev = df_dev["label"]
reference = s_dev.tolist()
# print(reference)
# print(len(reference))
# print(len(prediction))
cm = confusion_matrix(reference,prediction)

print(cm)