from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from src.services.role import RoleService
from src.schemas.role import RoleCreate
from .dependencies import role_service





role_router = APIRouter(
    prefix="/roles",
    tags=["Roles"],
)


@role_router.post("/")
async def add_role(
        role: RoleCreate,
        roles_service: Annotated[RoleService, Depends(role_service)],
):
    role_id = await roles_service.add_role(role)
    return {"role_id": role_id}










