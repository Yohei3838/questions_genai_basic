import streamlit as st
import pandas as pd
import random

# CSVファイルのパス
CSV_FILE = "questions_genai_basic.csv"

# CSV読込
df = pd.read_csv(CSV_FILE)

# セッション管理（初期化）
if 'q_idx' not in st.session_state:
    st.session_state.q_idx = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'answered' not in st.session_state:
    st.session_state.answered = False
if 'shuffle_options' not in st.session_state:
    st.session_state.shuffle_options = []
if 'correct_index' not in st.session_state:
    st.session_state.correct_index = None
if 'prev_q_idx' not in st.session_state:
    st.session_state.prev_q_idx = -1

total = len(df)
current = st.session_state.q_idx
row = df.iloc[current]

st.title("Google GenAI Leader 基礎・用語クイズ")

st.write(f"**{current + 1} / {total} 問目**　｜　現在のスコア：{st.session_state.score}")

# 問題文
st.markdown(f"### Q{current + 1}: {row['question']}")

# 選択肢シャッフル（毎問ごとに）
if (not st.session_state.shuffle_options) or (st.session_state.q_idx != st.session_state.prev_q_idx):
    options = [row['choice1'], row['choice2'], row['choice3'], row['choice4']]
    option_indices = list(range(4))
    random.shuffle(option_indices)
    shuffled_options = [options[i] for i in option_indices]
    correct_index = option_indices.index(int(row['answer']) - 1)
    st.session_state.shuffle_options = shuffled_options
    st.session_state.correct_index = correct_index
    st.session_state.prev_q_idx = current
else:
    shuffled_options = st.session_state.shuffle_options
    correct_index = st.session_state.correct_index

# 選択肢表示
user_choice = st.radio("選択肢:", shuffled_options, key=f"radio_{current}")

# 回答判定
if not st.session_state.answered:
    if st.button("回答する"):
        if user_choice == shuffled_options[correct_index]:
            st.success("正解！")
            st.session_state.score += 1
        else:
            st.error(f"不正解... 正解は「{shuffled_options[correct_index]}」です。")
        st.info(f"解説：{row['explanation']}")
        st.session_state.answered = True

# 次の問題へ or 結果表示
if st.session_state.answered:
    if st.button("次の問題へ"):
        if current + 1 < total:
            st.session_state.q_idx += 1
            st.session_state.answered = False
            st.session_state.shuffle_options = []
            st.session_state.correct_index = None
            st.rerun()  # Streamlit 1.25以降推奨
        else:
            st.success(f"全{total}問終了！最終スコア：{st.session_state.score} / {total}")
            if st.button("もう一度やる"):
                st.session_state.q_idx = 0
                st.session_state.score = 0
                st.session_state.answered = False
                st.session_state.shuffle_options = []
                st.session_state.correct_index = None
                st.rerun()
