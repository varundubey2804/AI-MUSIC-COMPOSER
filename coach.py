# coach.py
import json
import os
import re
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from prompt import COACH_SYSTEM_PROMPT

class SingingCoach:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY missing")
            
        self.llm = ChatGroq(
            temperature=0.3, # Lower temperature for stricter grading
            model_name="llama-3.1-8b-instant",
            api_key=api_key
        )

    def evaluate_performance(self, raga_name, voice_type, reference_notes, detected_notes, pitch_score):
        prompt = ChatPromptTemplate.from_template(COACH_SYSTEM_PROMPT)
        chain = prompt | self.llm
        
        # Convert numeric pitch score to text context
        accuracy_context = f"{pitch_score}% (Based on Signal Analysis)"
        
        try:
            response = chain.invoke({
                "input_type": "Singing Performance Analysis",
                "raga_name": raga_name,
                "voice_type": voice_type,
                "detected_notes": detected_notes,
                "pitch_accuracy": accuracy_context
            })
            return self._parse_json(response.content)
        except Exception as e:
            return {"error": str(e)}

    def _parse_json(self, raw_text):
        try:
            match = re.search(r'\{.*\}', raw_text, re.DOTALL)
            if match:
                clean_json = match.group(0)
                clean_json = re.sub(r',\s*([\]}])', r'\1', clean_json)
                return json.loads(clean_json)
            return {"error": "Coach output format error"}
        except:
            return {"error": "Parsing failed"}