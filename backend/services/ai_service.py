# backend/services/ai_service.py

import os
from openai import OpenAI
from sqlalchemy.orm import Session
from models import Followup  # import your Followup model
from db import SessionLocal  # your DB session

def get_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing OPENAI_API_KEY. Check your .env file.")
    return OpenAI(api_key=api_key)

def suggest_feedback(cases: list, db: Session = None) -> list:
    """
    Given a list of cases, call ChatGPT and return + persist suggestions.
    Each follow-up will be stored in DB with assigned_to = NULL.
    """
    client = get_client()
    results = []

    if db is None:
        db = SessionLocal()

    for case in cases:
        prompt = (
            f"Case details:\n"
            f"Room: {case.get('room')}\n"
            f"Status: {case.get('status')}\n"
            f"Importance: {case.get('importance')}\n"
            f"Type: {case.get('type')}\n"
            f"Case: {case.get('case')}\n"
            f"Action already taken: {case.get('action')}\n\n"
            f"Please suggest **only one concise sentence** describing the next follow-up action."
        )

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an assistant for guest relations team."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4
        )

        suggestion = response.choices[0].message.content.strip()

        # Persist to DB
        followup = Followup(
            case_id=case.get("id"),   # assuming case already exists in DB
            suggestion_text=suggestion,
            assigned_to=None          # admin will assign later
        )
        db.add(followup)
        db.commit()
        db.refresh(followup)

        results.append({
            **case,
            "suggested_feedback": suggestion,
            "followup_id": followup.id
        })

    return results
