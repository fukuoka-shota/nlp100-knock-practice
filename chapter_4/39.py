import json
import gzip
import re
import MeCab
import matplotlib.pyplot as plt
from collections import Counter
import japanize_matplotlib

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

def plot_word_frequency_rank():
    # MeCabの初期化
    mecab = MeCab.Tagger("-Owakati")

    # 単語の出現頻度をカウントするためのCounter
    word_counter = Counter()

    # gzipファイルを読み込む
    with gzip.open("jawiki-country.json.gz", "rt", encoding="utf-8") as f:
        for line in f:
            article = json.loads(line)
            text = article["text"]

            # マークアップを除去
            text = remove_markup(text)

            # 形態素解析を行い、単語をカウント
            words = mecab.parse(text).strip().split()
            word_counter.update(words)

    # 出現頻度の順位と頻度を取得
    frequencies = list(word_counter.values())
    frequencies.sort(reverse=True)
    ranks = range(1, len(frequencies) + 1)

    # グラフの描画
    japanize_matplotlib.japanize()
    plt.figure(figsize=(10, 6))
    plt.loglog(ranks, frequencies, "b-", label="単語の出現頻度")
    plt.grid(True)
    plt.xlabel("出現頻度順位")
    plt.ylabel("出現頻度")
    plt.title("単語の出現頻度順位と出現頻度の関係（Zipfの法則）")
    plt.legend()

    # グラフを保存
    plt.savefig("word_frequency_rank.png")
    plt.close()


if __name__ == "__main__":
    plot_word_frequency_rank()