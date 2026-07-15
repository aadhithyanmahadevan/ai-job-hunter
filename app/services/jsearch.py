import requests

from app.config.settings import settings


class JSearchProvider:

    BASE_URL = "https://jsearch.p.rapidapi.com/search"

    def search_jobs(self, query: str, page: int = 1):

        headers = {
            "X-RapidAPI-Key": settings.JSEARCH_API_KEY,
            "X-RapidAPI-Host": "jsearch.p.rapidapi.com",
        }

        params = {
            "query": query,
            "page": page,
            "num_pages": 1,
        }

        response = requests.get(
            self.BASE_URL,
            headers=headers,
            params=params,
            timeout=30,
        )

        response.raise_for_status()

        print(settings.JSEARCH_API_KEY)

        return response.json()
    