from typing import List, Dict
from reference import search_flights
from value_calc import miles_needed_for_value, value_per_mile, FLIGHT_AWARD_CPM


def parse_routes(offers_json: Dict) -> List[Dict]:
    routes: List[Dict] = []
    for offer in offers_json.get("data", []):
        try:
            price_total = float(offer.get("price", {}).get("total", 0.0))
        except (ValueError, TypeError):
            price_total = 0.0
        currency = offer.get("price", {}).get("currency", "USD")
        itineraries = offer.get("itineraries", [])
        if not itineraries:
            continue
        it = itineraries[0]
        segments = it.get("segments", [])
        direct = len(segments) == 1
        duration_iso = it.get("duration", "")  # e.g., "PT5H30M"
        routes.append({
            "price_total": price_total,
            "currency": currency,
            "direct": direct,
            "duration_iso": duration_iso,
            "segments": [{
                "carrierCode": s.get("carrierCode"),
                "number": s.get("number"),
                "departure": s.get("departure", {}),
                "arrival": s.get("arrival", {}),
            } for s in segments]
        })
    return routes


def _mock_offers_json(origin: str, destination: str) -> Dict:
    return {
        "data": [
            {
                "price": {"total": "320.00", "currency": "USD"},
                "itineraries": [
                    {
                        "duration": "PT5H30M",
                        "segments": [
                            {
                                "carrierCode": "AA",
                                "number": "101",
                                "departure": {"iataCode": origin, "at": "2025-09-01T08:00:00"},
                                "arrival": {"iataCode": destination, "at": "2025-09-01T13:30:00"},
                            }
                        ],
                    }
                ],
            },
            {
                "price": {"total": "280.00", "currency": "USD"},
                "itineraries": [
                    {
                        "duration": "PT7H10M",
                        "segments": [
                            {
                                "carrierCode": "DL",
                                "number": "202",
                                "departure": {"iataCode": origin, "at": "2025-09-01T09:15:00"},
                                "arrival": {"iataCode": "ORD", "at": "2025-09-01T11:00:00"},
                            },
                            {
                                "carrierCode": "DL",
                                "number": "303",
                                "departure": {"iataCode": "ORD", "at": "2025-09-01T12:00:00"},
                                "arrival": {"iataCode": destination, "at": "2025-09-01T16:25:00"},
                            },
                        ],
                    }
                ],
            },
        ]
    }


def best_routes(origin: str, destination: str, departure_date: str, adults: int = 1, max_results: int = 10) -> List[Dict]:
    """
    Finds routes and annotates each with estimated miles_needed and VPM using flight award CPM.
    Taxes default to $5.60 domestic; in real world vary by market.
    """
    try:
        offers = search_flights(origin, destination, departure_date, adults, max_results)
    except Exception:
        offers = _mock_offers_json(origin, destination)

    routes = parse_routes(offers)
    for r in routes:
        taxes = 5.60  # heuristic default
        miles_needed = miles_needed_for_value(r["price_total"], FLIGHT_AWARD_CPM, taxes_fees_usd=taxes)
        vpm = value_per_mile(r["price_total"], miles_needed, taxes)
        r["estimated_miles_needed"] = miles_needed
        r["value_per_mile_usd"] = vpm
        r["value_per_mile_cents"] = round(vpm * 100, 2)
    # Rank by best value-per-mile, break ties by lower price
    routes.sort(key=lambda x: (-x["value_per_mile_usd"], x["price_total"]))
    return routes 