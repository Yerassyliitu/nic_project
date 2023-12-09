from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException

from src.services.role import RoleService
from src.schemas.role import RoleCreate, RoleRead
from src.api.dependencies import role_service


role_router = APIRouter(
    prefix="/v1/roles",
    tags=["Roles"],
)


@role_router.post(
    "/",
    status_code=201,
    summary="Создать роль пользователю.",
    description="Создать роль пользователю. request: name, permissions: ['edit', 'delete', 'view']",
)
async def add_role(
    role: RoleCreate,
    roles_service: Annotated[RoleService, Depends(role_service)],
):
    role = await roles_service.add_role(role=role)
    if role:
        return role
    else:
        raise HTTPException(status_code=404, detail="Role not found")


@role_router.get(
    "/",
    status_code=200,
    response_model=List[RoleRead],
    summary="Возвращает все роли.",
    description="Возвращает все роли.",
)
async def get_roles(
    roles_service: Annotated[RoleService, Depends(role_service)],
):
    roles = await roles_service.get_roles()
    if roles:
        return roles
    else:
        raise HTTPException(status_code=404, detail="Roles not found")


@role_router.get(
    "/{id}/",
    status_code=200,
    response_model=RoleRead,
    summary="Возвращает конкретную роль.",
    description="Возвращает конкретную роль. id: int",
)
async def get_role(
    id: int,
    roles_service: Annotated[RoleService, Depends(role_service)],
):
    role = await roles_service.get_role(id=id)
    if role:
        return role
    else:
        raise HTTPException(status_code=404, detail="Role not found")



@role_router.put(
    "/{id}/",
    status_code=200,
    response_model=RoleRead,
    summary="Обновляет роль.",
    description="Обновляет роль. id: int, request: name, permissions: ['edit', 'delete', 'view']",
)
async def edit_role(
    id: int,
    role: RoleCreate,
    roles_service: Annotated[RoleService, Depends(role_service)],
):
    role = await roles_service.edit_role(id=id, role=role)
    if role:
        return role
    else:
        raise HTTPException(status_code=404, detail="Role not found")



@role_router.delete(
    "/{id}/",
    status_code=204,
    summary="Удаляет роль.",
    description="Удаляет роль. id: int",
)
async def delete_role(
    id: int,
    roles_service: Annotated[RoleService, Depends(role_service)],
):
    role = await roles_service.delete_role(id=id)
    if role:
        raise HTTPException(status_code=204, detail="Role successfully deleted")
    else:
        raise HTTPException(status_code=404, detail="Role not found")











