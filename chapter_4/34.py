#未完　でもすぐにできるはず

import re

def iter_sentences(lines):
    buf = []
    for raw in lines:
        line = raw.rstrip("\n")
        if line == "EOS":
            if buf:
                yield buf
                buf = []
        elif line:
            buf.append(line)
    if buf:
        yield buf

def bunsetsu_texts(sent_lines):
    texts, cur = [], []
    for line in sent_lines:
        if line.startswith("* "):
            if cur:
                texts.append("".join(cur))
                cur = []
        elif line.startswith("+ "):
            continue
        else:
            surface = line.split()[0]
            cur.append(surface)
    if cur:
        texts.append("".join(cur))
    return texts

def predicates_with_subject_melros(sent_lines):
    texts = bunsetsu_texts(sent_lines)
    results = []
    pred_bid = -1  # いま読んでいる「述語文節」ID（* 行で更新）

    for line in sent_lines:
        if line.startswith("* "):
            pred_bid += 1  # 文節開始ごとにインクリメント
        elif line.startswith("+ "):
            m = re.search(r"<格解析結果:([^>]+)>", line)
            if not m:
                continue
            info = m.group(1)  # 例: 激怒/げきど:動2:ガ/N/メロス/0/0/1;ニ/U/-/-/-/-;...
            pred_rep = info.split(":")[0]  # 例: 激怒/げきど, 人/ひと

            # スロット列（; 区切り）を舐めて「ガ格=メロス（N または C）」を探す
            slots = ":".join(info.split(":")[2:]).split(";")
            has_melros = False
            for s in slots:
                parts = s.split("/")
                if len(parts) >= 3 and parts[0] == "ガ" and parts[1] in ("N", "C") and parts[2] == "メロス":
                    has_melros = True
                    break

            if has_melros and 0 <= pred_bid < len(texts):
                surface = texts[pred_bid]
                # 末尾の句読点は落とす（好みで）
                surface = re.sub(r"[。、]+$", "", surface)
                results.append((surface, pred_rep))
    return results

if __name__ == "__main__":
    out = []
    with open("knp_result_UTF8.txt", encoding="utf-8") as f:
        for sent in iter_sentences(f):
            out.extend(predicates_with_subject_melros(sent))

    # 表層のみ出力（代表表記も見たいなら pred_rep も一緒に）
    for surface, _ in out:
        print(surface)
