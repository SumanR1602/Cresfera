from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter  # type: ignore
from app.graphql.schema import schema
import os
import logging
from app.config.database import Base, engine
from app.models.user import User
from app.models.portfolio import Portfolio

app = FastAPI(title="Cresfera Backend")

# -----------------------
# Logging setup
# -----------------------
log_dir = os.path.join(os.path.dirname(__file__), "..", "logs")
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(log_dir, "app.log"),
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)
logger.info("🚀 FastAPI application is starting...")

# -----------------------
# Database setup
# -----------------------
@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
    print("Database tables created!")

# -----------------------
# CORS setup
# -----------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for dev only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------
# GraphQL setup
# -----------------------
def get_context(request: Request):
    return {"request": request}

graphql_app = GraphQLRouter(schema, context_getter=get_context)
app.include_router(graphql_app, prefix="/graphql")
