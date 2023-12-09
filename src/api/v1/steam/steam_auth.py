import json
from typing import Annotated

from fastapi import Request, Form

from fastapi import APIRouter, HTTPException, Depends
from starlette.responses import RedirectResponse

from src.schemas.user import UserUpdateSteamId
from src.services.user import UserService
from src.utils.steamsignin import SteamSignIn

from src.api.dependencies import user_service
from src.utils.auth_handler import get_current_user

steam_auth_router = APIRouter(
    prefix="/v1/steam",
    tags=["Steam"],
)

# steam_id = 76561199403558855
# steam_id = 76561199096464451   #shiko
api_url = "http://127.0.0.1:8000"


@steam_auth_router.get('/login')
async def main(
    user: Annotated[dict, Depends(get_current_user)],
    steam_signin: SteamSignIn = Depends(SteamSignIn),
):
    url = steam_signin.ConstructURL(api_url + '/api/v1/steam/processlogin/')
    redirect_url = f"{url}?user={json.dumps(user)}"
    return steam_signin.RedirectUser(redirect_url)


@steam_auth_router.get('/processlogin')
async def pr(
        request: Request,
        steam_signin: SteamSignIn = Depends(SteamSignIn),
):
    # Retrieve user from query parameters
    user_json = request.query_params.get('user')
    user = json.loads(user_json) if user_json else None

    # Validate steam_id or perform other necessary logic
    steam_id = steam_signin.ValidateResults(request.query_params)

    # Pass user to save_steam_id by adding it as a form parameter in the redirect URL
    redirect_url = f"/api/v1/steam/save_steam_id?steam_id={steam_id}&user={json.dumps(user)}"
    return RedirectResponse(url=redirect_url, status_code=302)


@steam_auth_router.post('/save_steam_id')
async def save_steam_id(
        users_service: Annotated[UserService, Depends(user_service)],
        steam_id: str = Form(...),
        user: dict = Form(..., alias='user'),
):
    userid = user['id']
    if steam_id:
        user = await users_service.update_user_steam(steam_id=steam_id, id=userid)
        if user:
            return user
        else:
            raise HTTPException(status_code=404, detail="User not found")