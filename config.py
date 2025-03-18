import os
from dotenv import load_dotenv
import google.generativeai as genai  # Import Gemini API

def load_config():
    """Load environment variables and configure the API"""
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        raise ValueError("GOOGLE_API_KEY is missing. Please set it in your .env file.")
    
    genai.configure(api_key=api_key)  # Ensure the API key is set globally
    
    return {
        "GOOGLE_API_KEY": api_key,
        "DEFAULT_MODEL": "gemini-1.5-pro",
        "TEMPLATE_PATH": "template.txt",
    }
