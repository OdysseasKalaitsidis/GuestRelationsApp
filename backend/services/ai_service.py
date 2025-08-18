import os
from openai import OpenAI

def get_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing OPENAI_API_KEY. Check your .env file.")
    return OpenAI(api_key=api_key)

def suggest_feedback(cases: list) -> list:
    client = get_client()
    """
    Given a list of cases, call ChatGPT and return list of cases with single-sentence suggestions.
    """
    results = []

    for case in cases:
        prompt = (
            f"Case details:\n"
            f"Room: {case.get('room')}\n"
            f"Status: {case.get('status')}\n"
            f"Importance: {case.get('importance')}\n"
            f"Type: {case.get('type')}\n"
            f"Case: {case.get('case')}\n"
            f"Action already taken: {case.get('action')}\n\n"
            f"Please suggest **only one concise sentence** describing the next follow-up action for the guest relations team."
        )

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an assistant for Domes of Corfu guest relations team."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4
        )

        suggestion = response.choices[0].message.content.strip()

        results.append({
            **case,
            "suggested_feedback": suggestion
        })

    return results
