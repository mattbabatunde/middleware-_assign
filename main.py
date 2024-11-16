# Create a fastapi app exposing an only one endpoint to create users with the following data:
# First Name
# Last Name
# Age
# Email
# Height
# Notes:
# Make sure to use the right payload content type
# Use the appropriate status codes
# Use in-memory storage to store responses
# Add a CORS middleware to allow only http:localhost:8000 (your localhost origin)
# Add a logger middleware to print to the console the time taken for a request to complete.


# ----------------------------------------------------------------
from fastapi import FastAPI, HTTPException, Request, Body, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from time import time
from typing import Dict

app = FastAPI()

# In-memory storage for user data
user_storage: Dict[str, dict] = {}

# Pydantic model for user registration
class UserRegistration(BaseModel):
    first_name: str
    last_name: str
    age: int
    email: EmailStr
    height: str

# Middleware for logging request time
@app.middleware("http")
async def log_request_time(request: Request, call_next):
    start_time = time()
    response = await call_next(request)
    elapsed_time = time() - start_time
    print(
        {
            "elapsed_time_seconds": round(elapsed_time, 4),
            "client_ip": request.client.host,
            "response_status": response.status_code,
        }
    )
    return response

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint to register a user
@app.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserRegistration = Body(...)):
    # Check if the user already exists by email
    for stored_user in user_storage.values():
        if stored_user["email"] == user_data.email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists.",
            )
    # Generate a user ID and save to in-memory storage
    user_id = f"user_{len(user_storage) + 1}"
    user_storage[user_id] = user_data.dict()

    return {"message": "User created successfully!", "user_id": user_id}
