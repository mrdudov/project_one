from pydantic import EmailStr, BaseModel


class ReturnUser(BaseModel):
    id: int
    email: EmailStr


class UserLoginResponse(BaseModel):
    user: ReturnUser
    refresh_token: str
    access_token: str


class AccessToken(BaseModel):
    access_token: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str
