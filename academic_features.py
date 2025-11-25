
# 🎓 الميزات الأكاديمية المتقدمة
# Academic Features for Final Project

import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import sqlite3

class AcademicAnalytics:
    """
    نظام التحليل الأكاديمي المتطور
    Advanced Academic Analytics System
    """
    
    def __init__(self, chatbot_instance):
        self.chatbot = chatbot_instance
        self.setup_academic_database()
    
    def setup_academic_database(self):
        """إعداد قاعدة البيانات الأكاديمية"""
        conn = sqlite3.connect(self.chatbot.db_path)
        cursor = conn.cursor()
        
        # جدول تحليل الأداء الأكاديمي
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS academic_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model_type TEXT NOT NULL,
            language_detected TEXT,
            intent_predicted TEXT,
            confidence_score REAL,
            response_time REAL,
            accuracy_rating INTEGER,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # جدول تقييم المستخدمين
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_input TEXT,
            bot_response TEXT,
            user_rating INTEGER CHECK(user_rating BETWEEN 1 AND 5),
            feedback_text TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        conn.commit()
        conn.close()
    
    def generate_academic_report(self):
        """إنتاج التقرير الأكاديمي الشامل"""
        report = {
            "project_info": {
                "title": "نظام التشاتبوت الذكي متعدد اللغات",
                "subtitle": "مشروع التخرج - دعم mBERT و Transformers",
                "student_name": "ليال",
                "technologies": ["mBERT", "Transformers", "Flask", "SQLite", "APIs"],
                "languages_supported": ["Arabic", "English", "Mixed"],
                "generated_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            "technical_specifications": self.get_technical_specs(),
            "performance_metrics": self.get_performance_metrics(),
            "dataset_analysis": self.get_dataset_analysis(),
            "multilingual_support": self.get_multilingual_analysis(),
            "external_integrations": self.get_integration_analysis()
        }
        
        return report
    
    def get_technical_specs(self):
        """المواصفات التقنية"""
        return {
            "ai_model": "mBERT (bert-base-multilingual-cased)" if hasattr(self.chatbot, 'use_mbert') and self.chatbot.use_mbert else "Scikit-learn Pipeline",
            "database": "SQLite with 4 specialized tables",
            "api_integrations": ["wttr.in Weather API", "RSS News Feeds", "OpenWeatherMap (optional)"],
            "framework": "Flask Web Application",
            "supported_languages": ["Arabic", "English"],
            "response_types": ["Text", "Structured Data", "External APIs", "Real-time Information"]
        }
    
    def get_performance_metrics(self):
        """مقاييس الأداء"""
        conn = sqlite3.connect(self.chatbot.db_path)
        
        # إحصائيات الثقة
        df_conversations = pd.read_sql_query(
            "SELECT confidence, response_time, timestamp FROM conversations WHERE confidence > 0", 
            conn
        )
        
        if not df_conversations.empty:
            metrics = {
                "total_conversations": len(df_conversations),
                "average_confidence": df_conversations['confidence'].mean() * 100,
                "confidence_std": df_conversations['confidence'].std() * 100,
                "average_response_time": df_conversations['response_time'].mean() * 1000,  # ms
                "high_confidence_rate": len(df_conversations[df_conversations['confidence'] > 0.7]) / len(df_conversations) * 100,
                "confidence_distribution": {
                    "high (>70%)": len(df_conversations[df_conversations['confidence'] > 0.7]),
                    "medium (30-70%)": len(df_conversations[(df_conversations['confidence'] >= 0.3) & (df_conversations['confidence'] <= 0.7)]),
                    "low (<30%)": len(df_conversations[df_conversations['confidence'] < 0.3])
                }
            }
        else:
            metrics = {
                "total_conversations": 0,
                "average_confidence": 0,
                "note": "لم يتم إجراء محادثات كافية للتحليل"
            }
        
        conn.close()
        return metrics
    
    def get_dataset_analysis(self):
        """تحليل مجموعة البيانات"""
        datasets_info = {}
        
        # تحليل بيانات الطلاب
        try:
            students_df = pd.read_csv("students_data.csv")
            datasets_info["students"] = {
                "total_records": len(students_df),
                "unique_majors": students_df['major'].nunique(),
                "average_gpa": students_df['gpa'].mean(),
                "gpa_distribution": students_df['gpa'].describe().to_dict(),
                "university_distribution": students_df['university'].value_counts().to_dict()
            }
        except Exception as e:
            datasets_info["students"] = {"error": str(e)}
        
        # تحليل بيانات الطقس
        try:
            with open("weather_data.json", "r", encoding="utf-8") as f:
                weather_data = json.load(f)
                datasets_info["weather"] = {
                    "total_cities": len(weather_data),
                    "avg_temperature": sum(item['temp'] for item in weather_data) / len(weather_data),
                    "cities_covered": [item['city'] for item in weather_data],
                    "conditions_variety": len(set(item['condition'] for item in weather_data))
                }
        except Exception as e:
            datasets_info["weather"] = {"error": str(e)}
        
        return datasets_info
    
    def get_multilingual_analysis(self):
        """تحليل الدعم متعدد اللغات"""
        return {
            "mbert_status": hasattr(self.chatbot, 'use_mbert') and self.chatbot.use_mbert,
            "supported_features": {
                "arabic_processing": "✅ دعم كامل",
                "english_processing": "✅ دعم كامل", 
                "mixed_language": "✅ دعم ذكي",
                "language_detection": "✅ تلقائي",
                "intent_classification": "✅ متعدد اللغات"
            },
            "academic_value": {
                "transformer_integration": "mBERT للتصنيف المتقدم",
                "multilingual_nlp": "معالجة طبيعية للغات المتعددة",
                "cross_language_understanding": "فهم السياق عبر اللغات",
                "practical_application": "تطبيق عملي لأحدث تقنيات NLP"
            }
        }
    
    def get_integration_analysis(self):
        """تحليل التكاملات الخارجية"""
        return {
            "real_time_apis": {
                "weather_api": {"source": "wttr.in", "status": "active", "cost": "free"},
                "news_feeds": {"source": "RSS", "status": "active", "cost": "free"},
                "optional_apis": {"openweather": "configurable", "newsapi": "configurable"}
            },
            "data_sources": {
                "csv_files": ["students_data.csv"],
                "json_files": ["weather_data.json", "products_data.json", "companies_data.json", "restaurants_data.json"],
                "database": "chatbot.db (SQLite)",
                "external_apis": "3+ active integrations"
            },
            "academic_significance": {
                "real_world_data": "بيانات حقيقية من الإنترنت",
                "multi_source_integration": "دمج مصادر متعددة",
                "scalable_architecture": "قابل للتوسع والتطوير",
                "industry_standard": "معايير الصناعة الحديثة"
            }
        }
    
    def export_academic_report(self, format="json"):
        """تصدير التقرير الأكاديمي"""
        report = self.generate_academic_report()
        
        if format == "json":
            with open("academic_report.json", "w", encoding="utf-8") as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
        
        elif format == "markdown":
            markdown_content = self.generate_markdown_report(report)
            with open("academic_report.md", "w", encoding="utf-8") as f:
                f.write(markdown_content)
        
        return f"تم تصدير التقرير الأكاديمي بصيغة {format}"
    
    def generate_markdown_report(self, report):
        """إنتاج تقرير Markdown للمشروع الأكاديمي"""
        markdown = f"""# {report['project_info']['title']}

## {report['project_info']['subtitle']}

**الطالبة:** {report['project_info']['student_name']}  
**تاريخ الإنتاج:** {report['project_info']['generated_date']}

## التقنيات المستخدمة
{', '.join(report['project_info']['technologies'])}

## المواصفات التقنية

### نموذج الذكاء الاصطناعي
- **النموذج:** {report['technical_specifications']['ai_model']}
- **قاعدة البيانات:** {report['technical_specifications']['database']}
- **الإطار:** {report['technical_specifications']['framework']}

### الدعم اللغوي
- **اللغات المدعومة:** {', '.join(report['technical_specifications']['supported_languages'])}

## مقاييس الأداء

- **إجمالي المحادثات:** {report['performance_metrics'].get('total_conversations', 0)}
- **متوسط الثقة:** {report['performance_metrics'].get('average_confidence', 0):.2f}%
- **متوسط زمن الاستجابة:** {report['performance_metrics'].get('average_response_time', 0):.2f} ms

## التكاملات الخارجية

### APIs المفعلة
- wttr.in للطقس (مجاني)
- RSS للأخبار (مجاني)
- OpenWeatherMap (اختياري)

## الخلاصة الأكاديمية

هذا المشروع يمثل تطبيقاً متقدماً لتقنيات:
- **Transformers و mBERT**
- **معالجة اللغة الطبيعية متعددة اللغات** 
- **تكامل البيانات الحقيقية**
- **تطوير تطبيقات الويب التفاعلية**

---
*تم إنتاج هذا التقرير تلقائياً بواسطة نظام التحليل الأكاديمي*
"""
        return markdown

# دمج الميزات الأكاديمية في التطبيق الرئيسي
def integrate_academic_features(chatbot_instance):
    """دمج الميزات الأكاديمية"""
    academic_analytics = AcademicAnalytics(chatbot_instance)
    return academic_analytics
