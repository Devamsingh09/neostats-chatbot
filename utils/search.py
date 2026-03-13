from tavily import TavilyClient
from config.config import TAVILY_API_KEY


def web_search(query: str, max_results: int = 3) -> str:
    """Search the web using Tavily and return results as plain text."""
    try:
        client = TavilyClient(api_key=TAVILY_API_KEY)
        response = client.search(query=query, max_results=max_results)
        results = response.get("results", [])

        if not results:
            return "No web results found."

        parts = []
        for r in results:
            parts.append(
                f"Title: {r.get('title', '')}\n"
                f"Content: {r.get('content', '')}\n"
                f"Source: {r.get('url', '')}"
            )
        return "\n\n".join(parts)

    except Exception as e:
        return f"[Web search error: {e}]"