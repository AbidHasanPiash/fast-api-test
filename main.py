from fastapi import FastAPI
from app.routers import items, users

app = FastAPI()

app.include_router(items.router)
app.include_router(users.router)

@app.get("/")
async def read_root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
