from fastapi import APIRouter
from utils import engine
from sqlmodel import Session, select, SQLModel
from sqlalchemy.exc import NoResultFound
from models.user import User

router = APIRouter(prefix="/api/users")
session = Session(engine)


# Post new user
@router.post("/")
async def user(user: User):
    statement = select(User).where(User.username == user.username)
    try:
        result = session.exec(statement).one()
        return False
    except NoResultFound:
        session.add(user)
        session.commit()
        return True


# Get user by initials or surname, if there are no initials
@router.get("/{username},{surname}")
async def read_users(username: str = None, surname: str = None):
    if username != None:
        statement = select(User).where(User.username == username)
    elif surname != None:
        statement = select(User).where(User.surname == surname)
    results = session.exec(statement).first()
    return results


@router.get("/lists/id-username")
async def read_users_list():
    statement = select(User.id)
    results_list = session.exec(statement).all()
    return results_list


# Get list of users
@router.get("/lists/{list_name}")
async def list_users(list_name: str):
    if list_name == "initials":
        statement = select(User.username)
    elif list_name == "surname":
        statement = select(User.surname)
    results = session.exec(statement).all()
    return results


# Update users
@router.put("/")
async def update_users(username: str, user_email: str):
    statement = select(User).where(User.username == username)
    user_to_update = session.exec(statement).one()
    print(user_to_update)
    user_to_update.user_email = user_email
    session.add(user_to_update)
    session.commit()
    session.refresh(user_to_update)
    return True


# Delete users
@router.delete("/")
async def delete_users(username: str = None):
    statement = select(User).where(User.username == username)
    results = session.exec(statement)
    user_to_delete = results.one()
    session.delete(user_to_delete)
    session.commit()
    return True
