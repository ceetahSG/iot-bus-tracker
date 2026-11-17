# Software-Only IoT Bus Tracker — Foundation

This starter project demonstrates the first working milestone of a software-only IoT bus tracker:

1. A **virtual GPS device** simulates a bus moving through a list of coordinates.
2. The simulator sends each location update to a **Flask backend** over HTTP.
3. The backend validates the message, keeps the latest location for each bus in memory, and appends updates to a JSONL log file.
4. You can inspect the latest data through a REST API.

> Important: This is the foundation/demo milestone. The current prototype uses HTTP to keep the first end-to-end test simple. MQTT/Mosquitto, persistent database storage, and the Next.js live map are planned next stages and are not implemented in this starter yet.

## Project structure

```text
bus-tracker-starter/
├── backend/
│   └── app.py
├── simulator/
│   └── bus_simulator.py
├── docs/
│   ├── architecture.md
│   └── teacher_demo_checklist.md
├── requirements.txt
├── .gitignore
└── README.md
```

## Requirements

- Windows 10/11, macOS, or Linux
- Python 3.10 or newer
- VS Code (recommended)
- Internet connection for the first dependency installation

Check Python:

```bash
python --version
```

On some Windows installations, use `py --version` and replace `python` with `py` in the commands below if needed.

## Setup on Windows (PowerShell or VS Code terminal)

Open a terminal inside the `bus-tracker-starter` folder.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, run this for the current terminal only:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## Run the prototype

### Terminal 1 — start the backend

```powershell
python backend/app.py
```

The backend should report that it is listening at:

```text
http://127.0.0.1:5000
```

Check the health endpoint in your browser:

```text
http://127.0.0.1:5000/health
```

Expected response:

```json
{"status":"ok","service":"bus-tracker-backend"}
```

### Terminal 2 — start the virtual bus

Open a second terminal in the same project folder. Activate the virtual environment there too:

```powershell
.\.venv\Scripts\Activate.ps1
python simulator/bus_simulator.py
```

The simulator sends a location update every two seconds. The backend terminal should print each received update.

Press `Ctrl+C` in the simulator terminal to stop it.

## Inspect the received data

Open these URLs in a browser:

- Backend health: `http://127.0.0.1:5000/health`
- Latest locations: `http://127.0.0.1:5000/api/buses/latest`
- BUS-01 history: `http://127.0.0.1:5000/api/buses/BUS-01/history`

The backend also creates `backend/location_history.jsonl`, containing one JSON record per received update. This file is generated when the simulator sends its first update.

## What is implemented now?

- Python virtual GPS simulator
- Simulated route coordinates
- Periodic location updates
- HTTP communication from simulator to backend
- Flask endpoint to receive and validate location messages
- Latest-location and history API endpoints
- Basic JSONL logging for demonstration

## What comes next?

1. Replace the initial HTTP device-to-server link with MQTT using Mosquitto and the Eclipse Paho Python client.
2. Store bus and location history in SQLite.
3. Add real-time updates from backend to frontend using WebSockets (for example, Flask-SocketIO).
4. Build a Next.js + TypeScript dashboard.
5. Display buses and routes on a Leaflet/OpenStreetMap map.
6. Add multiple virtual buses, offline detection, and route selection.

## Academic honesty / project scope

The GPS points in this prototype are synthetic test coordinates. They are not being read from a physical GPS receiver, and the sample points are not guaranteed to follow actual roads. This prototype demonstrates the software simulation and backend data pipeline without purchasing hardware.
