import json
import random
import requests
from fastapi import Request, status, APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

class StartRequest(BaseModel):
    username: str

templates = Jinja2Templates(directory="./templates")

router = APIRouter()

with open("./data/profils.json", encoding='utf-8') as f:
  PROFILES = json.load(f).get('profils')


@router.get("/")
def home(request: Request):

  response = requests.get("http://127.0.0.1:8000/profiles")
  profiles = response.json()

  return templates.TemplateResponse("index.html", {"request": request, "profiles": profiles})


@router.post("/start")
def start(request_data: StartRequest):
    username = request_data.username
    print(f"Username: {username}")

    # Traitez les données ici

    # Rediriger vers la route /profiles/next
    return RedirectResponse(url="/profils", status_code=302)


@router.get("/profils")
def profils(request: Request):

  profile = get_next_profile()
  
  return templates.TemplateResponse("profils.html", {"request": request, "profile": profile})


@router.get("/profiles")
def get_profiles():
  return PROFILES


@router.get("/profiles/{profile_id}")
def get_profile(profile_id: str):

  for profile in PROFILES:
    if profile.get("uuid") == profile_id:
      return profile
  
  return status.HTTP_404_NOT_FOUND


@router.get("/profiles/next")
def get_next_profile():

  random_profiles = [x.get('uuid') for x in PROFILES if x.get('match') is None]

  next_profile = random.choice(random_profiles)

  return get_profile(next_profile)


@router.post("/profiles/{profile_id}/swipe")
def swipe(request: Request,
          profile_id: str):

  direction = request.form.get("direction")

  if direction == "right":
    
    for profile in PROFILES:
      if profile.get("uuid") == profile_id:
        profile['match'] = True
        break

    # Utiliser la route get_next_profile pour obtenir le profil aléatoire suivant
    next_profile = get_next_profile(profile_id)
    return {
      "match": True,
      "profile": next_profile
    }

  elif direction == "left":

    for profile in PROFILES:
      if profile.get("uuid") == profile_id:
        profile['match'] = False
        break

    # Utiliser la route get_next_profile pour obtenir le profil aléatoire suivant
    next_profile = get_next_profile(profile_id)
    return {
      "match": False,
      "profile": next_profile
    }

  else:
    return status.HTTP_400_BAD_REQUEST