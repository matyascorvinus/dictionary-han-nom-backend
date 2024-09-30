import uuid
from typing import Any

from app import crud
from fastapi import APIRouter, HTTPException

from app.api.deps import CurrentUser, SessionDep
from app.models import HanCharacter, Message

router = APIRouter()


@router.get("/", response_model=list[HanCharacter])
def read_han_characters(
    session: SessionDep, current_user: CurrentUser, search_word: str, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve han characters.
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    han_character_results = crud.get_han_character(session=session, search_word=search_word, skip=skip, limit=limit)
    return han_character_results


@router.get("/{id}", response_model=HanCharacter)
def read_han_character_by_id(session: SessionDep, current_user: CurrentUser, id: uuid.UUID) -> Any:
    """
    Get han character by ID.
    """
    han_character_result = session.get(HanCharacter, id)
    if not han_character_result:
        raise HTTPException(status_code=404, detail="Han character not found")
    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return han_character_result


@router.post("/", response_model=HanCharacter)
def create_han_character(
    *, session: SessionDep, current_user: CurrentUser, han_character: HanCharacter
) -> Any:
    """
    Create new han character.
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    han_character_result = crud.create_han_character(session=session, han_character=han_character)
    return han_character_result


@router.put("/{id}", response_model=HanCharacter)
def update_han_character(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    id: uuid.UUID,
    han_character_in: HanCharacter,
) -> Any:
    """
    Update a han character.
    """
    han_character_result = session.get(HanCharacter, id)
    if not han_character_result:
        raise HTTPException(status_code=404, detail="Han characternot found")
    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    han_character_result = crud.update_han_character(session=session, han_character=han_character_result, han_character_in=han_character_in)
    return han_character_result


@router.delete("/{id}")
def delete_han_character(
    session: SessionDep, current_user: CurrentUser, id: uuid.UUID
) -> Message:
    """
    Delete a han character.
    """
    han_character_result = session.get(HanCharacter, id)
    if not han_character_result:
        raise HTTPException(status_code=404, detail="Han characternot found")
    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    session.delete(han_character_result)
    session.commit()
    return Message(message="Item deleted successfully")
