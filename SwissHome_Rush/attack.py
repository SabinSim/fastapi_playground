import threading   # 하나의 프로그램 안에서 여러 명이 동시에 움직이게 함
import requests   # 파이썬 코드로 웹사이트에 접속하거나 데이터를 보낼때 사용
import time

# 공격 대상 URL (1번 매물에 대한 예약 주소)
URL = "http://127.0.0.1:8000/book/1"

def attempt_booking(user_id):
    """
    단일 유저의 행동: 예약을 위해 POST 요청을 보내야 한다.
    """

    try:
        # POST 요청 전송('예약' 버튼 클릭 시뮬레이션)
        response = requests.post(URL)
        # 결과 확인
        if response.status_code == 20 or response.status_code == 303:
            print(f"User-{user_id}: Request Sent! (Code: {response.status_code})")
        else:
            print(f"User-{user_id}: Failed (Code: {response.status_code})")

    except Exception as e:
        print(f"User-{user_id}: Error - {e}")

def start_war():
    """
    [ENG] Main function to launch the concurrency attack.
    [KOR] 동시성 공격을 시작하는 메인 함수입니다.
    """
    threads = []
    
    # [ENG] Create 15 concurrent users (Threads)
    # [KOR] 15명의 동시 접속자(스레드) 생성
    print("--- ⚔️ STARTING TICKETING WAR ⚔️ ---")
    for i in range(15):
        t = threading.Thread(target=attempt_booking, args=(i+1,))
        threads.append(t)
    
    # [ENG] Start all threads simultaneously
    # [KOR] 모든 스레드 동시 시작
    for t in threads:
        t.start()
        
    # [ENG] Wait for all threads to finish
    # [KOR] 모든 스레드가 끝날 때까지 대기
    for t in threads:
        t.join()

    print("--- 🏁 WAR ENDED 🏁 ---")

if __name__ == "__main__":
    # [ENG] Before starting, we need to reset the DB manually via browser or curl if needed.
    # [KOR] 시작하기 전, 필요하다면 브라우저나 curl을 통해 DB를 초기화해야 합니다.
    start_war()