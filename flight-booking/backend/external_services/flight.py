from amadeus import Client, ResponseError
from amadeus import Location
from dotenv import load_dotenv
import requests
from backend.external_services.interface import FlightServiceProtocol
from backend.utils.log_manager import get_app_logger
import os

logger = get_app_logger(__name__)

load_dotenv()

class AmadeusFlightService:
     def __init__(self):
        self.api_key, self.api_secret = self.get_amadeus_credentials()
        logger.info("Amadeus FlightService initialized")

        try:
            self.amadeus = Client(client_id=self.api_key, client_secret=self.api_secret)
        except Exception as e:
            raise Exception(f"Failed to create Amadeus client: {str(e)}")

     def  get_amadeus_credentials(self) -> tuple[str,str]:
        # Load Amadeus API credentials from environment variables
        api_key = os.getenv("AMADEUS_API_KEY")
        api_secret = os.getenv("AMADEUS_API_SECRET")
        if not api_key or not api_secret:
            raise ValueError("Amadeus API credentials not configured")
        return (api_key, api_secret)

     def get_amadeus_access_token(self) -> str:
        """
        Retrieves an Amadeus access token using client credentials from environment variables.

        Returns:
            The access token string if the request is successful.
        """
        client_id, client_secret = self.get_amadeus_credentials()

        url = "https://test.api.amadeus.com/v1/security/oauth2/token"

        data = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
        }

        try:
            response = requests.post(url, data=data)
            response.raise_for_status()
            response_json = response.json()
            return response_json.get("access_token")

        except requests.exceptions.RequestException as e:
            raise e

     def search_flights(self, request_body: dict) -> dict:
        logger.info("Amadeus FlightService search_flights")
        try:
            response = self.amadeus.shopping.flight_offers_search.post(request_body)
            return response

        except ResponseError as api_error:
            raise Exception(f"{api_error}")



def get_flight_service() -> FlightServiceProtocol:
    """
    Factory function that returns the appropriate flight service implementation
    based on the FLIGHT_SERVICE_PROVIDER environment variable.

    Supported values:
        - "amadeus" (default): Uses the real Amadeus Self-Service API
        - "mock": Uses pre-built JSON fixtures for demo/development mode
    """
    provider = "amadeus"

    # if provider == "mock":
    #     from backend.external_services.mock_flight_service import MockFlightService

    #     return MockFlightService()

    return AmadeusFlightService()


amadeus_flight_service = get_flight_service()
