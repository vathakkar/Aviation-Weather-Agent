import requests
from bs4 import BeautifulSoup

def search_web(query: str) -> str:
    try:
        url = "https://html.duckduckgo.com/html/"
        params = {"q": query}
        headers = {
            "User-Agent": "Mozilla/5.0 (AviationWeatherAgent)"
        }

        response = requests.post(url, data=params, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.find_all("a", class_="result__a", limit=3)

        if not results:
            return f"⚠️ No web results found for '{query}'."

        output = ""
        for result in results:
            title = result.text.strip()
            link = result["href"]
            output += f"🔗 {title}\n{link}\n\n"

        return output.strip()

    except Exception as e:
        return f"❌ Error during web search: {e}"
