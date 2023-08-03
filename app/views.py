# Lire les profils
import json
with open("data/profils.json") as f:
    PROFILES = json.load(f)

from fastapi import FastAPI, Request, status, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import random

templates = Jinja2Templates(directory="templates") 

app = FastAPI()

@app.get("/")
def home(request: Request):
   return templates.TemplateResponse("index.html", {"request": request, "profiles": PROFILES}) 


@app.get("/profiles/{profile_id}/next")
async def get_next_profile():
    # Filtrer pour ne garder que les profils non matchés 
    unmatched = [p for p in PROFILES if p.get('match') is None]
    
    # Choix aléatoire
    next_profile = random.choice(unmatched)
    
    return next_profile


@app.post("/swipe")
async def swipe(request: Request):

    # Récupérer la direction du swipe
    direction = request.form.get("direction")

    if direction == "right":
        # Swipe à droite = match
        
        # Charger le profil suivant
        next_profile = get_next_profile()

        return {
            "match": True,
            "profile": next_profile # Renvoyer le nouveau profil
        }

    elif direction == "left":
        # Swipe à gauche = pas match
        
        # Charger le profil suivant
        next_profile = get_next_profile()

        return {
            "match": False,
            "profile": next_profile # Renvoyer le nouveau profil
        }

    else:
        # Direction invalide
        return status.HTTP_400_BAD_REQUEST

@app.get("/profile/{profile_id}")
def get_profile(profile_id):
   profile = PROFILES[profile_id]
   
   # Lire le dossier des images  
   import os
   image_folder = f"data/images/{profile['prenom']}_{profile['age']}"
   images = os.listdir(image_folder)
   
   return {"profile": profile, "images": images}