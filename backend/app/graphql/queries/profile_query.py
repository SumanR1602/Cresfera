# app/graphql/queries/profile_query.py
import strawberry # type: ignore
from app.dependencies.auth import get_current_user
from app.config.database import SessionLocal
from app.models.user import User
from app.graphql.types import UserProfile

@strawberry.type
class ProfileQuery:
    @strawberry.field
    def profile(self, info) -> UserProfile:
        current_user = get_current_user(info)
        user_id = current_user["user_id"]
        with SessionLocal() as db:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                raise Exception("User not found")
            return UserProfile(
                id=user.id,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                mobile=user.mobile,
                dob=str(user.dob),
                country=user.country
            )