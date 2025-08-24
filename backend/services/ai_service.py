# backend/services/ai_service.py

import os
from openai import OpenAI
from typing import List, Dict, Any

def get_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing OPENAI_API_KEY. Check your .env file.")
    return OpenAI(api_key=api_key)

def suggest_feedback(cases: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Given a list of cases, call ChatGPT and return AI suggestions.
    Returns structured feedback that can be used to create followups.
    """
    client = get_client()
    results = []

    for case in cases:
        prompt = (
            f"Case details:\n"
            f"Room: {case.get('room', 'N/A')}\n"
            f"Status: {case.get('status', 'N/A')}\n"
            f"Importance: {case.get('importance', 'N/A')}\n"
            f"Type: {case.get('type', 'N/A')}\n"
            f"Title: {case.get('title', case.get('case', 'N/A'))}\n"
            f"Action already taken: {case.get('action', 'N/A')}\n\n"
            f"Please suggest **only one concise sentence** describing the next follow-up action."
        )

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an assistant for guest relations team. Provide clear, actionable follow-up suggestions."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4
            )

            suggestion = response.choices[0].message.content.strip()
            
            results.append({
                "case_id": len(results),  # temporary ID for matching
                "suggestion_text": suggestion,
                "confidence": 0.85,  # placeholder confidence score
                "case_data": case
            })
            
        except Exception as e:
            # Fallback suggestion if AI fails
            results.append({
                "case_id": len(results),
                "suggestion_text": "Please review this case and determine appropriate follow-up action.",
                "confidence": 0.0,
                "case_data": case,
                "error": str(e)
            })

    return results
