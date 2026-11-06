import os
from dotenv import load_dotenv
from google import genai


# Load API key from .env
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

def generate_basic_recommendations(results):
    """Generate basic recommendations without using an AI API."""

    matched_skills = results["matched_skills"]
    missing_skills = results["missing_skills"]
    match_score = results["match_score"]

    recommendations = []

    recommendations.append("RESUME STRENGTHS")
    if matched_skills:
        recommendations.append(
            "Your resume includes these relevant skills: "
            + ", ".join(matched_skills)
            + "."
        )
    else:
        recommendations.append(
            "No recognised matching skills were found."
        )

    recommendations.append("\nMISSING SKILLS")
    if missing_skills:
        recommendations.append(
            "The following job-related skills were not detected: "
            + ", ".join(missing_skills)
            + "."
        )
        recommendations.append(
            "If you have these skills, consider highlighting "
            "them in your resume with relevant examples."
        )
    else:
        recommendations.append(
            "All recognised skills from the job description "
            "were found in the resume."
        )

    recommendations.append("\nSKILL COVERAGE")
    recommendations.append(
        "Your resume covers "
        + str(match_score)
        + "% of the recognised skills required by the job."
    )

    recommendations.append("\nIMPROVEMENT SUGGESTION")
    recommendations.append(
        "Highlight relevant projects and explain how you used "
        "your skills. Only include skills and experience "
        "that you genuinely possess."
    )

    return "\n".join(recommendations)

def generate_recommendations(resume_text, job_description, results):
    """Generate resume improvement recommendations using Gemini."""

    if not api_key:
        return "Error: Gemini API key not found in .env file."

    try:
        # Connect to Gemini
        client = genai.Client(api_key=api_key)

        # Prompt for Gemini
        prompt = f"""
        You are an expert resume analyser and career advisor.

        Analyse the following resume based on the given job description.

        RESUME:
        {resume_text}

        JOB DESCRIPTION:
        {job_description}

        SKILL ANALYSIS:

        Matched Skills:
        {results["matched_skills"]}

        Missing Skills:
        {results["missing_skills"]}

        Skill Coverage Score:
        {results["match_score"]}%

        Based on this information, provide:

        1. Resume Strengths:
        Identify the strong points of the resume.

        2. Missing Skills Analysis:
        Explain the importance of the missing skills.

        3. Improvement Suggestions:
        Suggest specific ways to improve the resume.

        4. Keyword Recommendations:
        Suggest relevant keywords from the job description
        that the candidate could include where truthful.

        5. Overall Feedback:
        Give a brief assessment of how well the resume
        aligns with the job description.

        IMPORTANT:
        - Do not invent qualifications or experience.
        - Do not claim the candidate possesses missing skills.
        - Base your suggestions on the provided information.
        - Keep the response clear and beginner-friendly.
        """

        # Generate response
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )

        return response.text

    except Exception as e:
        print("Gemini API unavailable:", e)
        print("Using basic recommendations instead.")

        return generate_basic_recommendations(results)