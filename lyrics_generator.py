# lyrics_generator.py
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from prompt import get_composer_prompt

class LyricsGenerator:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0.8, # Higher creativity for poetry
            model_name="llama-3.1-8b-instant",
            api_key=os.getenv("GROQ_API_KEY")
        )

    def generate_lyrics(self, mood):
        prompt = ChatPromptTemplate.from_messages([
            ("system", get_composer_prompt),
            ("human", "Generate a {mood} romantic song about longing and love.")
        ])
        
        chain = prompt | self.llm
        try:
            response = chain.invoke({"mood": mood})
            return response.content.strip()
        except Exception as e:
            return f"Error generating lyrics: {str(e)}"