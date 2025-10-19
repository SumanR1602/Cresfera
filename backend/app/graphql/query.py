import strawberry  # type: ignore

@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "GraphQL API is running 🚀"