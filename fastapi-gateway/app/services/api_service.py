import requests
from app.core.config import settings
from app.utils.logger import logger

class APIService:
    def fetch_data(self, query_params):
        try:
            response = requests.get(
                settings.EXTERNAL_API_URL, params=query_params
            )
            response.raise_for_status()
            data = response.json()
            logger.info("Data fetched from external API")
            return data
        except requests.RequestException as e:
            logger.error(f"Error fetching data: {e}")
            return None
