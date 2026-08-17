import streamlit as st

from pdf_reader import extract_text_from_pdf
from ai import analyze_resume


st.set_page_config(
    page_title="Matchline",
    page_icon="M",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# -----------------------------
# CUSTOM STYLING
# -----------------------------

st.html("""
<style>

    .block-container {
        max-width: 1120px;
        padding-top: 1.8rem;
        padding-bottom: 5rem;
    }

    header[data-testid="stHeader"] {
        background: transparent;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    h1, h2, h3 {
        letter-spacing: -0.035em;
    }

    .nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 4.5rem;
    }

    .logo-wrap {
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .logo-mark {
        height: 30px;
        width: 30px;
        border-radius: 9px;
        background: #111827;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 0.82rem;
        font-weight: 800;
    }

    .logo-name {
        font-size: 1rem;
        font-weight: 700;
        color: #111827;
    }

    .nav-label {
        font-size: 0.82rem;
        color: #6B7280;
        border: 1px solid #E5E7EB;
        border-radius: 999px;
        padding: 7px 12px;
        background: #FFFFFF;
    }

    .hero {
        max-width: 850px;
        margin-bottom: 3.2rem;
    }

    .eyebrow {
        color: #2563EB;
        text-transform: uppercase;
        font-size: 0.74rem;
        font-weight: 750;
        letter-spacing: 0.13em;
        margin-bottom: 1rem;
    }

    .hero-title {
        color: #0F172A;
        font-size: 4rem;
        font-weight: 750;
        line-height: 1.02;
        letter-spacing: -0.058em;
        margin-bottom: 1.2rem;
    }

    .hero-copy {
        color: #64748B;
        font-size: 1.12rem;
        line-height: 1.65;
        max-width: 700px;
    }

    .workflow {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 12px;
        margin-bottom: 3.2rem;
    }

    .workflow-card {
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 17px 18px;
        background: #FAFAFA;
    }

    .workflow-num {
        color: #94A3B8;
        font-size: 0.72rem;
        font-weight: 700;
        margin-bottom: 0.45rem;
    }

    .workflow-title {
        color: #111827;
        font-size: 0.96rem;
        font-weight: 700;
        margin-bottom: 0.22rem;
    }

    .workflow-copy {
        color: #6B7280;
        font-size: 0.85rem;
        line-height: 1.45;
    }

    .input-heading {
        color: #111827;
        font-size: 1.12rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }

    .input-copy {
        color: #6B7280;
        font-size: 0.88rem;
        margin-bottom: 0.8rem;
    }

    div[data-testid="stFileUploader"] {
        border-radius: 12px;
    }

    div[data-testid="stTextArea"] textarea {
        border-radius: 12px !important;
        border-color: #E5E7EB !important;
        background: #F8FAFC !important;
    }

    .stButton > button {
        min-height: 50px !important;
        border-radius: 10px !important;
        font-weight: 650 !important;
        box-shadow: none !important;
        letter-spacing: -0.01em;
    }

    .section-kicker {
        color: #2563EB;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-size: 0.72rem;
        font-weight: 750;
        margin-bottom: 0.35rem;
    }

    .section-title {
        color: #111827;
        font-size: 2rem;
        font-weight: 730;
        letter-spacing: -0.04em;
        margin-bottom: 1.4rem;
    }

    .score-card {
        border: 1px solid #E5E7EB;
        border-radius: 16px;
        background: #FFFFFF;
        padding: 28px;
        margin-bottom: 14px;
    }

    .score-label {
        color: #64748B;
        font-size: 0.8rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }

    .score-number {
        color: #0F172A;
        font-size: 3.8rem;
        font-weight: 760;
        letter-spacing: -0.06em;
        line-height: 1;
    }

    .score-number span {
        color: #94A3B8;
        font-size: 1.6rem;
        font-weight: 500;
    }

    .score-caption {
        margin-top: 0.8rem;
        color: #64748B;
        font-size: 0.9rem;
    }

    .skill-card {
        border: 1px solid #E5E7EB;
        border-radius: 14px;
        padding: 22px;
        background: #FFFFFF;
        height: 100%;
    }

    .card-label {
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-size: 0.7rem;
        font-weight: 750;
        margin-bottom: 0.45rem;
    }

    .card-title {
        color: #111827;
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }

    .skill-pill {
        display: inline-block;
        padding: 7px 11px;
        border: 1px solid #E5E7EB;
        background: #F8FAFC;
        border-radius: 999px;
        color: #334155;
        font-size: 0.84rem;
        margin: 3px 4px 3px 0;
    }

    .gap-pill {
        background: #FFF7ED;
        border-color: #FED7AA;
        color: #9A3412;
    }

    .recommendation {
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 18px 20px;
        background: #FFFFFF;
        margin-bottom: 10px;
        display: flex;
        gap: 14px;
    }

    .rec-num {
        color: #2563EB;
        font-size: 0.78rem;
        font-weight: 750;
        min-width: 22px;
    }

    .rec-copy {
        color: #334155;
        font-size: 0.94rem;
        line-height: 1.55;
    }

    .question-box {
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 17px 19px;
        background: #F8FAFC;
        color: #334155;
        margin-bottom: 9px;
        line-height: 1.5;
        font-size: 0.94rem;
    }

    .footer-note {
        text-align: center;
        color: #94A3B8;
        font-size: 0.78rem;
        margin-top: 4rem;
    }

</style>
""")


# -----------------------------
# NAV / BRAND
# -----------------------------

st.html("""
<div class="nav">
    <div class="logo-wrap">
        <div class="logo-mark">M</div>
        <div class="logo-name">Matchline</div>
    </div>

    <div class="nav-label">
        Resume intelligence
    </div>
</div>
""")


# -----------------------------
# HERO
# -----------------------------

st.html("""
<div class="hero">
    <div class="eyebrow">Application intelligence</div>

    <div class="hero-title">
        Know where you stand before you apply.
    </div>

    <div class="hero-copy">
        Compare your resume with a target role, identify the skills that
        already align, and see exactly where your application can improve.
    </div>
</div>
""")


# -----------------------------
# WORKFLOW
# -----------------------------

st.html("""
<div class="workflow">

    <div class="workflow-card">
        <div class="workflow-num">01</div>
        <div class="workflow-title">Add your resume</div>
        <div class="workflow-copy">
            Upload the PDF you plan to use for your application.
        </div>
    </div>

    <div class="workflow-card">
        <div class="workflow-num">02</div>
        <div class="workflow-title">Add the role</div>
        <div class="workflow-copy">
            Paste the full description for the position you're targeting.
        </div>
    </div>

    <div class="workflow-card">
        <div class="workflow-num">03</div>
        <div class="workflow-title">Review your fit</div>
        <div class="workflow-copy">
            Get a match score, skill gaps, and focused next steps.
        </div>
    </div>

</div>
""")


# -----------------------------
# INPUT FORM
# -----------------------------

left, right = st.columns([1, 1], gap="large")

with left:

    st.html("""
    <div class="input-heading">Resume</div>
    <div class="input-copy">
        Upload a PDF copy of your current resume.
    </div>
    """)

    resume = st.file_uploader(
        "Upload resume",
        type=["pdf"],
        label_visibility="collapsed"
    )


with right:

    st.html("""
    <div class="input-heading">Target role</div>
    <div class="input-copy">
        Paste the job description you want to compare against.
    </div>
    """)

    job_description = st.text_area(
        "Job description",
        placeholder="Paste the job description here...",
        height=175,
        label_visibility="collapsed"
    )


st.write("")

analyze_button = st.button(
    "Run analysis",
    type="primary",
    width="stretch"
)


# -----------------------------
# ANALYSIS
# -----------------------------

if analyze_button:

    if resume is None:

        st.warning(
            "Upload your resume before running the analysis."
        )

    elif not job_description.strip():

        st.warning(
            "Paste a job description before running the analysis."
        )

    else:

        resume_text = extract_text_from_pdf(resume)

        with st.spinner(
            "Comparing your resume with the role..."
        ):

            analysis = analyze_resume(
                resume_text,
                job_description
            )


        score = analysis["match_score"]

        matched = analysis["matching_skills"]
        missing = analysis["missing_skills"]

        recommendations = analysis["resume_improvements"]
        questions = analysis["interview_questions"]


        st.write("")
        st.write("")
        st.divider()
        st.write("")
        st.write("")


        # -----------------------------
        # MATCH OVERVIEW
        # -----------------------------

        st.html("""
        <div class="section-kicker">Match analysis</div>
        <div class="section-title">Your application at a glance</div>
        """)

        score_col, details_col = st.columns(
            [0.85, 1.6],
            gap="large"
        )


        with score_col:

            if score >= 80:
                score_text = "Strong alignment"

            elif score >= 60:
                score_text = "Competitive with improvements"

            else:
                score_text = "Meaningful gaps to address"


            st.html(
                f"""
                <div class="score-card">

                    <div class="score-label">
                        Resume match score
                    </div>

                    <div class="score-number">
                        {score}<span>/100</span>
                    </div>

                    <div class="score-caption">
                        {score_text}
                    </div>

                </div>
                """
            )

            st.progress(score / 100)


        with details_col:

            skill_a, skill_b = st.columns(
                2,
                gap="medium"
            )

            with skill_a:

                pills = "".join(
                    f'<span class="skill-pill">{skill}</span>'
                    for skill in matched
                )

                st.html(
                    f"""
                    <div class="skill-card">

                        <div class="card-label">
                            Strengths
                        </div>

                        <div class="card-title">
                            Matching skills
                        </div>

                        {pills}

                    </div>
                    """
                )


            with skill_b:

                gap_pills = "".join(
                    f'<span class="skill-pill gap-pill">{skill}</span>'
                    for skill in missing
                )

                st.html(
                    f"""
                    <div class="skill-card">

                        <div class="card-label">
                            Opportunity
                        </div>

                        <div class="card-title">
                            Skills to strengthen
                        </div>

                        {gap_pills}

                    </div>
                    """
                )


        # -----------------------------
        # RECOMMENDATIONS
        # -----------------------------

        st.write("")
        st.write("")
        st.write("")

        st.html("""
        <div class="section-kicker">Recommendations</div>
        <div class="section-title">What to improve before applying</div>
        """)


        for index, recommendation in enumerate(
            recommendations,
            start=1
        ):

            st.html(
                f"""
                <div class="recommendation">

                    <div class="rec-num">
                        {str(index).zfill(2)}
                    </div>

                    <div class="rec-copy">
                        {recommendation}
                    </div>

                </div>
                """
            )


        # -----------------------------
        # INTERVIEW PREP
        # -----------------------------

        st.write("")
        st.write("")
        st.write("")

        st.html("""
        <div class="section-kicker">Interview preparation</div>
        <div class="section-title">Questions to prepare for</div>
        """)


        for question in questions:

            st.html(
                f"""
                <div class="question-box">
                    {question}
                </div>
                """
            )


        # -----------------------------
        # RAW RESUME
        # -----------------------------

        st.write("")

        with st.expander(
            "View extracted resume text"
        ):

            st.text(resume_text)


        st.html("""
        <div class="footer-note">
            Matchline • Built for smarter applications
        </div>
        """)