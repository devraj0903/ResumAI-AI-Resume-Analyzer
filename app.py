import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

from resume_parser import extract_resume_text
from skill_analyzer import analyze_skills
from ai_recommender import generate_recommendations


app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10 MB

# Creates uploads folder if it does not exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# to check whether the uploaded file is a PDF.
def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        # to get uploaded resume
        if "resume" not in request.files:
            return render_template(
                "index.html",
                error="Please upload your resume."
            )

        file = request.files["resume"]

        # checks whether a file was selected
        if file.filename == "":
            return render_template(
                "index.html",
                error="No file selected."
            )

        # to validate PDF extension
        if not allowed_file(file.filename):
            return render_template(
                "index.html",
                error="Please upload a PDF file only."
            )

        # to get job description
        job_description = request.form.get(
            "job_description", ""
        ).strip()

        if not job_description:
            return render_template(
                "index.html",
                error="Please enter a job description."
            )

        # savse uploaded file temporarily
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)

        try:
            file.save(file_path)

            # extracts resume text
            resume_text = extract_resume_text(file_path)

            if not resume_text:
                return render_template(
                    "index.html",
                    error="Could not extract text from this PDF."
                )

            # analyses skills
            results = analyze_skills(
                resume_text,
                job_description
            )

            # generates AI recommendations
            recommendations = generate_recommendations(
                resume_text,
                job_description,
                results
            )

            # displays results
            return render_template(
                "index.html",
                results=results,
                recommendations=recommendations
            )

        finally:
            # to delete the temporary resume file
            if os.path.exists(file_path):
                os.remove(file_path)

    return render_template("index.html")


@app.errorhandler(413)
def file_too_large(error):
    return render_template(
        "index.html",
        error="File is too large. Maximum allowed size is 10 MB."
    ), 413


if __name__ == "__main__":
    app.run(debug=True)