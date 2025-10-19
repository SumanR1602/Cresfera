from fastapi import FastAPI,Request
from strawberry.fastapi import GraphQLRouter #type: ignore
from app.graphql.schema import schema

from app.config.database import Base, engine
from app.models.user import User 

app = FastAPI(title="Cresfera Backend")

# Automatically create tables on startup
@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
    print("Database tables created!")

# GraphQL setup

def get_context(request: Request):
    return {"request": request}
graphql_app = GraphQLRouter(schema,context_getter=get_context)
app.include_router(graphql_app, prefix="/graphql")
