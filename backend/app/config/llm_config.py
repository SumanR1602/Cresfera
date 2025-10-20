import google.generativeai as genai
from dotenv import load_dotenv
import os
load_dotenv()
def setup_model():
    """
    Configures the API key and initializes the Generative AI model.
    """
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        model_name = os.getenv("GEMINI_MODEL_NAME", "gemini-pro-latest")
        if not api_key:
            raise ValueError("🛑 Error: GEMINI_API_KEY environment variable not found.")

        # Configure API
        genai.configure(api_key=api_key)

        generation_config = {
            "temperature": 0,
            "top_p": 1,
            "top_k": 1,
        }

        # Initialize model
        model = genai.GenerativeModel(
            model_name=model_name, generation_config=generation_config
        )

        return model

    except Exception as e:
        raise RuntimeError(f"Failed to initialize Gemini model: {e}")