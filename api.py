from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from ai import (
    analyze_resume,
    optimize_resume_bullets,
)
from pdf_reader import extract_text_from_pdf
from scoring import calculate_skill_match


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://192.168.1.80:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "status": "Matchline backend running"
    }


@app.post("/analyze")
async def analyze(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    resume_text = extract_text_from_pdf(
        resume.file
    )

    analysis = analyze_resume(
        resume_text,
        job_description
    )

    return analysis


@app.post("/optimize")
async def optimize(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    resume_text = extract_text_from_pdf(
        resume.file
    )

    skill_analysis = calculate_skill_match(
        resume_text,
        job_description
    )

    optimized_bullets = optimize_resume_bullets(
        resume_text,
        job_description,
        skill_analysis["matching_skills"],
        skill_analysis["missing_skills"]
    )

    print(
        "OPTIMIZED BULLETS:",
        optimized_bullets
    )

    return {
        "optimized_bullets": optimized_bullets
    }