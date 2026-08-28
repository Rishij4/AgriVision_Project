from datetime import datetime, timezone

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends,
    HTTPException,
    Query,
)

from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
)

from bson import ObjectId

from app.db.mongo import fs, analyses
from app.utils.security import decode_token

from app.services.gemini import analyze_image


router = APIRouter()

security = HTTPBearer()


# ============================================================
# SUPPORTED LANGUAGES
# ============================================================

ALLOWED_LANGUAGES = {
    "english",
    "hindi",
    "telugu",
}


# ============================================================
# GET USER ID FROM JWT
# ============================================================

def get_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(
        security
    ),
) -> str:

    token = credentials.credentials

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Missing authorization token",
        )

    return decode_token(token)


# ============================================================
# VALIDATE LANGUAGE
# ============================================================

def validate_language(
    language: str
) -> str:

    language = (
        language
        or "english"
    ).lower().strip()

    if language not in ALLOWED_LANGUAGES:

        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported language. "
                "Use english, hindi or telugu."
            ),
        )

    return language


# ============================================================
# GET LANGUAGE RESULT FROM STORED DATA
# ============================================================

def get_language_result(
    document: dict,
    language: str,
) -> dict:
    """
    Get the requested language directly from MongoDB.

    IMPORTANT:
    There is NO Gemini call here.
    """

    language = validate_language(
        language
    )

    analysis = document.get(
        "analysis",
        {}
    )

    # ========================================================
    # NEW FORMAT
    #
    # analysis:
    # {
    #     "english": {...},
    #     "hindi": {...},
    #     "telugu": {...}
    # }
    # ========================================================

    if (
        isinstance(analysis, dict)
        and language in analysis
        and isinstance(
            analysis[language],
            dict
        )
    ):

        return analysis[language]


    # ========================================================
    # OLD FORMAT SUPPORT
    #
    # This allows old analyses created before
    # the 3-language system to continue working.
    # ========================================================

    if (
        isinstance(analysis, dict)
        and "crop" in analysis
    ):

        return analysis


    # ========================================================
    # NO RESULT
    # ========================================================

    return {
        "crop": "Unknown",
        "probable_issue": "No analysis available",
        "confidence_percent": 0,
        "severity": "Unknown",
        "symptoms": [],
        "recommendations": [],
        "image_quality": "Poor",
        "notes": "",
    }


# ============================================================
# ANALYZE IMAGE
# ============================================================

@router.post("/analyze")
async def analyze(
    file: UploadFile = File(...),

    language: str = Query(
        "english",
        description=(
            "Selected language: "
            "english, hindi or telugu"
        ),
    ),

    user_id: str = Depends(
        get_user_id
    ),
):
    """
    Analyze a crop/leaf image.

    Gemini is called ONLY ONCE.

    Gemini returns:
        English
        Hindi
        Telugu

    All three are stored in MongoDB.
    """

    language = validate_language(
        language
    )


    # ========================================================
    # VALIDATE FILE
    # ========================================================

    allowed_types = {
        "image/jpeg",
        "image/png",
        "image/webp",
    }

    if file.content_type not in allowed_types:

        raise HTTPException(
            status_code=400,
            detail=(
                "Upload JPG, PNG or WEBP image"
            ),
        )


    # ========================================================
    # READ IMAGE
    # ========================================================

    data = await file.read()

    if not data:

        raise HTTPException(
            status_code=400,
            detail="Uploaded image is empty",
        )


    # ========================================================
    # MAXIMUM 10 MB
    # ========================================================

    max_size = 10 * 1024 * 1024

    if len(data) > max_size:

        raise HTTPException(
            status_code=400,
            detail=(
                "Image must be under 10 MB"
            ),
        )


    # ========================================================
    # SAVE IMAGE TO GRIDFS
    # ========================================================

    try:

        file_id = fs.put(
            data,

            filename=(
                file.filename
                or "uploaded_image"
            ),

            content_type=file.content_type,

            user_id=user_id,
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=(
                "Failed to store image: "
                f"{str(e)}"
            ),
        )


    # ========================================================
    # GEMINI ANALYSIS
    # ========================================================

    try:

        # IMPORTANT:
        #
        # This makes ONE Gemini request.
        #
        # The returned object contains:
        #
        # {
        #     "english": {...},
        #     "hindi": {...},
        #     "telugu": {...}
        # }

        result = analyze_image(
            data,
            file.content_type,
            language,
        )

    except Exception as e:

        # Delete image if Gemini fails

        try:
            fs.delete(
                file_id
            )
        except Exception:
            pass

        raise HTTPException(
            status_code=502,
            detail=(
                "AI analysis failed: "
                f"{str(e)}"
            ),
        )


    # ========================================================
    # VERIFY THREE LANGUAGES
    # ========================================================

    if not isinstance(
        result,
        dict
    ):

        try:
            fs.delete(
                file_id
            )
        except Exception:
            pass

        raise HTTPException(
            status_code=502,
            detail=(
                "AI returned an invalid "
                "analysis format."
            ),
        )


    for required_language in (
        "english",
        "hindi",
        "telugu",
    ):

        if (
            required_language
            not in result
        ):

            try:
                fs.delete(
                    file_id
                )
            except Exception:
                pass

            raise HTTPException(
                status_code=502,
                detail=(
                    "AI response is missing "
                    f"{required_language} translation."
                ),
            )


    # ========================================================
    # SAVE COMPLETE ANALYSIS
    # ========================================================

    document = {

        "user_id":
            user_id,

        "image_file_id":
            file_id,

        "filename":
            file.filename
            or "uploaded_image",

        "content_type":
            file.content_type,

        # Language selected when uploaded
        "language":
            language,

        # ====================================================
        # ALL THREE LANGUAGE RESULTS
        # ====================================================

        "analysis": {

            "english":
                result["english"],

            "hindi":
                result["hindi"],

            "telugu":
                result["telugu"],
        },

        "created_at":
            datetime.now(
                timezone.utc
            ),
    }


    # ========================================================
    # SAVE TO MONGODB
    # ========================================================

    try:

        inserted = analyses.insert_one(
            document
        )

    except Exception as e:

        try:
            fs.delete(
                file_id
            )
        except Exception:
            pass

        raise HTTPException(
            status_code=500,
            detail=(
                "Failed to save analysis: "
                f"{str(e)}"
            ),
        )


    # ========================================================
    # RETURN ONLY SELECTED LANGUAGE
    # ========================================================

    selected_result = result[
        language
    ]


    return {

        "id":
            str(
                inserted.inserted_id
            ),

        "image_file_id":
            str(
                file_id
            ),

        "language":
            language,

        **selected_result,
    }


# ============================================================
# ANALYSIS HISTORY
# ============================================================

@router.get("/history")
def history(
    user_id: str = Depends(
        get_user_id
    ),

    language: str = Query(
        "english",
        description=(
            "History language: "
            "english, hindi or telugu"
        ),
    ),
):
    """
    Return analysis history in the selected language.

    IMPORTANT:

    This endpoint ONLY reads MongoDB.

    Gemini is NOT called.
    """

    language = validate_language(
        language
    )


    # ========================================================
    # FIND USER DOCUMENTS
    # ========================================================

    documents = (
        analyses
        .find(
            {
                "user_id":
                    user_id
            }
        )
        .sort(
            "created_at",
            -1
        )
    )


    results = []


    # ========================================================
    # BUILD HISTORY
    # ========================================================

    for document in documents:

        analysis = get_language_result(
            document,
            language,
        )


        results.append({

            "id":
                str(
                    document["_id"]
                ),

            "filename":
                document.get(
                    "filename"
                ),

            "image_file_id": (

                str(
                    document[
                        "image_file_id"
                    ]
                )

                if document.get(
                    "image_file_id"
                )

                else None
            ),

            "language":
                language,

            "original_language":
                document.get(
                    "language",
                    "english",
                ),

            "created_at":
                document.get(
                    "created_at"
                ),

            **analysis,
        })


    return results


# ============================================================
# GET ONE ANALYSIS
# ============================================================

@router.get("/{analysis_id}")
def get_analysis(
    analysis_id: str,

    language: str = Query(
        "english",
        description=(
            "Language: "
            "english, hindi or telugu"
        ),
    ),

    user_id: str = Depends(
        get_user_id
    ),
):
    """
    Get one existing analysis
    in the selected language.

    IMPORTANT:

    This ONLY reads MongoDB.

    Gemini is NEVER called here.
    """

    language = validate_language(
        language
    )


    # ========================================================
    # VALIDATE OBJECT ID
    # ========================================================

    if not ObjectId.is_valid(
        analysis_id
    ):

        raise HTTPException(
            status_code=400,
            detail="Invalid analysis ID",
        )


    # ========================================================
    # FIND DOCUMENT
    # ========================================================

    document = analyses.find_one(
        {
            "_id":
                ObjectId(
                    analysis_id
                ),

            "user_id":
                user_id,
        }
    )


    if not document:

        raise HTTPException(
            status_code=404,
            detail="Analysis not found",
        )


    # ========================================================
    # GET REQUESTED LANGUAGE
    # ========================================================

    analysis = get_language_result(
        document,
        language,
    )


    # ========================================================
    # RETURN RESULT
    # ========================================================

    return {

        "id":
            str(
                document["_id"]
            ),

        "image_file_id": (

            str(
                document[
                    "image_file_id"
                ]
            )

            if document.get(
                "image_file_id"
            )

            else None
        ),

        "filename":
            document.get(
                "filename"
            ),

        "language":
            language,

        "original_language":
            document.get(
                "language",
                "english",
            ),

        "created_at":
            document.get(
                "created_at"
            ),

        **analysis,
    }