import json
import random
import requests
from fastapi import Request, status, APIRouter
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="./templates")

router = APIRouter()

with open("./data/profils.json", encoding='utf-8') as f:
  PROFILES = json.load(f).get('profils')


@router.get("/")
def home(request: Request):

  response = requests.get("http://127.0.0.1:8000/profiles")
  profiles = response.json()

  return templates.TemplateResponse("index.html", {"request": request, "profiles": profiles})


@router.get("/profiles")
def get_profiles():
  return PROFILES


@router.get("/profiles/{profile_id}")
def get_profile(profile_id: str):

  for profile in PROFILES:
    if profile.get("uuid") == profile_id:
      return profile
  
  return status.HTTP_404_NOT_FOUND


@router.get("/profiles/{profile_id}/next")
def get_next_profile(profile_id: str):

  profile = get_profile(profile_id)

  random_profiles = set([x.uuid for x in PROFILES]).symmetric_difference(profile.match + profile.nomatch)

  next_profile = random.choice(random_profiles)

  return get_profile(next_profile)


@router.post("/profiles/{profile_id}/{profile_match_id}/swipe")
def swipe(request: Request,
          profile_id: str,
          profile_match_id: str):

  direction = request.form.get("direction")

  if direction == "right":
    
    for profile in PROFILES:
      if profile.get("uuid") == profile_id:
        profile.get('match').append(profile_match_id)
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
        profile.get('nomatch').append(profile_match_id)
        break

    # Utiliser la route get_next_profile pour obtenir le profil aléatoire suivant
    next_profile = get_next_profile(profile_id)
    return {
      "match": False,
      "profile": next_profile
    }

  else:
    return status.HTTP_400_BAD_REQUEST