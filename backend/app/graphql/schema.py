# app/graphql/schema.py
import strawberry # type: ignore
from .mutations.login_mutation import LoginMutation
from .mutations.register_mutation import RegisterMutation
from .mutations.portfolio_mutation import PortfolioMutation
from .queries.profile_query import ProfileQuery
from .queries.portfolio_query import PortfolioQuery

@strawberry.type
class Query(ProfileQuery, PortfolioQuery):
    pass

@strawberry.type
class Mutation(RegisterMutation, LoginMutation, PortfolioMutation):
    pass

schema = strawberry.Schema(query=Query,mutation=Mutation)