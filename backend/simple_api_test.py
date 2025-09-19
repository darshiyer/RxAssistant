#!/usr/bin/env python3
"""
Simple OpenAI API test to verify the new key works
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

def test_api_key():
    """Simple test of the OpenAI API key"""
    print("🔑 Testing OpenAI API Key...")
    print("=" * 40)
    
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ No API key found in environment")
        return False
    
    print(f"✅ API Key loaded (ends with: ...{api_key[-10:]})")
    
    try:
        # Initialize OpenAI client (simple initialization)
        client = OpenAI(api_key=api_key)
        
        print("📡 Testing API connection...")
        
        # Simple test request
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Say 'API key is working!' in exactly those words."}
            ],
            max_tokens=20
        )
        
        if response and response.choices:
            message = response.choices[0].message.content.strip()
            print(f"✅ API Response: {message}")
            
            if "API key is working!" in message:
                print("🎉 SUCCESS: Your new OpenAI API key is working perfectly!")
                return True
            else:
                print("✅ API key works (got different response but still valid)")
                return True
        else:
            print("❌ No response received")
            return False
            
    except Exception as e:
        print(f"❌ API test failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_api_key()
    if success:
        print("\n🎯 Your API key is ready to use!")
    else:
        print("\n⚠️  Please check your API key configuration.")