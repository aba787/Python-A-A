"""
تدريب نموذج mBERT على تصنيف النوايا
mBERT Intent Classification Training Script
"""

import torch
from transformers import (
    BertTokenizer, BertForSequenceClassification,
    Trainer, TrainingArguments, DataCollatorWithPadding
)
from datasets import Dataset
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import json

def create_training_dataset():
    """إنشاء مجموعة بيانات التدريب المتوازنة"""

    # بيانات التدريب المتوازنة والمتنوعة
    training_data = [
        # التحيات - 50 جملة متوازنة
        ("مرحبا", "greeting"), ("أهلاً", "greeting"), ("السلام عليكم", "greeting"),
        ("صباح الخير", "greeting"), ("مساء الخير", "greeting"), ("هاي", "greeting"),
        ("هلو", "greeting"), ("كيف الحال", "greeting"), ("شلونك", "greeting"),
        ("وش اخبارك", "greeting"), ("كيفك", "greeting"), ("اهلين", "greeting"),
        ("مرحبتين", "greeting"), ("سلامات", "greeting"), ("يا هلا", "greeting"),
        ("مساء النور", "greeting"), ("صباح النور", "greeting"), ("تشرفنا", "greeting"),
        ("hello", "greeting"), ("hi", "greeting"), ("hey", "greeting"),
        ("good morning", "greeting"), ("good evening", "greeting"), ("greetings", "greeting"),
        ("howdy", "greeting"), ("أهلاً وسهلاً", "greeting"), ("مرحباً بك", "greeting"),
        ("وعليكم السلام", "greeting"), ("اهلاً بك", "greeting"), ("سلام عليكم", "greeting"),
        ("يا مرحبا", "greeting"), ("اهلاً وسهلاً بك", "greeting"), ("سعيد بلقائك", "greeting"),
        ("تشرفنا بوجودك", "greeting"), ("نورتنا", "greeting"), ("حياك الله", "greeting"),
        ("أهلاً ومرحباً", "greeting"), ("سلام", "greeting"), ("مساء الورد", "greeting"),
        ("صباح الورد", "greeting"), ("يسعد صباحك", "greeting"), ("يسعد مساك", "greeting"),
        ("hi there", "greeting"), ("good day", "greeting"), ("good afternoon", "greeting"),
        ("nice to see you", "greeting"), ("pleasure to meet you", "greeting"), ("welcome", "greeting"),
        ("what's up", "greeting"), ("how are you doing", "greeting"), ("how's everything", "greeting"),
        ("great to see you", "greeting"), ("lovely to meet you", "greeting"), ("hiya", "greeting"),

        # الوقت - 20 جملة
        ("كم الساعة", "time"), ("الوقت الآن", "time"), ("وش الوقت", "time"),
        ("كم الوقت", "time"), ("اي ساعة الحين", "time"), ("الساعة كم", "time"),
        ("وقت اللي الان", "time"), ("قول لي الوقت", "time"), ("ابي اعرف الوقت", "time"),
        ("الوقت كم الحين", "time"), ("كم الساعة الحين", "time"), ("الوقت بالضبط", "time"),
        ("what time is it", "time"), ("current time", "time"), ("time now", "time"),
        ("what's the time", "time"), ("tell me the time", "time"), ("time please", "time"),
        ("what time is it now", "time"), ("time check", "time"),

        # الطقس - 25 جملة
        ("كيف الطقس", "weather"), ("الجو", "weather"), ("درجة الحرارة", "weather"),
        ("المطر", "weather"), ("الشمس", "weather"), ("البرد", "weather"),
        ("الحر", "weather"), ("طقس اليوم", "weather"), ("الجو كيف", "weather"),
        ("الطقس ايش", "weather"), ("هل فيه مطر", "weather"), ("الجو بارد", "weather"),
        ("الجو حار", "weather"), ("درجة الحرارة كم", "weather"), ("الطقس برا", "weather"),
        ("الجو اليوم", "weather"), ("هل بيمطر", "weather"), ("الحالة الجوية", "weather"),
        ("weather", "weather"), ("temperature", "weather"), ("how's the weather", "weather"),
        ("rain", "weather"), ("sunny", "weather"), ("cold", "weather"), ("hot", "weather"),
        ("weather today", "weather"), ("weather forecast", "weather"),

        # المساعدة - 50 جملة متوازنة
        ("مساعدة", "help"), ("ساعدني", "help"), ("كيف تعمل", "help"),
        ("ماذا تستطيع أن تفعل", "help"), ("قائمة الأوامر", "help"), ("ابي مساعدة", "help"),
        ("وش تقدر تسوي", "help"), ("كيف استخدمك", "help"), ("ساعدني في شيء", "help"),
        ("احتاج مساعدة", "help"), ("دليل الاستخدام", "help"), ("التعليمات", "help"),
        ("كيف اشتغل معك", "help"), ("وش خدماتك", "help"), ("ايش تقدر تساعدني", "help"),
        ("كيف اقدر استفيد منك", "help"), ("وش الاوامر المتاحة", "help"), ("ساعدة", "help"),
        ("help", "help"), ("assist me", "help"), ("what can you do", "help"),
        ("commands", "help"), ("support", "help"), ("how do you work", "help"),
        ("assistance", "help"), ("guide", "help"), ("instructions", "help"),
        ("ممكن تساعدني", "help"), ("ابي مساعدة منك", "help"), ("كيف يمكنك مساعدتي", "help"),
        ("احتاج دعم", "help"), ("وش الخدمات المتاحة", "help"), ("كيف اقدر اتعامل معك", "help"),
        ("دليل المستخدم", "help"), ("شرح كيف تشتغل", "help"), ("وضحلي كيف اشتغل معك", "help"),
        ("طريقة الاستعمال", "help"), ("كيفية التعامل معك", "help"), ("شو قدراتك", "help"),
        ("وش تقدر تعملي", "help"), ("ايش مهامك", "help"), ("كيف ممكن تفيدني", "help"),
        ("I need help", "help"), ("can you help me", "help"), ("how do I use this", "help"),
        ("what are your features", "help"), ("show me commands", "help"), ("user manual", "help"),
        ("how to use", "help"), ("what can I ask you", "help"), ("available options", "help"),
        ("your capabilities", "help"), ("feature list", "help"), ("instruction manual", "help"),
        ("tutorial", "help"), ("getting started", "help"), ("how does this work", "help"),

        # الوداع - 20 جملة
        ("وداعاً", "goodbye"), ("باي", "goodbye"), ("مع السلامة", "goodbye"),
        ("شكراً", "goodbye"), ("تصبح على خير", "goodbye"), ("سلامة", "goodbye"),
        ("الله يعطيك العافية", "goodbye"), ("تسلم", "goodbye"), ("باي باي", "goodbye"),
        ("وداعا", "goodbye"), ("مع السلامة والعافية", "goodbye"), ("الله يوفقك", "goodbye"),
        ("شكرا لك", "goodbye"), ("اشكرك", "goodbye"), ("تسلم ايديك", "goodbye"),
        ("goodbye", "goodbye"), ("bye", "goodbye"), ("see you", "goodbye"),
        ("thank you", "goodbye"), ("thanks", "goodbye"), ("good night", "goodbye"),

        # معلومات عن البوت - 50 جملة متوازنة
        ("من أنت", "about"), ("ما هذا", "about"), ("عن المشروع", "about"),
        ("معلومات عنك", "about"), ("كيف تعمل", "about"), ("وش انت", "about"),
        ("ايش هذا البرنامج", "about"), ("قول لي عنك", "about"), ("كيف صنعوك", "about"),
        ("من صنعك", "about"), ("معلومات عن البوت", "about"), ("تفاصيل عنك", "about"),
        ("ايش قصتك", "about"), ("من طورك", "about"), ("كيف انتم مصممين", "about"),
        ("who are you", "about"), ("what is this", "about"), ("about", "about"),
        ("tell me about yourself", "about"), ("information", "about"), ("your details", "about"),
        ("ايش هذا الموقع", "about"), ("وش هذا التطبيق", "about"), ("معلومات عن النظام", "about"),
        ("نبذة عنك", "about"), ("تعريف بنفسك", "about"), ("قصة المشروع", "about"),
        ("كيف تم تطويرك", "about"), ("من بناك", "about"), ("ايش تقنيتك", "about"),
        ("وش نوع البرنامج هذا", "about"), ("ايش هويتك", "about"), ("تفاصيل التطبيق", "about"),
        ("نظرة عن البوت", "about"), ("سيرة ذاتية", "about"), ("بروفايل", "about"),
        ("ايش خلفيتك", "about"), ("وش مصدرك", "about"), ("من وين جيت", "about"),
        ("what's this bot", "about"), ("bot information", "about"), ("system details", "about"),
        ("project information", "about"), ("about this system", "about"), ("who created you", "about"),
        ("your background", "about"), ("system info", "about"), ("bot profile", "about"),
        ("tell me more", "about"), ("your story", "about"), ("how were you made", "about"),
        ("what kind of bot", "about"), ("bot details", "about"), ("your identity", "about"),
        ("system description", "about"), ("project details", "about"), ("about the project", "about"),

        # الطلبات الطبية والأدوية - 50 جملة متنوعة
        ("بدي دواء للصداع", "medicine"), ("عندي صداع شو آخد", "medicine"),
        ("أعطيني علاج للصداع", "medicine"), ("صداع قوي بدي دواء", "medicine"),
        ("ايش آخذ للصداع", "medicine"), ("دواء للصداع", "medicine"),
        ("علاج الصداع", "medicine"), ("مسكن للألم", "medicine"),
        ("صداعي يوجعني", "medicine"), ("راسي يوجعني", "medicine"),
        ("عندي وجع راس", "medicine"), ("صداع نصفي", "medicine"),
        ("مسكن صداع", "medicine"), ("حبة للصداع", "medicine"),
        ("دواء وجع الراس", "medicine"), ("علاج وجع الراس", "medicine"),
        ("ايش احط للصداع", "medicine"), ("وش اشرب للصداع", "medicine"),
        ("عقار للصداع", "medicine"), ("باراسيتامول للصداع", "medicine"),
        ("ايبوبروفين للصداع", "medicine"), ("مسكن قوي", "medicine"),
        ("عطيني دواء للصداع", "medicine"), ("أحتاج علاج للصداع", "medicine"),
        ("وش أخذ اذا راسي يوجعني", "medicine"), ("دواء لوجع الراس", "medicine"),
        ("عندي صداع شو آخذ", "medicine"), ("ايش يفيد للصداع", "medicine"),
        ("مسكن للصداع لو سمحت", "medicine"), ("حبوب للصداع", "medicine"),
        ("دواء الراس", "medicine"), ("علاج وجع الراس", "medicine"),
        ("صداع شديد ايش آخذ", "medicine"), ("راسي يعورني شو اعمل", "medicine"),
        ("ابي دواء للصداع", "medicine"), ("بدي مسكن للراس", "medicine"),
        ("وش العلاج للصداع", "medicine"), ("صداع مزعج ايش الحل", "medicine"),
        ("ايش افضل دواء للصداع", "medicine"), ("مين يعرف دواء للصداع", "medicine"),
        ("I have a headache what should I take", "medicine"),
        ("give me medicine for headache", "medicine"), ("headache treatment", "medicine"),
        ("pain relief", "medicine"), ("what to take for headache", "medicine"),
        ("headache medicine", "medicine"), ("my head hurts", "medicine"),
        ("I need pain killer", "medicine"), ("headache remedy", "medicine"),
        ("severe headache medicine", "medicine"), ("migraine treatment", "medicine"),

        # جمل مختلطة ومعقدة للتأكد من التنوع
        ("مرحبا كيف الحال", "greeting"), ("hello how are you", "greeting"),
        ("أهلاً وسهلاً بك", "greeting"), ("hi there friend", "greeting"),
        ("السلام عليكم ورحمة الله", "greeting"), ("good morning everyone", "greeting"),

        ("ممكن تساعدني في شيء", "help"), ("I need help with something", "help"),
        ("كيف أقدر أتواصل معك", "help"), ("how can I contact you", "help"),
        ("ايش الاشياء اللي تقدر تساعدني فيها", "help"), ("what are your capabilities", "help"),

        ("كم الساعة الآن بالضبط", "time"), ("what time is it right now", "time"),
        ("الوقت الحالي في السعودية", "time"), ("current time in Saudi Arabia", "time"),

        ("شكراً لك وداعاً", "goodbye"), ("thanks a lot goodbye", "goodbye"),
        ("أشكرك على المساعدة", "goodbye"), ("I appreciate your help", "goodbye"),

        ("كيف حالة الطقس اليوم", "weather"), ("what's the weather like today", "weather"),
        ("هل الجو بارد برا", "weather"), ("is it cold outside", "weather"),

        ("صداعي قوي جداً ايش آخذ", "medicine"), ("severe headache what medicine", "medicine"),

        # أسئلة عامة غير مصنفة - 50 جملة متوازنة
        ("ما رأيك في الطعام", "unknown"), ("what do you think about food", "unknown"),
        ("أحب اللون الأزرق", "unknown"), ("I like blue color", "unknown"),
        ("الرياضة مفيدة للصحة", "unknown"), ("sports are good for health", "unknown"),
        ("كم عمرك", "unknown"), ("how old are you", "unknown"),
        ("وين تسكن", "unknown"), ("where do you live", "unknown"),
        ("ايش تحب تاكل", "unknown"), ("what do you like to eat", "unknown"),
        ("هل تحب السفر", "unknown"), ("do you like traveling", "unknown"),
        ("ايش لونك المفضل", "unknown"), ("what's your favorite color", "unknown"),
        ("كيف كان يومك", "unknown"), ("how was your day", "unknown"),
        ("وش رأيك بالسيارات", "unknown"), ("what about cars", "unknown"),
        ("احب الموسيقى", "unknown"), ("I love music", "unknown"),
        ("الكتب مفيدة", "unknown"), ("books are useful", "unknown"),
        ("السينما ممتعة", "unknown"), ("movies are fun", "unknown"),
        ("ايش هواياتك", "unknown"), ("what are your hobbies", "unknown"),
        ("هل تحب القراءة", "unknown"), ("do you like reading", "unknown"),
        ("الطبخ فن جميل", "unknown"), ("cooking is beautiful art", "unknown"),
        ("وش رأيك بالألعاب", "unknown"), ("what about games", "unknown"),
        ("احب الشاي", "unknown"), ("I like tea", "unknown"),
        ("القهوة افضل", "unknown"), ("coffee is better", "unknown"),
        ("الورود جميلة", "unknown"), ("flowers are beautiful", "unknown"),
        ("البحر رائع", "unknown"), ("sea is wonderful", "unknown"),
        ("الجبال خلابة", "unknown"), ("mountains are stunning", "unknown"),
        ("احب الشتاء", "unknown"), ("I love winter", "unknown"),
        ("الصيف حار", "unknown"), ("summer is hot", "unknown"),
        ("العمل متعب", "unknown"), ("work is tiring", "unknown"),
        ("الدراسة مهمة", "unknown"), ("study is important", "unknown"),
        ("الأصدقاء غاليين", "unknown"), ("friends are precious", "unknown"),
        ("العائلة اهم شيء", "unknown"), ("family is most important", "unknown"),
        ("احب النوم", "unknown"), ("I love sleeping", "unknown"),
        ("الاستيقاظ صعب", "unknown"), ("waking up is hard", "unknown"),
        ("التكنولوجيا مذهلة", "unknown"), ("technology is amazing", "unknown"),
        ("الانترنت مفيد", "unknown"), ("internet is useful", "unknown"),
        ("الهاتف ضروري", "unknown"), ("phone is necessary", "unknown"),
        ("التلفاز ممل", "unknown"), ("TV is boring", "unknown"),
        ("الرسم موهبة", "unknown"), ("drawing is a talent", "unknown"),
        ("الغناء جميل", "unknown"), ("singing is beautiful", "unknown"),
        ("الرقص ممتع", "unknown"), ("dancing is fun", "unknown"),
        ("كلام فاضي", "unknown"), ("nonsense talk", "unknown"),
        ("شيء غريب", "unknown"), ("something weird", "unknown"),
        ("لا اعرف", "unknown"), ("I don't know", "unknown"),
        ("ماذا تعني", "unknown"), ("what do you mean", "unknown"),
        ("هذا صعب", "unknown"), ("this is difficult", "unknown"),
        ("انا متعب", "unknown"), ("I am tired", "unknown"),
        ("الحياة صعبة", "unknown"), ("life is hard", "unknown"),
        ("المال مهم", "unknown"), ("money is important", "unknown"),
    ]

    texts = [item[0] for item in training_data]
    labels = [item[1] for item in training_data]

    return texts, labels

def train_intent_classifier():
    """تدريب نموذج تصنيف النوايا"""

    print("📚 إنشاء مجموعة البيانات المتوازنة...")
    texts, labels = create_training_dataset()

    # تحضير البيانات
    df = pd.DataFrame({'text': texts, 'label': labels})

    # طباعة توزيع البيانات
    print("\n📊 توزيع البيانات:")
    label_counts = df['label'].value_counts()
    for label, count in label_counts.items():
        print(f"   {label}: {count} جملة")

    # تشفير التصنيفات
    label_encoder = LabelEncoder()
    df['label_encoded'] = label_encoder.fit_transform(df['label'])

    # حفظ تشفير التصنيفات
    label_mapping = {i: label for i, label in enumerate(label_encoder.classes_)}
    with open('./label_mapping.json', 'w', encoding='utf-8') as f:
        json.dump(label_mapping, f, ensure_ascii=False, indent=2)

    print(f"\n📈 إجمالي العينات: {len(df)}")
    print(f"🏷️ عدد التصنيفات: {len(label_encoder.classes_)}")
    print(f"📋 التصنيفات: {list(label_encoder.classes_)}")

    # تحميل النموذج والتوكنايزر
    print("\n🔄 تحميل mBERT...")
    model_name = "bert-base-multilingual-cased"
    tokenizer = BertTokenizer.from_pretrained(model_name)
    model = BertForSequenceClassification.from_pretrained(
        model_name, 
        num_labels=len(label_encoder.classes_)
    )

    # توكنة البيانات
    print("⚙️ معالجة النصوص...")
    def tokenize_function(examples):
        return tokenizer(
            examples['text'], 
            truncation=True, 
            padding=True, 
            max_length=128
        )

    # إنشاء dataset
    dataset = Dataset.from_pandas(df[['text', 'label_encoded']])
    dataset = dataset.rename_column('label_encoded', 'labels')
    tokenized_dataset = dataset.map(tokenize_function, batched=True)

    # تقسيم البيانات
    train_size = int(0.8 * len(tokenized_dataset))
    train_dataset = tokenized_dataset.select(range(train_size))
    eval_dataset = tokenized_dataset.select(range(train_size, len(tokenized_dataset)))

    print(f"🏋️ بيانات التدريب: {len(train_dataset)} عينة")
    print(f"🧪 بيانات التقييم: {len(eval_dataset)} عينة")

    # إعدادات التدريب محسنة لبيانات متوازنة
    training_args = TrainingArguments(
        output_dir='./fine_tuned_mbert',
        overwrite_output_dir=True,
        num_train_epochs=15,  # زيادة epochs للتعلم العميق المحسن
        per_device_train_batch_size=6,   # تقليل batch size للدقة الأعلى
        per_device_eval_batch_size=6,
        learning_rate=8e-6,  # تقليل learning rate للاستقرار الأمثل
        warmup_steps=200,    # زيادة warmup للاستقرار
        weight_decay=0.03,   # زيادة weight decay
        logging_dir='./logs',
        logging_steps=3,     # تسجيل أكثر تفصيلاً
        eval_steps=50,       # تقييم دوري
        save_steps=100,      # حفظ دوري
        load_best_model_at_end=True,  # تحميل أفضل نموذج
    )

    # Data collator
    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

    # إنشاء Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        tokenizer=tokenizer,
        data_collator=data_collator,
    )

    # بدء التدريب
    print("\n🚀 بدء التدريب المحسن...")
    trainer.train()

    # حفظ النموذج
    print("\n💾 حفظ النموذج...")
    trainer.save_model('./fine_tuned_mbert')
    tokenizer.save_pretrained('./fine_tuned_mbert')

    print("✅ انتهى التدريب بنجاح!")
    print("📁 النموذج محفوظ في: ./fine_tuned_mbert")

    # اختبار شامل ومفصل
    print("\n🧪 اختبار شامل للنموذج:")
    test_cases = [
        # اختبارات التحيات
        ("مرحبا كيف حالك", "greeting"),
        ("أهلاً وسهلاً", "greeting"),
        ("hello there", "greeting"),
        ("صباح الخير", "greeting"),

        # اختبارات الوقت
        ("كم الساعة الآن", "time"),
        ("الوقت الحين", "time"),
        ("what time is it", "time"),

        # اختبارات الطقس
        ("كيف الطقس اليوم", "weather"),
        ("الجو حار", "weather"),
        ("weather today", "weather"),

        # اختبارات المساعدة
        ("ساعدني في شيء", "help"),
        ("أحتاج مساعدة", "help"),
        ("I need help", "help"),

        # اختبارات الوداع
        ("شكراً وداعاً", "goodbye"),
        ("مع السلامة", "goodbye"),
        ("goodbye", "goodbye"),

        # اختبارات معلومات البوت
        ("من أنت", "about"),
        ("ما هذا البرنامج", "about"),
        ("who are you", "about"),

        # اختبارات الطب - المهمة!
        ("بدي دواء للصداع", "medicine"),
        ("عندي صداع شديد", "medicine"),
        ("راسي يوجعني", "medicine"),
        ("أعطيني مسكن للصداع", "medicine"),
        ("headache medicine", "medicine"),
        ("I have a severe headache", "medicine"),
        ("pain relief for headache", "medicine"),
    ]

    from transformers import pipeline
    classifier = pipeline(
        "text-classification",
        model='./fine_tuned_mbert',
        tokenizer='./fine_tuned_mbert'
    )

    print("=" * 60)
    correct_predictions = 0
    total_predictions = len(test_cases)

    for text, expected_intent in test_cases:
        result = classifier(text)
        label_id = int(result[0]['label'].split('_')[-1])
        predicted_intent = label_mapping[label_id]
        confidence = result[0]['score']

        # تحديد الحالة
        status = "✅" if predicted_intent == expected_intent else "❌"
        if predicted_intent == expected_intent:
            correct_predictions += 1

        print(f"{status} '{text}' -> {predicted_intent} ({confidence:.3f}) [Expected: {expected_intent}]")

    accuracy = (correct_predictions / total_predictions) * 100
    print("=" * 60)
    print(f"🎯 دقة النموذج: {accuracy:.1f}% ({correct_predictions}/{total_predictions})")
    print(f"🔥 اختبارات الطب الناجحة:")

    # اختبار مخصص للطب
    medicine_tests = [
        "بدي دواء للصداع",
        "عندي صداع شو آخد", 
        "راسي يوجعني ايش آخذ",
        "أعطيني مسكن للصداع"
    ]

    medicine_correct = 0
    for text in medicine_tests:
        result = classifier(text)
        label_id = int(result[0]['label'].split('_')[-1])
        predicted_intent = label_mapping[label_id]
        confidence = result[0]['score']

        if predicted_intent == "medicine":
            medicine_correct += 1
            print(f"   ✅ '{text}' -> {predicted_intent} ({confidence:.3f})")
        else:
            print(f"   ❌ '{text}' -> {predicted_intent} ({confidence:.3f}) [يجب أن يكون medicine]")

    print(f"\n💊 نجاح تصنيف الطب: {medicine_correct}/{len(medicine_tests)} ({(medicine_correct/len(medicine_tests)*100):.1f}%)")

if __name__ == "__main__":
    train_intent_classifier()