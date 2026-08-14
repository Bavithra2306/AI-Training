from pydantic import BaseModel


class CurrentWeather(BaseModel):
    time: str
    temperature_2m: float


class WeatherResponse(BaseModel):
    latitude: float
    longitude: float
    timezone: str
    current: CurrentWeather


class Holiday(BaseModel):
    date: str
    name: str
    countryCode: str
    subdivisionCodes: list[str] | None
    nationalHoliday: bool
    holidayTypes: list[str]


class ExchangeRate(BaseModel):
    date: str
    base: str
    quote: str
    rate: float
    