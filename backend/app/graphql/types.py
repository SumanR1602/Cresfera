# app/graphql/types.py
import strawberry # type: ignore
from datetime import date

@strawberry.type
class UserType:
    id: strawberry.ID
    first_name: str
    last_name: str
    email: str
    mobile: str
    dob: str  # or date
    country: str
    agreed: bool
