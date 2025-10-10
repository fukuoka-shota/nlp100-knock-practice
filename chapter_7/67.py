import pandas as pd
import pickle
from collections import defaultdict
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score

# モデルとベクトライザーの読み込み
with open("SST-2/logistic_model.pkl", "rb") as f:
    clf = pickle.load(f)
with open("SST-2/vectorizer.pkl", "rb") as f:
    vec = pickle.load(f)

print("-------------------------------------------")
print("検証データの各種スコア")
print("-------------------------------------------")

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

prediction = []
reference = []

for i in range(X_dev.shape[0]):
    pred = clf.predict(X_dev[i])
    pred_nbr = pred.tolist()[0]
    prediction.append(pred_nbr)

s_dev = df_dev["label"]
reference = s_dev.tolist()

cm = confusion_matrix(reference,prediction)
print(cm)
tn, fp, fn, tp = cm.flatten()
print(tn, fp, fn, tp)

correct_answer_nbr = 0
# print(len(reference))
for p, r in zip(prediction,reference):
    if p == r:
        correct_answer_nbr += 1


accuracy = correct_answer_nbr / len(reference)
print(f"正解率 : {accuracy:.3f}")
print(f"パッケージを利用して算出した正解率:{accuracy_score(reference, prediction)}")

precision = tp / (tp + fp)
print(f"適合率 : {precision:.3f}")
print(f"パッケージを利用して算出した適合率:{precision_score(reference, prediction)}")

recall = tp / (tp + fn)
print(f"再現率 : {recall:.3f}")
print(f"パッケージを利用して算出した再現率:{recall_score(reference, prediction)}")

f1 = (2 * precision * recall) / (precision + recall)
print(f"F1値 : {f1:.3f}")
print(f"パッケージを利用して算出したF1値:{f1_score(reference, prediction)}")

print("-------------------------------------------")
print("学習データの各種スコア")
print("-------------------------------------------")

# 学習データの読み込み
df_train = pd.read_csv("SST-2/train.tsv", sep="\t")

#textを特徴ベクトルに変換する関数
def text2vec(text:str) -> dict:
    bec = defaultdict(int)
    for token in text.split():
        bec[token] += 1
    return dict(bec)

df_train["feature"] = df_train["sentence"].apply(text2vec)
X_train = vec.transform([d["feature"] for d in df_train.to_dict(orient="records")])

prediction = []
reference = []

for i in range(X_train.shape[0]):
    pred = clf.predict(X_train[i])
    pred_nbr = pred.tolist()[0]
    prediction.append(pred_nbr)

s_train = df_train["label"]
reference = s_train.tolist()

cm = confusion_matrix(reference,prediction)
tn, fp, fn, tp = cm.flatten()
# print(tn, fp, fn, tp)

correct_answer_nbr = 0
# print(len(reference))
for p, r in zip(prediction,reference):
    if p == r:
        correct_answer_nbr += 1

accuracy = correct_answer_nbr / len(reference)
print(f"正解率 : {accuracy:.3f}")
print(f"パッケージを利用して算出した正解率:{accuracy_score(reference, prediction)}")

precision = tp / (tp + fp)
print(f"適合率 : {precision:.3f}")
print(f"パッケージを利用して算出した適合率:{precision_score(reference, prediction)}")

recall = tp / (tp + fn)
print(f"再現率 : {recall:.3f}")
print(f"パッケージを利用して算出した再現率:{recall_score(reference, prediction)}")

f1 = (2 * precision * recall) / (precision + recall)
print(f"F1値 : {f1:.3f}")
print(f"パッケージを利用して算出したF1値:{f1_score(reference, prediction)}")
