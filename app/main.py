from fastapi import FastAPI
from app.views import router
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.include_router(router)

app.mount("/data", StaticFiles(directory="data"), name="data")
app.mount("/static", StaticFiles(directory="static"), name="static")
#app.mount("/node_modules", StaticFiles(directory="node_modules"), name="node_modules")
