import os
import openai
from typing import List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from dotenv import load_dotenv
from services.training_service import load_training_documents

load_dotenv()

# Initialize OpenAI client
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_relevant_documents(query: str, limit: int = 3) -> List[str]:
    """Retrieve relevant documents using TF-IDF similarity from local training folder"""
    try:
        # Load training documents from local folder
        training_docs = load_training_documents()
        
        if not training_docs:
            return []
        
        # Prepare documents for similarity search
        documents = [doc['content'] for doc in training_docs]
        
        # Create TF-IDF vectors
        vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
        doc_vectors = vectorizer.fit_transform(documents)
        query_vector = vectorizer.transform([query])
        
        # Calculate similarities
        similarities = cosine_similarity(query_vector, doc_vectors).flatten()
        
        # Get top similar documents
        top_indices = np.argsort(similarities)[::-1][:limit]
        
        relevant_docs = []
        for idx in top_indices:
            if similarities[idx] > 0.1:  # Minimum similarity threshold
                relevant_docs.append(documents[idx])
        
        return relevant_docs
    
    except Exception as e:
        print(f"Error in document retrieval: {str(e)}")
        return []

def generate_email_response(email_content: str, relevant_docs: List[str]) -> str:
    """Generate email response using OpenAI with RAG context"""
    try:
        # Prepare context from relevant documents
        context = "\n\n".join(relevant_docs[:3])  # Use top 3 most relevant docs
        
        # Create the prompt
        prompt = f"""You are an AI assistant for a hotel guest relations team. You help staff respond to guest emails professionally and effectively.

CONTEXT FROM HOTEL DOCUMENTS:
{context}

GUEST EMAIL TO RESPOND TO:
{email_content}

Please provide a professional, helpful response to this guest email. Use the context from the hotel documents to provide accurate information. Be empathetic, solution-oriented, and maintain the hotel's high service standards.

Response:"""

        # Call OpenAI API
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional hotel guest relations assistant. Provide helpful, accurate, and empathetic responses to guest emails."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        return f"I apologize, but I'm having trouble generating a response right now. Please try again later. Error: {str(e)}"

def process_email_with_rag(email_content: str) -> dict:
    """Main RAG function to process email and generate response"""
    try:
        # Retrieve relevant documents
        relevant_docs = get_relevant_documents(email_content)
        
        # Generate response
        response = generate_email_response(email_content, relevant_docs)
        
        return {
            "response": response,
            "relevant_documents": len(relevant_docs)
        }
    
    except Exception as e:
        return {
            "response": f"I apologize, but I'm having trouble processing your request right now. Please try again later.",
            "relevant_documents": 0,
            "error": str(e)
        }
