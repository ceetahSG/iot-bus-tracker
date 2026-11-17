"""Flask API for the software-only IoT bus tracker foundation."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from typing import Any

from flask import Flask, jsonify, request

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
HISTORY_FILE = BASE_DIR / "location_history.jsonl"

# In-memory cache for the latest position of each bus.
# SQLite will replace this in a later milestone.
latest_locations: dict[str, dict[str, Any]] = {}
location_lock = Lock()

REQUIRED_FIELDS = {"bus_id", "latitude", "longitude", "speed", "heading", "status", "timestamp"}


def valid_location(data: Any) -> tuple[bool, str]:
    """Validate the shape and basic ranges of an incoming GPS message."""
    if not isinstance(data, dict):
        return False, "Request body must be a JSON object."

    missing = REQUIRED_FIELDS - data.keys()
    if missing:
        return False, f"Missing fields: {', '.join(sorted(missing))}"

    if not isinstance(data["bus_id"], str) or not data["bus_id"].strip():
        return False, "bus_id must be a non-empty string."

    try:
        latitude = float(data["latitude"])
        longitude = float(data["longitude"])
        speed = float(data["speed"])
        heading = float(data["heading"])
    except (TypeError, ValueError):
        return False, "latitude, longitude, speed, and heading must be numeric."

    if not -90 <= latitude <= 90:
        return False, "latitude must be between -90 and 90."
    if not -180 <= longitude <= 180:
        return False, "longitude must be between -180 and 180."
    if speed < 0:
        return False, "speed cannot be negative."
    if not 0 <= heading <= 360:
        return False, "heading must be between 0 and 360."

    if not isinstance(data["status"], str) or not data["status"].strip():
        return False, "status must be a non-empty string."

    return True, ""


@app.get("/health")
def health():
    return jsonify({"status": "ok", "service": "bus-tracker-backend"})


@app.post("/api/location")
def receive_location():
    data = request.get_json(silent=True)
    is_valid, error = valid_location(data)
    if not is_valid:
        return jsonify({"success": False, "error": error}), 400

    # Normalize numeric values before storing.
    record = {
        "bus_id": data["bus_id"].strip(),
        "latitude": float(data["latitude"]),
        "longitude": float(data["longitude"]),
        "speed": float(data["speed"]),
        "heading": float(data["heading"]),
        "status": data["status"].strip(),
        "timestamp": data["timestamp"],
        "received_at": datetime.now(timezone.utc).isoformat(),
    }

    with location_lock:
        latest_locations[record["bus_id"]] = record
        with HISTORY_FILE.open("a", encoding="utf-8") as log_file:
            log_file.write(json.dumps(record) + "\n")

    print(
        f"[LOCATION RECEIVED] {record['bus_id']} | "
        f"lat={record['latitude']:.6f}, lon={record['longitude']:.6f} | "
        f"speed={record['speed']:.1f} km/h"
    )
    return jsonify({"success": True, "message": "Location received", "data": record}), 201


@app.get("/api/buses/latest")
def get_latest_locations():
    with location_lock:
        result = list(latest_locations.values())
    return jsonify({"count": len(result), "buses": result})


@app.get("/api/buses/<bus_id>/history")
def get_bus_history(bus_id: str):
    records: list[dict[str, Any]] = []
    if HISTORY_FILE.exists():
        with HISTORY_FILE.open("r", encoding="utf-8") as log_file:
            for line in log_file:
                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if record.get("bus_id") == bus_id:
                    records.append(record)
    return jsonify({"bus_id": bus_id, "count": len(records), "history": records})


if __name__ == "__main__":
    print("Starting Bus Tracker backend...")
    app.run(host="127.0.0.1", port=5000, debug=False)
