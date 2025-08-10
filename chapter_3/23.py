import gzip
import json
import re

file_path = "jawiki-country.json.gz"
uk_text = ''

#タイトルがイギリスのテキストを取得
with gzip.open(file_path, "rt", encoding='utf-8') as f:
    for line in f:
        article = json.loads(line)
        if article["title"] == "イギリス":
            uk_text = article["text"]
            break

#textを改行ごとに分割→リスト
lines = uk_text.splitlines()

#?は非貪欲マッチ、\sはUnicode whitespace [ \t\n\r\f\v]
#findallで指定した正規表現の回数を数える
for line in lines:
    if re.match(r'^=+(.*)=+$', line):

        print((re.match(r'^=+\s*(.*?)\s*=+$', line)).group(1))
        level = int(len(re.findall(r"=", line))/2)-1
        print(f"level:{level}")