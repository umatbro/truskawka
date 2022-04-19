import uvicorn
from fastapi import FastAPI

from dto.auth import CreateUserRequest
from schema import graphql_app

app = FastAPI()
app.include_router(graphql_app)


@app.post("/user")
def create_user(create_user_request: CreateUserRequest):
    pass


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
