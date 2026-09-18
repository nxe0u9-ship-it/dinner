import streamlit as st
import random
import time

st.set_page_config(
    page_title="오늘 뭐 먹지? 🍽️",
    page_icon="🍓",
    layout="centered"
)

# ============================================================
# 디자인
# ============================================================

st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #fff5f8 0%, #fffcef 100%);
}

.block-container {
    max-width: 760px;
    padding-top: 2rem;
}

.title {
    text-align: center;
    font-size: 45px;
    font-weight: 900;
    color: #ff668c;
}

.subtitle {
    text-align: center;
    color: #888;
    font-size: 17px;
    margin-bottom: 30px;
}

div.stButton > button {
    width: 100%;
    border-radius: 20px;
    border: 0;
    background: #ff86a5;
    color: white;
    font-size: 18px;
    font-weight: 800;
    padding: 12px;
}

div.stButton > button:hover {
    background: #ff668c;
    color: white;
}

[data-testid="stAlert"] {
    border-radius: 20px;
}

.food-result {
    text-align: center;
    font-size: 42px;
    font-weight: 900;
    color: #ff5f87;
    padding: 15px;
}

.food-emoji {
    text-align: center;
    font-size: 80px;
}

.restaurant-title {
    font-size: 22px;
    font-weight: 800;
    color: #ff668c;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# 메뉴 데이터
# 메뉴 수 대폭 증가!
# ============================================================

menus = {

    "🍚 한식": [
        ("🥘", "김치찌개"),
        ("🍲", "부대찌개"),
        ("🥣", "된장찌개"),
        ("🥩", "삼겹살"),
        ("🍖", "갈비"),
        ("🌶️", "제육볶음"),
        ("🐙", "쭈꾸미"),
        ("🐔", "닭갈비"),
        ("🍚", "비빔밥"),
        ("🥣", "국밥"),
        ("🥩", "소고기"),
        ("🍜", "칼국수"),
        ("🍜", "냉면"),
        ("🥟", "만두"),
        ("🐟", "생선구이"),
        ("🍗", "찜닭"),
        ("🥘", "순두부찌개"),
        ("🍲", "감자탕"),
        ("🍚", "돌솥밥"),
        ("🍖", "보쌈")
    ],

    "🍣 일식": [
        ("🍣", "초밥"),
        ("🍜", "라멘"),
        ("🍱", "돈까스"),
        ("🍛", "카레"),
        ("🍜", "우동"),
        ("🍚", "규동"),
        ("🍚", "덮밥"),
        ("🍜", "소바"),
        ("🍤", "텐동"),
        ("🐟", "회"),
        ("🍙", "유부초밥"),
        ("🍗", "가라아게")
    ],

    "🥟 중식": [
        ("🍜", "짜장면"),
        ("🌶️", "짬뽕"),
        ("🍖", "탕수육"),
        ("🥟", "중국식 만두"),
        ("🌶️", "마라탕"),
        ("🌶️", "마라샹궈"),
        ("🍚", "중화볶음밥"),
        ("🥩", "고추잡채"),
        ("🍲", "마파두부"),
        ("🍜", "우육면")
    ],

    "🍝 양식": [
        ("🍝", "파스타"),
        ("🍕", "피자"),
        ("🍔", "햄버거"),
        ("🥩", "스테이크"),
        ("🥗", "샐러드"),
        ("🥪", "샌드위치"),
        ("🌯", "브리또"),
        ("🌮", "타코"),
        ("🍚", "리조또"),
        ("🥘", "필라프"),
        ("🍳", "오므라이스")
    ],

    "🍗 분식/야식": [
        ("🌶️", "떡볶이"),
        ("🍗", "치킨"),
        ("🍙", "김밥"),
        ("🍜", "라면"),
        ("🥟", "튀김"),
        ("🌭", "핫도그"),
        ("🍢", "어묵"),
        ("🍚", "컵밥"),
        ("🍳", "토스트")
    ],

    "🌏 이색 메뉴": [
        ("🍛", "인도카레"),
        ("🥙", "케밥"),
        ("🌮", "멕시칸"),
        ("🍜", "쌀국수"),
        ("🍚", "팟타이"),
        ("🥩", "샤브샤브"),
        ("🔥", "훠궈"),
        ("🥗", "포케")
    ]
}


# ============================================================
# 실제 둔산동 식당 데이터
#
# 여러 메뉴를 같은 식당과 연결할 수 있게 만들어둠.
# ============================================================

restaurants = {

    "칼국수": [
        ("🍜", "대선칼국수", "대전 서구 둔산중로40번길 28")
    ],

    "국밥": [
        ("🥣", "태평소국밥 둔산점", "대전 서구 둔산동")
    ],

    "쭈꾸미": [
        ("🐙", "손의손 본점", "대전 서구 둔산동")
    ],

    "초밥": [
        ("🍣", "시라스시", "대전 서구 둔산중로 54")
    ],

    "유부초밥": [
        ("🍙", "키츠네유부 둔산시청점", "대전 서구 둔산로 130")
    ],

    "짬뽕": [
        ("🍜", "이비가짬뽕 시청점", "대전 서구 둔산동 1447"),
        ("🍜", "첨아각", "대전 서구 둔산동 1448")
    ],

    "짜장면": [
        ("🥢", "첨아각", "대전 서구 둔산동 1448")
    ],

    "탕수육": [
        ("🍖", "첨아각", "대전 서구 둔산동 1448")
    ],

    "돈까스": [
        ("🍱", "동백카츠 대전둔산점", "대전 서구 둔산동"),
        ("🍱", "카이테키 대전점", "대전 서구 둔산동"),
        ("🍱", "어메이징카츠", "대전 서구 둔산동"),
        ("🍱", "별달돈까스카페", "대전 서구 둔산동")
    ],

    "파스타": [
        ("🍝", "세서미하우스", "대전 서구 둔산동"),
        ("🍝", "이태리국시", "대전 서구 둔산동")
    ],

    "피자": [
        ("🍕", "이태리국시", "대전 서구 둔산동")
    ],

    "떡볶이": [
        ("🌶️", "떡반집 본점", "대전 서구 둔산동")
    ],

    "햄버거": [
        ("🍔", "다운타우너 대전갤러리아", "대전 서구 대덕대로 211")
    ],

    "인도카레": [
        ("🍛", "인디 대전둔산점", "대전 서구 대덕대로 246")
    ],

    "덮밥": [
        ("🍚", "갓지동", "대전 서구 둔산동 1310")
    ],

    "우동": [
        ("🍜", "제면소의하루 둔산직영점", "대전 서구 둔산동 1433")
    ]
}


# ============================================================
# 세션
# ============================================================

if "result" not in st.session_state:
    st.session_state.result = None

if "count" not in st.session_state:
    st.session_state.count = 0


# ============================================================
# 제목
# ============================================================

st.markdown(
    '<div class="title">🍓 오늘 뭐 먹지? 🍓</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">저녁 고민은 귀여운 룰렛에게 맡겨버리자 🎀</div>',
    unsafe_allow_html=True
)


# ============================================================
# 카테고리 선택
# ============================================================

st.markdown("### 🍴 오늘 뭐가 땡겨?")

category = st.selectbox(
    "종류를 골라줘!",
    ["🌎 진짜 아무거나!"] + list(menus.keys())
)


if category == "🌎 진짜 아무거나!":

    candidates = []

    for menu_list in menus.values():
        candidates.extend(menu_list)

else:

    candidates = menus[category]


with st.expander("👀 룰렛 후보 메뉴 구경하기"):

    st.write(
        " · ".join(
            [name for emoji, name in candidates]
        )
    )


# ============================================================
# 룰렛
# ============================================================

st.markdown("---")

st.markdown("## 🎡 운명의 저녁 룰렛")

roulette = st.empty()


if st.session_state.result is None:

    roulette.markdown(
        """
        <div style="
            text-align:center;
            font-size:100px;
            padding:35px;
        ">
            🎡
        </div>
        """,
        unsafe_allow_html=True
    )


button_text = (
    "🎡 룰렛 돌리기!"
    if st.session_state.count == 0
    else "🎀 한 번만 더 돌릴래!"
)


if st.button(button_text):

    st.session_state.count += 1

    animation = [
        "🍕", "🍜", "🍣", "🍔",
        "🥘", "🍗", "🍛", "🥟",
        "🌮", "🍝", "🥩", "🍚"
    ]

    for i in range(18):

        roulette.markdown(
            f"""
            <div style="
                text-align:center;
                font-size:100px;
                padding:35px;
            ">
                {random.choice(animation)}
            </div>
            """,
            unsafe_allow_html=True
        )

        time.sleep(0.025 + i * 0.006)


    st.session_state.result = random.choice(candidates)

    st.rerun()


# ============================================================
# 결과
#
# ★ 여기 중요 ★
# 결과를 복잡한 HTML 카드 안에 넣지 않음.
# 그래서 HTML 코드가 글자로 튀어나오는 문제를 줄임.
# ============================================================

if st.session_state.result is not None:

    emoji, food = st.session_state.result

    roulette.empty()

    st.markdown(
        f'<div class="food-emoji">{emoji}</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="food-result">{food} 당첨! 🎉</div>',
        unsafe_allow_html=True
    )

    st.success(
        f"오늘 저녁은 {food} 어때? 💕"
    )


    # --------------------------------------------------------
    # 재추첨 멘트
    # --------------------------------------------------------

    count = st.session_state.count

    if count == 1:
        st.info("🍓 첫 번째 운명의 메뉴야!")

    elif count == 2:
        st.info("👀 첫 번째 메뉴는 마음에 안 들었나 봐...")

    elif count == 3:
        st.warning("🤨 혹시 먹고 싶은 게 이미 정해져 있는 거 아니야?")

    elif count == 4:
        st.warning("🥹 룰렛의 의견도 조금만 존중해주세요...")

    elif count >= 5:
        st.error("🚨 메뉴 결정 능력 상실! 이제 진짜 이거 먹자ㅋㅋ")


    # ========================================================
    # 식당 추천
    # ========================================================

    st.markdown("---")
    st.markdown(f"## 📍 {food} 먹으러 어디 갈까?")
    st.caption("대전 둔산동·시청역 주변에서 찾아봤어 🎀")


    if food in restaurants:

        choices = restaurants[food]

        # 하나만 보여주는 것보다
        # 있는 경우 최대 3곳까지 보여줌
        for restaurant_emoji, name, address in choices[:3]:

            with st.container(border=True):

                st.markdown(
                    f"### {restaurant_emoji} {name}"
                )

                st.write(f"📍 {address}")

                st.caption(
                    f"💕 {food} 먹고 싶을 때 가볼 수 있는 후보!"
                )

    else:

        # 식당 정보가 아직 연결되지 않은 메뉴
        st.info(
            f"🥺 아직 {food}에 연결해 둔 식당이 없어!\n\n"
            "그래도 메뉴는 맛있으니까 오늘의 후보로 찜 💕"
        )


# ============================================================
# 초기화
# ============================================================

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
        padding-bottom:30px;
    ">
        🍓 오늘도 맛있는 저녁 먹기 🍓
        <br>
        🎀 맛있는 건 행복이야 🎀
    </div>
    """,
    unsafe_allow_html=True
)
