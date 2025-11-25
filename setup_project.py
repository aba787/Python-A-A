
"""
سكربت إعداد المشروع
Project Setup Script
"""

import os
import subprocess
import sys
from pathlib import Path

def install_requirements():
    """تنصيب المتطلبات"""
    print("📦 تنصيب المتطلبات...")
    
    requirements = [
        "torch>=1.9.0",
        "transformers>=4.20.0", 
        "datasets>=2.0.0",
        "flask>=2.0.0",
        "pandas>=1.3.0",
        "numpy>=1.21.0",
        "scikit-learn>=1.0.0"
    ]
    
    for req in requirements:
        try:
            print(f"⬇️ تنصيب {req}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", req, "--quiet"])
            print(f"✅ تم تنصيب {req}")
        except subprocess.CalledProcessError as e:
            print(f"❌ خطأ في تنصيب {req}: {e}")

def create_directories():
    """إنشاء المجلدات المطلوبة"""
    print("📁 إنشاء المجلدات...")
    
    directories = [
        "templates",
        "static", 
        "models",
        "data",
        "logs"
    ]
    
    for dir_name in directories:
        Path(dir_name).mkdir(exist_ok=True)
        print(f"📂 تم إنشاء مجلد: {dir_name}")

def generate_dataset():
    """إنشاء مجموعة البيانات"""
    print("📊 إنشاء مجموعة البيانات...")
    try:
        from dataset_generator import generate_intent_dataset
        generate_intent_dataset()
        print("✅ تم إنشاء مجموعة البيانات")
    except Exception as e:
        print(f"❌ خطأ في إنشاء البيانات: {e}")

def train_model():
    """تدريب النموذج"""
    print("🎯 تدريب نموذج mBERT...")
    try:
        from train_mbert import train_intent_classifier
        train_intent_classifier()
        print("✅ تم تدريب النموذج")
    except Exception as e:
        print(f"❌ خطأ في التدريب: {e}")
        print("ℹ️ سيتم استخدام التصنيف الأساسي")

def setup_project():
    """إعداد المشروع الكامل"""
    print("🚀 بدء إعداد مشروع الشات بوت...")
    print("="*50)
    
    # 1. إنشاء المجلدات
    create_directories()
    
    # 2. تنصيب المتطلبات
    install_requirements()
    
    # 3. إنشاء مجموعة البيانات
    generate_dataset()
    
    # 4. تدريب النموذج
    train_model()
    
    print("="*50)
    print("✅ تم إعداد المشروع بنجاح!")
    print("🚀 يمكنك الآن تشغيل المشروع:")
    print("   python main.py")
    print("🌐 الرابط: http://0.0.0.0:5000")

if __name__ == "__main__":
    setup_project()
