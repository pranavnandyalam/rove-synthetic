from math import ceil
from typing import Dict

# Default cents-per-mile (CPM) assumptions
FLIGHT_AWARD_CPM = 1.3   # airline miles (average value)
HOTEL_CPM = 0.7          # hotel points
GIFT_CARD_CPM = 0.5      # gift cards or statement credits


def value_per_mile(cash_price_usd: float, miles_used: int, taxes_fees_usd: float = 0.0) -> float:
    """
    Value per mile (USD): (cash_price - taxes_fees) / miles_used
    Returns dollars per mile.
    """
    if miles_used <= 0:
        return 0.0
    return max((cash_price_usd - taxes_fees_usd), 0.0) / miles_used


def miles_needed_for_value(cash_price_usd: float, cpm_cents: float, taxes_fees_usd: float = 0.0) -> int:
    """
    Miles needed ≈ (cash_price - taxes_fees) / (cpm_cents / 100)
    Rounded up to whole miles.
    """
    effective = max(cash_price_usd - taxes_fees_usd, 0.0)
    if cpm_cents <= 0:
        return 0
    return int(ceil(effective / (cpm_cents / 100.0)))


def redemption_summary(cash_price_usd: float, taxes_fees_usd: float, cpm_cents: float) -> Dict:
    miles_needed = miles_needed_for_value(cash_price_usd, cpm_cents, taxes_fees_usd)
    vpm = value_per_mile(cash_price_usd, miles_needed, taxes_fees_usd) if miles_needed > 0 else 0.0
    return {
        "cash_price_usd": cash_price_usd,
        "taxes_fees_usd": taxes_fees_usd,
        "cpm_cents": cpm_cents,
        "miles_needed": miles_needed,
        "value_per_mile_usd": vpm,
        "value_per_mile_cents": round(vpm * 100, 2)
    }


def example_calculations() -> Dict[str, Dict]:
    """
    Example calculations for:
    - Flight redemption
    - Hotel redemption
    - Gift card redemption
    """
    # Example inputs (adjustable)
    flight_cash = 350.00
    flight_taxes = 5.60
    hotel_cash = 220.00
    hotel_taxes = 0.00
    gift_card_cash = 100.00  # face value
    gift_card_taxes = 0.00

    return {
        "flight": redemption_summary(flight_cash, flight_taxes, FLIGHT_AWARD_CPM),
        "hotel": redemption_summary(hotel_cash, hotel_taxes, HOTEL_CPM),
        "gift_card": redemption_summary(gift_card_cash, gift_card_taxes, GIFT_CARD_CPM),
    } 