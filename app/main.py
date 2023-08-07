from fastapi import FastAPI
from app.views import router
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()

# Configuration de la session
app.add_middleware(SessionMiddleware,
 secret_key="Ksq5RNnJqB3RZsn59T9H_D_aVbEszCfQ2BC8iQ84dLw",
 max_age=14 * 24 * 3600) # 14 jours en secondes)

app.include_router(router)

app.mount("/data", StaticFiles(directory="data"), name="data")
app.mount("/static", StaticFiles(directory="static"), name="static")
#app.mount("/node_modules", StaticFiles(directory="node_modules"), name="node_modules")
