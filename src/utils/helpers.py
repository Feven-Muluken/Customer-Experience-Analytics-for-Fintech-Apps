# Optional helper functions
import re

def clean_text(text):
    """
    Basic text cleaning:
    - Remove special characters
    - Convert to lowercase
    """
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return text
