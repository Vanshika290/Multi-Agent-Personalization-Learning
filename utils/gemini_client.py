"""Unified Gemini API client supporting both google-genai and google-generativeai SDKs.
Includes graceful error handling, fallback demo responses, and clear diagnostics.
"""

import os
from typing import Optional, Dict, Any

class GeminiClient:
    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-2.5-flash"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "").strip()
        self.model_name = model_name
        self._client_type = None
        self._init_client()

    def _init_client(self):
        """Initialize the SDK client based on available packages."""
        if not self.api_key:
            return

        # Attempt 1: New google-genai SDK
        try:
            from google import genai
            self.genai_client = genai.Client(api_key=self.api_key)
            self._client_type = "genai"
            return
        except Exception:
            pass

        # Attempt 2: Classic google-generativeai SDK
        try:
            import google.generativeai as genai_classic
            genai_classic.configure(api_key=self.api_key)
            self.genai_classic = genai_classic
            self._client_type = "generativeai"
            return
        except Exception:
            pass

    def is_configured(self) -> bool:
        """Check if an API key is provided and client is initialized."""
        return bool(self.api_key and len(self.api_key) > 5)

    def generate(self, prompt: str, system_instruction: Optional[str] = None) -> str:
        """
        Generate response from Gemini model.
        Returns generated text or helpful instructions if API key is missing.
        """
        if not self.is_configured():
            return (
                "⚠️ **Gemini API Key Required**\n\n"
                "Please enter your Google Gemini API Key in the left sidebar or add it to `.env` file (`GEMINI_API_KEY=...`).\n\n"
                "👉 Get a free API key at [Google AI Studio](https://aistudio.google.com/)."
            )

        try:
            if self._client_type == "genai":
                config = {}
                if system_instruction:
                    config["system_instruction"] = system_instruction
                
                # Check model name fallback
                target_model = self.model_name
                response = self.genai_client.models.generate_content(
                    model=target_model,
                    contents=prompt,
                    config=config if config else None
                )
                return response.text

            elif self._client_type == "generativeai":
                # Using classic SDK
                # Map model name if needed
                target_model = self.model_name
                if "gemini-2.5" in target_model:
                    # Classic SDK often maps to gemini-1.5-flash or gemini-1.5-pro
                    target_model = "gemini-1.5-flash"

                model = self.genai_classic.GenerativeModel(
                    model_name=target_model,
                    system_instruction=system_instruction
                )
                response = model.generate_content(prompt)
                return response.text

            else:
                # Re-try init
                self._init_client()
                if self._client_type:
                    return self.generate(prompt, system_instruction)
                return "⚠️ Unable to load Gemini client. Please check `requirements.txt` installation."

        except Exception as e:
            err_msg = str(e)
            if "API_KEY_INVALID" in err_msg or "400" in err_msg and "key" in err_msg.lower():
                return "❌ **Invalid Gemini API Key**: The provided API key was rejected. Please verify the key at [Google AI Studio](https://aistudio.google.com/)."
            elif "429" in err_msg or "RESOURCE_EXHAUSTED" in err_msg:
                return "⏳ **Rate Limit Exceeded**: Gemini API free tier rate limit was reached. Please wait a few seconds and try again."
            else:
                return f"❌ **Gemini API Error**: {err_msg}"
