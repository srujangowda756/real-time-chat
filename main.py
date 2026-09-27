from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.auth import router as auth_router
from api.user import router as user_router
from webSocket.routes import router as websocket_router


app = FastAPI(
    title="Real-Time Chat API",
)


# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# ROUTERS
# ---------------------------------------------------------

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(websocket_router)


# ---------------------------------------------------------
# HEALTH CHECK
# ---------------------------------------------------------

@app.get("/")
async def health_check():
    return {
        "status": "ok",
    }
