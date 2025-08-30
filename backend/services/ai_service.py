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
    
    # Use the new OpenAI client format
    from openai import OpenAI
    return OpenAI(api_key=api_key)

def check_openai_available():
    """Check if OpenAI API is available and configured"""
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return False, "OpenAI API key not configured"
        return True, "OpenAI API available"
    except Exception as e:
        return False, f"OpenAI API error: {str(e)}"

def parse_document_with_ai(text: str) -> List[Dict[str, Any]]:
    """
    Optimized AI parsing with faster model and better error handling.
    """
    client = get_client()
    
    # Simplified prompt for faster processing
    system_prompt = """Extract hotel guest cases from this document. Return as JSON array with fields:
    guest, room, status, importance, type, title, case_description, action, created, created_by, modified, modified_by, source, membership, in_out
    Use null for missing fields. Return only valid JSON."""
    
    user_prompt = f"Parse this guest relations report:\n\n{text}"

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Fastest model
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0,  # No randomness for speed
            max_tokens=4000,  # Limit for faster response
        )

        # Fast JSON parsing
        import json
        result = response.choices[0].message.content.strip()
        
        # Quick cleanup
        if result.startswith('```'):
            result = result.split('```')[1]
        if result.startswith('json'):
            result = result[4:]
        
        result = result.strip()
        
        # Parse JSON
        try:
            parsed_result = json.loads(result)
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
            # Try to extract any valid JSON from the response
            try:
                # Look for JSON array or object in the response
                import re
                json_match = re.search(r'\[.*\]|\{.*\}', result, re.DOTALL)
                if json_match:
                    parsed_result = json.loads(json_match.group())
                    if isinstance(parsed_result, list):
                        cases = parsed_result
                    elif isinstance(parsed_result, dict) and 'cases' in parsed_result:
                        cases = parsed_result['cases']
                    else:
                        cases = [parsed_result]
                    print(f"AI successfully parsed {len(cases)} cases from partial JSON")
                    return cases
            except:
                pass
            # Fallback to regex parsing
            return []
            
    except Exception as e:
        print(f"AI parsing failed: {e}")
        print(f"Error type: {type(e).__name__}")
        # Fallback to regex parsing
        return []

def suggest_feedback(cases: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Given a list of cases, call ChatGPT and return AI suggestions.
    Returns structured feedback that can be used to create followups.
    """
    client = get_client()
    results = []

    print(f"Generating AI suggestions for {len(cases)} cases...")

    for i, case in enumerate(cases):
        print(f"Processing case {i+1}/{len(cases)}: {case.get('title', 'Untitled')}")
        
        # Create a more detailed prompt for better suggestions
        prompt = (
            f"Case details:\n"
            f"Room: {case.get('room', 'N/A')}\n"
            f"Status: {case.get('status', 'N/A')}\n"
            f"Importance: {case.get('importance', 'N/A')}\n"
            f"Type: {case.get('type', 'N/A')}\n"
            f"Title: {case.get('title', case.get('case', 'N/A'))}\n"
            f"Case Description: {case.get('case_description', 'N/A')}\n"
            f"Action already taken: {case.get('action', 'N/A')}\n\n"
            f"Based on this case information, please suggest **only one concise sentence** describing the next follow-up action that should be taken by the guest relations team."
        )

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert guest relations manager. Provide clear, actionable, and specific follow-up suggestions. Focus on practical next steps that would improve guest satisfaction or resolve issues."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,  # Lower temperature for more consistent suggestions
                max_tokens=100    # Limit response length
            )

            suggestion = response.choices[0].message.content.strip()
            
            # Clean up the suggestion
            if suggestion.startswith('"') and suggestion.endswith('"'):
                suggestion = suggestion[1:-1]
            
            print(f"Generated suggestion: {suggestion}")
            
            results.append({
                "case_id": i,  # Use index for better matching
                "suggestion_text": suggestion,
                "confidence": 0.85,
                "case_data": case
            })
            
        except Exception as e:
            print(f"Error generating suggestion for case {i+1}: {e}")
            # Fallback suggestion if AI fails
            fallback_suggestion = "Please review this case and determine appropriate follow-up action."
            results.append({
                "case_id": i,
                "suggestion_text": fallback_suggestion,
                "confidence": 0.0,
                "case_data": case,
                "error": str(e)
            })

    print(f"Successfully generated {len(results)} AI suggestions")
    return results
