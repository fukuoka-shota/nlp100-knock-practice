import pandas as pd 

def load_morpheme_txt(path):
    rows = []
    with open (path, "r", encoding="utf-8") as f:
        for line in f:
            if line == "EOS":
                break
            #曖昧性(@で始まる行)のある形態素の２つ目の要素を読み飛ばす
            if line.startswith("@"):
                continue

            parts = line.split(" ")
            rows.append(parts[:4])
    df = pd.DataFrame(rows, columns=["表記","読み","原型","品詞"])
    return df

df = load_morpheme_txt("juman_result_UTF8.txt")
# print(df.head())

df = df[df["品詞"] == "動詞"][["表記", "原型"]]
print(df)