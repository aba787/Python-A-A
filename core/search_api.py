
import requests
from serpapi import GoogleSearch
import os

SERP_API_KEY = "4226c9b6b04b1f624e1330f170b1e0ea04427a997a5c86671b4d7c26889c0fdd"

def search_web(query):
    """البحث على الويب وإرجاع النتائج"""
    try:
        params = {
            "q": query,
            "api_key": SERP_API_KEY,
            "engine": "google",
            "num": 5,  # عدد النتائج
            "safe": "active"  # البحث الآمن
        }

        search = GoogleSearch(params)
        results = search.get_dict()

        snippets = []
        if "organic_results" in results:
            for r in results["organic_results"][:5]:
                if "snippet" in r:
                    snippets.append(f"• {r['snippet']}")

        return "\n".join(snippets) if snippets else ""
    except Exception as e:
        print(f"خطأ في البحث: {e}")
        return ""

def search_medical(query):
    """البحث المتخصص للمواضيع الطبية"""
    medical_query = f"{query} medicine treatment medical information"
    return search_web(medical_query)

def search_general(query):
    """البحث العام للمواضيع غير الطبية"""
    return search_web(query)
