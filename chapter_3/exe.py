import re

import pandas as pd


def remove_stress(dc):
    r = re.compile("'+")
    return {k: r.sub("", v) for k, v in dc.items()}


def remove_inner_links(dc):
    r = re.compile(r"\[\[(.+\||)(.+?)\]\]")
    return {k: r.sub(r"\2", v) for k, v in dc.items()}


def remove_mk(v):
    r1 = re.compile("'+")
    r2 = re.compile(r"\[\[(.+\||)(.+?)\]\]")
    r3 = re.compile(r"\{\{(.+\||)(.+?)\}\}")
    r4 = re.compile(r"<\s*?/*?\s*?br\s*?/*?\s*>")
    v = r1.sub("", v)
    v = r2.sub(r"\2", v)
    v = r3.sub(r"\2", v)
    v = r4.sub("", v)
    return v


df = pd.read_json("jawiki-country.json.gz", lines=True)
uk_text = df.query('title=="イギリス"')["text"].values[0]
uk_texts = uk_text.split("\n")

pattern = re.compile(r"\|(.+?)\s=\s*(.+)")
ans = {}
for line in uk_texts:
    r = re.search(pattern, line)
    if r:
        ans[r[1]] = r[2]

r = re.compile(r"\[\[(.+\||)(.+?)\]\]")
ans = {k: r.sub(r"\2", remove_mk(v)) for k, v in ans.items()}
dict = remove_inner_links(remove_stress(ans))

for k, v in dict.items():
    print(k,v)