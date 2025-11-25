
from .ai_client import AIClient
from .medical import basic_medical_response
from .utils import detect_language, wants_english, wants_arabic, get_current_time, is_medical_query
import random

class ChatResponder:
    def __init__(self):
        self.ai_client = AIClient()
    
    def get_response(self, text: str) -> str:
        """Simple method that always returns text response"""
        try:
            result = self.find_response(text)
            if isinstance(result, dict):
                reply = result.get('response', '⚠️ لم أتمكن من معالجة طلبك.')
            else:
                reply = str(result) if result else '⚠️ لم أتمكن من معالجة طلبك.'
            
            return reply if reply else '⚠️ لم أتمكن من معالجة طلبك.'
        except Exception as e:
            return "⚠️ حدث خطأ أثناء المعالجة."
    
    def find_response(self, user_input: str) -> dict:
        """Main response logic with proper language handling"""
        user_input = user_input.strip()
        
        # Determine preferred language
        force_language = self._determine_language(user_input)
        
        # Handle time queries
        if self._is_time_query(user_input):
            return self._handle_time_query(user_input, force_language)
        
        # Handle greetings
        if self._is_greeting(user_input):
            return self._handle_greeting(user_input, force_language)
        
        # Handle medical queries
        if is_medical_query(user_input):
            return self._handle_medical_query(user_input, force_language)
        
        # Handle general queries with AI
        return self._handle_general_query(user_input, force_language)
    
    def _determine_language(self, user_input: str) -> str:
        """Determine which language to respond in"""
        if wants_english(user_input):
            return "en"
        elif wants_arabic(user_input):
            return "ar"
        else:
            # Use natural language detection
            detected = detect_language(user_input)
            return detected
    
    def _is_time_query(self, user_input: str) -> bool:
        """Check if query is asking for time"""
        time_keywords = [
            "what time", "current time", "time now",
            "كم الساعة", "الوقت الآن", "وش الوقت"
        ]
        return any(keyword in user_input.lower() for keyword in time_keywords)
    
    def _is_greeting(self, user_input: str) -> bool:
        """Check if input is a greeting"""
        greetings = [
            "hello", "hi", "hey", "good morning", "good evening",
            "مرحبا", "اهلا", "السلام عليكم", "صباح الخير", "مساء الخير"
        ]
        return any(greeting in user_input.lower() for greeting in greetings)
    
    def _handle_time_query(self, user_input: str, language: str) -> dict:
        """Handle time-related queries"""
        current_time = get_current_time()
        
        if language == "ar":
            response = f"⏰ الوقت الحالي: {current_time}"
        else:
            response = f"⏰ Current time: {current_time}"
        
        return {
            "response": response,
            "type": "time_query",
            "confidence": 95,
            "language": language
        }
    
    def _handle_greeting(self, user_input: str, language: str) -> dict:
        """Handle greeting messages"""
        if language == "ar":
            responses = [
                "🌟 أهلاً وسهلاً! كيف يمكنني مساعدتك؟",
                "✨ مرحباً بك! أنا هنا لمساعدتك",
                "🚀 وعليكم السلام ورحمة الله، كيف أخدمك؟"
            ]
        else:
            responses = [
                "🌟 Hello! How can I help you today?",
                "✨ Hi there! I'm here to assist you",
                "🚀 Greetings! What can I do for you?"
            ]
        
        return {
            "response": random.choice(responses),
            "type": "greeting",
            "confidence": 90,
            "language": language
        }
    
    def _handle_medical_query(self, user_input: str, language: str) -> dict:
        """Handle medical queries"""
        # Start with basic medical response
        basic_response = basic_medical_response(user_input, language)
        
        # If AI is available, enhance the response
        if self.ai_client.available:
            try:
                prompt = f"Enhance this medical information response, keep it concise and include safety disclaimers: {basic_response}"
                enhanced = self.ai_client.get_response(prompt, force_language=language)
                response = enhanced
            except Exception:
                response = basic_response
        else:
            response = basic_response
        
        return {
            "response": response,
            "type": "medical_query",
            "confidence": 85,
            "language": language
        }
    
    def _handle_general_query(self, user_input: str, language: str) -> dict:
        """Handle general queries with AI + Web Search"""
        try:
            response = self.ai_client.get_response(user_input)
            confidence = 90  # ثقة أعلى مع البحث على الويب
        except Exception as e:
            # Fallback response
            if language == "ar":
                response = f"عذراً، لا أستطيع الإجابة على سؤالك حالياً: '{user_input}'. جرب مرة أخرى أو اطرح سؤالاً مختلفاً."
            else:
                response = f"Sorry, I can't answer your question right now: '{user_input}'. Please try again or ask something else."
            confidence = 30
        
        return {
            "response": response,
            "type": "general_query",
            "confidence": confidence,
            "language": language
        }
