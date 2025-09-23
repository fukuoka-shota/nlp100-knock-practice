import pandas as pd

df_dev = pd.read_csv("SST-2/dev.tsv", sep="\t")

s_dev = df_dev["label"]
count_1_dev = (s_dev == 1).sum()
print("dev_tsv:1(ポジティブ)")
print(count_1_dev)
count_0_dev = (s_dev == 0).sum()
print("dev_tsv:1(ネガティブ)")
print(count_0_dev)

print("-----")

df_train = pd.read_csv("SST-2/train.tsv", sep="\t")

s_train = df_train["label"]
count_1_train = (s_train == 1).sum()
print("train_tsv:1(ポジティブ)")
print(count_1_train)
count_0_train = (s_train == 0).sum()
print("train_tsv:1(ネガティブ)")
print(count_0_train)