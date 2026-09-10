import streamlit as st
import os
import json
import re
from dotenv import load_dotenv
from google import genai


# ============================================================
# CONFIG
# ============================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    try:
        API_KEY = st.secrets["GEMINI_API_KEY"]
    except Exception:
        API_KEY = None

MODEL = "gemini-3.6-flash"

st.set_page_config(
    page_title="ExamRisk AI",
    page_icon="🎯",
    layout="wide"
)


# ============================================================
# GLOBAL CSS
# ============================================================

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 0% 0%, rgba(124,58,237,.25), transparent 28%),
        radial-gradient(circle at 100% 0%, rgba(6,182,212,.20), transparent 28%),
        radial-gradient(circle at 50% 100%, rgba(79,70,229,.12), transparent 35%),
        #050812;
    color: #f8fafc;
}

.block-container {
    max-width: 1150px;
    padding-top: 25px;
    padding-bottom: 60px;
}

header {
    visibility: hidden;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}


/* ============================================================
   HERO
   ============================================================ */

.hero-box {
    position: relative;
    overflow: hidden;

    padding: 42px;

    border-radius: 28px;

    background:
        radial-gradient(circle at 85% 20%, rgba(6,182,212,.18), transparent 25%),
        linear-gradient(115deg, #241553, #151936 50%, #071522);

    border: 1px solid rgba(139,92,246,.55);

    box-shadow:
        0 25px 70px rgba(0,0,0,.45),
        0 0 50px rgba(124,58,237,.10);

    transition: all .3s ease;
}

.hero-box:hover {
    transform: translateY(-5px);

    border-color: rgba(34,211,238,.65);

    box-shadow:
        0 30px 80px rgba(0,0,0,.50),
        0 0 50px rgba(124,58,237,.20),
        0 0 70px rgba(6,182,212,.08);
}

.hero-badge {
    display: inline-block;

    padding: 9px 17px;

    border-radius: 999px;

    background: rgba(124,58,237,.16);

    border: 1px solid rgba(167,139,250,.55);

    color: #d8ccff;

    font-size: 12px;

    font-weight: 800;

    letter-spacing: .5px;

    margin-bottom: 18px;

    transition: all .25s ease;
}

.hero-badge:hover {
    transform: scale(1.06) translateY(-3px);

    box-shadow:
        0 0 25px rgba(139,92,246,.35);
}

.hero-title {
    margin: 0;

    font-size: 52px;

    line-height: 1;

    font-weight: 800;

    letter-spacing: -2.5px;
}

.gradient-text {
    background: linear-gradient(
        90deg,
        #a78bfa,
        #60a5fa,
        #22d3ee
    );

    -webkit-background-clip: text;

    -webkit-text-fill-color: transparent;
}

.hero-description {
    margin-top: 18px;

    max-width: 750px;

    color: #aab4c8;

    font-size: 16px;

    line-height: 1.65;
}


/* ============================================================
   STEPS
   ============================================================ */

.steps-container {
    display: flex;

    align-items: center;

    justify-content: center;

    gap: 16px;

    margin: 30px 0 35px;
}

.step-item {
    display: flex;

    align-items: center;

    gap: 10px;

    color: #71809a;

    font-size: 14px;

    font-weight: 700;

    transition: all .25s ease;

    cursor: default;
}

.step-item:hover {
    color: #ffffff;

    transform: translateY(-6px) scale(1.04);

    filter:
        drop-shadow(
            0 0 12px rgba(139,92,246,.45)
        );
}

.step-circle {
    width: 44px;

    height: 44px;

    min-width: 44px;

    border-radius: 50%;

    display: flex;

    align-items: center;

    justify-content: center;

    background: #101827;

    border: 1px solid #35415c;

    color: #8b98ae;

    font-weight: 800;

    transition: all .25s ease;
}

.step-item:hover .step-circle {
    transform: scale(1.22);

    background:
        linear-gradient(
            135deg,
            #7c3aed,
            #06b6d4
        );

    color: white;

    border-color: transparent;

    box-shadow:
        0 0 20px rgba(124,58,237,.7),
        0 0 35px rgba(6,182,212,.25);
}

.step-active {
    color: #ffffff;
}

.step-active .step-circle {
    background:
        linear-gradient(
            135deg,
            #7c3aed,
            #06b6d4
        );

    color: white;

    border-color: transparent;

    box-shadow:
        0 0 22px rgba(124,58,237,.7);
}

.step-line {
    width: 75px;

    height: 2px;

    background:
        linear-gradient(
            90deg,
            #39445b,
            #222c40
        );
}


/* ============================================================
   SECTION
   ============================================================ */

.section-title {
    font-size: 30px;

    font-weight: 800;

    letter-spacing: -.8px;

    margin-bottom: 6px;
}

.purple {
    color: #a78bfa;
}

.section-subtitle {
    color: #8995aa;

    font-size: 14px;

    line-height: 1.6;

    margin-bottom: 22px;
}


/* ============================================================
   CARDS
   ============================================================ */

.custom-card {
    padding: 24px;

    border-radius: 20px;

    background:
        linear-gradient(
            145deg,
            rgba(24,30,59,.95),
            rgba(9,15,29,.96)
        );

    border: 1px solid rgba(139,92,246,.28);

    box-shadow:
        0 15px 45px rgba(0,0,0,.25);

    transition: all .28s ease;
}

.custom-card:hover {
    transform: translateY(-7px);

    border-color: rgba(139,92,246,.65);

    box-shadow:
        0 25px 60px rgba(0,0,0,.35),
        0 0 30px rgba(124,58,237,.10);
}

.card-title {
    color: #f8fafc;

    font-size: 17px;

    font-weight: 800;

    margin-bottom: 5px;
}

.card-description {
    color: #8995aa;

    font-size: 12px;
}


/* ============================================================
   CONFIDENCE
   ============================================================ */

.confidence-card {
    padding: 20px;

    border-radius: 17px;

    background:
        linear-gradient(
            135deg,
            rgba(6,182,212,.08),
            rgba(124,58,237,.12)
        );

    border: 1px solid rgba(6,182,212,.28);

    transition: all .25s ease;
}

.confidence-card:hover {
    transform: translateY(-5px);

    border-color: rgba(6,182,212,.65);

    box-shadow:
        0 15px 40px rgba(6,182,212,.10);
}

.confidence-number {
    color: #67e8f9;

    font-size: 18px;

    font-weight: 800;
}

.confidence-message {
    color: #94a3b8;

    font-size: 13px;

    margin-top: 6px;
}


/* ============================================================
   BUTTONS
   ============================================================ */

.stButton > button {
    width: 100%;

    min-height: 56px;

    border: none !important;

    border-radius: 15px !important;

    background:
        linear-gradient(
            100deg,
            #7c3aed,
            #6366f1,
            #06b6d4
        ) !important;

    color: white !important;

    font-size: 16px !important;

    font-weight: 800 !important;

    box-shadow:
        0 10px 30px rgba(99,102,241,.30);

    transition:
        transform .2s ease,
        box-shadow .2s ease,
        filter .2s ease;
}

.stButton > button:hover {
    transform:
        translateY(-6px)
        scale(1.025);

    filter: brightness(1.1);

    box-shadow:
        0 18px 45px rgba(99,102,241,.45),
        0 0 35px rgba(6,182,212,.22);
}

.stButton > button:active {
    transform:
        translateY(-1px)
        scale(.98);
}


/* ============================================================
   INPUTS
   ============================================================ */

.stTextInput > div > div,
.stTextArea > div > div {
    background: #101827 !important;

    border: 1px solid #303b55 !important;

    border-radius: 12px !important;

    transition: all .2s ease;
}

.stTextInput > div > div:hover,
.stTextArea > div > div:hover {
    border-color: #8b5cf6 !important;

    box-shadow:
        0 0 22px rgba(124,58,237,.12);
}

.stTextInput input,
.stTextArea textarea {
    color: #ffffff !important;
}


/* ============================================================
   QUESTION
   ============================================================ */

.question-card {
    padding: 24px;

    margin-top: 20px;

    border-radius: 19px;

    background:
        linear-gradient(
            145deg,
            #121a2b,
            #0b1220
        );

    border: 1px solid #29354d;

    transition: all .25s ease;
}

.question-card:hover {
    transform: translateY(-5px);

    border-color: rgba(139,92,246,.6);

    box-shadow:
        0 20px 45px rgba(0,0,0,.3),
        0 0 25px rgba(124,58,237,.10);
}

.question-label {
    color: #a78bfa;

    font-size: 11px;

    font-weight: 800;

    letter-spacing: 1px;
}

.topic-pill {
    display: inline-block;

    margin-left: 8px;

    padding: 5px 9px;

    border-radius: 7px;

    background: rgba(6,182,212,.10);

    color: #67e8f9;

    font-size: 10px;

    font-weight: 700;
}

.question-text {
    margin-top: 13px;

    color: #ffffff;

    font-size: 18px;

    line-height: 1.55;

    font-weight: 600;
}


/* ============================================================
   METRICS
   ============================================================ */

.metric-card {
    padding: 23px;

    text-align: center;

    border-radius: 18px;

    background:
        linear-gradient(
            145deg,
            #12182a,
            #0c1322
        );

    border: 1px solid #29354d;

    transition: all .25s ease;
}

.metric-card:hover {
    transform:
        translateY(-7px)
        scale(1.025);

    border-color: rgba(139,92,246,.65);

    box-shadow:
        0 18px 45px rgba(0,0,0,.3),
        0 0 28px rgba(124,58,237,.10);
}

.metric-label {
    color: #8995aa;

    font-size: 11px;

    font-weight: 700;

    text-transform: uppercase;

    letter-spacing: 1px;
}

.metric-value {
    margin-top: 8px;

    color: white;

    font-size: 34px;

    font-weight: 800;
}


/* ============================================================
   RESULT
   ============================================================ */

.result-box {
    padding: 30px;

    text-align: center;

    border-radius: 22px;

    background:
        linear-gradient(
            135deg,
            #171d31,
            #0c1424
        );

    border: 1px solid rgba(139,92,246,.4);

    transition: all .3s ease;
}

.result-box:hover {
    transform: translateY(-5px);

    box-shadow:
        0 25px 60px rgba(0,0,0,.35),
        0 0 35px rgba(124,58,237,.12);
}

.result-label {
    color: #94a3b8;

    font-size: 12px;

    font-weight: 800;

    letter-spacing: 1.5px;
}

.risk-high {
    color: #fb7185;

    font-size: 43px;

    font-weight: 800;
}

.risk-medium {
    color: #fbbf24;

    font-size: 43px;

    font-weight: 800;
}

.risk-low {
    color: #34d399;

    font-size: 43px;

    font-weight: 800;
}


/* ============================================================
   FINDING
   ============================================================ */

.finding-box {
    padding: 21px;

    margin: 22px 0;

    border-radius: 17px;

    background:
        linear-gradient(
            135deg,
            rgba(124,58,237,.12),
            rgba(6,182,212,.05)
        );

    border: 1px solid rgba(139,92,246,.3);

    transition: all .25s ease;
}

.finding-box:hover {
    transform: translateY(-4px);

    border-color: rgba(139,92,246,.6);

    box-shadow:
        0 12px 35px rgba(0,0,0,.2);
}

.finding-title {
    color: #c4b5fd;

    font-weight: 800;

    margin-bottom: 7px;
}

.finding-text {
    color: #cbd5e1;

    font-size: 14px;

    line-height: 1.6;
}


/* ============================================================
   TOPIC
   ============================================================ */

.topic-card {
    padding: 17px 20px;

    margin: 10px 0;

    border-radius: 15px;

    background: #101827;

    border: 1px solid #29354d;

    transition: all .22s ease;
}

.topic-card:hover {
    transform: translateX(7px);

    border-color: rgba(6,182,212,.55);

    box-shadow:
        0 10px 30px rgba(0,0,0,.22);
}


/* ============================================================
   INFO
   ============================================================ */

.info-card {
    padding: 18px;

    margin: 12px 0;

    border-radius: 14px;

    background: rgba(6,182,212,.05);

    border: 1px solid rgba(6,182,212,.2);

    color: #c7f9ff;

    font-size: 13px;

    line-height: 1.6;

    transition: all .2s ease;
}

.info-card:hover {
    transform: translateY(-3px);

    border-color: rgba(6,182,212,.45);
}


/* ============================================================
   FOOTER
   ============================================================ */

.footer {
    margin-top: 45px;

    padding-top: 22px;

    text-align: center;

    border-top: 1px solid #1e293b;

    color: #536078;

    font-size: 11px;
}


/* ============================================================
   MOBILE
   ============================================================ */

@media (max-width: 768px) {

    .block-container {
        padding-left: 15px;
        padding-right: 15px;
    }

    .hero-box {
        padding: 28px 22px;
    }

    .hero-title {
        font-size: 36px;
    }

    .hero-description {
        font-size: 14px;
    }

    .steps-container {
        overflow-x: auto;
        justify-content: flex-start;
        padding: 5px;
    }

    .step-item {
        flex-shrink: 0;
        font-size: 11px;
    }

    .step-line {
        width: 25px;
    }

    .section-title {
        font-size: 24px;
    }

    .question-text {
        font-size: 16px;
    }

    .metric-card {
        margin-bottom: 12px;
    }

    .stButton > button {
        min-height: 54px;
    }
}
</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# SESSION STATE
# ============================================================

if "screen" not in st.session_state:
    st.session_state.screen = "setup"

if "questions" not in st.session_state:
    st.session_state.questions = []

if "answers" not in st.session_state:
    st.session_state.answers = {}

if "results" not in st.session_state:
    st.session_state.results = None

if "confidence" not in st.session_state:
    st.session_state.confidence = 70

if "subject" not in st.session_state:
    st.session_state.subject = ""

if "topics" not in st.session_state:
    st.session_state.topics = (
        ""
    )


# ============================================================
# GEMINI
# ============================================================

def get_client():

    if not API_KEY:
        st.error(
            "Gemini API key was not found. "
            "Check your .env file."
        )
        st.stop()

    return genai.Client(
        api_key=API_KEY
    )


def generate_questions(subject, topics):

    client = get_client()

    prompt = f"""
You are an expert exam diagnostic AI.

Create exactly 5 multiple-choice questions for:

Subject:
{subject}

Topics:
{topics}

The questions must detect hidden weaknesses rather than
only testing memorization.

Use a mixture of:

- conceptual understanding
- application
- practical reasoning
- common misconception
- tricky exam-style reasoning

Return ONLY valid JSON.

Use exactly this format:

{{
  "questions": [
    {{
      "id": 1,
      "topic": "topic",
      "question": "question",
      "options": [
        "A. option",
        "B. option",
        "C. option",
        "D. option"
      ],
      "correct_answer": "A",
      "explanation": "short explanation"
    }}
  ]
}}

Rules:

- Exactly 5 questions.
- Exactly 4 options per question.
- Every option must begin with A., B., C. or D.
- correct_answer must be exactly A, B, C or D.
- Questions must be different.
- Keep explanations short.
- Return JSON only.
"""

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    text = response.text.strip()

    text = re.sub(
        r"```json",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = text.replace(
        "```",
        ""
    ).strip()

    data = json.loads(text)

    questions = data.get(
        "questions",
        []
    )

    if len(questions) != 5:
        raise ValueError(
            "Gemini did not return exactly 5 questions."
        )

    return questions


# ============================================================
# HERO
# ============================================================

st.html(
    """
<div class="hero-box">
<div class="hero-badge">✦ AI-POWERED EXAM DIAGNOSTICS</div>
<div class="hero-title">🎯 ExamRisk <span class="gradient-text">AI</span></div>
<div class="hero-description">Find what you think you know — but actually don't.<br>Measure the gap between your confidence and your real performance before the exam does it for you.</div>
</div>
"""
)


# ============================================================
# STEP BAR
# ============================================================

screen = st.session_state.screen

active1 = "step-active" if screen == "setup" else ""
active2 = "step-active" if screen == "test" else ""
active3 = "step-active" if screen == "results" else ""

st.html(
    f"""
<div class="steps-container">
<div class="step-item {active1}">
<div class="step-circle">1</div>
<div>Preparation</div>
</div>
<div class="step-line"></div>
<div class="step-item {active2}">
<div class="step-circle">2</div>
<div>Diagnostic</div>
</div>
<div class="step-line"></div>
<div class="step-item {active3}">
<div class="step-circle">3</div>
<div>Risk Report</div>
</div>
</div>
"""
)


# ============================================================
# SETUP
# ============================================================

if screen == "setup":

    st.html(
        """
<div class="section-title">Build your <span class="purple">diagnostic</span></div>
<div class="section-subtitle">Tell ExamRisk what you're preparing for. Gemini will create questions designed to expose hidden weaknesses.</div>
"""
    )

    left, right = st.columns(
        2,
        gap="large"
    )

    with left:

        st.html(
            """
<div class="custom-card">
<div class="card-title">📚 Subject</div>
<div class="card-description">What subject are you preparing for?</div>
</div>
"""
        )

        subject = st.text_input(
    "Subject",
    value=st.session_state.subject,
    placeholder="Enter subject",
    label_visibility="collapsed"
        )

        st.html(
            """
<div style="height:12px"></div>
<div class="custom-card">
<div class="card-title">🧩 Topics</div>
<div class="card-description">List the key topics you want to test.</div>
</div>
"""
        )

        topics = st.text_area(
    "Topics",
    value=st.session_state.topics,
    placeholder="Enter subject topics",
    height=105,
    label_visibility="collapsed"
        )

    with right:

        st.html(
            """
<div class="custom-card">
<div class="card-title">🎯 Your confidence level</div>
<div class="card-description">How confident are you about these topics?</div>
</div>
"""
        )

        confidence = st.slider(
            "Confidence",
            0,
            100,
            st.session_state.confidence,
            format="%d%%",
            label_visibility="collapsed"
        )

        if confidence >= 80:
            icon = "🔥"
            message = "Very confident — let's put that confidence to the test."
        elif confidence >= 60:
            icon = "⚡"
            message = "Fairly confident — let's verify it."
        elif confidence >= 40:
            icon = "🧠"
            message = "Somewhat unsure — this diagnostic will help."
        else:
            icon = "🌱"
            message = "Low confidence — let's find your starting point."

        st.html(
            f"""
<div class="confidence-card">
<div class="confidence-number">{icon} {confidence}% confidence</div>
<div class="confidence-message">{message}</div>
</div>
"""
        )

    st.write("")

    if st.button(
        "🧠   Start Diagnostic Test   →",
        use_container_width=True
    ):

        if not subject.strip():

            st.warning(
                "Please enter a subject."
            )

        elif not topics.strip():

            st.warning(
                "Please enter at least one topic."
            )

        else:

            with st.spinner(
                "Gemini is building your diagnostic..."
            ):

                try:

                    questions = generate_questions(
                        subject,
                        topics
                    )

                    st.session_state.questions = questions

                    st.session_state.answers = {}

                    st.session_state.results = None

                    st.session_state.confidence = confidence

                    st.session_state.subject = subject

                    st.session_state.topics = topics

                    st.session_state.screen = "test"

                    st.rerun()

                except Exception as error:

                    st.error(
                        "Could not generate the diagnostic."
                    )

                    st.caption(
                        str(error)
                    )


# ============================================================
# TEST
# ============================================================

elif screen == "test":

    st.html(
        """
<div class="section-title">🧠 Diagnostic <span class="purple">Test</span></div>
<div class="section-subtitle">Answer honestly. The goal isn't simply to score high — it's to discover where confidence doesn't match reality.</div>
"""
    )

    questions = st.session_state.questions

    total = len(questions)

    answered = len(
        st.session_state.answers
    )

    st.progress(
        answered / total
    )

    st.caption(
        f"{answered} of {total} questions answered"
    )

    for index, question in enumerate(
        questions
    ):

        topic = question.get(
            "topic",
            "General"
        )

        question_text = question.get(
            "question",
            ""
        )

        st.html(
            f"""
<div class="question-card">
<div class="question-label">QUESTION {index + 1}<span class="topic-pill">{topic}</span></div>
<div class="question-text">{question_text}</div>
</div>
"""
        )

        options = question.get(
            "options",
            []
        )

        selected = st.radio(
            "Choose your answer:",
            options,
            key=f"answer_{index}",
            index=None
        )

        if selected:
            st.session_state.answers[index] = selected

    st.write("")

    if st.button(
        "📊   Analyze My Exam Risk   →",
        use_container_width=True
    ):

        if len(
            st.session_state.answers
        ) < total:

            remaining = (
                total
                -
                len(st.session_state.answers)
            )

            st.warning(
                f"Please answer {remaining} remaining question(s)."
            )

        else:

            correct = 0

            topic_stats = {}

            for index, question in enumerate(
                questions
            ):

                selected = (
                    st.session_state.answers[index]
                )

                selected_letter = (
                    selected.strip()[0].upper()
                )

                correct_letter = (
                    question[
                        "correct_answer"
                    ].strip()[0].upper()
                )

                is_correct = (
                    selected_letter
                    ==
                    correct_letter
                )

                if is_correct:
                    correct += 1

                topic = question.get(
                    "topic",
                    "General"
                )

                if topic not in topic_stats:

                    topic_stats[topic] = {
                        "correct": 0,
                        "total": 0
                    }

                topic_stats[
                    topic
                ]["total"] += 1

                if is_correct:

                    topic_stats[
                        topic
                    ]["correct"] += 1

            performance = round(
                correct / total * 100
            )

            confidence_value = (
                st.session_state.confidence
            )

            gap = max(
                confidence_value
                -
                performance,
                0
            )

            if (
                performance < 50
                or gap >= 35
            ):

                risk = "HIGH"

            elif (
                performance < 75
                or gap >= 20
            ):

                risk = "MEDIUM"

            else:

                risk = "LOW"

            st.session_state.results = {
                "correct": correct,
                "performance": performance,
                "confidence": confidence_value,
                "gap": gap,
                "risk": risk,
                "topic_stats": topic_stats
            }

            st.session_state.screen = "results"

            st.rerun()


# ============================================================
# RESULTS
# ============================================================

elif screen == "results":

    results = st.session_state.results

    confidence = results["confidence"]

    performance = results["performance"]

    gap = results["gap"]

    risk = results["risk"]

    if risk == "HIGH":

        risk_class = "risk-high"

        message = (
            "Your confidence may be hiding important knowledge gaps."
        )

    elif risk == "MEDIUM":

        risk_class = "risk-medium"

        message = (
            "Some areas need targeted revision before the exam."
        )

    else:

        risk_class = "risk-low"

        message = (
            "Your confidence and demonstrated performance are aligned."
        )

    st.html(
        f"""
<div class="section-title">📊 Your Exam Risk <span class="purple">Report</span></div>
<div class="section-subtitle">Your confidence compared with your demonstrated performance.</div>
<div class="result-box">
<div class="result-label">CURRENT EXAM RISK</div>
<div class="{risk_class}">{risk}</div>
<div style="color:#94A3B8;font-size:14px;margin-top:6px">{message}</div>
</div>
"""
    )

    m1, m2, m3 = st.columns(
        3,
        gap="medium"
    )

    with m1:

        st.html(
            f"""
<div class="metric-card">
<div class="metric-label">Your Confidence</div>
<div class="metric-value">{confidence}%</div>
</div>
"""
        )

    with m2:

        st.html(
            f"""
<div class="metric-card">
<div class="metric-label">Actual Performance</div>
<div class="metric-value">{performance}%</div>
</div>
"""
        )

    with m3:

        st.html(
            f"""
<div class="metric-card">
<div class="metric-label">Confidence Gap</div>
<div class="metric-value">{gap}%</div>
</div>
"""
        )

    if gap >= 25:

        finding = (
            "You may be experiencing false confidence. "
            "You believe you are more prepared than your "
            "demonstrated performance suggests."
        )

    elif performance < 60:

        finding = (
            "Your biggest risk is knowledge that hasn't "
            "become reliable enough to perform under exam conditions."
        )

    else:

        finding = (
            "Your confidence and performance are reasonably aligned. "
            "Focus your remaining preparation on weaker topics."
        )

    st.html(
        f"""
<div class="finding-box">
<div class="finding-title">🧠 The most important finding</div>
<div class="finding-text">{finding}</div>
</div>
"""
    )

    st.html(
        """
<div class="section-title">Confidence <span class="purple">vs Reality</span></div>
"""
    )

    st.caption(
        "A large gap can indicate false confidence."
    )

    st.markdown(
        f"**Confidence — {confidence}%**"
    )

    st.progress(
        confidence / 100
    )

    st.markdown(
        f"**Demonstrated performance — {performance}%**"
    )

    st.progress(
        performance / 100
    )

    st.html(
        """
<div class="section-title">🎯 Topic <span class="purple">Risk Map</span></div>
"""
    )

    st.caption(
        "Your weakest areas should get your attention first."
    )

    sorted_topics = sorted(
        results["topic_stats"].items(),
        key=lambda item:
        item[1]["correct"] /
        item[1]["total"]
    )

    for topic, stats in sorted_topics:

        score = round(
            stats["correct"]
            /
            stats["total"]
            *
            100
        )

        if score < 50:

            status = "🔴 High priority"

        elif score < 75:

            status = "🟡 Needs revision"

        else:

            status = "🟢 Strong"

        st.html(
            f"""
<div class="topic-card">
<div style="display:flex;justify-content:space-between;align-items:center">
<div style="color:#f1f5f9;font-weight:700">{topic}</div>
<div style="color:#67e8f9;font-weight:800">{score}%</div>
</div>
<div style="margin-top:6px;color:#64748b;font-size:12px">{status} · {stats["correct"]}/{stats["total"]} correct</div>
</div>
"""
        )

    st.html(
        """
<div class="section-title">🚀 What to <span class="purple">study next</span></div>
"""
    )

    weak_topics = []

    for topic, stats in sorted_topics:

        score = (
            stats["correct"]
            /
            stats["total"]
        )

        if score < 0.75:

            weak_topics.append(
                topic
            )

    if weak_topics:

        for topic in weak_topics[:3]:

            st.html(
                f"""
<div class="info-card">📌 <b>Prioritize {topic}</b><br>Revisit the core concept and then solve application-based questions without looking at your notes.</div>
"""
            )

    else:

        st.html(
            """
<div class="info-card">✨ No major weak topic detected.<br>Try another diagnostic with harder application-based questions.</div>
"""
        )

    st.html(
        """
<div class="section-title">💡 Answer <span class="purple">Review</span></div>
"""
    )

    for index, question in enumerate(
        st.session_state.questions
    ):

        selected = (
            st.session_state.answers[index]
        )

        selected_letter = (
            selected.strip()[0].upper()
        )

        correct_letter = (
            question[
                "correct_answer"
            ].strip()[0].upper()
        )

        if selected_letter == correct_letter:

            st.success(
                f"Question {index + 1} — Correct"
            )

        else:

            st.error(
                f"Question {index + 1} — Incorrect · "
                f"Correct answer: {correct_letter}"
            )

        with st.expander(
            "💡 View explanation"
        ):

            st.write(
                question.get(
                    "explanation",
                    "No explanation available."
                )
            )

    st.write("")

    if st.button(
        "🔄   Take Another Diagnostic   →",
        use_container_width=True
    ):

        st.session_state.screen = "setup"

        st.session_state.questions = []

        st.session_state.answers = {}

        st.session_state.results = None

        st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.html(
    """
<div class="footer">
ExamRisk AI · Powered by Gemini · Built for ML AlgoRush
</div>
"""
)