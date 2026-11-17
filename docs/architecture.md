# System architecture — current foundation and next stages

## Current working data flow

```text
┌─────────────────────────┐
│ Virtual GPS device      │
│ Python simulator        │
│ - bus ID                │
│ - latitude / longitude │
│ - speed / heading       │
└────────────┬────────────┘
             │ HTTP POST /api/location
             ▼
┌─────────────────────────┐
│ Flask backend           │
│ - validates JSON        │
│ - caches latest point   │
│ - appends JSONL history │
└────────────┬────────────┘
             │ REST API
             ▼
┌─────────────────────────┐
│ Browser / API testing   │
│ - /health               │
│ - /api/buses/latest     │
│ - /api/buses/<id>/history│
└─────────────────────────┘
```

## Planned target architecture

```text
Virtual GPS devices
       │ MQTT publish
       ▼
Mosquitto MQTT broker
       │ MQTT subscribe
       ▼
Backend service ─────── SQLite database
       │ WebSocket / REST
       ▼
Next.js dashboard + Leaflet / OpenStreetMap
```

The current HTTP link is a deliberate first integration step. MQTT will be introduced after the simulator-to-backend flow has been tested.
