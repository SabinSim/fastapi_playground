import random

class SBBAgent:
    # A wrapper class that handles communication with the SBB

    @staticmethod
    def get_commute_time(location_name: str) -> int:

        if "Zurich" in location_name:
            return 15  # 취리히 시내라면 15분
        elif "Bern" in location_name:
            return 60  # 베른이라면 1시간
        elif "Geneva" in location_name:
            return 170 # 제네바라면 약 3시간
        else:
            return random.randint(20, 90) # 그 외 지역은 랜덤