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
    """
    Extract and validate JWT token.
    """

    token = credentials.credentials

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Missing authorization token"
        )

    return decode_token(token)


# ============================================================
# LATEST PDF
# IMPORTANT: This MUST come BEFORE /{analysis_id}/pdf
# ============================================================

@router.get("/latest/pdf")
def latest_pdf(
    user_id: str = Depends(get_user_id),
):
    """
    Generate PDF for the user's latest analysis.
    """

    document = analyses.find_one(
        {"user_id": user_id},
        sort=[("created_at", -1)]
    )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="No analysis found"
        )

    # Get image from GridFS
    image_data = None

    try:
        if document.get("image_file_id"):
            image_data = fs.get(
                document["image_file_id"]
            ).read()
    except Exception as e:
        print("Could not load image from GridFS:", e)
        image_data = None

    # Build PDF
    try:
        pdf_data = build_report(
            document["analysis"],
            image_data=image_data
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate PDF: {str(e)}"
        )

    analysis_id = str(document["_id"])

    return Response(
        content=pdf_data,
        media_type="application/pdf",
        headers={
            "Content-Disposition":
                f'attachment; filename="agrivision-{analysis_id}.pdf"'
        },
    )


# ============================================================
# PDF BY ANALYSIS ID
# ============================================================

@router.get("/{analysis_id}/pdf")
def pdf(
    analysis_id: str,
    user_id: str = Depends(get_user_id),
):
    """
    Generate PDF for a specific analysis.
    """

    # Validate MongoDB ObjectId
    if not ObjectId.is_valid(analysis_id):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid analysis ID: {analysis_id}"
        )

    oid = ObjectId(analysis_id)

    # Find analysis belonging to logged-in user
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

    # Get image from GridFS
    image_data = None

    try:
        if document.get("image_file_id"):
            image_data = fs.get(
                document["image_file_id"]
            ).read()
    except Exception as e:
        print("Could not load image from GridFS:", e)
        image_data = None

    # Build PDF
    try:
        pdf_data = build_report(
            document["analysis"],
            image_data=image_data
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate PDF: {str(e)}"
        )

    return Response(
        content=pdf_data,
        media_type="application/pdf",
        headers={
            "Content-Disposition":
                f'attachment; filename="agrivision-{analysis_id}.pdf"'
        },
    )