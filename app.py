import streamlit as st
import pandas as pd

# CSV読み込み
df = pd.read_csv("questions_genai_basic.csv")

st.title("Google GenAI Leader 基礎・用語クイズ")

score = 0
user_answers = []
st.write("全20問、各問題の選択肢から正しいものを選んでください。")

# 問題ループ
for i, row in df.iterrows():
    st.markdown(f"**Q{i+1}: {row['question']}**")
    options = [row['choice1'], row['choice2'], row['choice3'], row['choice4']]
    user_choice = st.radio(
        f"選択してください（Q{i+1}）:",
        options,
        key=f"q_{i}"
    )
    user_answers.append(user_choice)

# 結果表示ボタン
if st.button("採点する"):
    score = 0
    st.markdown("---")
    st.subheader("解答結果・解説")
    for i, row in df.iterrows():
        answer_idx = int(row["answer"]) - 1
        correct = options[answer_idx]
        user_choice = user_answers[i]
        if user_choice == options[answer_idx]:
            st.success(f"Q{i+1}：正解！")
            score += 1
        else:
            st.error(f"Q{i+1}：不正解（あなたの回答：{user_choice} / 正解：{options[answer_idx]}）")
        st.info(f"解説：{row['explanation']}")
        st.markdown("---")
    st.subheader(f"最終スコア： {score} / {len(df)}")
