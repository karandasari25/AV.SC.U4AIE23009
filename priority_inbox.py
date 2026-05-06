import requests
import heapq
from datetime import datetime



API_URL = "http://20.207.122.201/evaluation-service/notifications"

ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiYXVkIjoiaHR0cDovLzIwLjI0NC41Ni4xNDQvZXZhbHVhdGlvbi1zZXJ2aWNlIiwiZW1haWwiOiJhdi5zYy51NGFpZTIzMDA5QGF2LnN0dWRlbnRzLmFtcml0YS5lZHUiLCJleHAiOjE3NzgwNjE0NzEsImlhdCI6MTc3ODA2MDU3MSwiaXNzIjoiQWZmb3JkIE1lZGljYWwgVGVjaG5vbG9naWVzIFByaXZhdGUgTGltaXRlZCIsImp0aSI6IjU5ZDlkYmI2LTM1MmQtNGU4ZC05MDdiLTk4YzFkMmU0ZjFjMiIsImxvY2FsZSI6ImVuLUlOIiwibmFtZSI6ImRhc2FyaSBrYXJhbiIsInN1YiI6ImRhMWY3MmQ4LWRlYjUtNGYwMS04MWYyLWJmMGYwZDU3OTY4MCJ9LCJlbWFpbCI6ImF2LnNjLnU0YWllMjMwMDlAYXYuc3R1ZGVudHMuYW1yaXRhLmVkdSIsIm5hbWUiOiJkYXNhcmkga2FyYW4iLCJyb2xsTm8iOiJhdi5zYy51NGFpZTIzMDA5IiwiYWNjZXNzQ29kZSI6IlBUQk1tUSIsImNsaWVudElEIjoiZGExZjcyZDgtZGViNS00ZjAxLTgxZjItYmYwZjBkNTc5NjgwIiwiY2xpZW50U2VjcmV0IjoienNDSHNIZEp5WXVLdWVqRyJ9.zQ8k_071UUwvkFUeH0gCyQQczYM-4z_6fEEid19YMYU"
TOP_N = 10


TYPE_PRIORITY = {
    "Placement": 3,
    "Result": 2,
    "Event": 1
}



headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

response = requests.get(API_URL, headers=headers)

if response.status_code != 200:
    print("Unable to fetch notifications")
    print(response.text)
    exit()

response_data = response.json()
notifications = response_data.get("notifications", [])



def get_priority_score(notification):
    """
    Score is calculated using:
    1. Notification type priority
    2. Recency of notification
    """

    notification_type = notification.get("Type", "Event")
    timestamp_string = notification.get("Timestamp")

   
    type_score = TYPE_PRIORITY.get(notification_type, 1)


    notification_time = datetime.strptime(
        timestamp_string,
        "%Y-%m-%d %H:%M:%S"
    )

    
    recency_score = notification_time.timestamp()

    
    final_score = (type_score * 1_000_000_000) + recency_score

    return final_score



top_notifications_heap = []

for notification in notifications:

    score = get_priority_score(notification)

    heap_item = (score, notification)

   
    if len(top_notifications_heap) < TOP_N:
        heapq.heappush(top_notifications_heap, heap_item)

    else:
       
        if score > top_notifications_heap[0][0]:
            heapq.heappushpop(top_notifications_heap, heap_item)



top_notifications = sorted(
    top_notifications_heap,
    reverse=True
)



print("\nTop Priority Notifications\n")

for index, (score, notification) in enumerate(top_notifications, start=1):

    print(f"Rank       : {index}")
    print(f"ID         : {notification.get('ID')}")
    print(f"Type       : {notification.get('Type')}")
    print(f"Message    : {notification.get('Message')}")
    print(f"Timestamp  : {notification.get('Timestamp')}")
    print(f"Score      : {score}")

    print("-" * 60)