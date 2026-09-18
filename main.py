import streamlit as st
import random
import time

st.set_page_config(
    page_title="오늘 뭐 먹지? 🍽️",
    page_icon="🍕",
    layout="centered"
)

# ---------------------------
# CSS
# ---------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #fff7fb 0%, #fff9e8 100%);
}

.block-container {
    max-width: 720px;
    padding-top: 2rem;
}

h1 {
    text-align: center;
    color: #ff668c;
}

.subtitle {
    text-align: center;
    color: #777;
    font-size: 18px;
    margin-bottom: 25px;
}

.food-box {
    background: white;
    border: 3px solid #ffb6ca;
    border-radius: 25px;
    padding: 25px;
    text-align: center;
    box-shadow: 0 8px 20px rgba(255, 120, 150, 0.15);
    margin: 20px 0;
}

.food-emoji {
    font-size: 70px;
}

.food-name {
    font-size: 35px;
    font-weight: 800;
    color: #ff527d;
    margin-top: 5px;
}

.spinning {
    background: white;
    border: 3px dashed #ffb6ca;
    border-radius: 50%;
    width: 230px;
    height: 230px;
    margin: 25px auto;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 65px;
    box-shadow: 0 8px 25px rgba(255, 120, 150, 0.18);
}

.message {
    background: #fff0f5;
    padding: 15px;
    border-radius: 18px;
    text-align: center;
    font-size: 17px;
    margin-top: 15px;
}

.small-title {
    font-size: 20px;
    font-weight: bold;
    color: #ff668c;
    margin-top: 15px;
}

div.stButton > button {
    width: 100%;
    border: none;
    border-radius: 18px;
    padding: 12px;
    font-size: 18px;
    font-weight: bold;
    background: #ff85a5;
    color: white;
    transition: 0.2s;
}

div.stButton > button:hover {
    background: #ff668c;
    color: white;
    transform: scale(1.02);
}
</style>
""", unsafe_allow_html=True)


# ---------------------------
# 메뉴 데이터
# ---------------------------
menus = {
    "🍚 한식": [
        ("🥘", "김치찌개"),
        ("🍲", "부대찌개"),
        ("🥩", "삼겹살"),
        ("🍚", "비빔밥"),
        ("🌶️", "제육볶음"),
        ("🐔", "닭갈비"),
        ("🍖", "갈비"),
        ("🥣", "국밥"),
        ("🍜", "칼국수"),
        ("🥞", "김치전"),
    ],

    "🍝 양식": [
        ("🍝", "파스타"),
        ("🍕", "피자"),
        ("🍔", "햄버거"),
        ("🥩", "스테이크"),
        ("🥗", "샐러드"),
        ("🌯", "브리또"),
        ("🥪", "샌드위치"),
    ],

    "🥟 중식": [
        ("🍜", "짜장면"),
        ("🍜", "짬뽕"),
        ("🥟", "만두"),
        ("🍖", "탕수육"),
        ("🌶️", "마라탕"),
        ("🍚", "볶음밥"),
    ],

    "🍣 일식": [
        ("🍣", "초밥"),
        ("🍜", "라멘"),
        ("🍛", "카레"),
        ("🍱", "돈까스"),
        ("🍲", "우동"),
        ("🐙", "타코야키"),
        ("🍚", "규동"),
    ],

    "🍗 분식/야식": [
        ("🌶️", "떡볶이"),
        ("🍗", "치킨"),
        ("🍜", "라면"),
        ("🥟", "튀김"),
        ("🍙", "김밥"),
        ("🌭", "핫도그"),
    ]
}


# ---------------------------
# 세션 상태
# ---------------------------
if "result" not in st.session_state:
    st.session_state.result = None

if "count" not in st.session_state:
    st.session_state.count = 0


# ---------------------------
# 제목
# ---------------------------
st.title("🍽️ 오늘 뭐 먹지? 🎡")

st.markdown(
    '<div class="subtitle">저녁 메뉴 고민은 이제 룰렛에게 맡겨버리자 ✨</div>',
    unsafe_allow_html=True
)

st.markdown("### 🩷 오늘 어떤 게 땡겨?")


category = st.selectbox(
    "메뉴 종류를 골라줘!",
    ["🌎 아무거나"] + list(menus.keys())
)


# ---------------------------
# 후보 메뉴 만들기
# ---------------------------
if category == "🌎 아무거나":
    candidates = []

    for food_list in menus.values():
        candidates.extend(food_list)

else:
    candidates = menus[category]


# 현재 후보 메뉴 표시
with st.expander("👀 룰렛에 들어있는 메뉴 보기"):
    names = [food[1] for food in candidates]
    st.write(" · ".join(names))


st.markdown("---")


# ---------------------------
# 룰렛
# ---------------------------
st.markdown("### 🎡 운명의 저녁 룰렛")

roulette_area = st.empty()


if st.session_state.result is None:

    roulette_area.markdown(
        """
        <div class="spinning">
            🍽️
        </div>
        """,
        unsafe_allow_html=True
    )


# ---------------------------
# 룰렛 돌리기
# ---------------------------
button_text = "🎡 룰렛 돌리기!"

if st.session_state.count > 0:
    button_text = "🔄 마음에 안 들어... 다시 돌리기"


if st.button(button_text):

    st.session_state.count += 1

    # 돌아가는 느낌의 애니메이션
    spin_emojis = [
        "🍕", "🍔", "🍜", "🍣",
        "🍗", "🥘", "🥟", "🍝",
        "🌮", "🍛"
    ]

    for i in range(15):

        emoji = random.choice(spin_emojis)

        roulette_area.markdown(
            f"""
            <div class="spinning">
                {emoji}
            </div>
            """,
            unsafe_allow_html=True
        )

        # 뒤로 갈수록 천천히
        time.sleep(0.04 + i * 0.012)


    st.session_state.result = random.choice(candidates)


# ---------------------------
# 결과 출력
# ---------------------------
if st.session_state.result:

    emoji, food = st.session_state.result

    roulette_area.markdown(
        f"""
        <div class="food-box">
            <div style="font-size:18px;">
                🎊 오늘의 저녁은...
            </div>

            <div class="food-emoji">
                {emoji}
            </div>

            <div class="food-name">
                {food}!
            </div>

            <div style="margin-top:10px; color:#888;">
                오늘은 이거 먹자 ✨
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


    # ---------------------------
    # 재추첨 잔소리
    # ---------------------------
    count = st.session_state.count

    if count == 1:
        message = "💗 첫 번째 선택! 운명을 믿어보는 건 어때?"

    elif count == 2:
        message = "👀 흠... 첫 번째 메뉴가 그렇게 별로였어?"

    elif count == 3:
        message = "🤨 혹시 먹고 싶은 게 이미 정해져 있는 거 아니야?"

    elif count == 4:
        message = "😑 룰렛의 의견도 조금은 존중해줘."

    elif count == 5:
        message = "🚨 메뉴 결정 능력 상실이 의심됩니다."

    elif count == 6:
        message = "🫵 이제 그냥 방금 나온 거 먹어."

    elif count >= 7:
        message = "🔒 룰렛도 지쳤습니다. 제발 밥을 먹으러 가세요."

    else:
        message = ""

    st.markdown(
        f'<div class="message">{message}</div>',
        unsafe_allow_html=True
    )


# ---------------------------
# 초기화
# ---------------------------
st.markdown("---")

if st.button("🧹 처음부터 다시 고르기"):
    st.session_state.result = None
    st.session_state.count = 0
    st.rerun()


st.markdown(
    """
    <div style="
        text-align:center;
        color:#aaa;
        font-size:13px;
        margin-top:25px;
    ">
        🍓 오늘도 맛있는 저녁 먹기 🍓
    </div>
    """,
    unsafe_allow_html=True
)
