from fastapi import FastAPI
import uvicorn

from hotels import router as router_hotels

app = FastAPI(title="BELS docs")
app.include_router(router_hotels)

if __name__ == "__main__":
    uvicorn.run(
        'main:app',
        reload=True
    )
