from collections.abc import Sequence


def calculate_percentage_changes_from_first(prices: Sequence[str]) -> list[float]:
    """Return each price's percentage change relative to the first price."""
    if not prices:
        return []

    numeric_prices = [float(price) for price in prices]
    starting_price = numeric_prices[0]
    if starting_price == 0:
        raise ValueError("The first price must not be zero")

    return [
        (price - starting_price) / starting_price * 100
        for price in numeric_prices
    ]
