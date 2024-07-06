from fastapi import APIRouter

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.get("/")
async def read_users():
    return [{"username": "user1"}, {"username": "user2"}]
