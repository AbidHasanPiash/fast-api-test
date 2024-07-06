from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from app.routers import items, users

app = FastAPI()

app.include_router(items.router)
app.include_router(users.router)

@app.get("/")
async def read_root():
    return {"message": "Hello World"}

# Generate OpenAPI schema with custom metadata
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Abid Hasan",
        version="1.0.0",
        description="This is a very cool project, with automatic API docs and more.",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
