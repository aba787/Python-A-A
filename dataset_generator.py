
"""
مولد مجموعة البيانات للتدريب
Dataset Generator for Training
"""

import json
import csv
import pandas as pd
from datetime import datetime

def generate_intent_dataset():
    """إنشاء مجموعة بيانات شاملة للتدريب"""
    
    # قاموس النوايا والأمثلة
    intents_dataset = {
        "greeting": {
            "arabic_examples": [
                "مرحبا", "أهلا", "السلام عليكم", "صباح الخير", "مساء الخير",
                "هاي", "هلو", "اهلاً وسهلاً", "مرحباً بك", "كيف الحال",
                "وعليكم السلام", "اهلاً بك", "مساء النور", "صباح النور",
                "سلام", "سلامات", "مرحبتين", "اهلين", "كيفك", "شلونك"
            ],
            "english_examples": [
                "hello", "hi", "hey", "good morning", "good evening",
                "greetings", "howdy", "what's up", "how are you", "hi there",
                "good day", "good afternoon", "nice to meet you", "hello there",
                "hey there", "morning", "evening", "sup", "yo", "hiya"
            ],
            "mixed_examples": [
                "مرحبا hello", "hi كيف الحال", "good morning صباح الخير",
                "سلام how are you", "hey كيفك", "مرحباً good day"
            ]
        },
        
        "time": {
            "arabic_examples": [
                "كم الساعة", "الوقت الآن", "وش الوقت", "كم الوقت",
                "اي ساعة الحين", "الساعة كم", "وقت اللي الان",
                "قول لي الوقت", "ابي اعرف الوقت", "الوقت كم الحين"
            ],
            "english_examples": [
                "what time is it", "current time", "time now", "what's the time",
                "tell me the time", "what time", "time please", "current time please",
                "what time is it now", "time check", "clock", "time"
            ],
            "mixed_examples": [
                "what time الان", "الوقت now", "time الحين", "ساعة time"
            ]
        },
        
        "weather": {
            "arabic_examples": [
                "كيف الطقس", "الجو", "درجة الحرارة", "المطر", "الشمس",
                "البرد", "الحر", "طقس اليوم", "الجو كيف", "الطقس ايش",
                "هل فيه مطر", "الجو بارد", "الجو حار", "درجة الحرارة كم"
            ],
            "english_examples": [
                "weather", "temperature", "how's the weather", "rain", "sunny",
                "cold", "hot", "weather today", "weather forecast", "climate",
                "is it raining", "weather report", "what's the weather like"
            ],
            "mixed_examples": [
                "weather الطقس", "الجو weather", "temperature درجة الحرارة"
            ]
        },
        
        "help": {
            "arabic_examples": [
                "مساعدة", "ساعدني", "كيف تعمل", "ماذا تستطيع", "قائمة الأوامر",
                "ابي مساعدة", "وش تقدر تسوي", "كيف استخدمك", "ساعدني في شيء",
                "احتاج مساعدة", "دليل الاستخدام", "التعليمات", "كيف اشتغل معك"
            ],
            "english_examples": [
                "help", "assist me", "what can you do", "commands", "support",
                "help me", "assistance", "guide", "how do you work", "instructions",
                "what are your capabilities", "user manual", "how to use"
            ],
            "mixed_examples": [
                "help مساعدة", "ساعدني please", "assistance ساعدة"
            ]
        },
        
        "goodbye": {
            "arabic_examples": [
                "وداعاً", "باي", "مع السلامة", "شكراً", "تصبح على خير",
                "سلامة", "الله يعطيك العافية", "تسلم", "باي باي", "وداعا",
                "مع السلامة والعافية", "الله يوفقك", "شكرا لك", "اشكرك"
            ],
            "english_examples": [
                "goodbye", "bye", "see you", "thank you", "thanks", "good night",
                "farewell", "see you later", "catch you later", "take care",
                "bye bye", "good bye", "until next time", "see ya"
            ],
            "mixed_examples": [
                "bye وداعاً", "شكراً thank you", "goodbye مع السلامة"
            ]
        },
        
        "about": {
            "arabic_examples": [
                "من أنت", "ما هذا", "عن المشروع", "معلومات عنك", "كيف تعمل",
                "وش انت", "ايش هذا البرنامج", "قول لي عنك", "كيف صنعوك",
                "من صنعك", "معلومات عن البوت", "تفاصيل عنك"
            ],
            "english_examples": [
                "who are you", "what is this", "about", "tell me about yourself",
                "information", "what are you", "about this bot", "your details",
                "who created you", "about this project", "bot information"
            ],
            "mixed_examples": [
                "who are you من انت", "about معلومات", "information عنك"
            ]
        }
    }
    
    # إنشاء مجموعة بيانات للتدريب
    training_data = []
    
    for intent, examples in intents_dataset.items():
        # إضافة الأمثلة العربية
        for example in examples["arabic_examples"]:
            training_data.append({
                "text": example,
                "intent": intent,
                "language": "arabic"
            })
        
        # إضافة الأمثلة الإنجليزية
        for example in examples["english_examples"]:
            training_data.append({
                "text": example,
                "intent": intent,
                "language": "english"
            })
        
        # إضافة الأمثلة المختلطة
        for example in examples["mixed_examples"]:
            training_data.append({
                "text": example,
                "intent": intent,
                "language": "mixed"
            })
    
    # حفظ البيانات في صيغ مختلفة
    
    # JSON
    with open('training_dataset.json', 'w', encoding='utf-8') as f:
        json.dump(training_data, f, ensure_ascii=False, indent=2)
    
    # CSV
    df = pd.DataFrame(training_data)
    df.to_csv('training_dataset.csv', index=False, encoding='utf-8')
    
    # إحصائيات
    stats = {
        "total_examples": len(training_data),
        "intents": list(intents_dataset.keys()),
        "intent_counts": df.groupby('intent').size().to_dict(),
        "language_distribution": df.groupby('language').size().to_dict(),
        "generated_at": datetime.now().isoformat()
    }
    
    with open('dataset_stats.json', 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    
    print(f"✅ تم إنشاء مجموعة البيانات بنجاح!")
    print(f"📊 إجمالي الأمثلة: {stats['total_examples']}")
    print(f"🏷️ عدد النوايا: {len(stats['intents'])}")
    print(f"📋 النوايا: {', '.join(stats['intents'])}")
    print(f"🌍 توزيع اللغات: {stats['language_distribution']}")
    
    return training_data

if __name__ == "__main__":
    generate_intent_dataset()
