import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from src.api.routers import all_routers

app = FastAPI(
    title="website for gamers",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home_view():
    return {"message": "Hello, World!"}


for router in all_routers:
    app.include_router(router)


@app.exception_handler(Exception)
def validation_exception_handler(request, err):
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    return JSONResponse(status_code=400, content={"message": f"{base_error_message}. Detail: {err}"})


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
