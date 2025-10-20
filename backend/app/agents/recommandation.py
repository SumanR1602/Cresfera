import json
import re
import logging
import google.generativeai as genai
from app.config.llm_config import setup_model

logger = logging.getLogger(__name__)

# --- Utility Functions ---

def _clean_llm_response(response_text: str) -> str:
    """Clean typical Gemini response artifacts."""
    cleaned = (
        response_text.strip()
        .replace("```json", "")
        .replace("```", "")
        .replace("'", '"')
        .replace("None", "null")
        .replace("True", "true")
        .replace("False", "false")
    )
    return cleaned

def _validate_cleaned_response(cleaned_text: str) -> bool:
    """Ensure no unsafe or code-like patterns are present."""
    if re.search(r"\*\*|\s*\(", cleaned_text):
        logger.error("🛑 Unsafe expression detected in AI response (e.g., '**' or '(').")
        return False
    return True

def _attempt_json_repair(text: str):
    """Try to extract and parse a JSON object from slightly malformed text."""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        json_match = re.search(r"\{.*\}", text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(0))
            except Exception:
                pass
    return None


# --- Main Function ---

def generate_investment_recommendation(amount: float, tenure: int, risk_profile: str) -> dict:
    prompt = f"""
    You are a financial advisor AI.
    Generate an investment portfolio recommendation STRICTLY in valid JSON. Do NOT include any text, explanation, or markdown outside the JSON.
    Context: Provide an allocation suitable for the following inputs, assuming standard current market conditions.

    Input:
    - Investment amount: ₹{amount}
    - Investment tenure: {tenure} years
    - Risk profile: {risk_profile} (e.g., Low, Moderate, High)

    Output (strict JSON only):
    {{
        "recommendation_summary": "Short explanation of portfolio strategy and risk management.",
        "funds": [
        {{
        "name": "Fund or Asset name",
        "type": "Stocks/Fds/Equity/Bond/ETF/ChitFund",
        "allocation": "allocation_percentage",
        "risk_level": "Low/Moderate/High",
        "historical_return": "X% CAGR over the last 5 years",
        "expense_ratio": "X%",
        "provider": "Company/Manager name (optional)"
        }}
        // Additional funds/assets as needed
        ]
    }}
    """

    try:
        model = setup_model() 
        response = model.generate_content(prompt)
        logger.info("✅ Prompt sent to Gemini for portfolio recommendation.")

        # --- Safely extract raw text ---
        raw_response = getattr(response, "text", None)
        if not raw_response and hasattr(response, "candidates"):
            parts = response.candidates[0].content.parts
            raw_response = parts[0].text if parts else None

        if not raw_response:
            logger.warning("⚠️ Empty or blocked Gemini response.")
            return None

        # --- Clean + validate ---
        cleaned_json = _clean_llm_response(raw_response)
        if not _validate_cleaned_response(cleaned_json):
            logger.error("🛑 Invalid content detected in LLM response.")
            logger.debug(f"Invalid Output:\n{cleaned_json}")
            return None

        # --- Parse JSON safely ---
        result = _attempt_json_repair(cleaned_json)
        if not result:
            logger.error("🛑 JSON parsing failed after repair attempt.")
            logger.debug(f"Malformed Gemini Output:\n{cleaned_json}")
            return None

        logger.info(f"✅ Successfully parsed investment recommendation JSON.{result}")
        return result

    except Exception as e:
        logger.error(f"🛑 Gemini content generation failed: {e}", exc_info=True)
        return None
