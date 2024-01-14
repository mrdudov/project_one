from fastapi import FastAPI

from app.auth.api import router as auth_router
from app.users.api import router as users_router
from app.foods.api import router as food_router

app = FastAPI()


app.include_router(auth_router)
app.include_router(users_router)
app.include_router(food_router)
