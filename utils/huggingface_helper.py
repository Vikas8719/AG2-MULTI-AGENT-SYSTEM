"""
Hugging Face Integration for AG2 Multi-Agent System
Provides utilities to use Hugging Face Inference API with AG2 agents
"""

import requests
from typing import Dict, Any, Optional, List
import logging
import time

logger = logging.getLogger(__name__)


class HuggingFaceClient:
    """Client for Hugging Face Inference API"""
    
    def __init__(
        self,
        api_key: str,
        model: str = "mistralai/Mixtral-8x7B-Instruct-v0.1",
        endpoint: Optional[str] = None
    ):
        """
        Initialize Hugging Face client
        
        Args:
            api_key: Hugging Face API key
            model: Model ID from Hugging Face Hub
            endpoint: Custom inference endpoint (optional)
        """
        self.api_key = api_key
        self.model = model
        self.endpoint = endpoint or f"https://api-inference.huggingface.co/models/{model}"
        self.headers = {"Authorization": f"Bearer {api_key}"}
        
        logger.info(f"Initialized HuggingFace client with model: {model}")
    
    def generate(
        self,
        prompt: str,
        max_tokens: int = 4000,
        temperature: float = 0.7,
        top_p: float = 0.9,
        timeout: int = 300,
        retry_count: int = 3
    ) -> Dict[str, Any]:
        """
        Generate text using Hugging Face Inference API
        
        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens to generate  
            temperature: Sampling temperature
            top_p: Top-p sampling
            timeout: Request timeout in seconds
            retry_count: Number of retries on failure
            
        Returns:
            Generated text response
        """
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": max_tokens,
                "temperature": temperature,
                "top_p": top_p,
                "return_full_text": False
            }
        }
        
        for attempt in range(retry_count):
            try:
                logger.info(f"Generating text with HF model: {self.model} (attempt {attempt + 1}/{retry_count})")
                
                response = requests.post(
                    self.endpoint,
                    headers=self.headers,
                    json=payload,
                    timeout=timeout
                )
                
                # Check if model is loading
                if response.status_code == 503:
                    error_data = response.json()
                    if "estimated_time" in error_data:
                        wait_time = error_data["estimated_time"]
                        logger.warning(f"Model is loading, waiting {wait_time} seconds...")
                        time.sleep(wait_time + 5)
                        continue
                
                response.raise_for_status()
                
                result = response.json()
                
                # Handle different response formats
                if isinstance(result, list) and len(result) > 0:
                    generated_text = result[0].get("generated_text", "")
                elif isinstance(result, dict):
                    generated_text = result.get("generated_text", "")
                else:
                    generated_text = str(result)
                
                logger.info("Successfully generated text")
                
                return {
                    "success": True,
                    "text": generated_text,
                    "model": self.model,
                    "provider": "huggingface"
                }
                
            except requests.exceptions.Timeout:
                logger.error(f"Request timeout (attempt {attempt + 1}/{retry_count})")
                if attempt == retry_count - 1:
                    raise
                time.sleep(2 ** attempt)  # Exponential backoff
                
            except requests.exceptions.RequestException as e:
                logger.error(f"Request failed: {str(e)} (attempt {attempt + 1}/{retry_count})")
                if attempt == retry_count - 1:
                    raise
                time.sleep(2 ** attempt)
        
        return {
            "success": False,
            "text": "",
            "error": "Max retries exceeded",
            "provider": "huggingface"
        }
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        max_tokens: int = 4000,
        temperature: float = 0.7,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Chat completion format (converts to prompt format)
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            **kwargs: Additional parameters
            
        Returns:
            Generated response
        """
        # Convert chat messages to prompt format
        prompt = self._format_chat_prompt(messages)
        
        return self.generate(
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            **kwargs
        )
    
    def _format_chat_prompt(self, messages: List[Dict[str, str]]) -> str:
        """
        Format chat messages into a prompt string for Mixtral/Mistral models
        
        Args:
            messages: List of message dicts
            
        Returns:
            Formatted prompt string
        """
        prompt = ""
        
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            
            if role == "system":
                prompt += f"[INST] {content} [/INST]\\n"
            elif role == "user":
                prompt += f"[INST] {content} [/INST]\\n"
            elif role == "assistant":
                prompt += f"{content}\\n"
        
        return prompt


# Recommended HuggingFace Models for AG2
RECOMMENDED_MODELS = {
    "free": [
        "mistralai/Mixtral-8x7B-Instruct-v0.1",  # Best free model
        "mistralai/Mistral-7B-Instruct-v0.2",
        "meta-llama/Llama-2-70b-chat-hf",
        "codellama/CodeLlama-34b-Instruct-hf",  # For code generation
    ],
    "serverless": [
        "microsoft/Phi-3-mini-4k-instruct",  # Fast and efficient
        "HuggingFaceH4/zephyr-7b-beta",
        "google/flan-t5-xxl",
    ],
    "pro": [  # Requires HuggingFace Pro
        "meta-llama/Meta-Llama-3-70B-Instruct",
        "mistralai/Mistral-Large-Instruct-2411",
    ]
}


def get_recommended_model(tier: str = "free") -> str:
    """
    Get recommended model for specific tier
    
    Args:
        tier: Model tier ('free', 'serverless', or 'pro')
        
    Returns:
        Model ID
    """
    models = RECOMMENDED_MODELS.get(tier, RECOMMENDED_MODELS["free"])
    return models[0]  # Return first (best) model


__all__ = ['HuggingFaceClient', 'RECOMMENDED_MODELS', 'get_recommended_model']
