from fastapi import HTTPException
from typing import List, Annotated

from fastapi import APIRouter, Depends

from src.api.dependencies import match_service
from src.schemas.match import MatchRead, MatchCreate
from src.services.match import MatchService


match_router = APIRouter(prefix="/v1/match", tags=["match"])


@match_router.post(
    "/",
    status_code=201,
    summary="Создать роль пользователю.",
    description="Создать роль пользователю. request: name, permissions: ['edit', 'delete', 'view']",
)
async def add_match(
        match: MatchCreate,
        matches_service: Annotated[MatchService, Depends(match_service)],
):
    match = await matches_service.add_match(match=match)
    if match:
        return match
    else:
        raise HTTPException(status_code=404, detail="Match not found")


@match_router.get(
    "/all/",
    status_code=200,
    response_model=List[MatchRead],
    summary="Возвращает всех пользователей, которые имеют доступ ко всем файлам."
)
async def get_matches(
        matches_service: Annotated[MatchService, Depends(match_service)]
):
    matches = await matches_service.get_matches()
    if matches:
        return matches
    else:
        raise HTTPException(status_code=404, detail="Matches not found")


@match_router.patch(
    "/status/True/{user1_id}/{user2_id}/",
    status_code=200,
    response_model=MatchRead,
)
async def edit_match(
        user1_id: int,
        user2_id: int,
        matches_service: Annotated[MatchService, Depends(match_service)],
):
    match = await matches_service.edit_match(user1_id=user1_id, user2_id=user2_id, status=True)
    if match:
        return match
    else:
        raise HTTPException(status_code=404, detail="Match not found")


@match_router.get(
    "/match/{id}/",
    status_code=200,
    response_model=List[MatchRead],
    summary="Возвращает всех пользователей, которые имеют доступ к конкретному файлу.",
)
async def get_matches(
        id: int,
        matches_service: Annotated[MatchService, Depends(match_service)]
):
    matches = await matches_service.get_matches_by_one_id(id=id)
    if matches:
        return matches
    else:
        raise HTTPException(status_code=404, detail="Matches not found")


@match_router.get(
    "/{user1_id}/{user2_id}/",
    status_code=200,
    response_model=MatchRead,
    summary="Проверяет имеет ли пользователь доступ к файлу.",
    description="Проверяет имеет ли пользователь доступ к файлу. "
                "Если у пользователя нет доступа, то выводит 404 ошибку, если есть, "
                "то возвращает user-file-association(permissions)."
                "file_id: int, user_id: int",
)
async def check_user_file(
        user1_id: int,
        user2_id: int,
        matches_service: Annotated[MatchService, Depends(match_service)]
):
    match = await matches_service.get_match_by_two_id(user1_id=user1_id, user2_id=user2_id)
    if match:
        return match
    else:
        raise HTTPException(status_code=404, detail="Match not found")



@match_router.delete(
    "/{user1_id}/{user2_id}/",
    status_code=204,
    summary="Удаляет роль пользователя для конкретного файла.",
    description="Удаляет роль пользователя для конкретного файла. file_id: int, user_id: int",
)
async def delete_match(
        user1_id: int,
        user2_id: int,
        matches_service: Annotated[MatchService, Depends(match_service)],
):
    match = await matches_service.delete_match(user1_id=user1_id, user2_id=user2_id)
    if match:
        return match
    else:
        raise HTTPException(status_code=404, detail="Match not found")
