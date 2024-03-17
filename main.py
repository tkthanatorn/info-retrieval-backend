from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from dependency import lifespan
from router.user import user_router
from router.auth import auth_router
from router.recipe import recipe_router
from router.bookmark import bookmark_router
from middleware import auth

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_auth_middleware(request: Request, call_next):
    if request.url.path == "/auth/login" or request.url.path == "/auth/register":
        return await call_next(request)
    return await auth.authorize_middleware(request, call_next)


app.include_router(auth_router, prefix="/auth")
app.include_router(user_router, prefix="/user")
app.include_router(recipe_router, prefix="/recipe")
app.include_router(bookmark_router, prefix="/bookmark")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
