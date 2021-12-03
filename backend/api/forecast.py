from fastapi import APIRouter
from models import engine
from sqlmodel import Session, select, SQLModel


router = APIRouter()
session = Session(engine)
