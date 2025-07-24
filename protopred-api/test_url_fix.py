#!/usr/bin/env python3
"""Test URL configuration without requiring requests"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from protopred.constants import BASE_URL

def test_url_configuration():
    """Test that URL is properly configured"""
    print("🔍 Testing URL Configuration")
    print("=" * 40)
    
    print(f"Base URL: {BASE_URL}")
    
    # Check URL format
    if BASE_URL.startswith('https://'):
        print("✅ URL uses HTTPS")
    else:
        print("❌ URL should use HTTPS")
        
    if BASE_URL.endswith('/'):
        print("✅ URL has trailing slash (matches Django pattern)")
    else:
        print("❌ URL missing trailing slash")
        
    if 'API/v2/' in BASE_URL:
        print("✅ URL contains correct API endpoint")
    else:
        print("❌ URL missing correct API endpoint")
        
    # Test URL against known working pattern
    expected_url = "https://protopred.protoqsar.com/API/v2/"
    if BASE_URL == expected_url:
        print("✅ URL matches expected format")
        print("\n🎉 URL configuration is correct!")
        print("\n📋 Next steps:")
        print("   1. Install requests: pip install requests")
        print("   2. Test API call: python3 examples/basic_usage.py")
    else:
        print(f"❌ URL doesn't match expected: {expected_url}")
        
    return BASE_URL == expected_url

if __name__ == "__main__":
    test_url_configuration()