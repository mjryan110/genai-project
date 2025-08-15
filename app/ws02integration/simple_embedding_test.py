"""
Simple Embedding Test for CBRE Azure OpenAI
"""

import os
from dotenv import load_dotenv
from openai import AzureOpenAI
from cbre_azureopenai_utils import get_access_token

# Load environment variables
load_dotenv()

def test_embedding():
    # Get token and create client
    token = get_access_token()
    
    client = AzureOpenAI(
        api_key=token,
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
    )
    
    # Test text
    text = "CBRE is a commercial real estate company"
    
    # Try different embedding models
    embedding_models = [
        os.getenv("AZURE_OPENAI_EMBEDDING_MODEL"),
        "text-embedding-ada-002",
        "text-embedding-3-small"
    ]
    
    for model in embedding_models:
        if not model:
            continue
            
        try:
            print(f"Trying model: {model}")
            
            # Get embedding
            response = client.embeddings.create(
                model=model,
                input=text
            )
            
            # Extract embedding vector
            embedding = response.data[0].embedding
            
            print(f"Text: {text}")
            print(f"Model: {model}")
            print(f"Embedding dimensions: {len(embedding)}")
            print(f"First 5 values: {embedding[:5]}")
            print(f"Last 5 values: {embedding[-5:]}")
            return  # Success, exit
            
        except Exception as e:
            print(f"Failed with {model}: {e}")
            continue
    
    print("No embedding models worked")

if __name__ == "__main__":
    test_embedding()
