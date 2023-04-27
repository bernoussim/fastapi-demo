from fastapi import FastAPI

import app_v1
import app_v2

app = FastAPI()

app.include_router(app_v1.router, prefix="/api/v1", tags=["v1"])
app.include_router(app_v2.router, prefix="/api/v2", tags=["v2"])
app.include_router(app_v1.router)


@app.get("/")
def root():
    return {"message": "This is the root of the API"}
