from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import search
app = FastAPI()

# origins=[
#     "http://localhost:5173"
# ]

# app.add_middleware(    
#         CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],)

@app.get("/")
def main():
    return {"message": "Hello World"}


app.include_router(search.router)