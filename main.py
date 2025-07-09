import streamlit as st
import random
import time

words = [
    "안녕하세요", "컴퓨터", "학교", "자바스크립트", "파이썬", "타자", "연습", "청소년",
    "생산성", "문서", "보고서", "과제", "키보드", "입력", "속도"
]

sentences = [
    "사랑해줘서 고마워.",
    "내생명은 네거야 홍지승 그러니 너를위해 사용하겠어.",
    "귀중하고 소중한건 언제나 곁에있어 하지만 그게 당연해지면 알지 못하게돼.",
    "자아 걱정할건 아무것도 없어 다들앞만 봐 등뒤는 내가 지켜줄게.",
    "아무것도 갖고 태어나지 않았기에 무엇이든  될수있다."
    "막힘없이 흘러라! 우리들은 혈액이다!"
    "자신을 믿지 않는 녀석 따위는 노력할 가치도 없어!!"
    "먹을 수 있는건 죄다 먹어치우고 자기보다 강한자는 이용하고 살아남는다."
    "할 수 있냐 , 없냐는 중요하지 않아.하고 싶으니까 하는거야."
    "재능은 꽃피우는것 센스는 갈고 닦는것"
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

# 다음 문제로 넘어가는 함수
def next_question():
    st.session_state["quiz_index"] += 1
    st.session_state["completed"] = False
    st.session_state["input_text"] = ""
    st.session_state["start_time"] = time.time()

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
            st.session_state["input_text"] = ""  # 결과 출력과 동시에 입력칸 비우기

        if st.session_state.get("completed", False):
            st.button("다음 문제", on_click=next_question)

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
