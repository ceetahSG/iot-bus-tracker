"""Virtual GPS device that sends simulated bus locations to Flask."""

from __future__ import annotations

import time
from datetime import datetime, timezone
from itertools import cycle

import requests

BUS_ID = "BUS-01"
BACKEND_URL = "http://127.0.0.1:5000/api/location"
UPDATE_INTERVAL_SECONDS = 2

# Synthetic sample coordinates around Dhaka for testing only.
# They are not road-snapped or verified as a real bus route.
ROUTE = [
    (23.81030, 90.41250),
    (23.81060, 90.41290),
    (23.81100, 90.41330),
    (23.81140, 90.41380),
    (23.81180, 90.41420),
    (23.81220, 90.41460),
    (23.81260, 90.41500),
]


def send_location(session: requests.Session, latitude: float, longitude: float, step: int) -> None:
    payload = {
        "bus_id": BUS_ID,
        "latitude": latitude,
        "longitude": longitude,
        "speed": 30 + (step % 4) * 2,
        "heading": 120,
        "status": "moving",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    try:
        response = session.post(BACKEND_URL, json=payload, timeout=5)
        response.raise_for_status()
        print(
            f"[SENT] {BUS_ID} | lat={latitude:.6f}, lon={longitude:.6f} | "
            f"HTTP {response.status_code}"
        )
    except requests.RequestException as exc:
        print(f"[SEND FAILED] Could not reach backend at {BACKEND_URL}: {exc}")
        print("Make sure the backend is running in the other terminal.")


def main() -> None:
    print(f"Virtual GPS device started for {BUS_ID}.")
    print(f"Sending updates to: {BACKEND_URL}")
    print(f"Update interval: {UPDATE_INTERVAL_SECONDS} seconds")
    print("Press Ctrl+C to stop.\n")

    with requests.Session() as session:
        for step, (latitude, longitude) in enumerate(cycle(ROUTE), start=1):
            send_location(session, latitude, longitude, step)
            time.sleep(UPDATE_INTERVAL_SECONDS)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nVirtual GPS device stopped.")
