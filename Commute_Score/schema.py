from pydantic import BaseModel

# [요청 데이터] 사용자가 입력한 집과 회사 주소
# [Request Data] Home and Work addresses input by the user
class CommuteRequest(BaseModel):
    home_address: str  # 출발지 (예: Zurich HB) / Departure (e.g., Zurich HB)
    work_address: str  # 도착지 (예: Bern) / Destination (e.g., Bern)

# [응답 데이터] 계산된 통근 정보 결과
# [Response Data] Calculated commute information result
class CommuteResponse(BaseModel):
    from_loc: str           # 출발 역 이름 / Departure station name
    to_loc: str             # 도착 역 이름 / Arrival station name
    duration_min: int       # 소요 시간 (분) / Duration in minutes
    transfers: int          # 환승 횟수 / Number of transfers
    score: str              # 등급 (A, B, C, D) / Grade score
    message: str            # 결과 메시지 / Result message