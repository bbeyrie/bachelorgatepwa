import json
import random
import requests
from fastapi import Request, status, APIRouter, Form
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

  # response = requests.get("http://127.0.0.1:8000/profiles")
  profiles = get_profiles()

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

  if isinstance(profile, dict):
    return templates.TemplateResponse("profils.html", {"request": request, "profile": profile})
  
  else:
    print(profile) 
    return templates.TemplateResponse("story.html", {"request": request, "candidats": profile})

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

  nb_match = sum([1 for x in PROFILES if x.get('match')==True])

  # Start the war
  if nb_match == 8:

    participants = [x for x in PROFILES if x.get('match')==True]

    return participants

  if random_profiles:

    next_profile = random.choice(random_profiles)

    return get_profile(next_profile)
  
  # Reset no match profiles till we get 8 profiles
  else:
    for p in PROFILES:
        if p.get("match") == False:
            p['match'] = None
  
    return get_next_profile()


@router.post("/profiles/{profile_id}/swipe")
def swipe_profile(profile_id: str, direction: str = Form(...)):
    profile = None

    for p in PROFILES:
        if p.get("uuid") == profile_id:
            profile = p
            break

    if profile:
        if direction == "right":
            profile['match'] = True
        elif direction == "left":
            profile['match'] = False
        else:
            return status.HTTP_400_BAD_REQUEST

        return RedirectResponse(url="/profils", status_code=302)
    else:
        return status.HTTP_404_NOT_FOUND