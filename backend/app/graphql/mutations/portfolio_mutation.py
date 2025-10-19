# app/graphql/mutations/portfolio_mutation.py
import strawberry # type: ignore
from datetime import datetime
from app.dependencies.auth import get_current_user
from app.config.database import SessionLocal
from app.models.portfolio import Portfolio
from app.graphql.types import PortfolioType
from strawberry.scalars import JSON # type: ignore


@strawberry.type
class PortfolioMutation:

    @strawberry.mutation
    def create_portfolio(
        self,
        info,
        portfolio_name: str,
        tenure: int,
        amount: float,
        risk_profile: str,
        recommendation: JSON
    ) -> PortfolioType:
        current_user = get_current_user(info)
        user_id = current_user["user_id"]

        with SessionLocal() as db:
            portfolio = Portfolio(
                user_id=user_id,
                portfolio_name=portfolio_name,
                tenure=tenure,
                amount=amount,
                risk_profile=risk_profile,
                recommendation=recommendation
            )
            db.add(portfolio)
            db.commit()
            db.refresh(portfolio)

        return PortfolioType(
            id=portfolio.id,
            user_id=portfolio.user_id,
            portfolio_name=portfolio.portfolio_name,
            tenure=portfolio.tenure,
            amount=float(portfolio.amount),
            risk_profile=portfolio.risk_profile,
            recommendation=portfolio.recommendation,
            created_at=portfolio.created_at,
            updated_at=portfolio.updated_at
        )

    @strawberry.mutation
    def update_portfolio(
        self,
        info,
        portfolio_id: int,
        portfolio_name: str | None = None,
        tenure: int | None = None,
        amount: float | None = None,
        risk_profile: str | None = None,
        recommendation: JSON | None = None
    ) -> PortfolioType:
        current_user = get_current_user(info)
        user_id = current_user["user_id"]

        with SessionLocal() as db:
            portfolio = db.query(Portfolio).filter(
                Portfolio.id == portfolio_id,
                Portfolio.user_id == user_id
            ).first()

            if not portfolio:
                raise Exception("Portfolio not found")

            if portfolio_name is not None:
                portfolio.portfolio_name = portfolio_name
            if tenure is not None:
                portfolio.tenure = tenure
            if amount is not None:
                portfolio.amount = amount
            if risk_profile is not None:
                portfolio.risk_profile = risk_profile
            if recommendation is not None:
                portfolio.recommendation = recommendation

            db.commit()
            db.refresh(portfolio)

        return PortfolioType(
            id=portfolio.id,
            user_id=portfolio.user_id,
            portfolio_name=portfolio.portfolio_name,
            tenure=portfolio.tenure,
            amount=float(portfolio.amount),
            risk_profile=portfolio.risk_profile,
            recommendation=portfolio.recommendation,
            created_at=portfolio.created_at,
            updated_at=portfolio.updated_at
        )

    @strawberry.mutation
    def delete_portfolio(self, info, portfolio_id: int) -> bool:
        current_user = get_current_user(info)
        user_id = current_user["user_id"]

        with SessionLocal() as db:
            portfolio = db.query(Portfolio).filter(
                Portfolio.id == portfolio_id,
                Portfolio.user_id == user_id
            ).first()

            if not portfolio:
                return False

            db.delete(portfolio)
            db.commit()
        return True
