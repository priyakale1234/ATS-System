import PyPDF2

def parse_resume(pdf):
    reader = PyPDF2.PdfReader(pdf)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text
