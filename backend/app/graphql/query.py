# app/graphql/queries.py
import strawberry # type: ignore

@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello Cresfera!"
