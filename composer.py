import json
import os
import re
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from prompt import get_composer_prompt

class BollywoodComposer:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY is missing. Please check your .env file.")
            
        self.llm = ChatGroq(
            temperature=0.5, # Lowered temperature for more stable JSON
            model_name="llama-3.1-8b-instant",
            api_key=api_key
        )

    def generate_full_song(self, user_input, mood, raga, voice):
        prompt_text = get_composer_prompt(user_input, mood, raga, voice)
        prompt = ChatPromptTemplate.from_template(prompt_text)
        chain = prompt | self.llm
        
        try:
            response = chain.invoke({})
            return self._robust_parse(response.content)
            
        except Exception as e:
            return {"error": f"Critical Failure: {str(e)}"}

    def _robust_parse(self, raw_text):
        """
        Attempts to clean and repair the JSON output from the AI.
        """
        try:
            # 1. Extract JSON block (between first { and last })
            match = re.search(r'\{.*\}', raw_text, re.DOTALL)
            if not match:
                return {"error": "No JSON structure found in AI response."}
            
            json_str = match.group(0)

            # 2. REPAIR: Remove trailing commas (common AI error)
            # Regex finds a comma followed immediately by } or ]
            json_str = re.sub(r',\s*([\]}])', r'\1', json_str)
            
            # 3. REPAIR: Remove comments (// or #)
            json_str = re.sub(r'//.*', '', json_str)
            
            # 4. Attempt Parse
            return json.loads(json_str)

        except json.JSONDecodeError as e:
            # Fallback: Return the raw string for debugging
            print(f"FAILED JSON: {raw_text}") 
            return {
                "error": f"JSON Parsing Failed. Try again. (Details: {str(e)})"
            }