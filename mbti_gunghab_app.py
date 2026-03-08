import streamlit as st
import pandas as pd
import random

st.set_page_config(
    page_title="MBTI 궁합 테스트",
    page_icon="💞",
    layout="wide"
)

TYPES = [
    "INFP", "ENFP", "INFJ", "ENFJ",
    "INTJ", "ENTJ", "INTP", "ENTP",
    "ISFP", "ESFP", "ISTP", "ESTP",
    "ISFJ", "ESFJ", "ISTJ", "ESTJ"
]

# 이미지 표를 기반으로 16x16 매트릭스로 정리
# 0: 다시 생각, 1: 나쁘진 않음, 2: 반반, 3: 좋은 관계, 4: 천생연분
MATRIX = [
    [3, 3, 3, 4, 3, 4, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0],
    [3, 3, 4, 3, 4, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0],
    [3, 4, 3, 3, 3, 3, 3, 4, 0, 0, 0, 0, 0, 0, 0, 0],
    [4, 3, 3, 3, 3, 3, 3, 3, 4, 0, 0, 0, 0, 0, 0, 0],
    [3, 4, 3, 3, 3, 3, 3, 4, 2, 2, 2, 2, 1, 1, 1, 1],
    [4, 3, 3, 3, 3, 3, 4, 3, 2, 2, 2, 2, 1, 1, 1, 1],
    [3, 3, 3, 3, 3, 4, 3, 3, 2, 2, 2, 2, 1, 1, 1, 4],
    [3, 3, 4, 3, 4, 3, 3, 3, 2, 2, 2, 2, 1, 1, 1, 1],
    [0, 0, 0, 4, 2, 2, 2, 2, 1, 1, 1, 1, 2, 4, 2, 4],
    [0, 0, 0, 0, 2, 2, 2, 2, 1, 1, 1, 1, 4, 2, 4, 2],
    [0, 0, 0, 0, 2, 2, 2, 2, 1, 1, 1, 1, 2, 4, 2, 4],
    [0, 0, 0, 0, 2, 2, 2, 2, 1, 1, 1, 1, 4, 2, 2, 2],
    [0, 0, 0, 0, 1, 2, 1, 1, 2, 4, 2, 4, 3, 3, 3, 3],
    [0, 0, 0, 0, 1, 2, 1, 1, 4, 2, 4, 2, 3, 3, 3, 3],
    [0, 0, 0, 0, 1, 2, 1, 1, 2, 4, 2, 2, 3, 3, 3, 3],
    [0, 0, 0, 0, 1, 2, 4, 1, 4, 2, 4, 2, 3, 3, 3, 3],
]

LEVEL_INFO = {
    0: {
        "label": "우리 궁합 다시 생각해봐요",
        "emoji": "😢",
        "score": 25,
        "color": "#d84315",
        "text": "성향 차이가 커서 자주 부딪힐 수 있어요. 서로를 이해하려는 노력이 특히 중요합니다."
    },
    1: {
        "label": "최악은 아니지만 좋지도 않음",
        "emoji": "🙂",
        "score": 45,
        "color": "#fdd835",
        "text": "무난하지만 자연스럽게 잘 맞는 조합은 아닐 수 있어요. 대화 방식 조율이 필요합니다."
    },
    2: {
        "label": "안 맞는 것 맞는 것, 반반!",
        "emoji": "🤔",
        "score": 65,
        "color": "#9ccc65",
        "text": "장점과 단점이 함께 있는 관계예요. 맞는 부분을 잘 키우면 충분히 좋은 관계가 될 수 있습니다."
    },
    3: {
        "label": "좋은 관계로 발전 가능",
        "emoji": "😊",
        "score": 85,
        "color": "#4caf50",
        "text": "기본적인 결이 잘 맞는 편이에요. 서로의 차이를 존중하면 안정적인 관계로 발전하기 좋습니다."
    },
    4: {
        "label": "우리 궁합은 천생연분",
        "emoji": "💙",
        "score": 98,
        "color": "#42a5f5",
        "text": "서로의 성향이 자연스럽게 잘 연결되는 편이에요. 함께 있을 때 시너지가 크게 날 가능성이 높습니다."
    }
}

CARD_STYLE = """
<style>
.stApp {
    background: linear-gradient(180deg, #fff8fb 0%, #f7f9ff 45%, #eef5ff 100%);
}

.block-container {
    padding-top: 5.2rem;
    padding-bottom: 2.5rem;
    max-width: 980px;
}

header[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}

div[data-testid="stToolbar"] {
    top: 0.5rem;
}

.hero-card {
    background: linear-gradient(135deg, rgba(255,255,255,0.92) 0%, rgba(255,255,255,0.78) 100%);
    border: 1px solid rgba(255,255,255,0.65);
    border-radius: 28px;
    padding: 2rem 1.6rem 1.6rem 1.6rem;
    box-shadow: 0 20px 45px rgba(125, 104, 170, 0.12);
    backdrop-filter: blur(10px);
    margin-bottom: 1.4rem;
}

.badge {
    display: inline-block;
    padding: 0.35rem 0.8rem;
    border-radius: 999px;
    background: #ffe4ef;
    color: #d63384;
    font-weight: 700;
    font-size: 0.88rem;
    margin-bottom: 0.9rem;
}

.main-title {
    font-size: 2.55rem;
    font-weight: 900;
    letter-spacing: -0.02em;
    color: #222;
    margin-bottom: 0.3rem;
    line-height: 1.15;
}

.sub-title {
    color: #666;
    font-size: 1.02rem;
    line-height: 1.7;
    margin-bottom: 0.2rem;
}

.selector-card {
    background: rgba(255,255,255,0.8);
    border: 1px solid rgba(255,255,255,0.7);
    border-radius: 24px;
    padding: 1rem 1rem 0.2rem 1rem;
    box-shadow: 0 10px 30px rgba(90, 116, 166, 0.08);
}

.result-card {
    border-radius: 28px;
    padding: 1.6rem;
    color: white;
    box-shadow: 0 18px 40px rgba(0,0,0,0.16);
    margin-top: 1rem;
    animation: fadeUp 0.7s ease;
}

@keyframes fadeUp {
    from {
        opacity: 0;
        transform: translateY(18px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.result-topline {
    font-size: 0.95rem;
    opacity: 0.92;
    margin-bottom: 0.5rem;
}

.result-pair {
    font-size: 2rem;
    font-weight: 900;
    letter-spacing: -0.02em;
    margin-bottom: 0.4rem;
}

.result-label {
    font-size: 1.25rem;
    font-weight: 800;
    margin-bottom: 0.8rem;
}

.result-desc {
    font-size: 1.02rem;
    line-height: 1.8;
    opacity: 0.98;
}

.metric-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.9rem;
    margin-top: 1.2rem;
}

.metric-box {
    background: rgba(255,255,255,0.14);
    border: 1px solid rgba(255,255,255,0.18);
    border-radius: 18px;
    padding: 0.9rem;
    text-align: center;
}

.metric-label {
    font-size: 0.85rem;
    opacity: 0.85;
    margin-bottom: 0.25rem;
}

.metric-value {
    font-size: 1.4rem;
    font-weight: 800;
}

.section-title {
    font-size: 1.2rem;
    font-weight: 800;
    color: #2b2b2b;
    margin: 1.2rem 0 0.7rem 0;
}

.tip-card {
    background: rgba(255,255,255,0.82);
    border: 1px solid rgba(255,255,255,0.7);
    border-radius: 22px;
    padding: 1.1rem 1rem;
    box-shadow: 0 10px 30px rgba(90, 116, 166, 0.08);
}

.quote-box {
    background: linear-gradient(135deg, #fff0f6 0%, #eef4ff 100%);
    border-radius: 20px;
    padding: 1rem 1.1rem;
    color: #444;
    border: 1px solid #f3d8e7;
}

.character-chip-wrap {
    display: flex;
    gap: 0.7rem;
    flex-wrap: wrap;
    margin-top: 0.9rem;
}

.character-chip {
    background: rgba(255,255,255,0.82);
    border: 1px solid rgba(255,255,255,0.7);
    border-radius: 999px;
    padding: 0.55rem 0.9rem;
    box-shadow: 0 8px 20px rgba(90, 116, 166, 0.08);
    font-size: 0.92rem;
    color: #444;
    font-weight: 700;
}

.result-banner {
    margin-top: 1rem;
    border-radius: 20px;
    padding: 0.95rem 1.1rem;
    color: white;
    font-weight: 700;
    box-shadow: 0 12px 24px rgba(0,0,0,0.12);
    animation: fadeUp 0.8s ease;
}

.small-note {
    color: #777;
    font-size: 0.92rem;
    text-align: center;
    margin-top: 1.2rem;
}

div[data-testid="stButton"] > button {
    width: 100%;
    border: 0;
    border-radius: 16px;
    min-height: 3.2rem;
    font-size: 1.05rem;
    font-weight: 800;
    background: linear-gradient(135deg, #ff4f93 0%, #7d6bff 100%);
    color: white;
    box-shadow: 0 14px 28px rgba(125, 107, 255, 0.28);
}

div[data-testid="stButton"] > button:hover {
    filter: brightness(1.03);
    transform: translateY(-1px);
}

@media (max-width: 768px) {
    .main-title {
        font-size: 2rem;
    }
    .result-pair {
        font-size: 1.6rem;
    }
    .metric-grid {
        grid-template-columns: 1fr;
    }
}
</style>
"""

st.markdown(CARD_STYLE, unsafe_allow_html=True)
st.markdown(
    '''
    <div class="hero-card">
        <div class="badge">MBTI Compatibility Service</div>
        <div class="main-title">💞 MBTI 궁합 테스트</div>
        <div class="sub-title">나의 MBTI와 상대방의 MBTI를 선택하면, 두 사람의 궁합을 감성적인 카드 형태로 확인할 수 있어요.<br>재미로 가볍게 즐기되, 서로의 차이를 이해하는 대화의 출발점으로 활용해보세요.</div>
    </div>
    ''',
    unsafe_allow_html=True
)


left, right = st.columns([1, 1])

with left:
    my_mbti = st.selectbox("나의 MBTI", TYPES, index=0)

with right:
    partner_mbti = st.selectbox("상대방의 MBTI", TYPES, index=1)




CHEMISTRY_LABELS = ["낯설지만 흥미로운 조합", "무난한 합", "서로 배울 점이 많은 조합", "자연스럽게 잘 맞는 조합", "설렘 시너지가 큰 조합"]
STYLE_LABELS = ["신중한 흐름", "천천히 가까워지는 스타일", "균형형 관계", "대화가 잘 통하는 스타일", "서로를 끌어주는 스타일"]
RESULT_BANNERS = {
    0: "서로의 차이를 먼저 이해하는 것이 가장 중요한 조합이에요.",
    1: "작은 배려와 대화 방식 조정이 관계 만족도를 크게 올려줄 수 있어요.",
    2: "의외의 공통점이 관계를 더 흥미롭게 만들어줄 수 있어요.",
    3: "편안함과 호감이 함께 자라기 좋은 안정형 궁합이에요.",
    4: "서로의 강점을 자연스럽게 끌어올리는 시너지형 궁합이에요."
}
MBTI_STYLE_MAP = {
    "INFP": "🌷 감성 공감형", "ENFP": "🎉 에너지 메이커", "INFJ": "🔮 통찰형", "ENFJ": "🤝 따뜻한 리더형",
    "INTJ": "🧠 전략가형", "ENTJ": "🔥 추진력형", "INTP": "📘 아이디어형", "ENTP": "⚡ 발상가형",
    "ISFP": "🎨 감각형", "ESFP": "💃 분위기 메이커", "ISTP": "🛠 실전형", "ESTP": "🏎 행동파형",
    "ISFJ": "🫶 배려형", "ESFJ": "🌼 친화형", "ISTJ": "📏 안정형", "ESTJ": "📌 현실 리더형"
}


def get_result(mbti_a: str, mbti_b: str) -> dict:
    row = TYPES.index(mbti_a)
    col = TYPES.index(mbti_b)
    level = MATRIX[row][col]
    result = LEVEL_INFO[level].copy()
    result["level"] = level
    result["chemistry"] = CHEMISTRY_LABELS[level]
    result["relationship_style"] = STYLE_LABELS[level]
    result["share_text"] = f"{mbti_a} × {mbti_b} 궁합 결과는 {result['score']}점, {result['label']}!"
    result["banner_text"] = RESULT_BANNERS[level]
    result["my_style"] = MBTI_STYLE_MAP[mbti_a]
    result["partner_style"] = MBTI_STYLE_MAP[mbti_b]
    return result


if st.button("💘 궁합 확인하기", use_container_width=True):
    result = get_result(my_mbti, partner_mbti)
    mood_messages = [
        "서로의 차이가 오히려 매력으로 느껴질 수 있어요.",
        "대화 방식만 잘 맞추면 충분히 편안한 관계가 될 수 있어요.",
        "조금씩 알아갈수록 의외의 케미가 살아나는 조합이에요.",
        "기본 결이 잘 맞아 관계가 안정적으로 흘러가기 쉬워요.",
        "함께 있을 때 설렘과 편안함을 동시에 느끼기 쉬운 조합이에요."
    ]
    random.seed(f"{my_mbti}-{partner_mbti}")
    mood_pick = random.choice(mood_messages)

    st.markdown(
        f'''
        <div class="result-card" style="background: linear-gradient(135deg, {result['color']} 0%, #1f2233 130%);">
            <div class="result-topline">Compatibility Result</div>
            <div class="result-pair">{my_mbti} ❤️ {partner_mbti}</div>
            <div class="result-label">{result['emoji']} {result['label']}</div>
            <div class="result-desc">{result['text']}<br><br>{mood_pick}</div>
            <div class="metric-grid">
                <div class="metric-box">
                    <div class="metric-label">궁합 점수</div>
                    <div class="metric-value">{result['score']}점</div>
                </div>
                <div class="metric-box">
                    <div class="metric-label">관계 무드</div>
                    <div class="metric-value" style="font-size:1.02rem;">{result['chemistry']}</div>
                </div>
                <div class="metric-box">
                    <div class="metric-label">관계 스타일</div>
                    <div class="metric-value" style="font-size:1.02rem;">{result['relationship_style']}</div>
                </div>
            </div>
        </div>
        ''',
        unsafe_allow_html=True
    )

    st.progress(result["score"] / 100)

    banner_gradients = {
        0: "linear-gradient(135deg, #ff7043 0%, #8d3b72 100%)",
        1: "linear-gradient(135deg, #f6c445 0%, #d28a30 100%)",
        2: "linear-gradient(135deg, #9ccc65 0%, #5f9f78 100%)",
        3: "linear-gradient(135deg, #4caf50 0%, #3d7bd9 100%)",
        4: "linear-gradient(135deg, #42a5f5 0%, #7b61ff 100%)",
    }

    st.markdown(
        f'''
        <div class="result-banner" style="background: {banner_gradients[result['level']]};">
            ✨ {result['banner_text']}
        </div>
        ''',
        unsafe_allow_html=True
    )

    st.markdown('<div class="character-chip-wrap">', unsafe_allow_html=True)
    st.markdown(
        f'''
        <span class="character-chip">나: {my_mbti} · {result['my_style']}</span>
        <span class="character-chip">상대: {partner_mbti} · {result['partner_style']}</span>
        ''',
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

    info_left, info_right = st.columns([1.1, 0.9])

    with info_left:
        st.markdown('<div class="section-title">💡 이렇게 해석해보세요</div>', unsafe_allow_html=True)
        st.markdown(
            f'''
            <div class="tip-card">
                <b>{my_mbti}</b>와 <b>{partner_mbti}</b>는 성향의 결이 완전히 같기보다는,
                서로를 보완하거나 자극할 수 있는 포인트가 있는 조합입니다.<br><br>
                중요한 것은 점수 자체보다도 <b>서로의 소통 방식</b>, <b>감정 표현 방식</b>, <b>혼자만의 시간이 필요한 정도</b>를 이해하는 거예요.
            </div>
            ''',
            unsafe_allow_html=True
        )

    with info_right:
        st.markdown('<div class="section-title">📤 공유용 한 줄</div>', unsafe_allow_html=True)
        st.markdown(
            f'''
            <div class="quote-box">{result['share_text']}</div>
            ''',
            unsafe_allow_html=True
        )
        st.code(result['share_text'])

    st.markdown("### 궁합 등급 가이드")
    guide_df = pd.DataFrame([
        ["😢 다시 생각", "25점", "성향 차이가 큰 편"],
        ["🙂 보통 이하", "45점", "조율이 필요한 관계"],
        ["🤔 반반", "65점", "장단점이 함께 있음"],
        ["😊 좋은 관계", "85점", "편안하게 발전 가능"],
        ["💙 천생연분", "98점", "매우 잘 맞는 편"],
    ], columns=["등급", "점수", "설명"])
    st.dataframe(guide_df, use_container_width=True, hide_index=True)





st.markdown(
    '<div class="small-note">※ 이 앱은 재미용 MBTI 궁합 테스트입니다.</div>',
    unsafe_allow_html=True
)
