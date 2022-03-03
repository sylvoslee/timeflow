import asyncio
from cProfile import label
import json
from idom import html, use_state, component, event
import requests
from sanic import response
from black import click
from datetime import datetime

from components.input import Input, SelectorDropdownKeyValue, Selector
from components.layout import Row, Column, Container
from components.table import SimpleTable
from config import base_url


@component
def page():
    name, set_name = use_state("")
    subitted_name, set_submitted_name = use_state("")
    user_id, set_user_id = use_state("")
    _, set_deact_name = use_state("")
    _, set_active_name = use_state("")

    return Container(
        create_team_form(
            name,
            set_name,
            user_id,
            set_user_id,
            set_submitted_name,
        ),
        # Column(
        #     Row(list_epic_areas(submitted_name)),
        # ),
        # Row(deactivate_team(set_deact_name)),
        # Row(activate_team(set_activ_name)),
    )


@component
def create_team_form(
    name,
    set_name,
    user_id,
    set_user_id,
    set_submitted_name,
):
    """
    Create a form that allows admin to add a new team.

    post endpoint: /api/teams
    schema: {
        "epic_id": "int",
        "name": "string,
        "is_active": True
        "created_at": "2022-02-17T15:31:39.103Z",
        "updated_at": "2022-02-17T15:31:39.103Z"
    }
    """

    @event(prevent_default=True)
    async def handle_submit(event):
        """Call a post request for the given team when given event is triggered."""
        data = {
            "name": name,
            "user_id": user_id,
            "is_active": True,
            "created_at": str(datetime.now()),
            "updated_at": str(datetime.now()),
        }
        print("here", data)
        response = requests.post(
            f"{base_url}/api/teams",
            data=json.dumps(data),
            headers={"accept": "application/json", "Content-Type": "application/json"},
        )
        set_submitted_name(name)

    # Connect to active users endpoint
    api_user_name = f"{base_url}/api/epics/active"
    response_team_name = requests.get(api_user_name)

    # Create dropdown of active users which can then be selected
    user_name_rows = [{item["name"]: item["id"]} for item in response_team_name.json()]
    team_name_dropdown_list = SelectorDropdownKeyValue(rows=user_name_rows)
    selector_team_name = Selector(set_value=set_user_id, placeholder="Select User")
