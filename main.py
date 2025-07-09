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
    st.title("한국어 타자 연습기")

    st.write("""
    ## 문제 정의
    타자 속도가 느린 청소년이 효율적인 문서 작성에 어려움을 겪습니다.

    ## 기능 소개
    - 한국어 단어/문장 타자 연습
    - 타자 속도(WPM) 및 정확도 계산
    - 연습 기록 저장 및 확인
    """)

    mode = st.radio("연습 모드 선택:", ("단어 연습", "문장 연습"))

    if "completed" not in st.session_state:
        st.session_state["completed"] = False

    start_clicked = st.button("연습 시작")

    if start_clicked or "target_text" not in st.session_state:
        if mode == "단어 연습":
            target = random.choice(words)
        else:
            target = random.choice(sentences)

        st.session_state["target_text"] = target
        st.session_state["start_time"] = time.time()
        st.session_state["input_text"] = ""
        st.session_state["completed"] = False

    if "target_text" in st.session_state:
        target_text = st.session_state["target_text"]
        st.markdown(f"### 다음 내용을 타이핑하세요:\n\n> {target_text}")

        input_text = st.text_input("입력:", value=st.session_state.get("input_text", ""), key="typing_input")
        st.session_state["input_text"] = input_text

        if not st.session_state["completed"] and input_text == target_text:
            elapsed = time.time() - st.session_state["start_time"]
            wpm = calculate_wpm(input_text, elapsed)
            accuracy = calculate_accuracy(target_text, input_text)

            st.success(f"정확히 입력하셨습니다! 🎉 소요 시간: {elapsed:.2f}초")
            st.write(f"- 타자 속도(WPM): {wpm:.2f}")
            st.write(f"- 정확도: {accuracy:.2f}%")

            # 연습 기록 저장
            if "records" not in st.session_state:
                st.session_state["records"] = []
            st.session_state["records"].append({
                "mode": mode,
                "text": target_text,
                "time_sec": elapsed,
                "wpm": wpm,
                "accuracy": accuracy
            })

            st.session_state["completed"] = True

        if st.session_state["completed"]:
            if st.button("다시 연습하기"):
                del st.session_state["target_text"]
                del st.session_state["start_time"]
                del st.session_state["input_text"]
                st.session_state["completed"] = False

    if "records" in st.session_state and st.session_state["records"]:
        st.markdown("---")
        st.subheader("연습 기록")
        for i, rec in enumerate(st.session_state["records"], 1):
            st.write(f"{i}. [{rec['mode']}] \"{rec['text']}\" — 시간: {rec['time_sec']:.2f}s, WPM: {rec['wpm']:.2f}, 정확도: {rec['accuracy']:.2f}%")

if __name__ == "__main__":
    main()
