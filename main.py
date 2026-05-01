from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy import create_engine, text
from pydantic import BaseModel
from typing import Optional

BASE_DIR = Path(__file__).parent

app = FastAPI()

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

DB_URL = "mysql+pymysql://root:0320@localhost:3306/cjeats"
engine = create_engine(DB_URL)


class Restaurant(BaseModel):
    id: int
    kakao_id: str
    name: str
    category: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    place_url: Optional[str] = None
    lat: float
    lng: float
    price_range: Optional[str] = None
    rank_score: Optional[float] = None
    is_franchise: bool


@app.get("/")
def index():
    return FileResponse(BASE_DIR / "static" / "index.html")


@app.get("/restaurants", response_model=list[Restaurant])
def get_restaurants():
    with engine.connect() as conn:
        rows = conn.execute(text("SELECT * FROM restaurants")).mappings().all()
    return [dict(row) for row in rows]
