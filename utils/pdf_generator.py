from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def create_pdf(best_prompt, results, filename="Prompt_Report.pdf"):

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    story = []

    # Title
    story.append(Paragraph("<b>PromptPilot AI</b>", styles["Title"]))
    story.append(Paragraph("Prompt Evaluation Report", styles["Heading2"]))
    story.append(Paragraph("<br/>", styles["Normal"]))

    # Best Prompt
    story.append(Paragraph(f"<b>Best Prompt:</b> {best_prompt['title']}", styles["Heading2"]))
    story.append(Paragraph(f"<b>Score:</b> {best_prompt['score']}/100", styles["Normal"]))
    story.append(Paragraph("<br/>", styles["Normal"]))

    # All Results
    story.append(Paragraph("<b>Prompt Results</b>", styles["Heading2"]))

    for result in results:
        story.append(
            Paragraph(
                f"<b>{result['title']}</b> - Score: {result['score']}/100",
                styles["Normal"]
            )
        )

    doc.build(story)

    return filename