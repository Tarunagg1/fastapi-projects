from fastapi import APIRouter, HTTPException
from backend.schemas.flight import FlightSearchResponse
from backend.schemas.flights_search import FlightSearchRequestPost
from backend.external_services.flight import amadeus_flight_service

router = APIRouter()
 

@router.post("/shopping/flight-offers", response_model=FlightSearchResponse)
async def search_flight(request: FlightSearchRequestPost):
    try:
        request_body = request.model_dump()
        # TO DO: Search in cache first (REDIS)
        response = amadeus_flight_service.search_flights(request_body)
        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid request body: {str(e)}")
    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail=f"Flight provider request failed: {str(e)}",
        )
