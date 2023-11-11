import uvicorn
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer

from src.api.routers import all_routers

app = FastAPI(
    title="website for gamers",
)

@app.get("/")
def home_view():
    return {"message": "Hello, World!"}


for router in all_routers:
    app.include_router(router)



if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
