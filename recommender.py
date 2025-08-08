from typing import Dict, List
from routing import best_routes
from value_calc import (
    FLIGHT_AWARD_CPM, HOTEL_CPM, GIFT_CARD_CPM,
    miles_needed_for_value, value_per_mile, redemption_summary
)


def recommend_best_redemptions(origin: str, destination: str, departure_date: str, miles_available: int, adults: int = 1) -> Dict:
    """
    Inputs:
      - origin, destination, departure_date, miles_available
    Process:
      - Gather public data: flight cash offers via Amadeus
      - Compute value-per-mile across categories
    Output:
      - Sorted recommendations with rationale
    """
    # Flight options
    routes = best_routes(origin, destination, departure_date, adults=adults, max_results=10)

    flight_candidates: List[Dict] = []
    for r in routes:
        taxes = 5.60
        miles_needed = miles_needed_for_value(r["price_total"], FLIGHT_AWARD_CPM, taxes)
        vpm = value_per_mile(r["price_total"], miles_needed, taxes)
        affordable = miles_needed <= miles_available
        flight_candidates.append({
            "type": "flight_award",
            "direct": r["direct"],
            "price_total": r["price_total"],
            "currency": r["currency"],
            "estimated_miles_needed": miles_needed,
            "value_per_mile_cents": round(vpm * 100, 2),
            "affordable": affordable,
            "segments": r["segments"],
        })

    # Hotel and gift card comparators (generic)
    sample_hotel_cash = 220.0
    hotel_summary = redemption_summary(sample_hotel_cash, taxes_fees_usd=0.0, cpm_cents=HOTEL_CPM)

    gift_card_face_value = miles_available * (GIFT_CARD_CPM / 100.0)
    gift_card_option = {
        "type": "gift_card",
        "cash_value_usd": round(gift_card_face_value, 2),
        "value_per_mile_cents": GIFT_CARD_CPM
    }

    # Pick top 5 flight options user can afford in miles; if none, show top 3 overall
    affordable_flights = [f for f in flight_candidates if f["affordable"]]
    affordable_flights.sort(key=lambda x: -x["value_per_mile_cents"])
    top_flights = (affordable_flights or sorted(flight_candidates, key=lambda x: -x["value_per_mile_cents"]))[:5]

    # Overall recommendations ranked by value-per-mile proxy
    recommendations = top_flights.copy()
    recommendations.append({
        "type": "hotel_award (example)",
        "cash_price_usd": sample_hotel_cash,
        "miles_needed": hotel_summary["miles_needed"],
        "value_per_mile_cents": hotel_summary["value_per_mile_cents"]
    })
    recommendations.append(gift_card_option)

    recommendations.sort(key=lambda x: -x.get("value_per_mile_cents", 0))
    return {
        "recommendations": recommendations,
        "assumptions": {
            "flight_award_cpm_cents": FLIGHT_AWARD_CPM,
            "hotel_cpm_cents": HOTEL_CPM,
            "gift_card_cpm_cents": GIFT_CARD_CPM,
            "flight_taxes_usd": 5.60
        }
    } 