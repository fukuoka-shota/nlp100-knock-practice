import google.generativeai as genai
import os
import csv

api_key = os.getenv("GOOGLE_API_KEY")

# APIキーを設定
genai.configure(api_key=api_key)

# モデルの設定
model = genai.GenerativeModel("gemini-1.5-flash")

def load_jmmlu_data(file_path):
    """JMMLUのデータセットを読み込む"""
    #返り値は辞書のリスト
    data = []
    with open(file_path, "r", encoding="utf-8") as f:
        #csv.readerオブジェクトは行を反復処理するイテレータで、for文で行ごとのデータをリストで取得できる
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 6:  # 問題、選択肢A、B、C、D、正解の6列があることを確認
                data.append({"question": row[0], "choices": row[1:5], "answer": row[5]})
    #リストの中に辞書を入れた形式で返している。
    # {
    #     "question": "問題文1",
    #     "choices": ["選択肢A1", "選択肢B1", "選択肢C1", "選択肢D1"],
    #     "answer": "正解1"
    # }
    return data

def create_prompt(question, choices):
    """プロンプトを作成する"""
    prompt = f"""
以下の問題に対して、選択肢A、B、C、Dの中から最も適切なものを1つ選んでください。
回答は選択肢のアルファベット（A、B、C、D）のみを返してください。

問題：{question}

選択肢：
A. {choices[0]}
B. {choices[1]}
C. {choices[2]}
D. {choices[3]}
"""
    return prompt

def evaluate_model(num_questions=1):
    dataset_path = "anatomy.csv"
    
    questions = load_jmmlu_data(dataset_path)

    # questions[:None] は questions[:] と同じ意味
    questions = questions[:num_questions]

    correct_count = 0
    total_questions = len(questions)
    total_available = len(load_jmmlu_data(dataset_path))

    print(f"科目: anatomy")
    print(f"問題数: {total_questions} (全{total_available}問中)")
    print("評価を開始します...")

    for i, q in enumerate(questions, 1):
        #iは1からindexをふる
        #プロンプトの作成
        prompt = create_prompt(q["question"], q["choices"])

        try:
            # APIリクエストの送信
            response = model.generate_content(prompt,)
            #strip()で前後の空白を除去、upper()で文字列の小文字を大文字に変換
            answer = response.text.strip().upper()

            # 正解判定
            is_correct = answer == q["answer"]
            correct_count += int(is_correct)

            # 進捗表示
            print(
                f"\r進捗: {i}/{total_questions} (正解率: {correct_count / i * 100:.1f}%)",
                end="",
            )

        except Exception as e:
            print(f"\nエラー: {e}")
            continue

    # 最終結果の表示
    final_accuracy = correct_count / total_questions * 100
    print("\n\n評価結果:")
    print(f"正解数: {correct_count}/{total_questions}")
    print(f"正解率: {final_accuracy:.1f}%")


if __name__ == "__main__":
    # 評価する問題数を全問題数に設定
    num_questions = None  # Noneを指定すると全問題を評価

    evaluate_model(num_questions)