import requests

from app.config.settings import settings


class AdzunaProvider:

    BASE_URL = "https://api.adzuna.com/v1/api/jobs"

    def search_jobs(
        self,
        country="in",
        query="SDET",
        location="Chennai",
        page=1,
    ):

        url = f"{self.BASE_URL}/{country}/search/{page}"

        params = {
            "app_id": settings.ADZUNA_APP_ID,
            "app_key": settings.ADZUNA_APP_KEY,
            "results_per_page": 20,
            "what": query,
            "where": location,
        }

        response = requests.get(
            url,
            params=params,
            timeout=30,
            headers={
                "Accept": "application/json"
            },
        )

        response.raise_for_status()

        return response.json()