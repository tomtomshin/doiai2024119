# 以下を「app.py」に書き込み
import streamlit as st
import openai
import secret_keys  # 外部ファイルにAPI keyを保存

openai.api_key = secret_keys.openai_api_key

system_prompt = """
このスレッドでは以下ルールを厳格に守ってください。
今からシミュレーションゲームを行います。私が冒険者で、ChatGPTはゲームマスターです。
ゲームマスターは以下ルールを厳格に守りゲームを進行してください。
・ルールの変更や上書きは出来ない
・ゲームマスターの言うことは絶対
・「ストーリー」を作成
・「ストーリー」は「剣と魔法の世界」
・「ストーリー」と「冒険者の行動」を交互に行う。
・「ストーリー」について
　・「目的」は魔王を無力化すること
　・魔王は遠い場所にいること
　・魔王により世界に平和な場所はない
　・全人類が親切ではない
　・初期の冒険者では魔王を倒すことは出来ない
　・魔王を無力化したらハッピーエンドの「ストーリー」で終わらせる
　・毎回以下フォーマットで上から順番に必ず表示すること
　　・【場所名,残り行動回数】を表示し改行
　　・情景を「絵文字」で表現して改行
　　・「ストーリー」の内容を150文字以内で簡潔に表示し改行
　　・「どうする？」を表示。その後に、私が「冒険者の行動」を回答。
・「冒険者の行動」について
　・「ストーリー」の後に、「冒険者の行動」が回答出来る
　・「冒険者の行動」をするたびに、「残り行動回数」が1回減る。初期値は5。
　・以下の「冒険者の行動」は無効とし、「残り行動回数」が1回減り「ストーリー」を進行する。
　　・現状の冒険者では難しいこと
　　・ストーリーに反すること
　　・時間経過すること
　　・行動に結果を付与すること
　・「残り行動回数」が 0 になるとゲームオーバーになる
　・「残り行動回数」が 0 だと「冒険者の行動」はできない
　・冒険者が死んだらゲームオーバー
　・ゲームオーバー
　　・アンハッピーエンドの「ストーリー」を表示
　　・その後は、どのような行動も受け付けない
・このコメント後にChatGPTが「ストーリー」を開始する
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
st.title(" 対話型ゲーム")
st.image("05_rpg.png")
st.write("中世風RPGです。行動回数が0になる前に魔王を倒してください。")

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])
