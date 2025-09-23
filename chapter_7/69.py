import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics import accuracy_score
from collections import defaultdict
import japanize_matplotlib

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

C_values = np.logspace(-5, 5, 21)

train_accuracies = []
dev_accuracies = []

for C in C_values:
    model = LogisticRegression(C=C, max_iter=1000)
    model.fit(X_train, y_train)

    train_pred = model.predict(X_train)
    dev_pred = model.predict(X_dev)

    train_acc = accuracy_score(y_train, train_pred)
    dev_acc = accuracy_score(y_dev, dev_pred)

    train_accuracies.append(train_acc)
    dev_accuracies.append(dev_acc)

    print(
        f"C = {C:.2e}, 訓練データの正解率:{train_acc:.4f}, 検証データの正解率:{dev_acc:.4f}"
    )

# 結果の可視化
japanize_matplotlib.japanize()
plt.figure(figsize=(10, 6))
plt.semilogx(C_values, train_accuracies, "o-", label="訓練データ")
plt.semilogx(C_values, dev_accuracies, "o-", label="検証データ")
plt.grid(True)
plt.xlabel("正則化パラメータ C")
plt.ylabel("正解率")
plt.title("正則化パラメータと正解率の関係")
plt.legend()
plt.tight_layout()
plt.savefig("regularization_accuracy.png")
plt.close()