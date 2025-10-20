# app/graphql/types.py
import strawberry # type: ignore
from datetime import datetime
from strawberry.scalars import JSON # type: ignore
from typing import Optional

@strawberry.type
class UserType:
    id: strawberry.ID
    first_name: str
    last_name: str
    email: str
    mobile: str
    dob: str 
    country: str
    agreed: bool


@strawberry.input
class LoginInput:
    email: str
    password: str

@strawberry.type
class LoginResponse:
    success: bool
    message: str
    token: str | None = None



@strawberry.type
class UserProfile:
    id: int
    first_name: str
    last_name: str
    email: str
    mobile: str
    dob: str
    country: str


@strawberry.type
class PortfolioType:
    id: strawberry.ID
    user_id: strawberry.ID
    portfolio_name: str
    tenure: int
    amount: float
    risk_profile: str
    recommendation: Optional[JSON] = None
    created_at: datetime
    updated_at: datetime
