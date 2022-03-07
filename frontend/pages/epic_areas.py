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
from components.controls import Button
from config import base_url


@component
def page():
    epic_id, set_epic_id = use_state("")
    name, set_name = use_state("")
    submitted_name, set_submitted_name = use_state("")
    _, set_deact_name = use_state("")
    _, set_activ_name = use_state("")
    print(name)

    return Container(
        create_epic_area_form(
            epic_id,
            set_epic_id,
            name,
            set_name,
            set_submitted_name,
        ),
        Column(
            Row(list_epic_areas(submitted_name)),
        ),
        Row(deactivate_epic_area(set_deact_name)),
        Row(activate_epic_area(set_activ_name)),
    )


@component
def create_epic_area_form(
    epic_id,
    set_epic_id,
    name,
    set_name,
    set_submitted_name,
):
    """
    Create a form that allows admin to add a new epic area.

    post endpoint: /api/epic_areas
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
        """Call a post request for the given epic area when given event is triggered."""
        data = {
            "epic_id": epic_id,
            "name": name,
            "is_active": True,
            "created_at": str(datetime.now()),
            "updated_at": str(datetime.now()),
        }
        print("here", data)
        response = requests.post(
            f"{base_url}/api/epic_areas",
            data=json.dumps(data),
            headers={"accept": "application/json", "Content-Type": "application/json"},
        )
        set_submitted_name(name)

    # Connect to active epics endpoint
    api_epic_name = f"{base_url}/api/epics/active"
    response_epic_name = requests.get(api_epic_name)

    # Create dropdown of active epics which can then be selected
    epic_name_rows = [{item["name"]: item["id"]} for item in response_epic_name.json()]
    epic_name_dropdown_list = SelectorDropdownKeyValue(rows=epic_name_rows)
    selector_epic_name = Selector(
        set_value=set_epic_id,
        placeholder="Select Epic",
        dropdown_list=epic_name_dropdown_list,
    )

    inp_name = Input(set_value=set_name, label="name")
    is_disabled = True
    if epic_id != "" and name != "":
        is_disabled = False
    btn = Button(is_disabled, handle_submit, label="Submit")

    return Column(
        Row(
            selector_epic_name,
            inp_name,
        ),
        Row(btn),
    )


@component
def list_epic_areas(submitted_name):
    """
    Return rows consisting of each epic area along with its epic.

    Obtain a json response from a get request to the active epic areas endpoint.
    Store in rows the names of the epic and epic area, along with the id.
    Return an HTML div that contains the rows in a table.
    """
    api = f"{base_url}/api/epic_areas/active"
    response = requests.get(api)

    rows = []
    for item in response.json():
        d = {
            "Epic": item["epic_name"],
            "Epic Area": item["epic_area_name"],
            "ID": item["id"],
        }
        rows.append(d)
    return html.div({"class": "flex w-full"}, SimpleTable(rows=rows))


@component
def deactivate_epic_area(set_deact_name):
    """Deactivate an epic area without deleting it."""
    name_to_deact, set_name_to_deact = use_state("")

    def handle_deactivation(event):
        """Set the given epic area's active column to False."""
        api = f"{base_url}/api/epic_areas/{name_to_deact}/deactivate"
        response = requests.put(api)
        set_deact_name(name_to_deact)
        return True

    inp_deact_name = Input(
        set_value=set_name_to_deact, label="epic area to be deactivated"
    )
    is_disabled = True
    if name_to_deact != "":
        is_disabled = False
    btn = Button(is_disabled, handle_submit=handle_deactivation, label="Deactivate")
    return Column(Row(inp_deact_name), Row(btn))


@component
def activate_epic_area(set_activ_name):
    """Activate an epic area."""
    name_to_activ, set_name_to_activ = use_state("")

    def handle_activation(event):
        """Set the given epic area's active column to True."""
        api = f"{base_url}/api/epic_areas/{name_to_activ}/activate"
        response = requests.put(api)
        set_activ_name(name_to_activ)
        return True

    inp_activ_name = Input(
        set_value=set_name_to_activ, label="epic area to be activated"
    )
    is_disabled = True
    if name_to_activ != "":
        is_disabled = False
    btn = Button(is_disabled, handle_submit=handle_activation, label="Activate")
    return Column(Row(inp_activ_name), Row(btn))
