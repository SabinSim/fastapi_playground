import httpx
import os
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv("SWISS_TRANSPORT_API_URL")

class CommuteService:
    @staticmethod
    async def get_commute_data(home: str, work: str):
        
        params = {
            "from": home,
            "to": work,
            "limit": 1
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(API_URL, params=params)
                response.raise_for_status()
                data = response.json()
            except httpx.HTTPError as e:
                print(f"HTTP Error: {e}")
                return None

        if not data.get("connections"):
            return None

        connection = data["connections"][0]
        
        
        # [Fixed Logic] Use timestamps instead of string parsing (Safest method)
        
        
        departure_timestamp = connection["from"]["departureTimestamp"]
        
        arrival_timestamp = connection["to"]["arrivalTimestamp"]
        
        if arrival_timestamp and departure_timestamp:
            # 초(Seconds) 단위 차이 계산 -> 분(Minutes)으로 변환
            duration_seconds = arrival_timestamp - departure_timestamp
            total_minutes = int(duration_seconds / 60)
        else:
            total_minutes = 0

        return {
            "duration_min": total_minutes,
            "transfers": connection.get("transfers", 0),
            "from": connection["from"]["station"]["name"],
            "to": connection["to"]["station"]["name"]
        }

    @staticmethod
    def calculate_score(duration_min: int) -> tuple[str, str]:
        
        if duration_min <= 30:
            return "A", "🌟 Fantastic! Quality of life improves!"
        elif duration_min <= 60:
            return "B", "✅ Good. Standard commute distance."
        elif duration_min <= 90:
            return "C", "⚠️ Tired. Read a book or watch Netflix."
        else:
            return "D", "🚨 Hell. Reconsider moving here."
