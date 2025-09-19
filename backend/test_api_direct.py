#!/usr/bin/env python3
"""
Direct API test using requests to bypass OpenAI client issues
"""

import os
import requests
import json
from dotenv import load_dotenv

def test_api_direct():
    """Test OpenAI API directly using requests"""
    print("🔑 Testing OpenAI API Key (Direct HTTP Request)...")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ No API key found in environment")
        return False
    
    print(f"✅ API Key loaded (ends with: ...{api_key[-10:]})")
    
    # Direct API call using requests
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": "Say 'API key is working!' in exactly those words."}
        ],
        "max_tokens": 20
    }
    
    try:
        print("📡 Making direct API request...")
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            message = result['choices'][0]['message']['content'].strip()
            print(f"✅ API Response: {message}")
            print("🎉 SUCCESS: Your OpenAI API key is working perfectly!")
            return True
        else:
            print(f"❌ API request failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Direct API test failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_api_direct()
    if success:
        print("\n🎯 Your API key is ready to use!")
        print("The issue is with the OpenAI Python library, not your key.")
    else:
        print("\n⚠️  Please check your API key.")