from fastapi import APIRouter
from utils import engine
from sqlmodel import Session, select, SQLModel


router = APIRouter()
session = Session(engine)
