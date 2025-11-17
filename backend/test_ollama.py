#!/usr/bin/env python3
"""
Test script to check Ollama connectivity and list available models
"""
import asyncio
import httpx

async def test_ollama():
    """Test connection to Ollama and list models"""
    base_url = "http://localhost:11434"
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            # Test basic connectivity
            print("Testing Ollama connection...")
            response = await client.get(f"{base_url}/api/tags")
            
            if response.status_code == 200:
                print("✅ Ollama is running!")
                data = response.json()
                models = data.get("models", [])
                
                if models:
                    print(f"\n📋 Available models ({len(models)}):")
                    for model in models:
                        name = model.get("name", "Unknown")
                        size = model.get("size", 0)
                        size_mb = round(size / (1024 * 1024), 1) if size else "Unknown"
                        print(f"  • {name} ({size_mb} MB)")
                else:
                    print("\n⚠️  No models found. You may need to pull a model first.")
                    print("   Example: ollama pull llama3.2")
                    
            else:
                print(f"❌ Ollama responded with status {response.status_code}")
                print(f"   Response: {response.text}")
                
        except httpx.ConnectError:
            print("❌ Cannot connect to Ollama at localhost:11434")
            print("   Make sure Ollama is installed and running:")
            print("   • Install: https://ollama.ai")
            print("   • Start: ollama serve")
            
        except Exception as e:
            print(f"❌ Error testing Ollama: {e}")

if __name__ == "__main__":
    asyncio.run(test_ollama())