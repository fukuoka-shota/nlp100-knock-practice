from sklearn.metrics import confusion_matrix
import pandas as pd
import pickle
from collections import defaultdict

# モデルとベクトライザーの読み込み
with open("SST-2/logistic_model.pkl", "rb") as f:
    clf = pickle.load(f)
with open("SST-2/vectorizer.pkl", "rb") as f:
    vec = pickle.load(f)

print(type(vec))
print(type(clf.coef_))
print(clf.coef_.shape)

feature_names = vec.get_feature_names_out()
print(feature_names)

weights = pd.DataFrame({
    "feature":feature_names,
    "weight":clf.coef_[0]
})

print("重みの高い特徴量トップ20")
print(weights.sort_values("weight", ascending=False).head(20))

print("----------------")

print("重みの低い特徴量トップ20")
print(weights.sort_values("weight", ascending=True).head(20))
