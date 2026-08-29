from io import BytesIO
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


# ============================================================
# FONT SETUP
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
FONT_DIR = BASE_DIR / "fonts"


def setup_fonts(language):

    language = (
        language or "english"
    ).lower().strip()

    # --------------------------------------------------------
    # ENGLISH
    # --------------------------------------------------------

    if language == "english":

        return {
            "regular": "Helvetica",
            "bold": "Helvetica-Bold",
            "italic": "Helvetica-Oblique",
        }

    # --------------------------------------------------------
    # HINDI
    # --------------------------------------------------------

    if language == "hindi":

        regular_path = (
            FONT_DIR /
            "NotoSansDevanagari-Regular.ttf"
        )

        bold_path = (
            FONT_DIR /
            "NotoSansDevanagari-Bold.ttf"
        )

        if not regular_path.exists():

            raise RuntimeError(
                "Hindi font missing: "
                f"{regular_path}"
            )

        pdfmetrics.registerFont(
            TTFont(
                "NotoHindi",
                str(regular_path)
            )
        )

        if bold_path.exists():

            pdfmetrics.registerFont(
                TTFont(
                    "NotoHindiBold",
                    str(bold_path)
                )
            )

            return {
                "regular": "NotoHindi",
                "bold": "NotoHindiBold",
                "italic": "NotoHindi",
            }

        return {
            "regular": "NotoHindi",
            "bold": "NotoHindi",
            "italic": "NotoHindi",
        }

    # --------------------------------------------------------
    # TELUGU
    # --------------------------------------------------------

    if language == "telugu":

        regular_path = (
            FONT_DIR /
            "NotoSansTelugu-Regular.ttf"
        )

        bold_path = (
            FONT_DIR /
            "NotoSansTelugu-Bold.ttf"
        )

        if not regular_path.exists():

            raise RuntimeError(
                "Telugu font missing: "
                f"{regular_path}"
            )

        pdfmetrics.registerFont(
            TTFont(
                "NotoTelugu",
                str(regular_path)
            )
        )

        if bold_path.exists():

            pdfmetrics.registerFont(
                TTFont(
                    "NotoTeluguBold",
                    str(bold_path)
                )
            )

            return {
                "regular": "NotoTelugu",
                "bold": "NotoTeluguBold",
                "italic": "NotoTelugu",
            }

        return {
            "regular": "NotoTelugu",
            "bold": "NotoTelugu",
            "italic": "NotoTelugu",
        }

    # --------------------------------------------------------
    # FALLBACK
    # --------------------------------------------------------

    return {
        "regular": "Helvetica",
        "bold": "Helvetica-Bold",
        "italic": "Helvetica-Oblique",
    }


# ============================================================
# TRANSLATED PDF LABELS
# ============================================================

PDF_TEXT = {

    "english": {

        "title":
            "AgriVision - Crop Health Analysis Report",

        "crop":
            "Crop",

        "issue":
            "Probable Issue",

        "confidence":
            "Confidence",

        "severity":
            "Severity",

        "quality":
            "Image Quality",

        "symptoms":
            "Symptoms",

        "recommendations":
            "Recommended Actions",

        "notes":
            "Notes",

        "no_symptoms":
            "No symptoms provided.",

        "no_recommendations":
            "No recommendations provided.",

        "disclaimer":
            "AI-assisted screening only. "
            "Seek professional agricultural advice "
            "for confirmation.",
    },


    "hindi": {

        "title":
            "AgriVision - फसल स्वास्थ्य विश्लेषण रिपोर्ट",

        "crop":
            "फसल",

        "issue":
            "संभावित समस्या",

        "confidence":
            "विश्वसनीयता",

        "severity":
            "गंभीरता",

        "quality":
            "तस्वीर की गुणवत्ता",

        "symptoms":
            "लक्षण",

        "recommendations":
            "सुझाए गए उपाय",

        "notes":
            "टिप्पणियां",

        "no_symptoms":
            "कोई लक्षण उपलब्ध नहीं है।",

        "no_recommendations":
            "कोई सुझाव उपलब्ध नहीं है।",

        "disclaimer":
            "यह केवल AI आधारित प्रारंभिक जांच है। "
            "पुष्टि के लिए कृषि विशेषज्ञ से सलाह लें।",
    },


    "telugu": {

        "title":
            "AgriVision - పంట ఆరోగ్య విశ్లేషణ నివేదిక",

        "crop":
            "పంట",

        "issue":
            "సంభావ్య సమస్య",

        "confidence":
            "నమ్మక స్థాయి",

        "severity":
            "తీవ్రత",

        "quality":
            "చిత్ర నాణ్యత",

        "symptoms":
            "లక్షణాలు",

        "recommendations":
            "సిఫార్సు చేసిన చర్యలు",

        "notes":
            "గమనికలు",

        "no_symptoms":
            "లక్షణాలు అందుబాటులో లేవు.",

        "no_recommendations":
            "సిఫార్సులు అందుబాటులో లేవు.",

        "disclaimer":
            "ఇది AI ఆధారిత ప్రాథమిక పరీక్ష మాత్రమే. "
            "నిర్ధారణ కోసం వ్యవసాయ నిపుణుల సలహా తీసుకోండి.",
    },
}


# ============================================================
# SAFE TEXT
# ============================================================

def safe_text(value):

    if value is None:
        return ""

    return escape(
        str(value)
    )


# ============================================================
# BUILD PDF
# ============================================================

def build_report(
    a,
    image_data=None,
    language="english"
):

    language = (
        language or "english"
    ).lower().strip()

    if language not in PDF_TEXT:

        language = "english"

    # --------------------------------------------------------
    # FONT
    # --------------------------------------------------------

    fonts = setup_fonts(
        language
    )

    labels = PDF_TEXT[
        language
    ]

    # --------------------------------------------------------
    # PDF DOCUMENT
    # --------------------------------------------------------

    b = BytesIO()

    doc = SimpleDocTemplate(
        b,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    # --------------------------------------------------------
    # STYLES
    # --------------------------------------------------------

    title_style = ParagraphStyle(
        "PDFTitle",
        fontName=fonts["bold"],
        fontSize=18,
        leading=24,
        spaceAfter=10,
    )

    heading_style = ParagraphStyle(
        "PDFHeading",
        fontName=fonts["bold"],
        fontSize=13,
        leading=18,
        spaceBefore=8,
        spaceAfter=8,
    )

    body_style = ParagraphStyle(
        "PDFBody",
        fontName=fonts["regular"],
        fontSize=10,
        leading=15,
    )

    italic_style = ParagraphStyle(
        "PDFItalic",
        fontName=fonts["italic"],
        fontSize=8,
        leading=12,
    )

    story = []

    # ========================================================
    # TITLE
    # ========================================================

    story.append(
        Paragraph(
            safe_text(
                labels["title"]
            ),
            title_style
        )
    )

    story.append(
        Spacer(1, 15)
    )

    # ========================================================
    # IMAGE
    # ========================================================

    if image_data:

        try:

            image = Image(
                BytesIO(image_data)
            )

            image.drawWidth = 350
            image.drawHeight = 250

            story.append(
                image
            )

            story.append(
                Spacer(1, 15)
            )

        except Exception as e:

            print(
                "Could not add image to PDF:",
                e
            )

    # ========================================================
    # ANALYSIS INFORMATION
    # ========================================================

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

        (
            labels["crop"],
            crop
        ),

        (
            labels["issue"],
            probable_issue
        ),

        (
            labels["confidence"],
            f"{confidence}%"
        ),

        (
            labels["severity"],
            severity
        ),

        (
            labels["quality"],
            image_quality
        ),
    ]

    for key, value in information:

        story.append(
            Paragraph(
                f"<b>{safe_text(key)}:</b> "
                f"{safe_text(value)}",
                body_style
            )
        )

        story.append(
            Spacer(1, 5)
        )

    # ========================================================
    # SYMPTOMS
    # ========================================================

    story.append(
        Spacer(1, 10)
    )

    story.append(
        Paragraph(
            safe_text(
                labels["symptoms"]
            ),
            heading_style
        )
    )

    symptoms = a.get(
        "symptoms",
        []
    )

    if isinstance(
        symptoms,
        list
    ) and symptoms:

        for symptom in symptoms:

            story.append(
                Paragraph(
                    f"• {safe_text(symptom)}",
                    body_style
                )
            )

            story.append(
                Spacer(1, 4)
            )

    else:

        story.append(
            Paragraph(
                safe_text(
                    labels["no_symptoms"]
                ),
                body_style
            )
        )

    # ========================================================
    # RECOMMENDATIONS
    # ========================================================

    story.append(
        Spacer(1, 10)
    )

    story.append(
        Paragraph(
            safe_text(
                labels["recommendations"]
            ),
            heading_style
        )
    )

    recommendations = a.get(
        "recommendations",
        []
    )

    if (
        isinstance(
            recommendations,
            list
        )
        and recommendations
    ):

        for recommendation in recommendations:

            story.append(
                Paragraph(
                    f"• {safe_text(recommendation)}",
                    body_style
                )
            )

            story.append(
                Spacer(1, 4)
            )

    else:

        story.append(
            Paragraph(
                safe_text(
                    labels["no_recommendations"]
                ),
                body_style
            )
        )

    # ========================================================
    # NOTES
    # ========================================================

    story.append(
        Spacer(1, 10)
    )

    story.append(
        Paragraph(
            safe_text(
                labels["notes"]
            ),
            heading_style
        )
    )

    notes = a.get(
        "notes",
        ""
    )

    story.append(
        Paragraph(
            safe_text(notes),
            body_style
        )
    )

    # ========================================================
    # DISCLAIMER
    # ========================================================

    story.append(
        Spacer(1, 15)
    )

    story.append(
        Paragraph(
            safe_text(
                labels["disclaimer"]
            ),
            italic_style
        )
    )

    # ========================================================
    # BUILD
    # ========================================================

    doc.build(
        story
    )

    return b.getvalue()
