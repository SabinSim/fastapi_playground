import requests
import threading
import time

URL = "http://127.0.0.1:8000/booking/reserve"
USER_COUNT = 15 

def send_request(user_id):
    try:
        response = requests.post(URL)
        if response.status_code == 200:
            print(f"✅ User-{user_id}: Success! (Reserved)")
        else:
            print(f"❌ User-{user_id}: Failed ({response.json()['detail']})")
    except Exception as e:
        print(f"⚠️ Error: {e}")

# ==========================================
# Start Attack
# ==========================================
print(f"🔥 {USER_COUNT} users are clicking the reserve button simultaneously!!!")

threads = []
start_time = time.time()

# [KOR] 스레드 생성 및 시작
# [ENG] Create and start threads
for i in range(USER_COUNT):
    t = threading.Thread(target=send_request, args=(i,))
    threads.append(t)
    t.start()

# [KOR] 모든 스레드가 끝날 때까지 대기
# [ENG] Wait for all threads to finish
for t in threads:
    t.join()

end_time = time.time()
print("="*40)
print(f"Total Time: {end_time - start_time:.2f} seconds")
print("="*40)