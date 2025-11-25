
"""
مولد بيانات متوازنة لتحسين أداء تصنيف النوايا
Balanced Dataset Generator for Better Intent Classification
"""

def generate_balanced_training_data():
    """إنشاء مجموعة بيانات متوازنة بـ 60 جملة لكل نية"""
    
    balanced_data = [
        # التحيات - 60 جملة
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
        ("سلام عليكم ورحمة الله", "greeting"), ("صبحكم الله بالخير", "greeting"), 
        ("مساكم الله بالخير", "greeting"), ("السلام عليكم جميعاً", "greeting"),
        ("أسعد الله أوقاتكم", "greeting"), ("حياكم الله", "greeting"),
        
        # المساعدة - 60 جملة
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
        ("كيف اقدر اسألك", "help"), ("وش الاسئلة المسموحة", "help"), ("ايش الموضوعات اللي تعرفها", "help"),
        ("كيف اخليك تفهمني", "help"), ("وش اللغات اللي تفهمها", "help"), ("ممكن تعلمني كيف اشتغل معك", "help"),
        ("ابي اعرف كيف استخدمك صح", "help"), ("علمني كيف اتكلم معك", "help"), ("ايش افضل طريقة اسألك فيها", "help"),
        
        # معلومات عن البوت - 60 جملة
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
        ("ايش نوعك", "about"), ("وش فئتك", "about"), ("ايش تخصصك", "about"),
        ("قولي عن نفسك", "about"), ("ايش حدودك", "about"), ("وش قدراتك الحقيقية", "about"),
        ("من اللي خلاك", "about"), ("ايش الهدف منك", "about"), ("ليش تم تطويرك", "about"),
        ("وش الغرض من وجودك", "about"), ("ايش مجالك", "about"), ("في ايش تتخصص", "about"),
        
        # الأدوية والطب - 60 جملة متوازنة
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
        ("I have a headache", "medicine"), ("headache medicine", "medicine"),
        ("pain relief", "medicine"), ("give me something for headache", "medicine"),
        ("my head hurts", "medicine"), ("severe headache", "medicine"),
        ("migraine treatment", "medicine"), ("headache remedy", "medicine"),
        ("عندي زكام", "medicine"), ("بدي دواء للزكام", "medicine"),
        ("علاج البرد", "medicine"), ("عندي برد شديد", "medicine"),
        ("انفي مسدود", "medicine"), ("مزكوم", "medicine"),
        ("عندي انفلونزا", "medicine"), ("علاج الانفلونزا", "medicine"),
        ("cold medicine", "medicine"), ("flu treatment", "medicine"),
        ("عندي حمى", "medicine"), ("درجة حرارتي عالية", "medicine"),
        ("عندي سخونة", "medicine"), ("fever medicine", "medicine"),
        ("خافض حرارة", "medicine"), ("دواء الحرارة", "medicine"),
        ("عندي سعال", "medicine"), ("كحة شديدة", "medicine"),
        ("cough medicine", "medicine"), ("شراب للسعال", "medicine"),
        ("عندي التهاب حلق", "medicine"), ("حلقي يوجعني", "medicine"),
        ("sore throat", "medicine"), ("throat infection", "medicine"),
        ("عندي ألم في البطن", "medicine"), ("وجع معدة", "medicine"),
        ("stomach pain", "medicine"), ("معدتي تؤلمني", "medicine"),
        
        # الوقت - 30 جملة
        ("كم الساعة", "time"), ("الوقت الآن", "time"), ("وش الوقت", "time"),
        ("كم الوقت", "time"), ("اي ساعة الحين", "time"), ("الساعة كم", "time"),
        ("وقت اللي الان", "time"), ("قول لي الوقت", "time"), ("ابي اعرف الوقت", "time"),
        ("الوقت كم الحين", "time"), ("كم الساعة الحين", "time"), ("الوقت بالضبط", "time"),
        ("what time is it", "time"), ("current time", "time"), ("time now", "time"),
        ("what's the time", "time"), ("tell me the time", "time"), ("time please", "time"),
        ("كم الساعة بالضبط", "time"), ("الوقت الحالي", "time"), ("التوقيت الآن", "time"),
        ("وش الساعة الحين", "time"), ("كم صار الوقت", "time"), ("الساعة كام", "time"),
        ("what time is it now", "time"), ("current local time", "time"), ("the time", "time"),
        ("ايش الوقت الحين", "time"), ("كم بقى من اليوم", "time"), ("وقت كم", "time"),
        ("check time", "time"), ("time check", "time"),
        
        # الطقس - 30 جملة
        ("كيف الطقس", "weather"), ("الجو", "weather"), ("درجة الحرارة", "weather"),
        ("المطر", "weather"), ("الشمس", "weather"), ("البرد", "weather"),
        ("الحر", "weather"), ("طقس اليوم", "weather"), ("الجو كيف", "weather"),
        ("الطقس ايش", "weather"), ("هل فيه مطر", "weather"), ("الجو بارد", "weather"),
        ("الجو حار", "weather"), ("درجة الحرارة كم", "weather"), ("الطقس برا", "weather"),
        ("الجو اليوم", "weather"), ("هل بيمطر", "weather"), ("الحالة الجوية", "weather"),
        ("weather", "weather"), ("temperature", "weather"), ("how's the weather", "weather"),
        ("rain", "weather"), ("sunny", "weather"), ("cold", "weather"), ("hot", "weather"),
        ("weather today", "weather"), ("weather forecast", "weather"),
        ("الجو شلون", "weather"), ("كيف حالة الطقس", "weather"), ("الطقس كيف اليوم", "weather"),
        
        # الوداع - 30 جملة
        ("وداعاً", "goodbye"), ("باي", "goodbye"), ("مع السلامة", "goodbye"),
        ("شكراً", "goodbye"), ("تصبح على خير", "goodbye"), ("سلامة", "goodbye"),
        ("الله يعطيك العافية", "goodbye"), ("تسلم", "goodbye"), ("باي باي", "goodbye"),
        ("وداعا", "goodbye"), ("مع السلامة والعافية", "goodbye"), ("الله يوفقك", "goodbye"),
        ("شكرا لك", "goodbye"), ("اشكرك", "goodbye"), ("تسلم ايديك", "goodbye"),
        ("goodbye", "goodbye"), ("bye", "goodbye"), ("see you", "goodbye"),
        ("thank you", "goodbye"), ("thanks", "goodbye"), ("good night", "goodbye"),
        ("تشكرات", "goodbye"), ("يعطيك العافية", "goodbye"), ("الله يسعدك", "goodbye"),
        ("see you later", "goodbye"), ("catch you later", "goodbye"), ("take care", "goodbye"),
        ("farewell", "goodbye"), ("until next time", "goodbye"), ("bye for now", "goodbye"),
        
        # أسئلة غير معروفة - 30 جملة
        ("ما رأيك في الطعام", "unknown"), ("أحب اللون الأزرق", "unknown"),
        ("الرياضة مفيدة", "unknown"), ("كم عمرك", "unknown"),
        ("وين تسكن", "unknown"), ("هل تحب السفر", "unknown"),
        ("ايش لونك المفضل", "unknown"), ("كيف كان يومك", "unknown"),
        ("احب الموسيقى", "unknown"), ("الكتب مفيدة", "unknown"),
        ("what do you think about food", "unknown"), ("I like blue", "unknown"),
        ("sports are good", "unknown"), ("how old are you", "unknown"),
        ("where do you live", "unknown"), ("do you like traveling", "unknown"),
        ("كلام فاضي", "unknown"), ("شيء غريب", "unknown"), ("لا اعرف", "unknown"),
        ("هذا صعب", "unknown"), ("انا متعب", "unknown"), ("الحياة صعبة", "unknown"),
        ("nonsense", "unknown"), ("something weird", "unknown"), ("I don't know", "unknown"),
        ("this is hard", "unknown"), ("I am tired", "unknown"), ("life is difficult", "unknown"),
        ("random question", "unknown"), ("strange query", "unknown"), ("unclear request", "unknown")
    ]
    
    return balanced_data

if __name__ == "__main__":
    data = generate_balanced_training_data()
    print(f"✅ تم إنشاء {len(data)} جملة متوازنة")
    
    # عد الجمل لكل نية
    from collections import Counter
    intent_counts = Counter([item[1] for item in data])
    print("\n📊 توزيع البيانات المتوازن:")
    for intent, count in intent_counts.items():
        print(f"   {intent}: {count} جملة")
