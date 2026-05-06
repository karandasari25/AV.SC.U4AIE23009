import requests
from typing import List, Dict, Tuple

BASE_URL = "http://20.207.122.201/evaluation-service"
DEPOTS_API = f"{BASE_URL}/depots"
VEHICLES_API = f"{BASE_URL}/vehicles"
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"

def fetch_depots() -> List[Dict]:
    response = requests.get(DEPOTS_API)
    response.raise_for_status()
    return response.json().get("depots", [])

def fetch_vehicle_tasks() -> List[Dict]:
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    response = requests.get(VEHICLES_API, headers=headers)
    response.raise_for_status()
    return response.json().get("vehicles", [])

def choose_optimal_tasks(tasks: List[Dict], capacity: int) -> Tuple[List[Dict], int]:
    n = len(tasks)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        duration = tasks[i - 1]["Duration"]
        impact = tasks[i - 1]["Impact"]

        for hours in range(capacity + 1):
            if duration <= hours:
                dp[i][hours] = max(
                    dp[i - 1][hours],
                    dp[i - 1][hours - duration] + impact
                )
            else:
                dp[i][hours] = dp[i - 1][hours]

    selected = []
    remaining_hours = capacity

    for i in range(n, 0, -1):
        if dp[i][remaining_hours] != dp[i - 1][remaining_hours]:
            selected.append(tasks[i - 1])
            remaining_hours -= tasks[i - 1]["Duration"]

    selected.reverse()
    return selected, dp[n][capacity]

def main():
    depots = fetch_depots()
    tasks = fetch_vehicle_tasks()

    for depot in depots:
        depot_id = depot["ID"]
        mechanic_hours = depot["MechanicHours"]

        selected_tasks, total_impact = choose_optimal_tasks(tasks, mechanic_hours)
        total_duration = sum(task["Duration"] for task in selected_tasks)

        print("\n" + "=" * 70)
        print(f"Depot ID          : {depot_id}")
        print(f"Available Hours   : {mechanic_hours}")
        print(f"Used Hours        : {total_duration}")
        print(f"Total Impact      : {total_impact}")
        print("=" * 70)

        for task in selected_tasks:
            print(f"Task ID     : {task['TaskID']}")
            print(f"Duration    : {task['Duration']} hours")
            print(f"Impact      : {task['Impact']}")
            print("-" * 70)

if __name__ == "__main__":
    main()