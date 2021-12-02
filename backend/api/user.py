from fastapi import APIRouter
from models import User, engine
from sqlmodel import Session, select, SQLModel
from sqlalchemy.exc import NoResultFound

router = APIRouter()
session = Session(engine)


# Post new user
@router.post("/api/users/create")
async def user(user: User):
    statement = select(User).where(User.user_initials == user.user_initials)
    try:
        result = session.exec(statement).one()
        return False
    except NoResultFound:
        session.add(user)
        session.commit()
        return True


@router.get("/api/users/read")
async def read_users(user_initials: str = None, user_surname: str = None):
    if user_initials != None:
        statement = select(User).where(User.user_initials == user_initials)
    elif user_surname != None:
        statement = select(User).where(User.user_surname == user_surname)
    results = session.exec(statement).first()
    return results


# Get list of users
@router.get("/api/users/list")
async def list_users(list_name: str):
    if list_name == "initials":
        statement = select(User.user_initials)
    elif list_name == "surname":
        statement = select(User.user_surname)
    results = session.exec(statement).all()
    return results


# # Update users
@router.put("/api/users/update")
async def update_users(user_initials: str, user_email: str):
    statement = select(User).where(User.user_initials == user_initials)
    user_to_update = session.exec(statement).one()
    print(user_to_update)
    user_to_update.user_email = user_email
    session.add(user_to_update)
    session.commit()
    session.refresh(user_to_update)
    return True


# Delete users
@router.delete("/api/users/delete")
async def delete_users(user_initials: str = None):
    statement = select(User).where(User.user_initials == user_initials)
    results = session.exec(statement)
    user_to_delete = results.one()
    print("User: ", user_to_delete)
    session.delete(user_to_delete)
    session.commit()
    print("Deleted hero:", user_to_delete)
    statement = select(User).where(User.user_initials == user_initials)
    result = session.exec(statement)
    hero = result.first()
    if hero is None:
        print(f"There's no user named {user_to_delete.user_initials}")


METHODS
