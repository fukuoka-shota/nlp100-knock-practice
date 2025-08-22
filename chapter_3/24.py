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

#[^a]はa以外のあらゆる文字にマッチ、()がキャプチャ
#|と]以外のあらゆる文字にマッチさせる
prog = re.compile(r'\[\[ファイル:([^|\]]+)')
#非重複のリストを返す
files = re.findall(prog, uk_text)

for file in files:
    print(file)