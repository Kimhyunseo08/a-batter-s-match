import streamlit as st
import random
import time

words = [
    "안녕하세요", "컴퓨터", "학교", "자바스크립트", "파이썬", "타자", "연습", "청소년",
    "생산성", "문서", "보고서", "과제", "키보드", "입력", "속도"
]

sentences = [
    "타자 속도가 빠르면 생각을 더 잘 표현할 수 있습니다.",
    "문서 작성 시간을 줄여 더 많은 일을 할 수 있어요.",
    "효율적인 타자 연습은 청소년들의 학습에 도움이 됩니다.",
    "키보드를 잘 다루면 보고서 작성이 훨씬 수월해집니다.",
    "생산성을 높이려면 꾸준한 연습이 필요합니다."
]

NUM_QUESTIONS = 5

def calculate_wpm(input_text, elapsed_sec):
    chars = len(input_text)
    minutes = elapsed_sec / 60
    if minutes == 0:
        return 0
    return chars / minutes

def calculate_accuracy(target, input_text):
    correct_chars = 0
    for i in range(min(len(target), len(input_text))):
        if target[i] == input_text[i]:
            correct_chars += 1
    if len(input_text) == 0:
        return 0
    return (correct_chars / len(input_text)) * 100

def main():
    st.title("한국어 타자 연습기 - 5문제 연속 연습")

    st.write("""
    ## 문제 정의
    타자 속도가 느린 청소년이 효율적인 문서 작성에 어려움을 겪습니다.

    ## 기능 소개
    - 한국어 단어/문장 타자 연습 5문제 연속 진행
    - 타자 속도(WPM) 및 정확도 계산
    - 연습 기록 저장 및 확인
    """)

    mode = st.radio("연습 모드 선택:", ("단어 연습", "문장 연습"))

    if "quiz_list" not in st.session_state or "quiz_index" not in st.session_state:
        st.session_state["quiz_list"] = []
        st.session_state["quiz_index"] = 0

    if st.button("연습 시작") or len(st.session_state["quiz_list"]) == 0:
        if mode == "단어 연습":
            st.session_state["quiz_list"] = random.sample(words, k=NUM_QUESTIONS)
        else:
            if len(sentences) < NUM_QUESTIONS:
                st.session_state["quiz_list"] = sentences.copy()
            else:
                st.session_state["quiz_list"] = random.sample(sentences, k=NUM_QUESTIONS)
        st.session_state["quiz_index"] = 0
        st.session_state["completed"] = False
        st.session_state["input_text"] = ""
        st.session_state["start_time"] = time.time()

    if st.session_state["quiz_index"] < len(st.session_state["quiz_list"]):
        current_text = st.session_state["quiz_list"][st.session_state["quiz_index"]]
        st.markdown(f"### 문제 {st.session_state['quiz_index']+1} / {len(st.session_state['quiz_list'])}")
        st.markdown(f"> {current_text}")

        input_text = st.text_input("입력:", value=st.session_state.get("input_text", ""), key="typing_input")
        st.session_state["input_text"] = input_text

        if not st.session_state.get("completed", False) and input_text == current_text:
            elapsed = time.time() - st.session_state["start_time"]
            wpm = calculate_wpm(input_text, elapsed)
            accuracy = calculate_accuracy(current_text, input_text)

            st.success(f"정확히 입력하셨습니다! 🎉 소요 시간: {elapsed:.2f}초")
            st.write(f"- 타자 속도(WPM): {wpm:.2f}")
            st.write(f"- 정확도: {accuracy:.2f}%")

            if "records" not in st.session_state:
                st.session_state["records"] = []
            st.session_state["records"].append({
                "mode": mode,
                "text": current_text,
                "time_sec": elapsed,
                "wpm": wpm,
                "accuracy": accuracy
            })

            st.session_state["completed"] = True

            # 입력창 자동 초기화 (결과와 동시에 입력 칸 비우기)
            st.session_state["input_text"] = ""

        if st.session_state.get("completed", False):
            if st.button("다음 문제"):
                st.session_state["quiz_index"] += 1
                st.session_state["completed"] = False
                st.session_state["input_text"] = ""
                st.session_state["start_time"] = time.time()
    else:
        st.success("5문제 모두 완료하셨습니다! 잘 하셨어요 🎉")
        if st.button("다시 5문제 연습하기"):
            st.session_state["quiz_list"] = []
            st.session_state["quiz_index"] = 0
            st.session_state["completed"] = False
            st.session_state["input_text"] = ""

    if "records" in st.session_state and st.session_state["records"]:
        st.markdown("---")
        st.subheader("연습 기록")
        for i, rec in enumerate(st.session_state["records"], 1):
            st.write(f"{i}. [{rec['mode']}] \"{rec['text']}\" — 시간: {rec['time_sec']:.2f}s, WPM: {rec['wpm']:.2f}, 정확도: {rec['accuracy']:.2f}%")

if __name__ == "__main__":
    main()
