from app.users.models import User
from sqlalchemy.future import select


async def get_user_by_email(*, session, email: str):
    query = await session.execute(select(User).where(User.email == email))
    return query.scalar_one()


async def get_user_by_id(*, session, id: int):
    query = await session.execute(select(User).where(User.id == id))
    return query.scalar_one()


def get_user_claims(user) -> dict:
    return {"user_id": user["id"], "user_email": user["email"]}
