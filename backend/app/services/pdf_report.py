from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
)
from reportlab.lib.styles import getSampleStyleSheet


def build_report(a, image_data=None):

    # ---------------------------------------------------------
    # PDF DOCUMENT
    # ---------------------------------------------------------

    b = BytesIO()

    doc = SimpleDocTemplate(
        b,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()

    story = []

    # ---------------------------------------------------------
    # TITLE
    # ---------------------------------------------------------

    story.append(
        Paragraph(
            "AgriVision - Crop Health Analysis Report",
            styles["Title"]
        )
    )

    story.append(Spacer(1, 15))

    # ---------------------------------------------------------
    # CROP IMAGE
    # ---------------------------------------------------------

    if image_data:

        try:
            image = Image(
                BytesIO(image_data)
            )

            # Keep image inside A4 page
            image.drawWidth = 350
            image.drawHeight = 250

            story.append(image)

            story.append(
                Spacer(1, 15)
            )

        except Exception as e:
            print(
                "Could not add image to PDF:",
                e
            )

    # ---------------------------------------------------------
    # BASIC ANALYSIS INFORMATION
    # ---------------------------------------------------------

    crop = a.get(
        "crop",
        "Unknown"
    )

    probable_issue = a.get(
        "probable_issue",
        "Unknown"
    )

    confidence = a.get(
        "confidence_percent",
        "N/A"
    )

    severity = a.get(
        "severity",
        "Unknown"
    )

    image_quality = a.get(
        "image_quality",
        "Unknown"
    )

    information = [
        ("Crop", crop),
        ("Probable Issue", probable_issue),
        ("Confidence", f"{confidence}%"),
        ("Severity", severity),
        ("Image Quality", image_quality),
    ]

    for key, value in information:

        story.append(
            Paragraph(
                f"<b>{key}:</b> {value}",
                styles["BodyText"]
            )
        )

        story.append(
            Spacer(1, 5)
        )

    # ---------------------------------------------------------
    # SYMPTOMS
    # ---------------------------------------------------------

    story.append(
        Spacer(1, 10)
    )

    story.append(
        Paragraph(
            "Symptoms",
            styles["Heading2"]
        )
    )

    symptoms = a.get(
        "symptoms",
        []
    )

    if symptoms:

        for symptom in symptoms:

            story.append(
                Paragraph(
                    f"• {symptom}",
                    styles["BodyText"]
                )
            )

            story.append(
                Spacer(1, 4)
            )

    else:

        story.append(
            Paragraph(
                "No symptoms provided.",
                styles["BodyText"]
            )
        )

    # ---------------------------------------------------------
    # RECOMMENDED ACTIONS
    # ---------------------------------------------------------

    story.append(
        Spacer(1, 10)
    )

    story.append(
        Paragraph(
            "Recommended Actions",
            styles["Heading2"]
        )
    )

    recommendations = a.get(
        "recommendations",
        []
    )

    if recommendations:

        for recommendation in recommendations:

            story.append(
                Paragraph(
                    f"• {recommendation}",
                    styles["BodyText"]
                )
            )

            story.append(
                Spacer(1, 4)
            )

    else:

        story.append(
            Paragraph(
                "No recommendations provided.",
                styles["BodyText"]
            )
        )

    # ---------------------------------------------------------
    # NOTES
    # ---------------------------------------------------------

    story.append(
        Spacer(1, 10)
    )

    story.append(
        Paragraph(
            "Notes",
            styles["Heading2"]
        )
    )

    notes = a.get(
        "notes",
        ""
    )

    story.append(
        Paragraph(
            str(notes),
            styles["BodyText"]
        )
    )

    # ---------------------------------------------------------
    # DISCLAIMER
    # ---------------------------------------------------------

    story.append(
        Spacer(1, 15)
    )

    story.append(
        Paragraph(
            "AI-assisted screening only. "
            "Seek professional agricultural advice "
            "for confirmation.",
            styles["Italic"]
        )
    )

    # ---------------------------------------------------------
    # BUILD PDF
    # ---------------------------------------------------------

    doc.build(story)

    return b.getvalue()