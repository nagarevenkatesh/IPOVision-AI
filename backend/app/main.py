from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from apscheduler.schedulers.background import BackgroundScheduler

from app.core.database import Base, engine, SessionLocal

from app.api.routes.auth import router as auth_router
from app.api.routes.ipo import router as ipo_router
from app.api.routes.prediction import router as prediction_router
from app.api.routes.live_ipo import router as live_ipo_router

from app.services.live_ipo_service import sync_live_ipos

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="IPO Insight Platform")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth_router, prefix="/api/v1")
app.include_router(ipo_router, prefix="/api/v1")
app.include_router(prediction_router, prefix="/api/v1")
app.include_router(live_ipo_router, prefix="/api/v1")

# Scheduler
scheduler = BackgroundScheduler()


def auto_sync():
    db = SessionLocal()
    try:
        sync_live_ipos(db)
        print("Live IPO sync completed")
    except Exception as e:
        print("Sync failed:", e)
    finally:
        db.close()


scheduler.add_job(auto_sync, "interval", minutes=30)
scheduler.start()


@app.get("/")
def root():
    return {"message": "IPO Insight Platform API Running"}