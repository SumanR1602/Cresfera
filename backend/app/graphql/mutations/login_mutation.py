import strawberry # type: ignore
from app.models.user import User
from app.config.database import SessionLocal
from app.utils.hashing import verify_password
from app.utils.jwt import create_access_token
from app.schemas.user_schema import UserLogin
from app.graphql.types import LoginInput, LoginResponse


@strawberry.type
class LoginMutation:
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
