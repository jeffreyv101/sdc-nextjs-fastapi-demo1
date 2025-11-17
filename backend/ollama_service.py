import httpx
import asyncio
from typing import Optional

class OllamaService:
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def generate_response(self, message: str, model: str = "gemma3:12b") -> Optional[str]:
        """
        Generate a response using Ollama
        
        Args:
            message: The user's message
            model: The Ollama model to use (default: llama3.2)
            
        Returns:
            The AI's response or None if there was an error
        """
        try:
            # Ollama API endpoint for generate
            url = f"{self.base_url}/api/generate"
            
            # Prepare the request payload
            payload = {
                "model": model,
                "prompt": message,
                "stream": False  # We want a complete response, not streaming
            }
            
            # Make the request to Ollama
            response = await self.client.post(url, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "Sorry, I couldn't generate a response.")
            else:
                print(f"Ollama API error: {response.status_code} - {response.text}")
                return None
                
        except httpx.ConnectError:
            print("Error: Could not connect to Ollama. Make sure Ollama is running on localhost:11434")
            return None
        except Exception as e:
            print(f"Error communicating with Ollama: {e}")
            return None
    
    async def list_models(self) -> list:
        """
        Get list of available models from Ollama
        
        Returns:
            List of available models
        """
        try:
            url = f"{self.base_url}/api/tags"
            response = await self.client.get(url)
            
            if response.status_code == 200:
                result = response.json()
                return [model["name"] for model in result.get("models", [])]
            else:
                print(f"Error fetching models: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"Error fetching models: {e}")
            return []
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()

# Global instance
ollama_service = OllamaService()