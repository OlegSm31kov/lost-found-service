import httpx, os

BACKEND_URL = "http://backend:8000"

async def find_item(data: dict):

    async with httpx.AsyncClient() as client:

        response = await client.get(
            f"{BACKEND_URL}/items/find",
            params=data
        )

        return response.json()