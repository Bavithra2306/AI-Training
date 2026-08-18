import time
from urllib import response
import httpx
from pydantic import TypeAdapter

from models import WeatherResponse, Holiday, ExchangeRate


# ============================================================
# 1. WEATHER API
# ============================================================

def get_weather() -> WeatherResponse:

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": 13.08,
        "longitude": 80.27,
        "current": "temperature_2m",
    }

    response = httpx.get(
        url,
        params=params,
        timeout=10.0,
    )

    response.raise_for_status()

    weather = WeatherResponse.model_validate(
        response.json()
    )

    return weather


# ============================================================
# 2. PUBLIC HOLIDAYS API
# ============================================================

def get_holidays() -> list[Holiday]:

    url = "https://date.nager.at/api/v4/Holidays/AT/2026"

    response = httpx.get(
        url,
        timeout=10.0,
    )

    response.raise_for_status()

    holidays = TypeAdapter(list[Holiday]).validate_python(
        response.json()
    )
    return holidays


# ============================================================
# 3. EXCHANGE RATE API
# ============================================================

def get_exchange_rates() -> list[ExchangeRate]:

    url = "https://api.frankfurter.dev/v2/rates"

    response = httpx.get(
        url,
        timeout=30.0,
    )

    response.raise_for_status()

    rates = [
        ExchangeRate.model_validate(item)
        for item in response.json()
    ]

    return rates


# ============================================================
# 4. TEST 404 ERROR
# ============================================================

def test_404():

    url = "https://api.frankfurter.dev/v2/this-does-not-exist"

    try:

        response = httpx.get(
            url,
            timeout=10.0,
        )

        response.raise_for_status()

    except httpx.HTTPStatusError as exc:

        print(
            f"404 handled successfully. "
            f"Status: {exc.response.status_code}"
        )


# ============================================================
# 5. TEST TIMEOUT ERROR
# ============================================================

def test_timeout():

    url = "https://api.frankfurter.dev/v2/rates"

    try:

        response = httpx.get(
            url,
            timeout=0.001,
        )

        response.raise_for_status()

    except httpx.TimeoutException:

        print("Timeout handled successfully!")


# ============================================================
# 6. RETRY LOGIC
# ============================================================

def test_retry():

    url = "https://api.frankfurter.dev/v2/this-does-not-exist"

    for attempt in range(3):

        try:

            print(f"Attempt {attempt + 1}")

            response = httpx.get(
                url,
                timeout=10.0,
            )

            response.raise_for_status()

            return response

        except httpx.HTTPStatusError as exc:

            status_code = exc.response.status_code

            # 404 should NOT be retried
            if status_code not in (
                429,
                500,
                502,
                503,
                504,
            ):

                print(
                    f"Not retrying status {status_code}"
                )

                return None

            wait_time = 2 ** attempt

            print(
                f"Failed with {status_code}. "
                f"Waiting {wait_time} seconds..."
            )

            time.sleep(wait_time)

    print("Failed after 3 attempts.")

    return None


# ============================================================
# 7. PROVE RETRY WITH 500 ERROR
# ============================================================

def test_retry_500():
    for attempt in range(3):

        try:
            print(f"Attempt {attempt + 1}")

            # Simulate a server error
            request = httpx.Request(
                "GET",
                "https://example.com"
            )

            response = httpx.Response(
                500,
                request=request
            )

            response.raise_for_status()

            return response

        except httpx.HTTPStatusError as exc:

            status_code = exc.response.status_code

            if status_code not in (
                429,
                500,
                502,
                503,
                504,
            ):
                print(
                    f"Not retrying status {status_code}"
                )
                return None

            wait_time = 2 ** attempt

            print(
                f"Failed with {status_code}. "
                f"Waiting {wait_time} seconds..."
            )

            time.sleep(wait_time)

    print("Failed after 3 attempts.")

    return None

# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    # --------------------------------------------------------
    # Weather
    # --------------------------------------------------------

    weather = get_weather()

    print("\nWeather:")
    print(weather)

    print("\nTemperature:")
    print(weather.current.temperature_2m)


    # --------------------------------------------------------
    # Holidays
    # --------------------------------------------------------

    holidays = get_holidays()

    print("\nHolidays:")

    for holiday in holidays:
        print(holiday)


    # --------------------------------------------------------
    # Exchange Rates
    # --------------------------------------------------------

    rates = get_exchange_rates()

    print("\nExchange Rates:")

    for rate in rates:
        print(rate)


    # --------------------------------------------------------
    # Error handling
    # --------------------------------------------------------

    print("\n--- Testing 404 ---")

    test_404()


    print("\n--- Testing Timeout ---")

    test_timeout()


    print("\n--- Testing Retry ---")

    test_retry()


    print("\n--- Testing 500 Retry ---")

    test_retry_500()
    # day 1 tasks completed