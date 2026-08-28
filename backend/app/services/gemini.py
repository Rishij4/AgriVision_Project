import os
import json
import base64
import requests

from dotenv import load_dotenv

load_dotenv()


# ============================================================
# GEMINI CONFIGURATION
# ============================================================

MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.6-flash"
)

LANGUAGES = [
    "english",
    "hindi",
    "telugu",
]


# ============================================================
# MAIN PROMPT
# ============================================================

PROMPT = """
Analyze this crop/leaf image as an agricultural AI assistant.

We need the result in THREE languages:
1. English
2. Hindi
3. Telugu

Return ONLY valid JSON.

The JSON must have EXACTLY this structure:

{
  "english": {
    "crop": "string",
    "probable_issue": "string",
    "confidence_percent": number,
    "severity": "Low|Moderate|High|Unknown",
    "symptoms": ["string"],
    "recommendations": ["string"],
    "image_quality": "Good|Acceptable|Poor",
    "notes": "string"
  },

  "hindi": {
    "crop": "string",
    "probable_issue": "string",
    "confidence_percent": number,
    "severity": "Low|Moderate|High|Unknown",
    "symptoms": ["string"],
    "recommendations": ["string"],
    "image_quality": "Good|Acceptable|Poor",
    "notes": "string"
  },

  "telugu": {
    "crop": "string",
    "probable_issue": "string",
    "confidence_percent": number,
    "severity": "Low|Moderate|High|Unknown",
    "symptoms": ["string"],
    "recommendations": ["string"],
    "image_quality": "Good|Acceptable|Poor",
    "notes": "string"
  }
}

IMPORTANT RULES:

1. Analyze the image only once.
2. The three language responses must describe the SAME analysis.
3. Do not change the diagnosis/issue between languages.
4. confidence_percent must be the SAME number in all languages.
5. The information in symptoms must be equivalent in all languages.
6. The information in recommendations must be equivalent in all languages.
7. Translate the text naturally for farmers.
8. Hindi must be written in Hindi.
9. Telugu must be written in Telugu.
10. English must be written in English.
11. Do NOT use English text inside Hindi or Telugu values unless it is a proper scientific/crop name.
12. Use probable / AI-assisted language.
13. Do NOT claim a definitive diagnosis.
14. If the image is unsuitable, clearly explain that in all three languages.
15. Keep recommendations practical and safe for farmers.
16. Return ONLY JSON. No markdown.
"""


# ============================================================
# CLEAN JSON RESPONSE
# ============================================================

def clean_json(text: str) -> str:

    text = text.strip()

    if text.startswith("```json"):
        text = text[7:]

    elif text.startswith("```"):
        text = text[3:]

    if text.endswith("```"):
        text = text[:-3]

    return text.strip()


# ============================================================
# VALIDATE ONE LANGUAGE RESULT
# ============================================================

def validate_language_result(
    result: dict,
    language: str,
) -> dict:

    if not isinstance(result, dict):
        result = {}

    result.setdefault(
        "crop",
        "Unknown"
    )

    result.setdefault(
        "probable_issue",
        "Unable to determine"
    )

    result.setdefault(
        "confidence_percent",
        0
    )

    result.setdefault(
        "severity",
        "Unknown"
    )

    result.setdefault(
        "symptoms",
        []
    )

    result.setdefault(
        "recommendations",
        []
    )

    result.setdefault(
        "image_quality",
        "Poor"
    )

    result.setdefault(
        "notes",
        ""
    )

    # --------------------------------------------------------
    # Make sure arrays are arrays
    # --------------------------------------------------------

    if not isinstance(
        result["symptoms"],
        list
    ):

        result["symptoms"] = [
            str(result["symptoms"])
        ]

    if not isinstance(
        result["recommendations"],
        list
    ):

        result["recommendations"] = [
            str(result["recommendations"])
        ]

    return result


# ============================================================
# ANALYZE IMAGE
# ============================================================

def analyze_image(
    image_bytes: bytes,
    mime_type: str,
    language: str = "english",
):
    """
    Analyze the image ONCE using Gemini.

    Gemini returns English + Hindi + Telugu
    in the same API request.

    The caller can then save all three versions
    directly into MongoDB.

    The 'language' parameter is kept for compatibility
    with the existing analysis.py, but the analysis is
    intentionally generated in all three languages.
    """

    key = os.getenv(
        "GEMINI_API_KEY"
    )

    if not key:

        raise RuntimeError(
            "GEMINI_API_KEY is not configured"
        )

    # --------------------------------------------------------
    # Model
    # --------------------------------------------------------

    model = MODEL

    url = (
        "https://generativelanguage.googleapis.com/"
        f"v1beta/models/{model}:generateContent"
    )

    # --------------------------------------------------------
    # Encode image
    # --------------------------------------------------------

    image_base64 = base64.b64encode(
        image_bytes
    ).decode("utf-8")

    # --------------------------------------------------------
    # Request
    # --------------------------------------------------------

    payload = {
        "contents": [
            {
                "parts": [

                    {
                        "text": PROMPT
                    },

                    {
                        "inline_data": {
                            "mime_type": mime_type,
                            "data": image_base64
                        }
                    }

                ]
            }
        ],

        "generationConfig": {

            "temperature": 0.2,

            "responseMimeType":
                "application/json"
        }
    }

    headers = {
        "Content-Type":
            "application/json"
    }

    # --------------------------------------------------------
    # Send request
    # --------------------------------------------------------

    try:

        response = requests.post(
            url,
            params={
                "key": key
            },
            headers=headers,
            json=payload,
            timeout=90,
        )

    except requests.RequestException as e:

        raise RuntimeError(
            "Gemini connection failed. "
            "Please try again."
        ) from e

    # --------------------------------------------------------
    # Handle errors
    # --------------------------------------------------------

    if response.status_code != 200:

        try:

            error_data = response.json()

            error_message = (
                error_data
                .get("error", {})
                .get(
                    "message",
                    "Gemini request failed"
                )
            )

        except Exception:

            error_message = (
                "Gemini request failed"
            )

        # Don't expose API key or complete URL
        raise RuntimeError(
            f"Gemini API error "
            f"{response.status_code}: "
            f"{error_message}"
        )

    # --------------------------------------------------------
    # Read Gemini response
    # --------------------------------------------------------

    try:

        response_data = response.json()

        candidates = response_data.get(
            "candidates",
            []
        )

        if not candidates:

            raise RuntimeError(
                "Gemini returned no candidates"
            )

        parts = (
            candidates[0]
            .get("content", {})
            .get("parts", [])
        )

        if not parts:

            raise RuntimeError(
                "Gemini returned no content"
            )

        text = parts[0].get(
            "text",
            ""
        ).strip()

        if not text:

            raise RuntimeError(
                "Gemini returned an empty response"
            )

    except RuntimeError:

        raise

    except Exception as e:

        raise RuntimeError(
            f"Invalid Gemini response: {str(e)}"
        )

    # --------------------------------------------------------
    # Parse JSON
    # --------------------------------------------------------

    text = clean_json(text)

    try:

        result = json.loads(
            text
        )

    except json.JSONDecodeError as e:

        raise RuntimeError(
            "Gemini returned invalid JSON: "
            f"{str(e)}"
        )

    # ========================================================
    # VALIDATE THREE LANGUAGES
    # ========================================================

    if not isinstance(
        result,
        dict
    ):

        raise RuntimeError(
            "Gemini returned an invalid result."
        )

    # --------------------------------------------------------
    # English
    # --------------------------------------------------------

    english = validate_language_result(
        result.get(
            "english",
            {}
        ),
        "english"
    )

    # --------------------------------------------------------
    # Hindi
    # --------------------------------------------------------

    hindi = validate_language_result(
        result.get(
            "hindi",
            {}
        ),
        "hindi"
    )

    # --------------------------------------------------------
    # Telugu
    # --------------------------------------------------------

    telugu = validate_language_result(
        result.get(
            "telugu",
            {}
        ),
        "telugu"
    )

    # ========================================================
    # FINAL RESULT
    # ========================================================

    return {
        "english": english,
        "hindi": hindi,
        "telugu": telugu,
    }