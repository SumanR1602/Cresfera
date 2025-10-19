import strawberry  # type: ignore
from datetime import datetime
from app.models.user import User
from app.config.database import SessionLocal
from app.utils.hashing import hash_password
from ..types import UserType
from app.schemas.user_schema import UserCreate
from pydantic import ValidationError

@strawberry.type
class RegisterMutation:
    @strawberry.mutation
    def register_user(
        self,
        first_name: str,
        last_name: str,
        email: str,
        mobile: str,
        password: str,
        confirm_password: str,
        dob: str,
        country: str,
        agreed: bool
    ) -> UserType:
        try:
            data = UserCreate(
                first_name=first_name,
                last_name=last_name,
                email=email,
                mobile=mobile,
                password=password,
                confirm_password=confirm_password,
                dob=datetime.strptime(dob, "%Y-%m-%d").date(),
                country=country,
                agreed=agreed
            )
        except ValidationError as e:
            raise ValueError(e.errors()[0]["msg"])

        with SessionLocal() as db:
            if db.query(User).filter_by(email=data.email).first():
                raise ValueError("Email already registered")
            if db.query(User).filter_by(mobile=data.mobile).first():
                raise ValueError("Mobile already registered")

            user = User(
                first_name=data.first_name.strip(),
                last_name=data.last_name.strip(),
                email=data.email.lower().strip(),
                mobile=data.mobile.strip(),
                hashed_password=hash_password(data.password),
                dob=data.dob,
                country=data.country.strip(),
                agreed=data.agreed,
            )
            db.add(user)
            db.commit()
            db.refresh(user)

        return UserType(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            mobile=user.mobile,
            dob=str(user.dob),
            country=user.country,
            agreed=user.agreed,
        )
    
