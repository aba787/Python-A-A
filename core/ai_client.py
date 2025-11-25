
import os
import time
import logging
import openai
from typing import Optional
from .search_api import search_web, search_medical, search_general
from .utils import detect_language, is_medical_query

logger = logging.getLogger(__name__)

SYSTEM_GENERAL = """
You are a multilingual assistant with web search capabilities.
If the user writes in Arabic → answer in Arabic.
If the user writes in English → answer in English.
Use the provided web search results to give accurate, up-to-date information.
Always include medical warnings when discussing health topics.
"""

class AIClient:
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if self.api_key:
            openai.api_key = self.api_key
        self.model = model
        self.available = bool(self.api_key)

    def get_response(self, user_input: str, force_language: str = None, max_retries: int = 2, **kwargs) -> str:
        """
        الحصول على إجابة ذكية مع البحث على الويب
        """
        if not self.available:
            return self._fallback_response(user_input, force_language)
        
        # تحديد نوع البحث حسب الموضوع
        if is_medical_query(user_input):
            web_info = search_medical(user_input)
            search_context = "المعلومات الطبية من الويب"
        else:
            web_info = search_general(user_input)
            search_context = "معلومات من الويب"
        
        # تحديد اللغة
        language = detect_language(user_input)
        
        # بناء الرسالة مع نتائج البحث
        if web_info:
            if language == "ar":
                prompt = f"""
السؤال: {user_input}

نتائج البحث من الإنترنت:
{web_info}

بناءً على المعلومات أعلاه من الويب، اكتب إجابة دقيقة ومفيدة.
إذا كانت النتائج ضعيفة، أجب من المعرفة العامة.
إذا كان الموضوع طبي، اذكر تحذيرات السلامة.
"""
            else:
                prompt = f"""
User question: {user_input}

Web search results:
{web_info}

Based on the online information above, write a clean, accurate answer.
If the web results are weak, answer from general knowledge.
Include safety warnings for medical topics.
"""
        else:
            # لا توجد نتائج بحث، استخدم المعرفة العامة
            prompt = user_input
        
        messages = [
            {"role": "system", "content": SYSTEM_GENERAL},
            {"role": "user", "content": prompt}
        ]
        
        for attempt in range(max_retries + 1):
            try:
                client = openai.OpenAI(api_key=self.api_key)
                response = client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=0.3,  # أقل عشوائية للدقة
                    max_tokens=600,   # مساحة أكبر للإجابات المفصلة
                    **kwargs
                )
                
                answer = response.choices[0].message.content
                
                # إضافة إشارة للبحث على الويب
                if web_info:
                    if language == "ar":
                        answer += "\n\n🌐 *تم البحث على الإنترنت لأحدث المعلومات*"
                    else:
                        answer += "\n\n🌐 *Searched the web for latest information*"
                
                return answer
                
            except Exception as e:
                logger.exception("AI request failed attempt %s: %s", attempt, e)
                time.sleep(1 + attempt * 2)
        
        return self._fallback_response(user_input, force_language)

    def _fallback_response(self, user_input: str, force_language: str) -> str:
        """Fallback responses when AI is unavailable"""
        if detect_language(user_input) == "ar":
            return f"عذراً، لا يمكنني الوصول للذكاء الاصطناعي حالياً. سؤالك كان: '{user_input}'. جرب مرة أخرى لاحقاً."
        return f"Sorry, I can't reach the AI right now. Your question was: '{user_input}'. Please try again later."
