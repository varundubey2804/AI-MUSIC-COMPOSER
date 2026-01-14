# melody_generator.py
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from prompt import get_composer_prompt

class MelodyGenerator:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0.6, # Lower temp for consistent music syntax
            model_name="llama-3.1-8b-instant",
            api_key=os.getenv("GROQ_API_KEY")
        )

    def generate_melody_notes(self, lyrics_snippet):
        """Generates notes for the Mukhda (first few lines)"""
        prompt = ChatPromptTemplate.from_messages([
            ("system", get_composer_prompt),
            ("human", "Here are the lyrics:\n{lyrics}\n\nCompose a melody (approx 30-50 notes).")
        ])
        
        chain = prompt | self.llm
        try:
            response = chain.invoke({"lyrics": lyrics_snippet})
            return response.content.strip()
        except Exception as e:
            print(f"Melody Gen Error: {e}")
            return "C4 E4 G4" # Fallback