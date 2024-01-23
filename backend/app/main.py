from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound


from app.auth.api import router as auth_router
from app.users.api import router as users_router
from app.foods.api import router as food_router
from app.categories.api import router as category_router
from app.restaurants.api import router as restaurant_router

app = FastAPI()


@app.exception_handler(NoResultFound)
async def no_result_found_exception_handler(request: Request, exc: NoResultFound):
    return JSONResponse(
        status_code=404,
        content={"message": f"item not found. {exc}."},
    )


@app.exception_handler(MultipleResultsFound)
async def multiple_result_found_exception_handler(
    request: Request, exc: MultipleResultsFound
):
    return JSONResponse(
        status_code=404,
        content={"message": f"multiple items found. {exc}."},
    )


app.include_router(auth_router)
app.include_router(users_router)
app.include_router(food_router)
app.include_router(category_router)
app.include_router(restaurant_router)
