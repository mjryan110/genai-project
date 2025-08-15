"""
Basic CBRE OpenAI Connection Test

Very simple test to verify connection and basic functionality.
"""

import os
from dotenv import load_dotenv
from cbre_azureopenai_utils import get_access_token, get_token_status

# Load environment variables
load_dotenv()

def test_connection():
    """Test basic connection to CBRE OpenAI."""
    
    print("🔍 CBRE OpenAI Basic Connection Test")
    print("=" * 40)
    
    try:
        # Test 1: Check environment variables
        print("1️⃣ Checking environment variables...")
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
        
        if endpoint and deployment:
            print(f"   ✅ Endpoint: {endpoint[:50]}...")
            print(f"   ✅ Deployment: {deployment}")
        else:
            print("   ❌ Missing environment variables")
            return False
        
        # Test 2: Get WSO2 token
        print("\n2️⃣ Testing WSO2 authentication...")
        token = get_access_token()
        print("   ✅ WSO2 token obtained successfully")
        
        # Test 3: Check token status
        print("\n3️⃣ Checking token status...")
        status = get_token_status()
        print(f"   Status: {status['status']}")
        print(f"   Minutes remaining: {status['minutes_remaining']}")
        
        # Test 4: Simple OpenAI call
        print("\n4️⃣ Testing basic OpenAI call...")
        from openai import AzureOpenAI
        
        client = AzureOpenAI(
            api_key=token,
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
            azure_endpoint=endpoint
        )
        
        response = client.chat.completions.create(
            model=deployment,
            messages=[{"role": "user", "content": "Say hello in one word"}],
            max_tokens=10,
            temperature=0.0
        )
        
        print(f"   ✅ AI Response: {response.choices[0].message.content}")
        
        print("\n🎉 All basic tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_connection()
    if success:
        print("\n✅ Connection test successful! Ready for function calling.")
    else:
        print("\n❌ Connection test failed. Check configuration.")
