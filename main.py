import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


from routes import auth_router, frontend_router, user_account_router

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


app.include_router(frontend_router, prefix="", tags=["frontend"])

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(user_account_router, prefix="/account", tags=["account"])



if __name__ == "__main__":
    uvicorn.run(f"{__name__}:app", port=8000, reload=True)
