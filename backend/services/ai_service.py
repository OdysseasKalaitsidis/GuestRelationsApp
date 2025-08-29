# backend/services/ai_service.py

import os
import openai
from typing import List, Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing OPENAI_API_KEY. Check your .env file.")
    
    # Set the API key for the older openai package
    openai.api_key = api_key
    return openai

def parse_document_with_ai(text: str) -> List[Dict[str, Any]]:
    """
    Use OpenAI to parse document text and extract structured case data.
    This is much more reliable than regex-based parsing.
    """
    client = get_client()
    
    # Create a comprehensive prompt for the AI
    system_prompt = """You are an expert at parsing hotel guest relations reports. 
    Extract all cases from the document and return them as a JSON array.
    
    Each case should have these fields:
    - created: The creation date and time
    - guest: Guest name
    - status: Case status (e.g., CLOSED, OPEN)
    - created_by: Staff member who created the case
    - room: Room number
    - importance: Importance level (e.g., LOW, MEDIUM, HIGH)
    - modified: Last modification date and time
    - modified_by: Staff member who last modified the case
    - source: Source of the case (e.g., Open Greece, Membership)
    - membership: Membership type
    - type: Case type (e.g., NEGATIVE, POSITIVE, NEUTRAL)
    - case_description: Description of the case
    - action: Action taken or required
    - in_out: Check-in/check-out dates
    - title: A descriptive title for the case (use guest name if available)
    
    Return ONLY valid JSON, no other text. If a field is not present, use null."""
    
    user_prompt = f"""Please parse this guest relations report and extract all cases as JSON:

{text}

Return the cases as a JSON array with the exact field names specified above."""

    try:
        response = client.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.1,  # Low temperature for consistent parsing
        )

        # Parse the JSON response
        import json
        result = response.choices[0].message.content.strip()
        
        # Clean up the response - remove markdown code blocks if present
        if result.startswith('```json'):
            result = result[7:]  # Remove ```json
        if result.startswith('```'):
            result = result[3:]   # Remove ```
        if result.endswith('```'):
            result = result[:-3]  # Remove trailing ```
        
        result = result.strip()
        
        # Try to parse the response
        try:
            parsed_result = json.loads(result)
            # Handle both array and object with cases key
            if isinstance(parsed_result, list):
                cases = parsed_result
            elif isinstance(parsed_result, dict) and 'cases' in parsed_result:
                cases = parsed_result['cases']
            else:
                cases = [parsed_result]  # Single case
                
            print(f"AI successfully parsed {len(cases)} cases")
            return cases
            
        except json.JSONDecodeError as e:
            print(f"Failed to parse AI response as JSON: {e}")
            print(f"Raw response: {result}")
            # Fallback to regex parsing
            return []
            
    except Exception as e:
        print(f"AI parsing failed: {e}")
        # Fallback to regex parsing
        return []

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
            response = client.ChatCompletion.create(
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
