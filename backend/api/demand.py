from fastapi import APIRouter, Depends
from ..utils import engine, get_session
from ..models.demand import Demand
from sqlmodel import Session, select, SQLModel, and_
from sqlalchemy.exc import NoResultFound
from ..models.user import User
from ..models.team import Team
from ..models.epic import Epic

router = APIRouter(prefix="/api/demands", tags=["demand"])
session = Session(engine)


@router.post("/")
async def post_demand(*, demand: Demand, session: Session = Depends(get_session)):
    """Post a demand."""
    statement = select(Demand).where(
        and_(
            Demand.team_id == demand.team_id,
            Demand.epic_id == demand.epic_id,
            Demand.year == demand.year,
            Demand.month == demand.month,
        )
    )
    try:
        result = session.exec(statement).one()
        return False
    except NoResultFound:
        session.add(demand)
        session.commit()
        session.refresh(demand)
        return demand


@router.get("/")
async def get_demands(
    session: Session = Depends(get_session),
    is_locked: bool = None,
    team_id: int = None,
    epic_id: int = None,
    month: int = None,
    year: int = None,
):
    """Get list of all demands"""
    statement = select(Demand)
    """Select demand by epic_id, team_id, month, year"""
    if (team_id and epic_id and month and year) != None:
        statement = (
            select(
                Demand.id.label("demand_id"),
                Team.short_name.label("team_short_name"),
                Epic.short_name.label("epic_short_name"),
                Demand.year,
                Demand.month,
                Demand.days,
            )
            .select_from(Demand)
            .join(Team, Demand.team_id == Team.id)
            .join(Epic, Demand.epic_id == Epic.id)
            .where(Demand.team_id == team_id)
            .where(Demand.epic_id == epic_id)
            .where(Demand.month == month)
            .where(Demand.year == year)
        )

    result = session.exec(statement).all()
    return result


@router.delete("/")
async def delete_demands(
    demand_id: str = None,
    session: Session = Depends(get_session),
):
    """Delete a demand"""
    statement = select(Demand).where(
        Demand.id == demand_id,
    )

    demand_to_delete = session.exec(statement).one()
    session.delete(demand_to_delete)
    session.commit()
    return True
