# import re

# def parse_query(query: str):
#     return {
#         "age": int(re.search(r'(\d+)[ -]?year', query).group(1)) if re.search(r'(\d+)[ -]?year', query) else None,
#         "procedure": re.search(r'(\w+\s+surgery)', query).group(1) if re.search(r'(\w+\s+surgery)', query) else None,
#         "location": re.search(r'in\s([A-Za-z]+)', query).group(1) if re.search(r'in\s([A-Za-z]+)', query) else None,
#         "policy_duration": int(re.search(r'(\d+)[ -]?month', query).group(1)) if re.search(r'(\d+)[ -]?month', query) else None,
#         "gender": "male" if "male" in query.lower() else "female"
#     }

import re
import os
import json
import google.generativeai as genai

# configure Gemini only if API key is available
use_llm = os.getenv("GEMINI_API_KEY") is not None
if use_llm:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel("gemini-pro")

def parse_query_with_regex(query: str):
    return {
        "age": int(re.search(r'(\d+)[ -]?year', query).group(1)) if re.search(r'(\d+)[ -]?year', query) else None,
        "procedure": re.search(r'(\w+\s+surgery)', query).group(1) if re.search(r'(\w+\s+surgery)', query) else None,
        "location": re.search(r'in\s([A-Za-z]+)', query).group(1) if re.search(r'in\s([A-Za-z]+)', query) else None,
        "policy_duration": int(re.search(r'(\d+)[ -]?month', query).group(1)) if re.search(r'(\d+)[ -]?month', query) else None,
        "gender": "male" if "male" in query.lower() else "female"
    }

def parse_query(query: str):
    if use_llm:
        try:
            prompt = f"""
            Parse the following insurance-related query and return this structured JSON:
            {{
              "age": int,
              "gender": "male/female",
              "procedure": string,
              "location": string,
              "policy_duration": int (in months)
            }}

            Query: "{query}"
            """
            response = model.generate_content(prompt)
            return json.loads(response.text)
        except:
            print("⚠️ Gemini parsing failed. Falling back to regex.")
    return parse_query_with_regex(query)
