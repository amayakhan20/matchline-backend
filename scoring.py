import re


COMPETENCIES = {
    "Python": [
        "python"
    ],

    "SQL": [
        "sql",
        "postgresql",
        "mysql",
        "sqlite"
    ],

    "R": [
        "r programming",
        "rstudio",
        "tidyverse",
        "ggplot2",
        "dplyr"
    ],

    "Excel": [
        "excel",
        "microsoft excel"
    ],

    "Tableau": [
        "tableau"
    ],

    "Power BI": [
        "power bi",
        "powerbi"
    ],

    "Pandas": [
        "pandas"
    ],

    "NumPy": [
        "numpy"
    ],

    "Matplotlib": [
        "matplotlib"
    ],

    "Scikit-learn": [
        "scikit-learn",
        "sklearn"
    ],

    "XGBoost": [
        "xgboost"
    ],

    "Machine Learning": [
        "machine learning",
        "predictive modeling",
        "predictive modelling",
        "predictive model",
        "predictive models"
    ],

    "Statistics": [
        "statistics",
        "statistical analysis",
        "statistical modeling",
        "statistical modelling",
        "statistical methods",
        "statistical"
    ],

    "Data Analysis": [
        "data analysis",
        "data analytics",
        "analyze data",
        "analyse data"
    ],

    "Data Cleaning": [
        "data cleaning",
        "data preprocessing",
        "data preparation",
        "cleaned data",
        "cleaning data"
    ],

    "Data Visualization": [
        "data visualization",
        "data visualisation",
        "visualization",
        "visualisation",
        "dashboard",
        "dashboards"
    ],

    "Regression": [
        "regression",
        "linear regression",
        "logistic regression"
    ],

    "Classification": [
        "classification",
        "classifier"
    ],

    "Clustering": [
        "clustering",
        "k-means",
        "kmeans"
    ],

    "Feature Engineering": [
        "feature engineering"
    ],

    "Cross-Validation": [
        "cross-validation",
        "cross validation"
    ],

    "A/B Testing": [
        "a/b testing",
        "a/b test",
        "ab testing",
        "experimentation",
        "experiment design"
    ],

    "Hypothesis Testing": [
        "hypothesis testing",
        "hypothesis test"
    ],

    "Model Evaluation": [
        "model evaluation",
        "model accuracy",
        "model performance",
        "evaluate models",
        "evaluate model",
        "evaluation metrics",
        "accuracy",
        "precision",
        "recall",
        "f1 score",
        "mse",
        "rmse",
        "auc"
    ],

    "NLP": [
        "natural language processing",
        "nlp"
    ],

    "Generative AI": [
        "generative ai",
        "genai",
        "large language model",
        "large language models",
        "llm",
        "llms"
    ],

    "AI Evaluation": [
        "ai evaluation",
        "evaluate ai",
        "review ai-generated",
        "ai-generated content",
        "model reasoning",
        "ai systems",
        "ai system"
    ],

    "Git": [
        "git",
        "github"
    ],

    "Docker": [
        "docker"
    ],

    "AWS": [
        "aws",
        "amazon web services"
    ],

    "Azure": [
        "azure"
    ],

    "Google Cloud": [
        "google cloud",
        "gcp"
    ],

    "Spark": [
        "apache spark",
        "pyspark",
        "spark"
    ],

    "Communication": [
        "communication",
        "communicate",
        "communicating",
        "presentation",
        "present findings",
        "stakeholder communication"
    ],

    "Leadership": [
        "leadership",
        "team lead",
        "shift lead",
        "led a team",
        "led team"
    ],

    "Analytical Thinking": [
        "analytical thinking",
        "analytical skills",
        "problem solving",
        "problem-solving",
        "critical thinking"
    ],
}


JOB_SIGNALS = {
    "data science": [
        "Data Analysis",
        "Statistics",
        "Machine Learning"
    ],

    "data scientist": [
        "Data Analysis",
        "Statistics",
        "Machine Learning"
    ],

    "data science expertise": [
        "Data Analysis",
        "Statistics",
        "Machine Learning"
    ],

    "model accuracy": [
        "Model Evaluation"
    ],

    "model performance": [
        "Model Evaluation"
    ],

    "model reasoning": [
        "AI Evaluation"
    ],

    "ai-generated": [
        "AI Evaluation"
    ],

    "ai systems": [
        "AI Evaluation"
    ],

    "analytical thinking": [
        "Analytical Thinking"
    ],

    "communication skills": [
        "Communication"
    ],
}


COMPETENCY_WEIGHTS = {
    "AI Evaluation": 3,
    "Model Evaluation": 3,
    "Machine Learning": 3,
    "Python": 3,
    "SQL": 3,
    "Scikit-learn": 3,
    "XGBoost": 3,
    "NLP": 3,
    "Generative AI": 3,

    "Statistics": 2,
    "Data Analysis": 2,
    "Analytical Thinking": 2,
    "R": 2,
    "Tableau": 2,
    "Power BI": 2,
    "Pandas": 2,
    "NumPy": 2,
    "Data Cleaning": 2,
    "Data Visualization": 2,
    "Regression": 2,
    "Classification": 2,
    "Clustering": 2,
    "Feature Engineering": 2,
    "Cross-Validation": 2,
    "A/B Testing": 2,
    "Hypothesis Testing": 2,
    "Docker": 2,
    "AWS": 2,
    "Azure": 2,
    "Google Cloud": 2,
    "Spark": 2,

    "Communication": 1,
    "Excel": 1,
    "Matplotlib": 1,
    "Git": 1,
    "Leadership": 1,
}


def normalize_text(text):
    text = text.lower()
    text = text.replace("–", "-")
    text = text.replace("—", "-")
    text = re.sub(r"\s+", " ", text)

    return text


def contains_phrase(text, phrase):
    text = normalize_text(text)
    phrase = normalize_text(phrase)

    pattern = (
        r"(?<!\w)"
        + re.escape(phrase)
        + r"(?!\w)"
    )

    return (
        re.search(
            pattern,
            text,
            flags=re.IGNORECASE
        )
        is not None
    )


def extract_resume_competencies(resume_text):
    detected = set()

    for competency, aliases in COMPETENCIES.items():
        for alias in aliases:
            if contains_phrase(
                resume_text,
                alias
            ):
                detected.add(competency)
                break

    return detected


def extract_job_competencies(job_description):
    detected = set()

    for competency, aliases in COMPETENCIES.items():
        for alias in aliases:
            if contains_phrase(
                job_description,
                alias
            ):
                detected.add(competency)
                break

    for phrase, competencies in JOB_SIGNALS.items():
        if contains_phrase(
            job_description,
            phrase
        ):
            for competency in competencies:
                detected.add(competency)

    return detected


def find_skill_evidence(
    text,
    competency
):
    aliases = COMPETENCIES.get(
        competency,
        []
    )

    lines = re.split(
        r"(?<=[.!?])\s+|\n+",
        text
    )

    for line in lines:
        line = line.strip()

        if not line:
            continue

        for alias in aliases:
            if contains_phrase(
                line,
                alias
            ):
                evidence = re.sub(
                    r"\s+",
                    " ",
                    line
                ).strip()

                if len(evidence) > 280:
                    evidence = (
                        evidence[:277]
                        + "..."
                    )

                return evidence

    return ""


def calculate_skill_match(
    resume_text,
    job_description
):
    resume_skills = (
        extract_resume_competencies(
            resume_text
        )
    )

    job_skills = (
        extract_job_competencies(
            job_description
        )
    )

    matching_skills = sorted(
        resume_skills.intersection(
            job_skills
        )
    )

    missing_skills = sorted(
        job_skills.difference(
            resume_skills
        )
    )

    total_job_skills = len(
        job_skills
    )

    total_weight = sum(
        COMPETENCY_WEIGHTS.get(
            skill,
            1
        )
        for skill in job_skills
    )

    matched_weight = sum(
        COMPETENCY_WEIGHTS.get(
            skill,
            1
        )
        for skill in matching_skills
    )

    if total_weight == 0:
        match_score = 0
    else:
        match_score = round(
            (
                matched_weight
                / total_weight
            )
            * 100
        )

    if match_score >= 80:
        match_label = "Strong match"

    elif match_score >= 60:
        match_label = "Good match"

    elif match_score >= 40:
        match_label = "Moderate match"

    else:
        match_label = "Low match"

    matching_evidence = {}

    for skill in matching_skills:
        matching_evidence[
            skill
        ] = find_skill_evidence(
            resume_text,
            skill
        )
    ats_score = 100

    ats_passed = []

    ats_warnings = []

    if "@" in resume_text:

        ats_passed.append("Email detected")

    else:

        ats_warnings.append("Email not detected")

        ats_score -= 10

    if "skills" in resume_text.lower():

        ats_passed.append("Skills section")

    else:

        ats_warnings.append("Skills section missing")

        ats_score -= 10

    if "education" in resume_text.lower():

        ats_passed.append("Education section")

    else:

        ats_warnings.append("Education section missing")

        ats_score -= 10

    if "experience" in resume_text.lower():

        ats_passed.append("Experience section")

    else:

        ats_warnings.append("Experience section missing")

        ats_score -= 10

    return {
        "match_score": match_score,
        "match_label": match_label,

        "matching_skills":
            matching_skills,

        "missing_skills":
            missing_skills,

        "resume_skills":
            sorted(resume_skills),

        "job_skills":
            sorted(job_skills),

        "matched_count":
            len(matching_skills),

        "missing_count":
            len(missing_skills),

        "total_job_skills":
            total_job_skills,

        "matching_evidence":
            matching_evidence,

        "matched_weight":
            matched_weight,

        "total_weight":
            total_weight,

    "ats_score": ats_score,
    "ats_passed": ats_passed,
    "ats_warnings": ats_warnings,
    }