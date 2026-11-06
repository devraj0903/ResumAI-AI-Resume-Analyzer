import pymupdf

# to extract resume text
def extract_resume_text(pdf_path):
    text = ""

    try:
        doc = pymupdf.open(pdf_path)

        for page in doc:
            text += page.get_text() + "\n"

        doc.close()

        if not text.strip():
            return None

        return text.strip()

    except Exception as e:
        print("Error reading PDF:", e)
        return None