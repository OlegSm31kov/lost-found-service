import httpx, os

BACKEND_URL = "http://backend:8000"
async def find_item(date_lost, station: str, summary: str, location: str | None):
    params = {
        "date_lost": date_lost,
        "station": station,
        "summary": summary,
    }

    if location != "Не помню":
        params["location"] = location

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BACKEND_URL}/items/find",
            params=params,
            timeout=30.0
        )

        response.raise_for_status()
        return response.json()