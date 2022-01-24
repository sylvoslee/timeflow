from fastapi.testclient import TestClient
import pytest
import os
from ..main import app
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool
from ..utils import get_session


@pytest.mark.order(4)
def test_post_timelog(client):
    # testing post
    response1 = client.post(
        "/api/timelogs/",
        json={
            "user_id": 1,
            "start_time": "2022-01-19T08:30:00.000Z",
            "end_time": "2022-01-19T10:50:00.000Z",
            "client_id": 1,
            "epic_id": 1,
            "count_hours": 0,
            "count_days": 0,
            "month": 0,
            "year": 0,
        },
    )
    data1 = response1.json()
    assert data1 == {
        "start_time": "2022-01-19T08:30:00.000Z",
        "end_time": "2022-01-19T10:50:00.000Z",
        "user_id": 1,
        "client_id": 1,
        "count_hours": 2.33,
        "month": 1,
        "id": 1,
        "epic_id": 1,
        "count_days": 0.29,
        "year": 2022,
    }
    # testing overlap
    response2 = client.post(
        "/api/timelogs/",
        json={
            "start_time": "2022-01-19T08:30:00.000Z",
            "end_time": "2022-01-19T10:50:00.000Z",
            "user_id": 1,
            "client_id": 1,
            "epic_id": 1,
            "count_hours": 0,
            "count_days": 0,
            "month": 0,
            "year": 0,
        },
    )
    data2 = response2.json()
    assert data2 == "currently posted timelog overlaps another timelog"
    # testing start_time > end_time
    response3 = client.post(
        "/api/timelogs/",
        json={
            "start_time": "2022-01-20T08:30:00.000Z",
            "end_time": "2022-01-20T07:50:00.000Z",
            "user_id": 1,
            "client_id": 1,
            "epic_id": 1,
            "count_hours": 0,
            "count_days": 0,
            "month": 0,
            "year": 0,
        },
    )
    data3 = response3.json()
    assert response3.status_code == 422
    assert data3 == {
        "detail": [
            {
                "loc": ["body", "__root__"],
                "msg": "start_time must be smaller then end_time",
                "type": "assertion_error",
            }
        ]
    }
    # testing working time over 12 hours
    response4 = client.post(
        "/api/timelogs/",
        json={
            "user_id": 1,
            "start_time": "2022-01-20T08:30:00.000Z",
            "end_time": "2022-01-21T07:50:00.000Z",
            "client_id": 1,
            "epic_id": 1,
            "count_hours": 0,
            "count_days": 0,
            "month": 0,
            "year": 0,
        },
    )
    data4 = response4.json()
    assert response4.status_code == 422
    assert data4 == {
        "detail": [
            {
                "loc": ["body", "count_hours"],
                "msg": "user worked over 12 hours",
                "type": "assertion_error",
            }
        ]
    }


def test_get_timelogs_all(client):
    response = client.get("/api/timelogs/")
    data = response.json()
    assert data == [
        {
            "end_time": "2022-01-19T10:50:00.000Z",
            "user_id": 1,
            "client_id": 1,
            "count_hours": 2.33,
            "month": 1,
            "start_time": "2022-01-19T08:30:00.000Z",
            "id": 1,
            "epic_id": 1,
            "count_days": 0.29,
            "year": 2022,
        }
    ]


def test_get_timelog_user_month_year_client(client):
    response = client.get("/api/timelogs/users/1/months/1/years/2022/clients/1")
    data = response.json()
    assert data == [
        {
            "end_time": "2022-01-19T10:50:00.000Z",
            "user_id": 1,
            "client_id": 1,
            "count_hours": 2.33,
            "month": 1,
            "id": 1,
            "start_time": "2022-01-19T08:30:00.000Z",
            "epic_id": 1,
            "count_days": 0.29,
            "year": 2022,
        }
    ]


def test_update_timelogs(client):
    response = client.put(
        "/api/timelogs/1/new-start-time?timelog_new_start_time=2022-01-19T08%3A31%3A00.000Z"
    )
    data = response.json()
    assert data == {
        "end_time": "2022-01-19T10:50:00.000Z",
        "user_id": 1,
        "client_id": 1,
        "count_hours": 2.33,
        "month": 1,
        "id": 1,
        "start_time": "2022-01-19T08:31:00.000Z",
        "epic_id": 1,
        "count_days": 0.29,
        "year": 2022,
    }


def test_delete_timelogs(client):
    response = client.delete(
        "/api/timelogs/1?user_id=1&start_time=2022-01-19T08%3A31%3A00.000Z&end_time=2022-01-19T10%3A50%3A00.000Z&client_id=1&epic_id=1"
    )
    data = response.json()
    assert data == True
