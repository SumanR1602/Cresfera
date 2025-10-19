import strawberry # type: ignore
from app.dependencies.auth import get_current_user
from app.config.database import SessionLocal
from app.models.portfolio import Portfolio
from app.graphql.types import PortfolioType

@strawberry.type
class PortfolioQuery:
    @strawberry.field
    def portfolios(self, info) -> list[PortfolioType]:
        current_user = get_current_user(info)
        user_id = current_user["user_id"]

        with SessionLocal() as db:
            portfolios = db.query(Portfolio).filter(Portfolio.user_id == user_id).all()

            return [
                PortfolioType(
                    id=pf.id,
                    user_id=pf.user_id,
                    portfolio_name=pf.portfolio_name,
                    tenure=pf.tenure,
                    amount=float(pf.amount),
                    risk_profile=pf.risk_profile,
                    recommendation=pf.recommendation,
                    created_at=pf.created_at,
                    updated_at=pf.updated_at
                )
                for pf in portfolios
            ]
