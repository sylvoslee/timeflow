from fastapi import APIRouter, Depends
from ..utils import engine, get_session
from sqlmodel import Session, select, SQLModel, or_
from ..models.epic import Epic
from ..models.client import Client
from sqlalchemy.exc import NoResultFound
from datetime import datetime

router = APIRouter(prefix="/api/epic_areas", tags=["epic"])
session = Session(engine)
