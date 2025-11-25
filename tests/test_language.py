
import unittest
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from core.utils import detect_language, wants_english, wants_arabic

class TestLanguageDetection(unittest.TestCase):
    
    def test_arabic_detection(self):
        self.assertEqual(detect_language("مرحبا كيف حالك"), "ar")
        self.assertEqual(detect_language("معلومات عن الدواء"), "ar")
        
    def test_english_detection(self):
        self.assertEqual(detect_language("Hello how are you"), "en")
        self.assertEqual(detect_language("Medicine information"), "en")
        
    def test_english_preference(self):
        self.assertTrue(wants_english("Please respond in English"))
        self.assertTrue(wants_english("اجب بالانجليزي"))
        self.assertFalse(wants_english("مرحبا"))
        
    def test_arabic_preference(self):
        self.assertTrue(wants_arabic("اجب بالعربي"))
        self.assertTrue(wants_arabic("respond in Arabic"))
        self.assertFalse(wants_arabic("Hello"))

if __name__ == '__main__':
    unittest.main()
