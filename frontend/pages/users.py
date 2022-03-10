import asyncio
from cProfile import label
import json
from black import click
from idom import html, run, use_state, component, event, vdom
from idom.server.sanic import PerClientStateServer
import requests
from sanic import Sanic, response
from datetime import datetime
from components.input import Input, Selector2
from components.layout import Row, Column, Container
from components.lists import ListSimple
from components.table import SimpleTable
from components.controls import Button
from config import base_url

from data.users import to_user
from data.roles import roles_id_name
from data.teams import teams_id_name
from data.common import year_month_dict_list, days_in_month


@component
def page():
    short_name, set_short_name = use_state("")
    first_name, set_first_name = use_state("")
    last_name, set_last_name = use_state("")
    email, set_email = use_state("")
    role_id, set_role_id = use_state("")
    team_id, set_team_id = use_state("")
    year_month, set_year_month = use_state("")
    submitted_name, set_submitted_name = use_state("")
    print("year month is", year_month)
    return Container(
        Row(
            create_user_form(
                short_name,
                set_short_name,
                first_name,
                set_first_name,
                last_name,
                set_last_name,
                email,
                set_email,
                role_id,
                set_role_id,
                team_id,
                set_team_id,
                year_month,
                set_year_month,
                # day,
                # set_day,
                set_submitted_name,
            )
        ),
        # Column(
        #     Row(list_users(submitted_surname)),
        # ),
        # Row(delete_user(set_deleted_user)),
    )


@component
def create_user_form(
    short_name,
    set_short_name,
    first_name,
    set_first_name,
    year_month,
    set_year_month,
    last_name,
    set_last_name,
    email,
    set_email,
    role_id,
    set_role_id,
    team_id,
    set_team_id,
    # day,
    # set_day,
    set_submitted_name,
):
    """
        endpoint: /api/users
        schema: {
      "short_name": "string",
      "first_name": "string",
      "last_name": "string",
      "email": "string",
      "role_id": 0,
      "team_id": 0,
      "start_date": "2022-03-10",
      "created_at": "2022-03-10T13:11:49.625Z",
      "updated_at": "2022-03-10T13:11:49.625Z",
      "is_active": true
    }"""
    day, set_day = use_state("")

    @event(prevent_default=True)
    async def handle_submit(event):

        to_user(
            short_name=short_name,
            first_name=first_name,
            last_name=last_name,
            email=email,
            role_id=role_id,
            team_id=team_id,
            year_month=year_month,
            day=day,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        set_submitted_name(short_name)

    print("year month", year_month)
    print("day is", day)

    inp_short_name = Input(set_value=set_short_name, label="short name")
    inp_first_name = Input(set_value=set_first_name, label="first name")
    inp_last_name = Input(set_value=set_last_name, label="last name")
    inp_email = Input(set_value=set_email, label="email")
    selector_role = Selector2(set_role_id, roles_id_name())
    selector_team = Selector2(set_team_id, teams_id_name())
    selector_start_month = Selector2(
        set_year_month, year_month_dict_list(label="select start month")
    )
    selector_start_day = Selector2(set_day, days_in_month(label="select start day"))

    # is_disabled = True
    # if username != "" and name != "" and surname != "" and email != "":
    is_disabled = False
    btn = Button(is_disabled, handle_submit, label="Submit")

    return Column(
        Row(inp_short_name, inp_first_name, inp_last_name, inp_email),
        Row(
            selector_role,
            selector_team,
            selector_start_month,
            selector_start_day,
        ),
        Row(btn),
    )


@component
def list_users(submitted_surname):
    api = f"{base_url}/api/users"
    response = requests.get(api)
    rows = []
    for item in response.json():
        d = {
            "name": item["name"],
            "surname": item["surname"],
            "username": item["username"],
            "email": item["email"],
        }
        rows.append(d)
    return html.div({"class": "flex w-full"}, SimpleTable(rows=rows))


@component
def delete_user(set_delete_user):
    delete_user, set_delete_user = use_state("")

    def delete_user(event):
        api = f"{base_url}/api/users?username={delete_user}"
        response = requests.delete(api)
        set_deleted_user(delete_user)

    inp_username = Input(set_value=set_delete_user, label="delete user (username)")
    btn = html.button(
        {
            "class": "relative w-fit h-fit px-2 py-1 text-lg border text-gray-50  border-secondary-200",
            "onClick": delete_user,
        },
        "Submit",
    )
    return Column(Row(inp_username), Row(btn))
