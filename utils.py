import string
import random

def generate_short_code(length=6):
    """Generate a random short code."""
    characters = string.ascii_letters + string.digits
    for _ in range(10):  
        code = ''.join(random.choice(characters) for _ in range(length))
        from .models import URL
        if not URL.query.filter_by(short_code=code).first():
            return code
    return None  