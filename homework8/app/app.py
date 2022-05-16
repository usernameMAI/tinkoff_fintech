# type: ignore[attr-defined]
from fastapi import FastAPI

from app.endpoints.about_me import router_about
from app.endpoints.auth import router_auth
from app.endpoints.comments import router_comments
from app.endpoints.posts import router_posts
from app.endpoints.rating import router_rating

app = FastAPI()
app.include_router(router_auth)
app.include_router(router_posts)
app.include_router(router_about)
app.include_router(router_comments)
app.include_router(router_rating)
