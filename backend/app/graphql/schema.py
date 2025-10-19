# app/graphql/schema.py
import strawberry # type: ignore
from .mutations.login_mutation import LoginMutation
from .mutations.register_mutation import RegisterMutation
from .query import Query

@strawberry.type
class Mutation(RegisterMutation, LoginMutation):
    pass

schema = strawberry.Schema(query=Query,mutation=Mutation)