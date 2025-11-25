
import unittest
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from core.medical import basic_medical_response, get_medicine_info
from core.utils import is_medical_query, detect_language

class TestMedicalModule(unittest.TestCase):
    
    def test_paracetamol_english(self):
        response = basic_medical_response("paracetamol information", "en")
        self.assertIn("Paracetamol", response)
        self.assertIn("500-1000", response)
        
    def test_paracetamol_arabic(self):
        response = basic_medical_response("معلومات عن الباراسيتامول", "ar")
        self.assertIn("باراسيتامول", response)
        self.assertIn("500-1000", response)
        
    def test_medical_query_detection(self):
        self.assertTrue(is_medical_query("I have a headache"))
        self.assertTrue(is_medical_query("عندي صداع"))
        self.assertFalse(is_medical_query("What's the weather?"))
        
    def test_medicine_info_retrieval(self):
        info = get_medicine_info("paracetamol", "en")
        self.assertIsNotNone(info)
        self.assertIn("uses", info)
        self.assertIn("dose_adult", info)
        self.assertIn("warnings", info)

if __name__ == '__main__':
    unittest.main()
