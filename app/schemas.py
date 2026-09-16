from pydantic import BaseModel, Field


class Patient(BaseModel):

    age: int = Field(
        ge=1,
        le=120
    )

    glucose: float = Field(
        gt=0
    )

    bmi: float = Field(
        gt=0
    )
class PredictionResponse(BaseModel):
    prediction: int
    probability: float
    result: str

class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class UserResponse(BaseModel):
    id: int
    username: str
    role: str

class UserUpdate(BaseModel):
    username: str
    password: str

class UserPatch(BaseModel):
    username: str | None = None
    password: str | None = None

