
from typing import Dict, Optional
from .utils import detect_language

# Medical knowledge database
MED_DB = {
    "paracetamol": {
        "uses_en": "Pain relief and fever reducer",
        "uses_ar": "مسكن للألم وخافض للحرارة",
        "dose_adult_en": "500-1000 mg every 4-6 hours, max 4000mg/day",
        "dose_adult_ar": "500-1000 ملغ كل 4-6 ساعات، الحد الأقصى 4000 ملغ يومياً",
        "warnings_en": "Avoid with severe liver disease; check alcohol interactions",
        "warnings_ar": "تجنب مع أمراض الكبد الشديدة؛ احذر التداخل مع الكحول"
    },
    "ibuprofen": {
        "uses_en": "NSAID for pain, inflammation, and fever",
        "uses_ar": "مضاد التهاب غير ستيرويدي للألم والالتهاب والحمى",
        "dose_adult_en": "200-400 mg every 6-8 hours, max 1200mg/day OTC",
        "dose_adult_ar": "200-400 ملغ كل 6-8 ساعات، الحد الأقصى 1200 ملغ يومياً",
        "warnings_en": "Avoid with peptic ulcer, kidney disease; may increase bleeding risk",
        "warnings_ar": "تجنب مع قرحة المعدة وأمراض الكلى؛ قد يزيد خطر النزيف"
    }
}

def get_medicine_info(medicine_name: str, language: str = "en") -> Optional[Dict[str, str]]:
    """Get medicine information in specified language"""
    med_name = medicine_name.lower()
    
    # Handle Arabic names
    if "باراسيتامول" in med_name:
        med_name = "paracetamol"
    elif "إيبوبروفين" in med_name:
        med_name = "ibuprofen"
    
    if med_name in MED_DB:
        med = MED_DB[med_name]
        lang_suffix = "_ar" if language == "ar" else "_en"
        
        return {
            "uses": med.get(f"uses{lang_suffix}", med["uses_en"]),
            "dose_adult": med.get(f"dose_adult{lang_suffix}", med["dose_adult_en"]),
            "warnings": med.get(f"warnings{lang_suffix}", med["warnings_en"])
        }
    
    return None

def basic_medical_response(user_input: str, language: str = "en") -> str:
    """Generate basic medical response"""
    query_lower = user_input.lower()
    
    # Check for specific medicines
    if any(term in query_lower for term in ["paracetamol", "باراسيتامول", "acetaminophen"]):
        med_info = get_medicine_info("paracetamol", language)
        if language == "ar":
            return format_medicine_response_ar("باراسيتامول", med_info)
        return format_medicine_response_en("Paracetamol", med_info)
    
    elif any(term in query_lower for term in ["ibuprofen", "إيبوبروفين"]):
        med_info = get_medicine_info("ibuprofen", language)
        if language == "ar":
            return format_medicine_response_ar("إيبوبروفين", med_info)
        return format_medicine_response_en("Ibuprofen", med_info)
    
    # Check for symptoms
    elif any(term in query_lower for term in ["headache", "صداع"]):
        if language == "ar":
            return """🤒 **علاج الصداع:**

💊 الأدوية الشائعة: باراسيتامول (500-1000 ملغ) أو إيبوبروفين (200-400 ملغ)
🏠 العلاج المنزلي: راحة، كمادات باردة، شرب الماء
⚠️ هذه معلومات إرشادية فقط - استشر الطبيب أو الصيدلي"""
        return """🤒 **Headache Treatment:**

💊 Common options: Paracetamol (500-1000mg) or Ibuprofen (200-400mg)
🏠 Home care: Rest, cold compress, stay hydrated
⚠️ This is informational only - consult a healthcare professional"""
    
    # Generic response
    if language == "ar":
        return """🩺 يمكنني تقديم معلومات عن الأدوية الشائعة مثل الباراسيتامول والإيبوبروفين.
        
⚠️ تذكر: هذه معلومات عامة فقط. استشر طبيباً أو صيدلانياً مؤهلاً للحصول على المشورة الطبية المناسبة."""
    
    return """🩺 I can provide info on common OTC medications like paracetamol and ibuprofen.
    
⚠️ Remember: This is general information only. Consult a qualified healthcare professional for proper medical advice."""

def format_medicine_response_en(medicine_name: str, med_info: Dict[str, str]) -> str:
    """Format medicine information in English"""
    return f"""💊 **{medicine_name} Information:**

🎯 **Uses:** {med_info['uses']}
💊 **Adult Dosage:** {med_info['dose_adult']}
⚠️ **Warnings:** {med_info['warnings']}

**⚠️ Important:** This is informational only - consult a healthcare professional before taking any medication."""

def format_medicine_response_ar(medicine_name: str, med_info: Dict[str, str]) -> str:
    """Format medicine information in Arabic"""
    return f"""💊 **معلومات عن {medicine_name}:**

🎯 **الاستخدامات:** {med_info['uses']}
💊 **الجرعة للبالغين:** {med_info['dose_adult']}
⚠️ **تحذيرات:** {med_info['warnings']}

**⚠️ مهم:** هذه معلومات إرشادية فقط - استشر مختصاً في الرعاية الصحية قبل تناول أي دواء."""
