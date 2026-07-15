from app.services.jsearch import JSearchProvider


class JobSearchAgent:

    def __init__(self):
        self.provider = JSearchProvider()

    def search(self):
        return self.provider.search_jobs(
            "SDET in India"
        )