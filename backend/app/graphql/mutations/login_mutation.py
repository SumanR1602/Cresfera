import strawberry # type: ignore
from app.models.user import User
from app.config.database import SessionLocal
from app.utils.hashing import verify_password
from app.utils.jwt import create_access_token, create_refresh_token
from app.schemas.user_schema import UserLogin
from app.graphql.types import LoginInput, LoginResponse
import logging

logger = logging.getLogger(__name__)

@strawberry.type
class LoginMutation:
    @strawberry.mutation
    def login(self, login_data: LoginInput) -> LoginResponse:
        validated_data = UserLogin(email=login_data.email, password=login_data.password)
        logger.info(f"Attempting login for: {validated_data.email}")

        with SessionLocal() as db:
            # Actual query
            user = db.query(User).filter(User.email == validated_data.email).first()
            logger.info(f"Query result: {user}")

            if not user:
                return LoginResponse(success=False, message=f"User not found: {validated_data.email}")

            if not verify_password(validated_data.password, user.hashed_password):
                return LoginResponse(success=False, message="Incorrect password")

            access_token = create_access_token({"user_id": user.id})
            refresh_token = create_refresh_token({"user_id": user.id})

            return LoginResponse(
                success=True,
                message="Login successful",
                access_token=access_token,
                refresh_token=refresh_token,
            )
