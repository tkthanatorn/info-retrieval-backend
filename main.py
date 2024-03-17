from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dependency import lifespan
from router.user import user_router
from router.auth import auth_router
from router.recipe import recipe_router
from router.bookmark import bookmark_router
from middleware import auth

app = FastAPI(lifespan=lifespan)
app.add_middleware(auth.AuthMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth")
app.include_router(user_router, prefix="/user")
app.include_router(recipe_router, prefix="/recipe")
app.include_router(bookmark_router, prefix="/bookmark")
