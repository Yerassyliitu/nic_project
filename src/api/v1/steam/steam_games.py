from typing import Annotated

import httpx
from fastapi import APIRouter, HTTPException, Depends

from settings.steam_config.config import BASE_STEAM_API_URL, STEAM_API_KEY
from src.utils.auth_handler import get_current_user

games_router = APIRouter(
    prefix="/v1/steam",
    tags=["Steam"],
)


# steam_id = 76561199403558855
# steam_id = 76561199096464451   #shiko

async def get_games(steam_id):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_STEAM_API_URL}/IPlayerService/GetOwnedGames/v1/",
            params={
                "key": STEAM_API_KEY,
                "steamid": steam_id,
                "format": "json",
                "include_appinfo": 1,
            },
        )
        data = response.json()
        if data:
            return data
        else:
            raise HTTPException(status_code=404, detail="Games not found")


async def get_steam_id(
    user: Annotated[dict, Depends(get_current_user)],
):
    return user['steam_id']


@games_router.get("/games/")
async def games(
    user: str = Depends(get_current_user),
):
    steam_id = user["steam_id"]
    if steam_id is None:
        raise HTTPException(status_code=404, detail="Steam id not found")
    return await get_games(steam_id)


@games_router.get("/top-games/")
async def top_10_games(
    user: str = Depends(get_current_user),
):
    steam_id = user["steam_id"]
    all_games = await get_games(steam_id)
    top = sorted(all_games, key=lambda x: x["playtime_forever"], reverse=True)
    return top
