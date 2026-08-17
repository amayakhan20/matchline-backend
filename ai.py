import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from scoring import calculate_skill_match


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def generate_analysis_feedback(
    resume_text,
    job_description,
    matching_skills,
    missing_skills
):
    prompt = f"""
Analyze this candidate's resume for the target job.

Matching competencies:
{matching_skills}

Missing competencies:
{missing_skills}

Return ONLY valid JSON in this exact structure:

{{
  "resume_improvements": [
    "recommendation 1",
    "recommendation 2",
    "recommendation 3"
  ],
  "interview_questions": [
    "question 1",
    "question 2",
    "question 3"
  ]
}}

Rules:
- Return exactly 3 resume improvements.
- Return exactly 3 interview questions.
- Do not invent experience, skills, metrics, projects, or accomplishments.
- Recommendations must be specific to this candidate and role.
- Interview questions should use the candidate's real experience when useful.
- If a missing competency is not supported by the resume, do not tell the
  candidate to falsely claim it.
- Do not include markdown.
- Do not include commentary before or after the JSON.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}
"""

    response = client.responses.create(
        model="gpt-5-mini",
        instructions=(
            "You are a precise career coach. "
            "Return only valid JSON and never invent candidate experience."
        ),
        input=prompt,
    )

    raw_output = response.output_text.strip()

    try:
        data = json.loads(raw_output)

        resume_improvements = data.get(
            "resume_improvements",
            []
        )

        interview_questions = data.get(
            "interview_questions",
            []
        )

    except Exception as error:
        print(
            "Analysis JSON parsing error:",
            error
        )

        print(
            "RAW ANALYSIS OUTPUT:",
            raw_output
        )

        resume_improvements = []
        interview_questions = []

    # Fallback recommendations
    if len(resume_improvements) < 3 and missing_skills:
        resume_improvements.append(
            "Strengthen the resume's evidence for role-relevant areas such as "
            + ", ".join(missing_skills[:3])
            + ", but only add skills that accurately reflect your experience."
        )

    if len(resume_improvements) < 3:
        resume_improvements.append(
            "Make your most relevant technical projects easier to find by "
            "emphasizing the methods, tools, and outcomes that align with "
            "the target role."
        )

    if len(resume_improvements) < 3:
        resume_improvements.append(
            "Strengthen impact-focused bullets by connecting your technical "
            "work to the result or decision it supported without adding "
            "unsupported metrics."
        )

    # Fallback interview questions
    if len(interview_questions) < 3:
        interview_questions.append(
            "How would you evaluate the quality and reliability of a model's "
            "output for this role?"
        )

    if len(interview_questions) < 3:
        interview_questions.append(
            "Tell me about a project where you used data to make or support "
            "a decision."
        )

    if len(interview_questions) < 3:
        interview_questions.append(
            "How would you communicate a complex analytical finding to a "
            "non-technical stakeholder?"
        )

    return {
        "resume_improvements":
            resume_improvements[:3],

        "interview_questions":
            interview_questions[:3],
    }


def optimize_resume_bullets(
    resume_text,
    job_description,
    matching_skills,
    missing_skills
):
    prompt = f"""
You are rewriting resume bullets.

Return ONLY valid JSON.

{{
  "optimized_bullets": [
    {{
      "original": "...",
      "optimized": "..."
    }},
    {{
      "original": "...",
      "optimized": "..."
    }},
    {{
      "original": "...",
      "optimized": "..."
    }}
  ]
}}

Rules:
- Return exactly 3 bullet pairs.
- The "original" field must be copied EXACTLY from the resume.
- The "optimized" field should rewrite that same bullet.
- Never invent experience.
- Never invent metrics.
- Never invent projects.
- Never invent skills.
- Never invent accomplishments.
- Preserve factual accuracy.
- Use stronger wording where appropriate.
- Make the optimized bullet recruiter-friendly.
- Do not include markdown.
- Do not include commentary.

Matching competencies:
{matching_skills}

Missing competencies:
{missing_skills}

RESUME:

{resume_text}

JOB DESCRIPTION:

{job_description}
"""

    response = client.responses.create(
        model="gpt-5-mini",
        instructions=(
            "Return only valid JSON."
        ),
        input=prompt,
    )

    raw_output = response.output_text.strip()

    try:
        data = json.loads(raw_output)

        optimized_bullets = data.get(
            "optimized_bullets",
            []
        )

    except Exception as error:
        print(
            "Optimizer JSON parsing error:",
            error
        )

        print(
            "RAW OPTIMIZER OUTPUT:",
            raw_output
        )

        optimized_bullets = []

    return optimized_bullets[:3]


def analyze_resume(
    resume_text,
    job_description
):
    # -----------------------------------
    # 1. DETERMINISTIC PYTHON SCORING
    # -----------------------------------

    skill_analysis = calculate_skill_match(
        resume_text,
        job_description
    )

    match_score = skill_analysis[
        "match_score"
    ]

    match_label = skill_analysis[
        "match_label"
    ]

    matching_skills = skill_analysis[
        "matching_skills"
    ]

    missing_skills = skill_analysis[
        "missing_skills"
    ]

    # -----------------------------------
    # 2. ONE OPENAI CALL
    # -----------------------------------

    feedback = generate_analysis_feedback(
        resume_text,
        job_description,
        matching_skills,
        missing_skills
    )

    resume_improvements = feedback[
        "resume_improvements"
    ]

    interview_questions = feedback[
        "interview_questions"
    ]

    # -----------------------------------
    # DEBUG
    # -----------------------------------

    print("\n==============================")
    print("MATCHLINE ANALYSIS")
    print("==============================")

    print(
        "MATCH SCORE:",
        match_score
    )

    print(
        "MATCH LABEL:",
        match_label
    )

    print(
        "MATCHING SKILLS:",
        matching_skills
    )

    print(
        "MISSING SKILLS:",
        missing_skills
    )

    print(
        "MATCHING EVIDENCE:",
        skill_analysis[
            "matching_evidence"
        ]
    )

    print(
        "RESUME IMPROVEMENTS:",
        resume_improvements
    )

    print(
        "INTERVIEW QUESTIONS:",
        interview_questions
    )

    print("==============================\n")

    # -----------------------------------
    # RETURN TO NEXT.JS
    # -----------------------------------

    return {
        "match_score":
            match_score,

        "match_label":
            match_label,

        "matched_count":
            skill_analysis[
                "matched_count"
            ],

        "missing_count":
            skill_analysis[
                "missing_count"
            ],

        "total_job_skills":
            skill_analysis[
                "total_job_skills"
            ],

        "matched_weight":
            skill_analysis[
                "matched_weight"
            ],

        "total_weight":
            skill_analysis[
                "total_weight"
            ],
        "ats_score":
            skill_analysis[
                "ats_score"
            ],

        "ats_passed":
            skill_analysis[
                "ats_passed"
            ],

        "ats_warnings":
            skill_analysis[
                "ats_warnings"
            ],

        "matching_skills":
            matching_skills,

        "missing_skills":
            missing_skills,

        "resume_skills":
            skill_analysis[
                "resume_skills"
            ],

        "job_skills":
            skill_analysis[
                "job_skills"
            ],

        "matching_evidence":
            skill_analysis[
                "matching_evidence"
            ],

        "resume_improvements":
            resume_improvements,

        "interview_questions":
            interview_questions,
    }