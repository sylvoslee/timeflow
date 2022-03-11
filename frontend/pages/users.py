import asyncio
from cProfile import label
import json
from black import click
from idom import html, run, use_state, component, event, vdom
from idom.server.sanic import PerClientStateServer
import requests
from sanic import Sanic, response
from datetime import datetime

from pages.utils import switch_state
from components.input import Input, Selector2
from components.layout import Row, Column, Container
from components.lists import ListSimple
from components.table import SimpleTable
from components.controls import Button
from config import base_url

from data.users import to_user, users_active, update_user
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
    team_id, set_team_id = use_state(None)
    on_submit, set_on_submit = use_state(True)
    on_update, set_on_update = use_state(True)
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
                on_submit,
                set_on_submit,
            )
        ),
        Column(
            Row(update_user(on_update, set_on_update)),
        ),
    )


@component
def create_user_form(
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
    on_submit,
    set_on_submit,
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
    # Initializes day state, should be in parent(?), here due to a bug
    day, set_day = use_state("")
    year_month, set_year_month = use_state("")

    @event(prevent_default=True)
    async def handle_submit(event):
        print("post select team is", team_id)
        # Bypass of a bug, selector not able to set a value=None
        if team_id is "":
            set_team_id(None)
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
        switch_state(on_submit, set_on_submit)

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
def list_users(submitted_name):
    """Calls a list of active users"""
    rows = users_active()
    return html.div({"class": "flex w-full"}, SimpleTable(rows=rows))


@component
def update_user(on_update):
    new_team_id, set_new_team_id = use_state("")
    update_user_id, set_update_user_id = use_state("")

    @event(prevent_default=True)
    def handle_update(event):
        update_user(user_id=user_id, new_team_id=new_team_id)
        # Changes state triggering refresh on update
        switch_state(on_update)

    # selector_update_user = Selector2(
    #     set_update_user_id,
    # )
