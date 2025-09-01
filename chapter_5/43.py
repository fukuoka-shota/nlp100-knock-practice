import google.generativeai as genai
import os
import csv
import random

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

def create_prompt(question, choices, prompt_type="standard", choice_symbols=None):
    """プロンプトを作成する"""
    if choice_symbols is None:
        choice_symbols = ["A", "B", "C", "D"]
    if prompt_type == "standard":
        prompt = f"""
以下の問題に対して、選択肢{choice_symbols[0]}、{choice_symbols[1]}、{choice_symbols[2]}、{choice_symbols[3]}の中から最も適切なものを1つ選んでください。
回答は選択肢の記号（{choice_symbols[0]}、{choice_symbols[1]}、{choice_symbols[2]}、{choice_symbols[3]}）のみを返してください。

問題：{question}

選択肢：
{choice_symbols[0]}. {choices[0]}
{choice_symbols[1]}. {choices[1]}
{choice_symbols[2]}. {choices[2]}
{choice_symbols[3]}. {choices[3]}
"""
    elif prompt_type == "detailed":
        prompt = f"""
以下の問題に対して、選択肢{choice_symbols[0]}、{choice_symbols[1]}、{choice_symbols[2]}、{choice_symbols[3]}の中から最も適切なものを1つ選んでください。
回答は選択肢の記号（{choice_symbols[0]}、{choice_symbols[1]}、{choice_symbols[2]}、{choice_symbols[3]}）のみを返してください。
各選択肢を慎重に検討し、最も正確な回答を選んでください。

問題：{question}

選択肢：
{choice_symbols[0]}. {choices[0]}
{choice_symbols[1]}. {choices[1]}
{choice_symbols[2]}. {choices[2]}
{choice_symbols[3]}. {choices[3]}
"""
    elif prompt_type == "concise":
        prompt = f"""
問題：{question}

選択肢：
{choice_symbols[0]}. {choices[0]}
{choice_symbols[1]}. {choices[1]}
{choice_symbols[2]}. {choices[2]}
{choice_symbols[3]}. {choices[3]}

回答（{choice_symbols[0]}、{choice_symbols[1]}、{choice_symbols[2]}、{choice_symbols[3]}のいずれか）：
"""

    return prompt

def shuffle_choices(choices, answer):
    """選択肢の順番をシャッフルする"""
    # 選択肢とインデックスのペアを作成
    #indexed_choicesはタプルのリスト　[(0, "選択肢A1"), (1, "選択肢B1"), (2, "選択肢C1"), (3, "選択肢D1")]
    indexed_choices = list(enumerate(choices))
    # シャッフル
    random.shuffle(indexed_choices)
    # 新しい順番の選択肢と、元のインデックスを取得
    new_choices = [c[1] for c in indexed_choices]
    # 正解のインデックスを更新
    #ordでunicode値に変換
    #ord("B")-ord("A")=66-65=1
    #list.index(x)はリストの中で、最初にxと等しい要素のインデックスを返すメソッド
    old_index = ord(answer) - ord("A")
    new_index = indexed_choices.index((old_index, choices[old_index]))
    #chrでunicodeポイントを文字に変換
    new_answer = chr(ord("A") + new_index)

    return new_choices, new_answer

def evaluate_model(settings,num_questions=1):
    dataset_path = "anatomy.csv"
    
    questions = load_jmmlu_data(dataset_path)

    # questions[:None] は questions[:] と同じ意味
    questions = questions[:num_questions]

    # 各設定での結果を格納する辞書
    results = {}

    #各設定で評価
    for setting_name, setting in settings.items():
        print(f"\n設定:{setting_name}")
        #これはdict.get(key,default)の形で使う。keyに対応する値を返し、keyが辞書に存在しない場合、defaultを返す
        #settingにはこの時点で、一つ内側の辞書が格納されていることに注意
        print(
            f"温度: {setting.get('temperature', 0.7)}, プロンプトタイプ: {setting.get('prompt_type', 'standard')}"
        )
        
        # モデルの設定
        model = genai.GenerativeModel(
            "gemini-1.5-flash",
            generation_config={"temperature": setting.get("temperature", 0.7)},
        )

        correct_count = 0
        total_questions = len(questions)

        for i, q in enumerate(questions, 1):
            # 選択肢の順番をシャッフルするかどうか
            if setting.get("shuffle_choices", False):
                shuffled_choices, shuffled_answer = shuffle_choices(
                    q["choices"], q["answer"]
                )
                choices = shuffled_choices
                answer = shuffled_answer
            else:
                choices = q["choices"]
                answer = q["answer"]

            # 選択肢の記号を変更するかどうか
            choice_symbols = setting.get("choice_symbols", ["A", "B", "C", "D"])

            # プロンプトの作成
            prompt = create_prompt(
                q["question"],
                choices,
                setting.get("prompt_type", "standard"),
                choice_symbols,
            )

            try:
                # APIリクエストの送信
                response = model.generate_content(prompt)
                model_answer = response.text.strip().upper()

                # 選択肢の記号が変更されている場合、回答を変換
                if choice_symbols != ["A", "B", "C", "D"]:
                    # 元の記号に変換
                    symbol_map = {
                        choice_symbols[i]: chr(ord("A") + i) for i in range(4)
                    }
                    model_answer = symbol_map.get(model_answer, model_answer)

                # 正解判定
                #model_anwser == answerでbool型に変換され、それがis_xorrectに入る
                is_correct = model_answer == answer
                #int(bool)でtrueなら１、falseが0に変換される
                correct_count += int(is_correct)

                # 進捗表示
                #:.1fで小数点以下一桁
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

        # 結果を保存
        results[setting_name] = {
            "correct_count": correct_count,
            "total_questions": total_questions,
            "accuracy": final_accuracy,
        }

    return results


def run_experiments(num_questions=10):
    """様々な実験設定で評価を実行する"""
    # 実験設定
    settings = {
        "標準設定": {
            "temperature": 0.7,
            "prompt_type": "standard",
            "shuffle_choices": False,
            "choice_symbols": ["A", "B", "C", "D"],
        },
        "低温度": {
            "temperature": 0.1,
            "prompt_type": "standard",
            "shuffle_choices": False,
            "choice_symbols": ["A", "B", "C", "D"],
        },
        "高温度": {
            "temperature": 1.0,
            "prompt_type": "standard",
            "shuffle_choices": False,
            "choice_symbols": ["A", "B", "C", "D"],
        },
        "詳細プロンプト": {
            "temperature": 0.7,
            "prompt_type": "detailed",
            "shuffle_choices": False,
            "choice_symbols": ["A", "B", "C", "D"],
        },
        "簡潔プロンプト": {
            "temperature": 0.7,
            "prompt_type": "concise",
            "shuffle_choices": False,
            "choice_symbols": ["A", "B", "C", "D"],
        },
        "選択肢シャッフル": {
            "temperature": 0.7,
            "prompt_type": "standard",
            "shuffle_choices": True,
            "choice_symbols": ["A", "B", "C", "D"],
        },
        "数字記号": {
            "temperature": 0.7,
            "prompt_type": "standard",
            "shuffle_choices": False,
            "choice_symbols": ["1", "2", "3", "4"],
        },
    }

    # 評価実行
    results = evaluate_model(settings, num_questions)

    # 結果の比較
    print("\n\n実験結果の比較:")
    print("=" * 50)
    print(f"{'設定名':<15} {'正解数':<10} {'正解率':<10}")
    print("-" * 50)

    for setting_name, result in results.items():
        print(
            f"{setting_name:<15} {result['correct_count']}/{result['total_questions']:<10} {result['accuracy']:.1f}%"
        )

    print("=" * 50)

if __name__ == "__main__":
    # 評価する問題数を全問題数に設定
    num_questions = 10  # Noneを指定すると全問題を評価

    run_experiments(num_questions)