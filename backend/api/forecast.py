from fastapi import APIRouter
from models import TimeLog, User, engine
from sqlmodel import Session, select, SQLModel
from utils import *

router = APIRouter()
session = Session(engine)
