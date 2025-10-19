import strawberry  # type: ignore
from datetime import datetime, timedelta
from app.models.user import User
from app.config.database import SessionLocal
from app.utils.hashing import hash_password,verify_password
from .types import UserType, LoginInput, LoginResponse
from app.schemas.user_schema import UserCreate, UserLogin
from pydantic import ValidationError
from app.utils.jwt import create_access_token

@strawberry.type
class Mutation:
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
            # Validate input using Pydantic model
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
            # Pydantic gives nice structured errors
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
    @strawberry.mutation
    def login(self, login_data: LoginInput) -> LoginResponse:
        validated_data = UserLogin(email=login_data.email, password=login_data.password)

        with SessionLocal() as db:
            user = db.query(User).filter(User.email == validated_data.email).first()
            if not user:
                return LoginResponse(success=False, message="User not found")

            if not verify_password(validated_data.password, user.hashed_password):
                return LoginResponse(success=False, message="Incorrect password")

            token = create_access_token({"user_id": user.id})
            return LoginResponse(success=True, message="Login successful", token=token)
