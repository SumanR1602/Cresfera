import strawberry  # type: ignore
from app.utils.jwt import decode_refresh_token, create_access_token, create_refresh_token
from app.graphql.types import LoginResponse


@strawberry.type
class RefreshTokenMutation:
    @strawberry.mutation
    def refresh_token(self, refresh_token: str) -> LoginResponse:
        """
        Validates the refresh token and returns a new access token.
        """
        try:
            # Decode and validate the refresh token
            payload = decode_refresh_token(refresh_token)
            user_id = payload.get("user_id")
            if not user_id:
                return LoginResponse(success=False, message="Invalid token payload")

            new_access_token = create_access_token({"user_id": user_id})
            new_refresh_token = create_refresh_token({"user_id": user_id})
            return LoginResponse(
                success=True,
                message="Token refreshed successfully",
                access_token=new_access_token,
                refresh_token=refresh_token 
            )

        except ValueError as e:
            return LoginResponse(success=False, message=str(e))
