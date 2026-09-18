import streamlit as st
import random
import time
import pandas as pd

# =========================================================
# 페이지 설정
# =========================================================
st.set_page_config(
    page_title="오늘 뭐 먹지? 🍽️",
    page_icon="🎀",
    layout="centered"
)

# =========================================================
# 귀여운 디자인
# =========================================================
st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at 10% 10%, #ffe4ef 0, transparent 25%),
        radial-gradient(circle at 90% 20%, #fff0bf 0, transparent 25%),
        linear-gradient(180deg, #fff9fc 0%, #fffdf5 100%);
}

.block-container {
    max-width: 760px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

.main-title {
    text-align: center;
    font-size: 46px;
    font-weight: 900;
    color: #ff668c;
    margin-bottom: 3px;
}

.subtitle {
    text-align: center;
    color: #888;
    font-size: 17px;
    margin-bottom: 30px;
}

/* 룰렛 */

.roulette {
    width: 240px;
    height: 240px;
    margin: 25px auto;
    border-radius: 50%;

    background:
        conic-gradient(
            #ffb7ca 0deg 45deg,
            #ffe08a 45deg 90deg,
            #bfe7d0 90deg 135deg,
            #c9d8ff 135deg 180deg,
            #e2c6ff 180deg 225deg,
            #ffc9a9 225deg 270deg,
            #ffdae7 270deg 315deg,
            #fff0a8 315deg 360deg
        );

    border: 9px solid white;

    box-shadow:
        0 12px 30px rgba(255, 105, 145, 0.25),
        inset 0 0 0 3px #ff91ad;

    display: flex;
    align-items: center;
    justify-content: center;

    font-size: 75px;
}

.arrow {
    text-align: center;
    font-size: 42px;
    height: 30px;
    margin-bottom: -15px;
}

/* 결과 카드 */

.result-card {
    background: white;
    border: 3px solid #ffb4c8;
    border-radius: 28px;
    padding: 28px;
    text-align: center;
    box-shadow: 0 10px 25px rgba(255,100,140,0.14);
    margin: 20px 0;
}

.result-small {
    font-size: 17px;
    color: #888;
}

.result-emoji {
    font-size: 72px;
}

.result-name {
    font-size: 38px;
    font-weight: 900;
    color: #ff5f87;
}

/* 식당 카드 */

.restaurant-card {
    background: white;
    border: 2px solid #ffd0dc;
    border-radius: 22px;
    padding: 20px;
    margin: 15px 0;
    box-shadow: 0 6px 18px rgba(255,100,140,0.10);
}

.restaurant-name {
    font-size: 23px;
    font-weight: 800;
    color: #ff668c;
}

.restaurant-info {
    color: #666;
    font-size: 15px;
    margin-top: 6px;
}

.message {
    background: #fff0f5;
    padding: 15px;
    border-radius: 18px;
    text-align: center;
    font-size: 16px;
    margin-top: 15px;
}

/* 버튼 */

div.stButton > button {
    width: 100%;
    border: none;
    border-radius: 18px;
    padding: 12px;
    font-size: 17px;
    font-weight: 800;

    background: linear-gradient(
        90deg,
        #ff91ad,
        #ff7298
    );

    color: white;
}

div.stButton > button:hover {
    color: white;
    transform: scale(1.02);
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# 메뉴
# =========================================================

menus = {

    "🍚 한식": [
        ("🍜", "칼국수"),
        ("🥣", "국밥"),
        ("🥘", "김치찌개"),
        ("🥩", "삼겹살"),
        ("🌶️", "제육볶음"),
        ("🍚", "비빔밥")
    ],

    "🍝 양식": [
        ("🍝", "파스타"),
        ("🍕", "피자"),
        ("🍔", "햄버거"),
        ("🥩", "스테이크")
    ],

    "🥟 중식": [
        ("🍜", "짜장면"),
        ("🌶️", "짬뽕"),
        ("🥟", "만두"),
        ("🍖", "탕수육")
    ],

    "🍣 일식": [
        ("🍣", "초밥"),
        ("🍜", "라멘"),
        ("🍱", "돈까스"),
        ("🍛", "카레")
    ],

    "🍗 분식/야식": [
        ("🌶️", "떡볶이"),
        ("🍗", "치킨"),
        ("🍙", "김밥"),
        ("🍜", "라면")
    ]
}


# =========================================================
# 음식점 데이터
#
# API를 사용하지 않기 때문에
# 음식점 정보를 코드 안에 저장해두는 방식이야.
#
# 위도/경도는 지도 표시용 예시 위치로,
# 추후 정확한 좌표로 더 추가/수정할 수 있어.
# =========================================================

restaurants = {

    "칼국수": [
        {
            "name": "대선칼국수",
            "address": "대전 서구 둔산중로40번길 28",
            "lat": 36.3518,
            "lon": 127.3868
        }
    ],

    "초밥": [
        {
            "name": "시라스시",
            "address": "대전 서구 둔산중로 54",
            "lat": 36.3514,
            "lon": 127.3860
        }
    ],

    "피자": [
        {
            "name": "리골레토 시카고피자 대전시청점",
            "address": "대전 서구 둔산동",
            "lat": 36.3517,
            "lon": 127.3880
        }
    ],

    "파스타": [
        {
            "name": "서가앤쿡 대전시청점",
            "address": "대전 서구 둔산동",
            "lat": 36.3515,
            "lon": 127.3877
        }
    ],

    "돈까스": [
        {
            "name": "하루엔소쿠",
            "address": "대전 서구 둔산로123번길 18",
            "lat": 36.3509,
            "lon": 127.3872
        }
    ]
}


# =========================================================
# 세션 상태
# =========================================================

if "result" not in st.session_state:
    st.session_state.result = None

if "count" not in st.session_state:
    st.session_state.count = 0


# =========================================================
# 제목
# =========================================================

st.markdown(
    '<div class="main-title">🍓 오늘 뭐 먹지? 🍓</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">오늘의 저녁 메뉴를 룰렛에게 맡겨봐 ✨</div>',
    unsafe_allow_html=True
)


# =========================================================
# 카테고리
# =========================================================

st.markdown("### 🎀 어떤 음식이 땡겨?")

category = st.selectbox(
    "종류를 골라줘!",
    ["🌎 아무거나"] + list(menus.keys())
)


if category == "🌎 아무거나":

    candidates = []

    for food_list in menus.values():
        candidates.extend(food_list)

else:

    candidates = menus[category]


with st.expander("🍴 룰렛에 들어간 메뉴 구경하기"):

    names = [food[1] for food in candidates]

    st.write(" · ".join(names))


st.markdown("---")


# =========================================================
# 룰렛
# =========================================================

st.markdown("### 🎡 운명의 저녁 룰렛")

roulette_area = st.empty()


if st.session_state.result is None:

    roulette_area.markdown("""
<div class="arrow">▼</div>
<div class="roulette">🍽️</div>
""", unsafe_allow_html=True)


# =========================================================
# 버튼
# =========================================================

if st.session_state.count == 0:

    button_text = "🎡 룰렛 돌리기!"

else:

    button_text = "🎀 다시 돌려볼래!"


if st.button(button_text):

    st.session_state.count += 1

    spin_emojis = [
        "🍕",
        "🍔",
        "🍜",
        "🍣",
        "🍗",
        "🥘",
        "🥟",
        "🍝",
        "🍛",
        "🥩"
    ]

    # 룰렛 애니메이션
    for i in range(18):

        emoji = random.choice(spin_emojis)

        roulette_area.markdown(
            f"""
<div class="arrow">▼</div>
<div class="roulette">{emoji}</div>
""",
            unsafe_allow_html=True
        )

        time.sleep(0.035 + i * 0.008)

    st.session_state.result = random.choice(candidates)

    st.rerun()


# =========================================================
# 결과
# =========================================================

if st.session_state.result:

    emoji, food = st.session_state.result

    roulette_area.markdown(
        f"""
<div class="result-card">
    <div class="result-small">
        🎊 오늘의 저녁은...
    </div>

    <div class="result-emoji">
        {emoji}
    </div>

    <div class="result-name">
        {food}
    </div>

    <div class="result-small">
        오늘은 이거 먹으러 가자 ♡
    </div>
</div>
""",
        unsafe_allow_html=True
    )


    # =====================================================
    # 다시 돌린 횟수에 따른 멘트
    # =====================================================

    count = st.session_state.count

    if count == 1:
        message = "🍓 첫 번째 운명의 메뉴야!"

    elif count == 2:
        message = "👀 아까 거는 마음에 안 들었나 봐..."

    elif count == 3:
        message = "🤨 혹시 이미 먹고 싶은 거 정해둔 거 아니야?"

    elif count == 4:
        message = "🥹 룰렛의 의견도 존중해주세요..."

    elif count == 5:
        message = "🚨 메뉴 결정 능력 상실이 의심됩니다."

    else:
        message = "🫵 이제 진짜 이거 먹자."

    st.markdown(
        f'<div class="message">{message}</div>',
        unsafe_allow_html=True
    )


    # =====================================================
    # 식당 추천
    # =====================================================

    st.markdown("---")

    st.markdown("## 📍 이 메뉴 먹으러 어디 갈까?")

    st.caption(
        "대전 둔산동 시청역 근처에서 찾아봤어 💕"
    )


    if food in restaurants:

        food_restaurants = restaurants[food]

        for restaurant in food_restaurants:

            st.markdown(
                f"""
<div class="restaurant-card">
    <div class="restaurant-name">
        🍴 {restaurant["name"]}
    </div>

    <div class="restaurant-info">
        📍 {restaurant["address"]}
    </div>

    <div class="restaurant-info">
        💕 오늘의 {food} 후보!
    </div>
</div>
""",
                unsafe_allow_html=True
            )


        # 지도 데이터
        map_data = pd.DataFrame(
            [
                {
                    "lat": r["lat"],
                    "lon": r["lon"]
                }
                for r in food_restaurants
            ]
        )


        st.markdown("### 🗺️ 여기쯤이야!")

        st.map(
            map_data,
            latitude="lat",
            longitude="lon",
            zoom=15
        )


    else:

        st.info(
            f"🍽️ {food} 맛집은 아직 지도에 등록되지 않았어! "
            "다른 메뉴도 돌려봐 💕"
        )


# =========================================================
# 처음부터
# =========================================================

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
    margin-top:30px;
">
    🎀 오늘도 맛있는 저녁 먹기 🎀
    <br>
    🍓 맛있는 건 행복이야 🍓
</div>
""",
    unsafe_allow_html=True
)
