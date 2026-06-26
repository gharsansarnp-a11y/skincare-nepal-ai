"""
Google Cloud Vision API Integration

Analyzes skin images and detects skin conditions using Google's AI.
This is the core AI engine for the platform.
"""

import json
import os
from dotenv import load_dotenv

try:
    from google.cloud import vision
    from google.oauth2 import service_account
    VISION_AVAILABLE = True
except ImportError:
    print("WARNING: Google Cloud Vision not available - using mock analysis")
    VISION_AVAILABLE = False

load_dotenv()

# Initialize Vision client
def get_vision_client():
    """
    Initialize Google Cloud Vision client using credentials
    """
    if not VISION_AVAILABLE:
        return None

    credentials_path = os.getenv("GOOGLE_CLOUD_CREDENTIALS_PATH", "./credentials/google-cloud-key.json")

    if not os.path.exists(credentials_path):
        print(f"WARNING: Google Cloud credentials not found at {credentials_path}")
        return None

    try:
        credentials = service_account.Credentials.from_service_account_file(credentials_path)
        client = vision.ImageAnnotatorClient(credentials=credentials)
        return client
    except Exception as e:
        print(f"Error initializing Vision client: {e}")
        return None

# Skin condition mappings
SKIN_CONDITIONS_MAP = {
    "acne": {"category": "acne", "severity": "medium"},
    "pimple": {"category": "acne", "severity": "medium"},
    "pores": {"category": "pores", "severity": "low"},
    "wrinkle": {"category": "aging", "severity": "medium"},
    "dark spot": {"category": "pigmentation", "severity": "medium"},
    "melasma": {"category": "pigmentation", "severity": "high"},
    "redness": {"category": "sensitivity", "severity": "medium"},
    "dryness": {"category": "dryness", "severity": "low"},
    "oiliness": {"category": "oiliness", "severity": "low"},
}

def analyze_skin_image(image_path: str) -> dict:
    """
    Analyze a skin photo using Google Cloud Vision API

    Args:
        image_path: Path to the image file

    Returns:
        Dictionary with analysis results:
        {
            "conditions": [
                {"name": "Acne", "confidence": 0.85, "severity": "medium"},
                {"name": "Oily Skin", "confidence": 0.78, "severity": "low"}
            ],
            "skin_health_score": 65,
            "recommendations": [
                {"type": "cleanser", "product_name": "Gentle Face Wash"},
                {"type": "moisturizer", "product_name": "Oil-Control Moisturizer"}
            ],
            "success": True
        }
    """

    try:
        # Get Vision API client
        client = get_vision_client()
        if not client:
            return {
                "success": False,
                "error": "Vision API not initialized. Check credentials.",
                "conditions": [],
                "skin_health_score": 50,
                "recommendations": []
            }

        # Read image file
        if not os.path.exists(image_path):
            return {
                "success": False,
                "error": f"Image file not found: {image_path}",
                "conditions": [],
                "skin_health_score": 50,
                "recommendations": []
            }

        with open(image_path, "rb") as image_file:
            content = image_file.read()

        # Create image object
        image = vision.Image(content=content)

        # Call Vision API
        # We use LABEL_DETECTION to find objects (skin conditions) in the image
        response = client.label_detection(image=image)
        labels = response.label_annotations

        # Parse results
        detected_conditions = []
        for label in labels:
            label_text = label.description.lower()

            # Check if label matches known skin conditions
            for condition, details in SKIN_CONDITIONS_MAP.items():
                if condition in label_text:
                    detected_conditions.append({
                        "name": condition.capitalize(),
                        "confidence": float(label.score),
                        "severity": details["severity"]
                    })

        # Calculate skin health score (0-100)
        # Higher confidence in negative conditions = lower score
        negative_score = sum(
            (1 - cond["confidence"]) * 20
            for cond in detected_conditions
        )
        skin_health_score = max(0, min(100, 100 - negative_score))

        # Generate recommendations based on detected conditions
        recommendations = generate_recommendations(detected_conditions)

        return {
            "success": True,
            "conditions": detected_conditions,
            "skin_health_score": int(skin_health_score),
            "recommendations": recommendations,
            "raw_response": {
                "total_labels": len(labels),
                "top_labels": [
                    {
                        "name": label.description,
                        "confidence": float(label.score)
                    }
                    for label in labels[:5]
                ]
            }
        }

    except Exception as e:
        print(f"Error analyzing image: {e}")
        return {
            "success": False,
            "error": str(e),
            "conditions": [],
            "skin_health_score": 50,
            "recommendations": []
        }

def generate_recommendations(conditions: list) -> list:
    """
    Generate skincare product recommendations based on detected conditions

    Args:
        conditions: List of detected skin conditions

    Returns:
        List of recommended skincare routines
    """

    recommendations = []

    # Check what conditions are present
    has_acne = any(cond["name"].lower() == "acne" for cond in conditions)
    has_oiliness = any(cond["name"].lower() == "oiliness" for cond in conditions)
    has_dryness = any(cond["name"].lower() == "dryness" for cond in conditions)
    has_pigmentation = any(
        cond["name"].lower() in ["dark spot", "melasma", "pigmentation"]
        for cond in conditions
    )
    has_wrinkles = any(
        cond["name"].lower() in ["wrinkle", "fine line"]
        for cond in conditions
    )

    # Morning routine recommendations
    morning_routine = []

    if has_acne or has_oiliness:
        morning_routine.append({
            "type": "cleanser",
            "time": "morning",
            "recommendation": "Salicylic acid face wash (BHA)",
            "product_type": "cleanser",
            "priority": "high"
        })
    else:
        morning_routine.append({
            "type": "cleanser",
            "time": "morning",
            "recommendation": "Gentle cream cleanser",
            "product_type": "cleanser",
            "priority": "medium"
        })

    morning_routine.append({
        "type": "vitamin_c",
        "time": "morning",
        "recommendation": "Vitamin C serum (antioxidant protection)",
        "product_type": "serum",
        "priority": "high"
    })

    if has_dryness:
        morning_routine.append({
            "type": "moisturizer",
            "time": "morning",
            "recommendation": "Rich hydrating moisturizer with hyaluronic acid",
            "product_type": "moisturizer",
            "priority": "high"
        })
    elif has_oiliness:
        morning_routine.append({
            "type": "moisturizer",
            "time": "morning",
            "recommendation": "Oil-control lightweight moisturizer",
            "product_type": "moisturizer",
            "priority": "medium"
        })
    else:
        morning_routine.append({
            "type": "moisturizer",
            "time": "morning",
            "recommendation": "Balanced gel moisturizer",
            "product_type": "moisturizer",
            "priority": "medium"
        })

    morning_routine.append({
        "type": "sunscreen",
        "time": "morning",
        "recommendation": "SPF 50+ broad-spectrum sunscreen",
        "product_type": "sunscreen",
        "priority": "critical"
    })

    # Night routine recommendations
    night_routine = []

    if has_acne or has_oiliness:
        night_routine.append({
            "type": "cleanser",
            "time": "night",
            "recommendation": "Oil-control face wash",
            "product_type": "cleanser",
            "priority": "high"
        })
    else:
        night_routine.append({
            "type": "cleanser",
            "time": "night",
            "recommendation": "Gentle milky cleanser",
            "product_type": "cleanser",
            "priority": "medium"
        })

    if has_wrinkles or has_pigmentation:
        night_routine.append({
            "type": "retinol",
            "time": "night",
            "recommendation": "Retinol serum (cell turnover & anti-aging)",
            "product_type": "serum",
            "priority": "high"
        })
    elif has_acne:
        night_routine.append({
            "type": "niacinamide",
            "time": "night",
            "recommendation": "Niacinamide serum (pore minimizer)",
            "product_type": "serum",
            "priority": "high"
        })

    night_routine.append({
        "type": "moisturizer",
        "time": "night",
        "recommendation": "Intensive night moisturizer or sleeping mask",
        "product_type": "moisturizer",
        "priority": "high"
    })

    # Weekly treatments
    weekly_routine = []

    if has_acne:
        weekly_routine.append({
            "type": "mask",
            "frequency": "2x/week",
            "recommendation": "Clay mask (detoxifying)",
            "product_type": "mask",
            "priority": "medium"
        })

    if has_pigmentation:
        weekly_routine.append({
            "type": "treatment",
            "frequency": "1-2x/week",
            "recommendation": "Vitamin C mask or brightening sheet mask",
            "product_type": "mask",
            "priority": "high"
        })

    if has_dryness or has_wrinkles:
        weekly_routine.append({
            "type": "mask",
            "frequency": "1-2x/week",
            "recommendation": "Hydrating or collagen sheet mask",
            "product_type": "mask",
            "priority": "medium"
        })

    # Compile all recommendations
    recommendations = morning_routine + night_routine + weekly_routine

    return recommendations

# For testing without Google Cloud credentials
def analyze_skin_image_mock(image_path: str) -> dict:
    """
    Mock analysis function for testing (when Google Cloud not available)
    Returns fake data for development purposes
    """
    return {
        "success": True,
        "conditions": [
            {"name": "Acne", "confidence": 0.75, "severity": "medium"},
            {"name": "Oily Skin", "confidence": 0.82, "severity": "medium"},
        ],
        "skin_health_score": 62,
        "recommendations": [
            {
                "type": "cleanser",
                "time": "morning",
                "recommendation": "Salicylic acid face wash (BHA)",
                "product_type": "cleanser",
                "priority": "high"
            }
        ],
        "raw_response": {
            "total_labels": 5,
            "top_labels": [
                {"name": "face", "confidence": 0.98},
                {"name": "skin", "confidence": 0.95}
            ]
        }
    }
