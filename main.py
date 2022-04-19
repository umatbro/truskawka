import uvicorn  # type: ignore[import]
from fastapi import FastAPI  # type: ignore[import]

from dto.auth import CreateUserRequest

app = FastAPI()


@app.post("/user")
def create_user(create_user_request: CreateUserRequest):
    pass


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
