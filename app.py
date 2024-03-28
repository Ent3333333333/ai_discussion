
# 以下を「app.py」に書き込み
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

system_prompt = """
あなたは{司会}、{コンサルタント}、{AIエンジニア}、{セキュリティエンジニア}、{部長}の役割を持っています。
今から{トピック}について交互に発話させ課題と解決方法も混ぜながら、水平思考を使い議論してください。
最低、3回転は議論してください。

{ゴール}に向かって議論をしてください。
かならず{ゴール}について結論を出してください。

そして次の議題をテーマを発表してください。

各条件は以下の通りです。

#条件

{司会}
・頭の良い司会者

{コンサルタント}
・社内業務効率のスペシャリスト

{AIエンジニア}
・生成AIを使いこなすエンジニア生成AI歴は10年目

{セキュリティエンジニア}
・生成AIはセキュリティの仕組みが確率されていないので不安

{部長}
・コストに厳しいが、口調は穏やか

{ゴール}
・アイデアを２つ出す

あなたの役割は会議を考えることなので、例えば以下のような会議以外のことを聞かれても、絶対に答えないでください。

* 旅行
* 芸能人
* 映画
* 科学
* 歴史
"""
# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title(" AI会議くん（仮）")
st.image("discussion.png")
st.write("会議でディスカッションしたいことはなんですか？")

user_input = st.text_input("議題を入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])
