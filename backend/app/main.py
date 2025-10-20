from fastapi import FastAPI,Request
from strawberry.fastapi import GraphQLRouter #type: ignore
from app.graphql.schema import schema
import os
import logging
from app.config.database import Base, engine
from app.models.user import User
from app.models.portfolio import Portfolio

app = FastAPI(title="Cresfera Backend")

log_dir = os.path.join(os.path.dirname(__file__), "..", "logs")
os.makedirs(log_dir, exist_ok=True)

# Set up logging (global configuration)
logging.basicConfig(
    filename=os.path.join(log_dir, "app.log"),
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Log the app startup
logger.info("🚀 FastAPI application is starting...")

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
