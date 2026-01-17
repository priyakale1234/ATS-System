from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(data, path):
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(path)
    content = [Paragraph("ATS Report", styles["Title"])]

    for k, v in data.items():
        content.append(Paragraph(f"{k}: {v}", styles["Normal"]))

    doc.build(content)
