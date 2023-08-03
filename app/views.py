import json
import random
import requests
from fastapi import FastAPI, Request, status, APIRouter
from fastapi.responses import HTMLResponse  
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

router = APIRouter()

with open("data/profiles.json") as f:
  PROFILES = json.load(f)

@router.get("/")
def home(request: Request):

  response = requests.get("http://localhost:8000/api/profiles")
  profiles = response.json()

  return templates.TemplateResponse("index.html", {"request": request, "profiles": profiles})


@router.get("/profiles")
def get_profiles():
  return PROFILES


@router.get("/profiles/{profile_id}")
def get_profile(profile_id: str):

  for profile in PROFILES:
    if profile["uuid"] == profile_id:
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
    
    next_profile = get_next_profile()

    for profile in PROFILES:
      if profile.get("uuid")==profile_id:
        profile.get('match').append(profile_match_id)
        break

    return {
      "match": True,
      "profile": next_profile
    }

  elif direction == "left":

    next_profile = get_next_profile()

    for profile in PROFILES:
      if profile.get("uuid")==profile_id:
        profile.get('nomatch').append(profile_match_id)
        break

    return {
      "match": False,
      "profile": next_profile 
    }

  else:
    return status.HTTP_400_BAD_REQUEST