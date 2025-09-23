import pickle
from collections import defaultdict

# モデルとベクトライザーの読み込み
with open("SST-2/logistic_model.pkl", "rb") as f:
    clf = pickle.load(f)
with open("SST-2/vectorizer.pkl", "rb") as f:
    vec = pickle.load(f)

text = "the worst movie I've ever seen"

#textを特徴ベクトルに変換する関数
def text2vec(text:str) -> dict:
    bec = defaultdict(int)
    for token in text.split():
        bec[token] += 1
    return dict(bec)

feature_vec_dict = text2vec(text)
print(feature_vec_dict)

X_dev = vec.transform(feature_vec_dict)
print(X_dev)

pred = clf.predict_proba(X_dev)
pred_prob = pred.tolist()

pred_0 = format(pred_prob[0][0], '.5f')
pred_1 = format(pred_prob[0][1], '.5f')
print(f"0(ネガティブ)を予測する確率 : {pred_0}")
print(f"1(ポジティブ)を予測する確率 : {pred_1}")
