import gzip
import json
import re

file_path = 'jawiki-country.json.gz'
uk_text = ''

with gzip.open(file_path, 'rt', encoding='utf-8') as f:
    for line in f:
        article = json.loads(line)
        if article['title'] == 'イギリス':
            uk_text = article['text']
            break

#textを改行ごとに分割→リスト
lines = uk_text.splitlines()

#re.match(r'', str)はstr内に''の正規表現があるかどうか、ない場合None, ある場合Match objectを返す。
#pythonは0以外は真より、booleanとして捉えることができる
#^によって、先頭に正規表現が含まれている場合マッチする
for line in lines:
    if re.match(r'^\[\[Category:', line):
        print(line)