from openai import OpenAI
import os
from pathlib import Path
from dotenv import load_dotenv
from tavily import TavilyClient
load_dotenv()
clientTav = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
def call_llm(prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content
