import gzip
import json
import re
import MeCab
import  pandas as pd

def remove_markup(text):
    #prog_1:強調マークアップの除去
    #prog_2:内部リンクの除去
    #prog_3:外部リンクの除去 [http:...]
    #prog_4:タグ<...>の除去
    #prog_5:テンプレート{{...}}の除去
    #prog_6:基礎情報テンプレートの除去
    #prog_7:見出しの除去
    #prog_8:ファイルの除去
    #prog_9:コメントアウトの除去
    #prog_10:箇条書き(*の行)の除去、|で始まる行の削除
    #prog_11:space+|で始まる行の除去
    #prog_12:{{,}},()の削除
    #prog_13:2連続以上の改行を２の改行にする
    prog_1 = re.compile(r"'{2,5}")
    prog_2 = re.compile(r"\[\[(?:[^|]*\|)??([^|]*?)\]\]")
    prog_3 = re.compile(r"\[http[^\]]+\]")
    prog_4 = re.compile(r"\<.+?\>")
    prog_5 = re.compile(r"\{\{.*?\}\}")
    prog_6 = re.compile(r"{{基礎情報.*?\n.*?\n}}",re.DOTALL)
    prog_7 = re.compile(r"={2,}")
    prog_8 = re.compile(r"\[\[ファイル:.*?\]\]")
    prog_9 = re.compile(r"\<\!--.*--\>",re.DOTALL)
    #[]は文字の集合を表す
    prog_10 = re.compile(r"^[*#:;|].*$",re.MULTILINE)
    prog_11 = re.compile(r"^ \|.*$",re.MULTILINE)
    prog_12 = re.compile(r"\{\{|\}\}|\(\)")
    prog_13 = re.compile(r"\n{2,}")
    text = prog_1.sub("", text)
    text = prog_2.sub(r"\1", text)
    text = prog_3.sub("", text)
    text = prog_4.sub("", text)
    text = prog_5.sub("", text)
    text = prog_6.sub("", text)
    text = prog_7.sub("", text)
    text = prog_8.sub("", text)
    text = prog_9.sub("", text)
    text = prog_10.sub("", text)
    text = prog_11.sub("", text)
    text = prog_12.sub("", text)
    text = prog_13.sub("\n\n", text)

    return text

def word_frequency_df():
    mecab = MeCab.Tagger()
    
    with gzip.open("jawiki-country.json.gz", "rt", encoding="utf-8") as f:
        rows = []
        for line in f:
            article = json.loads(line)
            text = remove_markup(article["text"])

            parsed_lines = mecab.parse(text)
            
            for parsed_line in parsed_lines.splitlines():
                if not parsed_line or parsed_line == "EOS":
                    continue

                parts = parsed_line.split("\t")

                #基本的に「表層形\t品詞情報,...」
                if len(parts) < 2:
                    continue 
                surface = parts[0]
                if surface.isspace():
                    continue
                features = parts[1].split(",")
                hinshi = features[0] if features else ""
                rows.append([surface,hinshi])
        df = pd.DataFrame(rows, columns=["表層形","品詞"])
        return df

if __name__ == "__main__":
    df = word_frequency_df()
    df = df[df["品詞"]=="名詞"]
    #pandas.Series.value_count()はユニークな要素の値をインデックス、その個数を要素とするSeriesを返す
    freq = df["表層形"].value_counts()
    #Seriesに対して.reset_index()メソッドを使うと、元のindexは"index"列となり、値は"0"列に入る
    top20_df = freq.head(20).reset_index()
    top20_df.columns = ["表層形","出現頻度"]
    print(top20_df)