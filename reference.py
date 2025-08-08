import os
import requests
from dotenv import load_dotenv
from typing import List, Dict
from datetime import datetime

# Load credentials
load_dotenv()
CLIENT_ID = os.getenv("AMADEUS_API_KEY")
CLIENT_SECRET = os.getenv("AMADEUS_API_SECRET")

# Base URLs (test mode – switch to production when ready)
TOKEN_URL = "https://test.api.amadeus.com/v1/security/oauth2/token"
OFFERS_URL = "https://test.api.amadeus.com/v2/shopping/flight-offers"
PRICING_URL = "https://test.api.amadeus.com/v1/shopping/flight-offers/pricing"
BOOKING_URL = "https://test.api.amadeus.com/v1/booking/flight-orders"


def get_access_token() -> str:
    """
    Authenticate with Amadeus API using OAuth2 client credentials.
    Returns a Bearer token for subsequent API calls.
    """
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    resp = requests.post(TOKEN_URL, data=data, headers=headers)
    resp.raise_for_status()
    return resp.json()["access_token"]

def search_flights(origin: str, destination: str, departure_date: str,
                   adults: int = 1, max_results: int = 5) -> Dict:
    """
    Search for flight offers given origin, destination, and date. 
    Returns a JSON dictionary of offers.
    """
    token = get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "originLocationCode": origin,
        "destinationLocationCode": destination,
        "departureDate": departure_date,
        "adults": adults,
        "max": max_results
    }
    resp = requests.get(OFFERS_URL, headers=headers, params=params)
    resp.raise_for_status()
    return resp.json()

def confirm_offer_price(offer: Dict) -> Dict:
    """
    Confirm a flight offer’s price (ensures availability, tax updates, etc.).
    Returns full pricing breakdown JSON.
    """
    token = get_access_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    body = {"data": {"type": "flight-offers-pricing", "flightOffers": [offer]}}
    resp = requests.post(PRICING_URL, json=body, headers=headers)
    resp.raise_for_status()
    return resp.json()


def filter_by_flight_number(offers_data: Dict, flight_code: str) -> List[Dict]:
    """
    Returns all segments that match a given flight code (e.g., "AA123").
    If no matches, returns an empty list.
    """
    matches = []
    for offer in offers_data.get("data", []):
        for itiner in offer.get("itineraries", []):
            for seg in itiner.get("segments", []):
                code = f"{seg.get('carrierCode')}{seg.get('number')}"
                if code == flight_code:
                    matches.append(seg)
    return matches

def simplify_offers(offers_data: dict) -> list:
    """
    Takes full Amadeus offers JSON and returns simplified list with:
    - flight_code (e.g., AA123)
    - airline_code (e.g., AA)
    - price (e.g., 350.00 US
    - departure/arrival airports
    - departure/arrival times (date + time)
    """
    simplified = []

    for offer in offers_data.get("data", []):
        price = offer.get("price", {}).get("total")
        currency = offer.get("price", {}).get("currency")
        itineraries = offer.get("itineraries", [])

        for itinerary in itineraries:
            for segment in itinerary.get("segments", []):
                flight_code = f"{segment.get('carrierCode')}{segment.get('number')}"
                airline_code = segment.get("carrierCode")
                departure_airport = segment.get("departure", {}).get("iataCode")
                departure_time = segment.get("departure", {}).get("at")
                arrival_airport = segment.get("arrival", {}).get("iataCode")
                arrival_time = segment.get("arrival", {}).get("at")

                simplified.append({
                    "flight_code": flight_code,
                    "airline_code": airline_code,
                    "price": f"{price} {currency}",
                    "departure_airport": departure_airport,
                    "departure_time": departure_time,
                    "arrival_airport": arrival_airport,
                    "arrival_time": arrival_time
                })
    return simplified

def simplify_data(simplified_offers: list) -> str:
    """
    Takes in simplified_offers and turns it into easy-to-read data
    """
    routes = []
    current_route = []

    for flight in simplified_offers:
        if not current_route:
            current_route.append(flight)
        else:
            last_arrival = current_route[-1]["arrival_airport"]
            if last_arrival == flight["departure_airport"]:
                current_route.append(flight)
            else:
                routes.append(current_route)
                current_route = [flight]
    if current_route:
        routes.append(current_route)

    final = ""
    route_num = 1
    for route in routes:
        if len(route) > 1:
            final += f"Route {route_num}: Connecting flight with {len(route)} segments\n\n"
        else:
            final += f"Route {route_num}: Direct flight\n\n"

        for i, flight in enumerate(route, start=1):
            final += f"  Segment {i}: {flight.get('departure_airport')} --> {flight.get('arrival_airport')}\n"
            final += f"    Flight Code: {flight.get('flight_code')}\n"
            final += f"    Airline Code: {flight.get('airline_code')}\n"
            final += f"    Departure: {iso_to_readable(flight.get('departure_time'))} from {flight.get('departure_airport')}\n"
            final += f"    Arrival:   {iso_to_readable(flight.get('arrival_time'))} at {flight.get('arrival_airport')}\n"
            final += f"    Price:     {flight.get('price')}\n\n"

        route_num += 1

    return final


def iso_to_readable(iso: str) -> str:
    """
    Converts iso-time to readable time
    """
    dt = datetime.fromisoformat(iso)
    readable_time = dt.strftime("%B %d, %Y at %I:%M %p")

    return readable_time

def save_flights_to_db(simplified_offers: List[Dict], route_name: str) -> None:
    """
    Saves flight data to SQLite database.
    """
    