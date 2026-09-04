from fastapi import FastAPI,HTTPException

app = FastAPI(title = " Station Monitoring API", description = "This API is used to monitor the station data", version = "1.0.0")

STATIONS = {
    "ST-01": {
        "name": "UR10 Deburring Cell", 
        "status": "running",
        "error_code": None, 
        "temperature_c": 42.5,
        "parts_produced": 1847, 
        "cycle_time_s": 54.2
    },
    "ST-02": {
        "name": "Screwdriving Station", 
        "status": "stopped",
        "error_code": "E-233", 
        "temperature_c": 38.1,
        "parts_produced": 902, 
        "cycle_time_s": 0.0
    },
    "ST-03": {
        "name": "Lubrication Station", 
        "status": "warning",
        "error_code": "W-107", 
        "temperature_c": 61.8,
        "parts_produced": 1203, 
        "cycle_time_s": 71.5
        },
}

@app.get("/stations")
def list_stations():
    return [{"id": k, **v} for k, v in STATIONS.items()]

@app.get("/stations/{station_id}")
def get_station(station_id: str):
    station = STATIONS.get(station_id)
    if station is None:
        raise HTTPException(status_code=404, detail="Station {station_id} not found")
    return {"id": station_id.upper(), **station}