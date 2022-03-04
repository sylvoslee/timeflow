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
    submitted_name, set_submitted_name = use_state("")
    short_name, set_short_name = use_state("")
    submitted_short_name, set_submitted_short_name = use_state("")
    user_id, set_user_id = use_state("")
    _, set_deact_name = use_state("")
    _, set_activ_name = use_state("")

    return Container(
        create_team_form(
            name,
            set_name,
            short_name,
            set_short_name,
            user_id,
            set_user_id,
            set_submitted_name,
            set_submitted_short_name,
        ),
        Column(
            Row(list_teams(submitted_name, submitted_short_name)),
        ),
        Row(deactivate_team(set_deact_name)),
        Row(activate_team(set_activ_name)),
    )


@component
def create_team_form(
    name,
    set_name,
    short_name,
    set_short_name,
    user_id,
    set_user_id,
    set_submitted_name,
    set_submitted_short_name,
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
            "short_name": short_name,
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
        set_submitted_short_name(short_name)

    inp_name = Input(set_value=set_name, label="name of the team")

    inp_short_name = Input(set_value=set_short_name, label="short name of the team")

    # Connect to active users list endpoint
    api_user_name = f"{base_url}/api/users"
    response_user_name = requests.get(api_user_name)

    # Create a dropdown of users which can then be selected
    user_name_rows = [{item["name"]: item["id"]} for item in response_user_name.json()]
    user_name_dropdown_list = SelectorDropdownKeyValue(rows=user_name_rows)
    selector_user_name = Selector(
        set_value=set_user_id,
        placeholder="Select Leader (User)",
        dropdown_list=user_name_dropdown_list,
    )

    btn = html.button(
        {
            "class": "relative w-fit h-fit px-2 py-1 text-lg border text-gray-50 border-secondary-200",
            "onClick": handle_submit,
        },
        "Submit",
    )

    return Column(
        Row(
            inp_name,
            inp_short_name,
            selector_user_name,
        ),
        Row(btn),
    )


@component
def list_teams(submitted_name, submitted_short_name):
    """
    Return rows consisting of each team along with its leader (user).

    Obtain a json response from a get request to the users endpoint.
    Store in rows the names of the user and team, along with the id.
    Return an HTML div that contains the rows in a table.
    """
    api = f"{base_url}/api/teams/active"
    response = requests.get(api)

    rows = []
    for item in response.json():
        d = {
            "Team name": item["team_name"],
            "Team short name": item["team_short_name"],
            "User lead": item["user_name"],
        }
        rows.append(d)
    return html.div({"class": "flex w-full"}, SimpleTable(rows=rows))


@component
def deactivate_team(set_deact_name):
    """Deactivate a team without deleting it."""
    name_to_deact, set_name_to_deact = use_state("")

    def handle_deactivation(event):
        """Set the given epic are'a active column to False."""
        api = f"{base_url}/api/teams/{name_to_deact}/deactivate"
        response = requests.put(api)
        set_deact_name(name_to_deact)
        return True

    inp_deact_name = Input(set_value=set_name_to_deact, label="team to be deactivated")
    btn = html.button(
        {
            "class": "relative w-fit h-fit px-2 py-1 text-lg border text-gray-50 border-secondary-200",
            "onClick": handle_deactivation,
        },
        "Submit",
    )
    return Column(Row(inp_deact_name), Row(btn))


@component
def activate_team(set_activ_name):
    """Activate a team."""
    name_to_activ, set_name_to_activ = use_state("")

    def handle_activation(event):
        """Set the given epic are'a active column to True."""
        api = f"{base_url}/api/teams/{name_to_activ}/activate"
        response = requests.put(api)
        set_activ_name(name_to_activ)
        return True

    inp_deact_name = Input(set_value=set_name_to_activ, label="team to be activated")
    btn = html.button(
        {
            "class": "relative w-fit h-fit px-2 py-1 text-lg border text-gray-50 border-secondary-200",
            "onClick": handle_activation,
        },
        "Submit",
    )
    return Column(Row(inp_deact_name), Row(btn))
