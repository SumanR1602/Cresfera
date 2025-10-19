from pydantic import BaseModel, EmailStr, Field, validator
import re
from datetime import date

class UserCreate(BaseModel):
    first_name: str = Field(..., min_length=3, description="First name must be at least 3 characters long")
    last_name: str = Field(..., min_length=3, description="Last name must be at least 3 characters long")
    email: EmailStr
    mobile: str
    password: str = Field(..., min_length=6, description="Password must be at least 6 characters long")
    confirm_password: str
    dob: date
    country: str
    agreed: bool

    @validator("mobile")
    def validate_mobile(cls, value):
        if not re.match(r"^[6-9]\d{9}$", value):
            raise ValueError("Mobile number must be a valid 10-digit Indian number")
        return value

    @validator("confirm_password")
    def check_password_match(cls, v, values):
        if "password" in values and v != values["password"]:
            raise ValueError("Passwords do not match")
        return v

    @validator("agreed")
    def must_agree(cls, value):
        if not value:
            raise ValueError("User agreement must be accepted")
        return value

    @validator("password")
    def password_length_limit(cls, v):
        if len(v.encode("utf-8")) > 72:
            raise ValueError("Password too long (max 72 bytes)")
        return v
