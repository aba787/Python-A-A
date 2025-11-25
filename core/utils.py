
import re
from datetime import datetime

def detect_language(text: str) -> str:
    """Detect if text is Arabic or English"""
    # لو النص فيه حروف عربية → عربي
    for ch in text:
        if '\u0600' <= ch <= '\u06FF':
            return "ar"
    return "en"

def wants_english(text: str) -> bool:
    """Check if user explicitly requested English"""
    text_lower = text.lower()
    english_indicators = [
        "in english", "english please", "respond in english",
        "بالانجليزي", "باللغة الانجليزية", "اجب بالانجليزي"
    ]
    return any(indicator in text_lower for indicator in english_indicators)

def wants_arabic(text: str) -> bool:
    """Check if user explicitly requested Arabic"""
    text_lower = text.lower()
    arabic_indicators = [
        "in arabic", "arabic please", "respond in arabic",
        "بالعربي", "باللغة العربية", "اجب بالعربي"
    ]
    return any(indicator in text_lower for indicator in arabic_indicators)

def get_current_time() -> str:
    """Get current time in readable format"""
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

def is_medical_query(text: str) -> bool:
    """Check if query is medical-related"""
    medical_keywords = [
        # العربية
        "دواء", "علاج", "باراسيتامول", "إيبوبروفين", "صداع", "حمى", "سعال",
        "مرض", "عرض", "أعراض", "مستشفى", "طبيب", "صيدلية", "حبوب", "كبسولة",
        "عدوى", "التهاب", "ألم", "وجع", "مضاد حيوي", "مسكن", "خافض حرارة",
        # English
        "medicine", "drug", "paracetamol", "ibuprofen", "headache", "fever", "cough",
        "treatment", "symptom", "symptoms", "disease", "illness", "doctor", "hospital",
        "pharmacy", "pill", "tablet", "capsule", "infection", "inflammation", "pain",
        "antibiotic", "painkiller", "medication", "health", "medical", "cure", "remedy"dication", "pill", "tablet"
    ]
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in medical_keywords)
