import google.generativeai as genai
import os

api_key = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-1.5-flash")

prompt = """
以下の川柳の面白さをそれぞれ10段階で評価してください。形式は以下の通りです。
川柳 : 評価する川柳
評価 : 1-10の整数
理由 : 評価理由

評価する川柳
1. 温かい言葉　感謝の心　胸に咲く
2. 些細なことにも　感謝の雨　降る日和
3. 笑顔一つで　感謝伝わる　幸せかな
4. 無言の支えに　深き感謝を　胸に抱く
5. 助けられた命　感謝の涙　溢れ出す
6. 言葉足らずも　感謝の気持ち　伝わると信じる
7. 毎日の暮らし　感謝の粒　積み重ねて
8. 大きな愛に　小さな感謝を　贈りたい
5. 助けられた命　感謝の涙　溢れ出す
6. 言葉足らずも　感謝の気持ち　伝わると信じる
9. 気づけば感謝　溢れる日々　幸せだね
10. ありがとうと　心から言う　至福の時
"""

response = model.generate_content(prompt)

print("解答:")
print(response.text)