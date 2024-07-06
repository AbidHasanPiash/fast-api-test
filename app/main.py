from fastapi import FastAPI, Request
import requests
from datetime import datetime
from app.routers import items, users

app = FastAPI()

app.include_router(items.router)
app.include_router(users.router)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = datetime.utcnow()
    response = await call_next(request)
    process_time = (datetime.utcnow() - start_time).total_seconds()
    response.headers["X-Process-Time"] = str(process_time)
    return response

def get_location(ip_address: str):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip_address}")
        return response.json()
    except requests.RequestException:
        return None

@app.get("/")
async def read_root(request: Request):
    ip_address = request.client.host  # Automatically detect client's IP address
    
    user_agent = request.headers.get('user-agent')
    request_time = datetime.utcnow()
    endpoint_url = str(request.url)
    http_method = request.method
    headers = dict(request.headers)

    location_info = get_location(ip_address)
    if location_info and location_info['status'] == 'success':
        location = {
            "country": location_info.get('country'),
            "region": location_info.get('regionName'),
            "city": location_info.get('city'),
            "lat": location_info.get('lat'),
            "lon": location_info.get('lon'),
            "isp": location_info.get('isp')
        }
    else:
        location = None

    return {
        "message": "Hello World, this is a test deploy!",
        "ip_address": ip_address,
        "user_agent": user_agent,
        "request_time": request_time,
        "endpoint_url": endpoint_url,
        "http_method": http_method,
        "headers": headers,
        "location": location
    }
