from sklearn.linear_model import LogisticRegression
import pandas as pd
from collections import defaultdict
from sklearn.feature_extraction import DictVectorizer
import pickle

df_train = pd.read_csv("SST-2/train.tsv", sep="\t")
df_dev = pd.read_csv("SST-2/dev.tsv", sep="\t")

def text2bec(text:str) -> dict:
    bec = defaultdict(int)
    for token in text.split():
        bec[token] += 1
    return dict(bec)

df_train["feature"] = df_train["sentence"].apply(text2bec)
df_dev["feature"] = df_dev["sentence"].apply(text2bec)

v = DictVectorizer(sparse=True)
X_train = v.fit_transform([d["feature"] for d in df_train.to_dict(orient="records")])
y_train = [d["label"] for d in df_train.to_dict(orient="records")]

X_dev = v.transform([d["feature"] for d in df_dev.to_dict(orient="records")])
y_dev = [d["label"] for d in df_dev.to_dict(orient="records")]

print(X_train)
print(X_dev)

clf = LogisticRegression(max_iter=1000)
clf.fit(X_train, y_train)

with open("SST-2/logistic_model.pkl", "wb") as f:
    pickle.dump(clf,f)
with open("SST-2/vectorizer.pkl","wb") as f:
    pickle.dump(v,f)