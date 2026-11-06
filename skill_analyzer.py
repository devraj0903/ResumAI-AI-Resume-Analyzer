import re


# main skills and alternative names
SKILL_SYNONYMS = {
    "Python": ["python", "python programming"],
    "Java": ["java", "java programming"],
    "C": ["c"],
    "C++": ["c++"],
    "JavaScript": ["javascript", "js"],
    "HTML": ["html", "html5"],
    "CSS": ["css", "css3"],
    "SQL": ["sql"],
    "MySQL": ["mysql"],
    "SQLite": ["sqlite"],
    "MongoDB": ["mongodb"],
    "Flask": ["flask"],
    "Django": ["django"],
    "FastAPI": ["fastapi"],
    "React": ["react", "react.js"],
    "Node.js": ["node.js", "nodejs"],
    "Git": ["git", "version control"],
    "GitHub": ["github"],
    "REST API": ["rest api", "rest apis", "restful api", "restful apis"],
    "Data Structures": ["data structures"],
    "Algorithms": ["algorithms"],
    "Machine Learning": ["machine learning", "ml"],
    "Deep Learning": ["deep learning"],
    "Artificial Intelligence": ["artificial intelligence", "ai"],
    "Data Analysis": ["data analysis", "data analytics"],
    "Pandas": ["pandas"],
    "NumPy": ["numpy"],
    "Matplotlib": ["matplotlib"],
    "Database Management": ["database management", "dbms"],
    "OOP": ["oop", "object-oriented programming", "object oriented programming"],
    "Operating Systems": ["operating systems", "os"],
    "Computer Networks": ["computer networks", "networking"],
    "Cloud Computing": ["cloud computing"],
    "Docker": ["docker"],
    "Linux": ["linux"],
    "Problem Solving": ["problem solving", "problem-solving"]
}

# to find recognised skills in a given text.
def find_skills(text):

    found_skills = []

    text = text.lower()

    for skill, synonyms in SKILL_SYNONYMS.items():

        for synonym in synonyms:

            # to match the complete term rather than part of another word
            pattern = r"(?<!\w)" + re.escape(synonym) + r"(?!\w)"

            if re.search(pattern, text):
                found_skills.append(skill)
                break

    return found_skills


def analyze_skills(resume_text, job_description):
    """Compare resume skills with job requirements."""

    resume_skills = find_skills(resume_text)
    required_skills = find_skills(job_description)

    matched_skills = []
    missing_skills = []

    for skill in required_skills:

        if skill in resume_skills:
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    # to calculate the percentage of recognised required skills found
    if len(required_skills) > 0:
        match_score = (
            len(matched_skills) / len(required_skills)
        ) * 100
    else:
        match_score = 0

    results = {
        "resume_skills": resume_skills,
        "required_skills": required_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "match_score": round(match_score, 2)
    }

    return results