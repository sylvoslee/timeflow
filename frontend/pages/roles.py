import json
from idom import html, use_state, component, event
import requests
from sanic import response
from black import click
from datetime import datetime

from components.input import Input, SelectorDropdownKeyValue, Selector
from components.layout import Row, Column, Container
from components.table import SimpleTable
from components.controls import Button
from config import base_url

from data.roles import to_role, roles_active


@component
def page():
    name, set_name = use_state("")
    submitted_name, set_submitted_name = use_state("")
    short_name, set_short_name = use_state("")
    submitted_short_name, set_submitted_short_name = use_state("")
    _, set_deact_name = use_state("")
    _, set_activ_name = use_state("")

    return Container(
        create_role_form(
            name,
            set_name,
            short_name,
            set_short_name,
            set_submitted_name,
        ),
        Column(
            Row(list_roles(submitted_name, submitted_short_name)),
        ),
        # Row(deactivate_sponsor(set_deact_name)),
        # Row(activate_sponsor(set_activ_name)),
    )


@component
def create_role_form(
    name,
    set_name,
    short_name,
    set_short_name,
    set_submitted_name,
):
    """
    Create a form that allows admin to add a new role.

    post endpoint: /api/sponsors
    schema: {
        "short_name": "string",
        "name": "string",
        "created_at": "2022-03-07T10:56:22.164Z",
        "updated_at": "2022-03-07T10:56:22.164Z",
        "is_active": true
    }
    """

    @event(prevent_default=True)
    async def handle_submit(event):
        """Call a post request for the given role when given event is triggered."""
        to_role(
            short_name=short_name,
            name=name,
            created_at=str(datetime.now()),
            updated_at=str(datetime.now()),
            is_active=True,
        )
        set_submitted_name(name)

    inp_name = Input(set_value=set_name, label="name of the role")
    inp_short_name = Input(set_value=set_short_name, label="short name of the role")

    is_disabled = True
    if name != "" and short_name != "":
        is_disabled = False
    btn = Button(is_disabled, handle_submit, label="Submit")

    return Column(
        Row(inp_name, inp_short_name),
        Row(btn),
    )


@component
def list_roles(submitted_name, submitted_short_name):
    """
    Return rows consisting of each role short name along with its full name.

    Obtain a json response from a get request to the client endpoint.
    Return an HTML div that contains the rows in a table.
    """
    rows = roles_active()

    return html.div({"class": "flex w-full"}, SimpleTable(rows=rows))


@component
def deactivate_sponsor(set_deact_name):
    """Deactivate a sponsor without deleting it."""
    name_to_deact, set_name_to_deact = use_state("")

    def handle_deactivation(event):
        """Set the given sponsor's active column to False."""
        api = f"{base_url}/api/sponsors/{name_to_deact}/deactivate"
        response = requests.put(api)
        set_deact_name(name_to_deact)
        return True

    inp_deact_name = Input(
        set_value=set_name_to_deact, label="sponsor to be deactivated"
    )
    btn = html.button(
        {
            "class": "relative w-fit h-fit px-2 py-1 text-lg border text-gray-50 border-secondary-200",
            "onClick": handle_deactivation,
        },
        "Submit",
    )
    return Column(Row(inp_deact_name), Row(btn))


@component
def activate_sponsor(set_activ_name):
    """Activate a sponsor."""
    name_to_activ, set_name_to_activ = use_state("")

    def handle_activation(event):
        """Set the given sponsor's active column to True."""
        api = f"{base_url}/api/sponsors/{name_to_activ}/activate"
        response = requests.put(api)
        set_activ_name(name_to_activ)
        return True

    inp_deact_name = Input(set_value=set_name_to_activ, label="sponsor to be activated")
    btn = html.button(
        {
            "class": "relative w-fit h-fit px-2 py-1 text-lg border text-gray-50 border-secondary-200",
            "onClick": handle_activation,
        },
        "Submit",
    )
    return Column(Row(inp_deact_name), Row(btn))
