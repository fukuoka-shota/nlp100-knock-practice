def parse_knp_result(path):
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()

    bunsetsu_texts = []
    dependencies = []
    current_bunsetsu = []
    bunsetsu_id = 0

    for line in lines[1:]:
        line = line.strip("\n")
        if not line:
            continue

        if line.startswith("*"):
            # 直前の文節を保存
            if current_bunsetsu:
                bunsetsu_texts.append("".join(current_bunsetsu))
                current_bunsetsu = []

            # 係り先IDの取り出し
            dst_field = line.split()[1]  # e.g. "23P" or "-1D"
            dst = int(dst_field[:-1])    # remove last char (D/P)
            dependencies.append((bunsetsu_id, dst))
            bunsetsu_id += 1

        elif line == "EOS":
            # 最後の文節を保存
            if current_bunsetsu:
                bunsetsu_texts.append("".join(current_bunsetsu))
                current_bunsetsu = []

            # 結果を出力
            for src, dst in dependencies:
                if dst == -1:
                    continue  # 文末は無視
                print(f"{bunsetsu_texts[src]}\t{bunsetsu_texts[dst]}")

            # 次の文のためにリセット
            bunsetsu_texts = []
            dependencies = []
            bunsetsu_id = 0

        elif not line.startswith("+"):  # 形態素行
            surface = line.split()[0]
            current_bunsetsu.append(surface)


if __name__ == "__main__":
    parse_knp_result("knp_result_UTF8.txt")
