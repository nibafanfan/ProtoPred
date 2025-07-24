import sys
sys.path.insert(0, '.')
from protopred.constants import BASE_URL
print(f"BASE_URL from constants: {BASE_URL}")

# Test the URL transformation
base_url = BASE_URL.rstrip('/')
print(f"After rstrip('/'): {base_url}")
