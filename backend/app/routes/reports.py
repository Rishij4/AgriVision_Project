from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from bson import ObjectId

from app.db.mongo import analyses, fs
from app.utils.security import decode_token
from app.services.pdf_report import build_report


router = APIRouter()

security = HTTPBearer()


def get_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:

    token = credentials.credentials

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Missing authorization token"
        )

    return decode_token(token)


# ============================================================
# GET ANALYSIS IN SELECTED LANGUAGE
# ============================================================

def get_language_analysis(document, language):

    language = (language or "english").lower().strip()

    # Supported languages
    if language not in ["english", "hindi", "telugu"]:
        language = "english"

    analysis = document.get("analysis")

    if not analysis:
        raise HTTPException(
            status_code=500,
            detail="Analysis data not found"
        )

    print("PDF language:", language)
    print("Analysis type:", type(analysis))

    # --------------------------------------------------------
    # CASE 1:
    # analysis contains:
    #
    # {
    #   "english": {...},
    #   "hindi": {...},
    #   "telugu": {...}
    # }
    # --------------------------------------------------------

    if isinstance(analysis, dict):

        if language in analysis:

            selected = analysis[language]

            if isinstance(selected, dict):
                return selected

        # ----------------------------------------------------
        # CASE 2:
        # Some backends may store the languages under
        # translations
        # ----------------------------------------------------

        translations = analysis.get("translations")

        if isinstance(translations, dict):

            if language in translations:

                selected = translations[language]

                if isinstance(selected, dict):
                    return selected

        # ----------------------------------------------------
        # CASE 3:
        # Already a normal analysis object.
        #
        # This allows old records to continue working.
        # ----------------------------------------------------

        if (
            "crop" in analysis
            or "probable_issue" in analysis
            or "confidence_percent" in analysis
        ):
            return analysis

    raise HTTPException(
        status_code=404,
        detail=f"No {language} analysis found for this report"
    )


# ============================================================
# GET IMAGE
# ============================================================

def get_image_data(document):

    image_data = None

    try:

        if document.get("image_file_id"):

            image_data = fs.get(
                document["image_file_id"]
            ).read()

    except Exception as e:

        print(
            "Could not load image from GridFS:",
            e
        )

        image_data = None

    return image_data


# ============================================================
# LATEST PDF
# ============================================================

@router.get("/latest/pdf")
def latest_pdf(
    language: str = "english",
    user_id: str = Depends(get_user_id),
):

    document = analyses.find_one(
        {"user_id": user_id},
        sort=[("created_at", -1)]
    )

    if not document:

        raise HTTPException(
            status_code=404,
            detail="No analysis found"
        )

    selected_analysis = get_language_analysis(
        document,
        language
    )

    image_data = get_image_data(
        document
    )

    try:

        pdf_data = build_report(
    selected_analysis,
    image_data=image_data,
    language=language
)

    except Exception as e:

        print(
            "PDF generation error:",
            e
        )

        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate PDF: {str(e)}"
        )

    analysis_id = str(
        document["_id"]
    )

    safe_language = (
        language.lower()
        if language in [
            "english",
            "hindi",
            "telugu"
        ]
        else "english"
    )

    return Response(
        content=pdf_data,
        media_type="application/pdf",
        headers={
            "Content-Disposition":
                f'attachment; filename="agrivision-{analysis_id}-{safe_language}.pdf"'
        },
    )


# ============================================================
# PDF BY ANALYSIS ID
# ============================================================

@router.get("/{analysis_id}/pdf")
def pdf(
    analysis_id: str,
    language: str = "english",
    user_id: str = Depends(get_user_id),
):

    # --------------------------------------------------------
    # Validate ObjectId
    # --------------------------------------------------------

    if not ObjectId.is_valid(
        analysis_id
    ):

        raise HTTPException(
            status_code=400,
            detail=f"Invalid analysis ID: {analysis_id}"
        )

    oid = ObjectId(
        analysis_id
    )

    # --------------------------------------------------------
    # Find analysis belonging to user
    # --------------------------------------------------------

    document = analyses.find_one(
        {
            "_id": oid,
            "user_id": user_id,
        }
    )

    if not document:

        raise HTTPException(
            status_code=404,
            detail="Analysis not found"
        )

    # --------------------------------------------------------
    # Get selected language
    # --------------------------------------------------------

    selected_analysis = get_language_analysis(
        document,
        language
    )

    # --------------------------------------------------------
    # Get image
    # --------------------------------------------------------

    image_data = get_image_data(
        document
    )

    # --------------------------------------------------------
    # Generate PDF
    # --------------------------------------------------------

    try:

        pdf_data = build_report(
    selected_analysis,
    image_data=image_data,
    language=language
)

    except Exception as e:

        print(
            "PDF generation error:",
            e
        )

        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate PDF: {str(e)}"
        )

    safe_language = (
        language.lower()
        if language in [
            "english",
            "hindi",
            "telugu"
        ]
        else "english"
    )

    return Response(
        content=pdf_data,
        media_type="application/pdf",
        headers={
            "Content-Disposition":
                f'attachment; filename="agrivision-{analysis_id}-{safe_language}.pdf"'
        },
    )
