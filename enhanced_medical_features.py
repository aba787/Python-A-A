
"""
🏥 النظام الطبي المتقدم - Enhanced Medical Features
نسخة محسنة بناءً على المخطط الأكاديمي المقترح
"""

import json
import sqlite3
from datetime import datetime
import re

class AdvancedMedicalSystem:
    """نظام طبي متقدم مع إمكانيات مطورة"""
    
    def __init__(self, chatbot_instance):
        self.chatbot = chatbot_instance
        self.medical_intents = self.load_medical_intents()
        self.drug_interactions = self.load_drug_interactions()
        self.setup_medical_database()
    
    def load_medical_intents(self):
        """تحميل النوايا الطبية المتقدمة حسب المخطط"""
        return {
            "prescription_reading": ["وصفة", "روشتة", "دواء", "علاج"],
            "medical_inquiry": ["مرض", "أعراض", "تشخيص", "حالة طبية"],
            "drug_information": ["معلومات دواء", "تفاعل دوائي", "جرعة"],
            "medical_terms": ["مصطلح طبي", "تعريف طبي", "شرح مصطلح"],
            "health_consultation": ["استشارة", "رأي طبي", "نصيحة طبية"],
            "emergency_symptoms": ["طوارئ", "أعراض خطيرة", "حالة عاجلة"]
        }
    
    def load_drug_interactions(self):
        """قاعدة بيانات التفاعلات الدوائية"""
        return {
            "باراسيتامول": {
                "interactions": ["كحول", "وارفارين"],
                "warnings": ["لا تتجاوز 4 جرام يومياً", "تجنب مع أمراض الكبد"]
            },
            "إيبوبروفين": {
                "interactions": ["أسبرين", "وارفارين", "أدوية الضغط"],
                "warnings": ["تجنب مع أمراض القلب", "تناول مع الطعام"]
            },
            "أموكسيسيلين": {
                "interactions": ["حبوب منع الحمل", "وارفارين"],
                "warnings": ["أكمل العلاج كاملاً", "أخبر الطبيب عن الحساسية"]
            }
        }
    
    def setup_medical_database(self):
        """إعداد قاعدة البيانات الطبية المتقدمة"""
        conn = sqlite3.connect(self.chatbot.db_path)
        cursor = conn.cursor()
        
        # جدول الوصفات المعالجة
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS processed_prescriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_session TEXT,
            image_hash TEXT,
            extracted_text TEXT,
            identified_medicines TEXT,
            analysis_result TEXT,
            confidence_score REAL,
            processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # جدول الاستشارات الطبية
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS medical_consultations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_query TEXT,
            medical_intent TEXT,
            bot_response TEXT,
            safety_warnings TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        conn.commit()
        conn.close()
    
    def classify_medical_intent(self, query):
        """تصنيف النية الطبية المتقدم"""
        query_lower = query.lower()
        
        # تصنيف النوايا بناءً على الكلمات المفتاحية
        for intent, keywords in self.medical_intents.items():
            if any(keyword in query_lower for keyword in keywords):
                return intent, self.get_intent_confidence(query_lower, keywords)
        
        return "general_medical", 0.3
    
    def get_intent_confidence(self, query, keywords):
        """حساب ثقة التصنيف"""
        matches = sum(1 for keyword in keywords if keyword in query)
        return min(0.95, 0.4 + (matches * 0.2))
    
    def advanced_prescription_analysis(self, extracted_text):
        """تحليل متقدم للوصفات الطبية"""
        analysis = {
            "medicines": [],
            "dosages": [],
            "frequencies": [],
            "warnings": [],
            "drug_interactions": [],
            "medical_advice": []
        }
        
        # تحليل أكثر تقدماً للأدوية
        medicine_patterns = [
            r'(\w+)\s*(\d+\s*(?:mg|ml|g))',  # دواء + جرعة
            r'(\w+)\s*كبسولة',  # دواء + كبسولة
            r'(\w+)\s*حبة',     # دواء + حبة
            r'(\w+)\s*شراب'     # دواء + شراب
        ]
        
        for pattern in medicine_patterns:
            matches = re.findall(pattern, extracted_text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    medicine_name = match[0]
                    dosage = match[1] if len(match) > 1 else "غير محدد"
                else:
                    medicine_name = match
                    dosage = "غير محدد"
                
                # البحث في قاعدة البيانات الطبية
                medicine_info = self.get_medicine_info(medicine_name)
                if medicine_info:
                    analysis["medicines"].append({
                        "name": medicine_name,
                        "dosage": dosage,
                        "info": medicine_info
                    })
        
        # تحليل التفاعلات الدوائية
        analysis["drug_interactions"] = self.check_drug_interactions(
            [med["name"] for med in analysis["medicines"]]
        )
        
        # نصائح طبية
        analysis["medical_advice"] = self.generate_medical_advice(analysis)
        
        return analysis
    
    def get_medicine_info(self, medicine_name):
        """الحصول على معلومات الدواء من قاعدة البيانات"""
        # البحث في قاعدة البيانات الطبية المحلية
        medicines_db = self.chatbot.data_manager.medical_database["medicines"]
        
        for medicine in medicines_db:
            if medicine_name.lower() in medicine["name"].lower() or \
               medicine_name.lower() in medicine["name_en"].lower():
                return medicine
        
        return None
    
    def check_drug_interactions(self, medicine_names):
        """فحص التفاعلات الدوائية"""
        interactions = []
        
        for medicine in medicine_names:
            if medicine in self.drug_interactions:
                drug_data = self.drug_interactions[medicine]
                for other_medicine in medicine_names:
                    if other_medicine != medicine and \
                       other_medicine in drug_data["interactions"]:
                        interactions.append({
                            "drug1": medicine,
                            "drug2": other_medicine,
                            "severity": "متوسط إلى عالي",
                            "recommendation": "استشر الطبيب قبل تناول هذين الدواءين معاً"
                        })
        
        return interactions
    
    def generate_medical_advice(self, analysis):
        """توليد نصائح طبية شخصية"""
        advice = [
            "⚠️ هذا التحليل للمعلومات فقط وليس بديلاً عن الاستشارة الطبية",
            "🏥 استشر طبيبك دائماً قبل تغيير أي دواء",
            "💊 تناول الأدوية حسب التعليمات المكتوبة",
            "📞 اتصل بالطبيب فوراً إذا ظهرت أعراض جانبية"
        ]
        
        # نصائح خاصة بناءً على الأدوية المكتشفة
        for medicine in analysis["medicines"]:
            medicine_name = medicine["name"]
            if medicine_name in self.drug_interactions:
                warnings = self.drug_interactions[medicine_name]["warnings"]
                advice.extend([f"⚡ {medicine_name}: {warning}" for warning in warnings])
        
        return advice
    
    def save_medical_consultation(self, user_query, intent, response, warnings):
        """حفظ الاستشارة الطبية"""
        conn = sqlite3.connect(self.chatbot.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
        INSERT INTO medical_consultations 
        (user_query, medical_intent, bot_response, safety_warnings)
        VALUES (?, ?, ?, ?)
        """, (user_query, intent, response, json.dumps(warnings, ensure_ascii=False)))
        
        conn.commit()
        conn.close()
    
    def generate_comprehensive_response(self, query):
        """توليد رد طبي شامل"""
        intent, confidence = self.classify_medical_intent(query)
        
        response_parts = []
        warnings = []
        
        if intent == "prescription_reading":
            response_parts.append("🏥 لقراءة الوصفة الطبية، يرجى رفع صورة واضحة للوصفة")
            response_parts.append("📱 استخدم زر 'رفع وصفة' في الواجهة")
            
        elif intent == "medical_inquiry":
            response_parts.append("🩺 أفهم أن لديك استفسار طبي")
            response_parts.append("⚠️ المعلومات المقدمة للإرشاد فقط")
            warnings.append("استشر طبيباً مؤهلاً للتشخيص الدقيق")
            
        elif intent == "drug_information":
            response_parts.append("💊 سأوفر معلومات عن الأدوية")
            response_parts.append("📚 المعلومات مستمدة من مصادر طبية موثوقة")
            warnings.append("لا تغير جرعة الدواء بدون استشارة طبية")
            
        elif intent == "emergency_symptoms":
            response_parts.append("🚨 إذا كانت حالة طارئة، اتصل بالطوارئ فوراً")
            response_parts.append("📞 الرقم الموحد للطوارئ: 997")
            warnings.append("لا تتأخر في طلب المساعدة الطبية العاجلة")
        
        # إضافة تحذيرات أمان
        response_parts.extend([
            "\n" + "="*50,
            "🛡️ تحذيرات السلامة الطبية:",
            "• هذا البوت للمعلومات العامة فقط",
            "• ليس بديلاً عن الطبيب المختص",
            "• في الطوارئ اتصل بـ 997 فوراً",
            "• استشر طبيبك لأي مشاكل صحية"
        ])
        
        full_response = "\n".join(response_parts)
        
        # حفظ الاستشارة
        self.save_medical_consultation(query, intent, full_response, warnings)
        
        return {
            "response": full_response,
            "intent": intent,
            "confidence": confidence,
            "warnings": warnings,
            "type": "medical_consultation"
        }

# تكامل مع النظام الرئيسي
def integrate_advanced_medical_features(chatbot_instance):
    """دمج النظام الطبي المتقدم"""
    return AdvancedMedicalSystem(chatbot_instance)
