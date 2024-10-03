import uuid
from typing import Any

from sqlmodel import Session, select, col, SQLModel, or_
from sqlalchemy import func

from app.core.security import get_password_hash, verify_password
from app.models import Item, ItemCreate, User, UserCreate, UserUpdate, HanCharacter, HanText


def create_user(*, session: Session, user_create: UserCreate) -> User:
    db_obj = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_user(*, session: Session, db_user: User, user_in: UserUpdate) -> Any:
    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
    db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user_by_email(*, session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user


def authenticate(*, session: Session, email: str, password: str) -> User | None:
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user


def create_item(*, session: Session, item_in: ItemCreate, owner_id: uuid.UUID) -> Item:
    db_item = Item.model_validate(item_in, update={"owner_id": owner_id})
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item

def create_han_character(*, session: Session, han_character: HanCharacter) -> User: 
    session.add(han_character)
    session.commit()
    session.refresh(han_character)
    return han_character


def update_han_character(*, session: Session, han_character: HanCharacter, han_character_in: HanCharacter) -> Any:
    han_character_data = han_character_in.model_dump(exclude_unset=True) 
    han_character.sqlmodel_update(han_character_data)
    session.add(han_character)
    session.commit()
    session.refresh(han_character)
    return han_character

def create_han_text(*, session: Session, han_text: HanText) -> User: 
    session.add(han_text)
    session.commit()
    session.refresh(han_text)
    return han_text


def update_han_text(*, session: Session, han_text: HanText, han_text_in: HanText) -> Any:
    han_text_data = han_text_in.model_dump(exclude_unset=True) 
    han_text.sqlmodel_update(han_text_data)
    session.add(han_text)
    session.commit()
    session.refresh(han_text)
    return han_text

def get_han_character(*, session: Session, search_word: str, skip: int = 0, limit: int = 100) -> list[HanCharacter] | None:
    search_word = search_word.lower()
    statement = select(HanCharacter) \
        .where(or_(
            func.lower(col(HanCharacter.han_character)).contains(search_word),
            func.lower(col(HanCharacter.english_translation)).contains(search_word),
            func.lower(col(HanCharacter.quoc_ngu)).contains(search_word),
            func.lower(col(HanCharacter.nom_character)).contains(search_word)
        )).offset(skip).limit(limit)
    data = session.exec(statement)
    return data

def get_han_text(*, session: Session, search_word: str, skip: int = 0, limit: int = 100) -> list[HanText] | None:
    search_word = search_word.lower()
    statement = select(HanText) \
        .where(or_(
            func.lower(col(HanText.han_character)).contains(search_word),
            func.lower(col(HanText.english_translation)).contains(search_word),
            func.lower(col(HanText.quoc_ngu)).contains(search_word),
            func.lower(col(HanText.nom_character)).contains(search_word)
        )).offset(skip).limit(limit)
    data = session.exec(statement)
    return data