import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
load_dotenv()
from app.routes.auth import router as auth
from app.routes.analysis import router as analysis
from app.routes.reports import router as reports
app=FastAPI(title="AgriVision API")
origins = [
    x.strip()
    for x in os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173"
    ).split(",")
    if x.strip()
]
app.add_middleware(CORSMiddleware,allow_origins=origins,allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
app.include_router(auth,prefix="/api/auth",tags=["Auth"])
app.include_router(analysis,prefix="/api/analysis",tags=["Analysis"])
app.include_router(reports,prefix="/api/reports",tags=["Reports"])
@app.get("/")
def root(): return {"message":"AgriVision API is running"}
