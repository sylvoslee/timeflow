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
    short_name, set_short_name = use_state("")
    client_id, set_client_id = use_state("")
    _, set_deact_name = use_state("")
    _, set_activ_name = use_state("")

    return Container(
        create_sponsor_form(
            name,
            set_name,
            short_name,
            set_short_name,
            client_id,
            set_client_id,
        ),
        Column(
            Row(list_sponsors()),
        ),
        Row(deactivate_sponsor(set_deact_name)),
        Row(activate_sponsor(set_activ_name)),
    )


@component
def create_sponsor_form(
    name,
    set_name,
    short_name,
    set_short_name,
    client_id,
    set_client_id,
):
    """
    Create a form that allows admin to add a new sponsor.

    post endpoint: /api/sponsors
    schema: {
        "name": "string",
        "short_name": "string",
        "client_id": "int",
        "is_active": True
        "created_at": "2022-02-17T15:31:39.103Z",
        "updated_at": "2022-02-17T15:31:39.103Z"
    }
    """

    @event(prevent_default=True)
    async def handle_submit(event):
        """Call a post request for the given sponsor when given event is triggered."""
        data = {
            "name": name,
            "short_name": short_name,
            "client_id": client_id,
            "is_active": True,
            "created_at": str(datetime.now()),
            "updated_at": str(datetime.now()),
        }
        response = requests.post(
            f"{base_url}/api/sponsors",
            data=json.dumps(data),
            headers={"accept": "application/json", "Content-Type": "application/json"},
        )

    inp_name = Input(set_value=set_name, label="name of the sponsor")
    inp_short_name = Input(set_value=set_short_name, label="short name of the sponsor")

    # Connect to clients list endpoint
    api_client_name = f"{base_url}/api/clients"
    response_client_name = requests.get(api_client_name)

    # Create a dropdown of clients which can then be selected
    client_name_rows = [
        {item["name"]: item["id"]} for item in response_client_name.json()
    ]
    client_name_dropdown_list = SelectorDropdownKeyValue(rows=client_name_rows)
    selector_client_name = Selector(
        set_value=set_client_id,
        placeholder="Select Client",
        dropdown_list=client_name_dropdown_list,
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
            selector_client_name,
        ),
        Row(btn),
    )


@component
def list_sponsors():
    """
    Return rows consisting of each sponsor along with its client.

    Obtain a json response from a get request to the client endpoint.
    Store in rows the names of the client and sponsor, along with the id.
    Return an HTML div that contains the rows in a table.
    """
    api = f"{base_url}/api/sponsors/active"
    response = requests.get(api)

    rows = []
    for item in response.json():
        d = {
            "Sponsor name": item["sponsor_name"],
            "Sponsor short name": item["sponsor_short_name"],
            "Client name": item["client_name"],
        }
        rows.append(d)
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
