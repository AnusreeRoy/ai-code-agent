# from dotenv import load_dotenv
# from tavily import TavilyClient
import os
from app.llm.client import clientTav
# load_dotenv()
#client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
#client = TavilyClient("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")
def web_search(query: str) -> str:
    """
    Web search tool using Tavily API.
    Returns clean, LLM-friendly search results.
    """
    response = clientTav.search(
        query=query,
        search_depth="basic",
        max_results=5
    )

    results = []
    for item in response.get("results", []):
        results.append(f"- {item['title']}: {item['content']}")

    return "\n".join(results)
