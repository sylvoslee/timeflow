import asyncio
from cProfile import label
import json
from idom import html, run, use_state, component, event, vdom
import requests
from sanic import Sanic, response
from black import click
from datetime import datetime

from components.input import Input, SelectorDropdownKeyValue, Selector
from components.layout import Row, Column, Container
from components.lists import ListSimple
from components.table import SimpleTable
from config import base_url


@component
def page():
    epic_id, set_epic_id = use_state("")
    name, set_name = use_state("")
    submitted_name, set_submitted_name = use_state("")
    delete_name, set_delete_name = use_state("")
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
        Row(delete_epic_area(set_delete_name)),
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
    post endpoint: /api/epic_areas
    schema: {
    "client_id": 0,
    "epic": "string",
    "name": "string,
    "active": True
    "created_at": "2022-02-17T15:31:39.103Z",
    "updated_at": "2022-02-17T15:31:39.103Z"
    }"""

    @event(prevent_default=True)
    async def handle_submit(event):
        data = {
            "epic_id": epic_id,
            "name": name,
            "active": True,
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

    epic_name_rows = [{item["name"]: item["id"]} for item in response_epic_name.json()]
    epic_name_dropdown_list = SelectorDropdownKeyValue(rows=epic_name_rows)
    selector_epic_name = Selector(
        set_value=set_epic_id,
        placeholder="select epic",
        dropdown_list=epic_name_dropdown_list,
    )

    inp_name = Input(set_value=set_name, label="name")
    btn = html.button(
        {
            "class": "relative w-fit h-fit px-2 py-1 text-lg border text-gray-50  border-secondary-200",
            "onClick": handle_submit,
        },
        "Submit",
    )

    return Column(
        Row(
            selector_epic_name,
            inp_name,
        ),
        Row(btn),
    )


@component
def list_epic_areas(submitted_name):
    api = f"{base_url}/api/epic_areas/active"
    response = requests.get(api)

    rows = []
    for item in response.json():
        d = {
            "" "epic": item["epic"],
            "name": item["name"],
        }
        rows.append(d)
    return html.div({"class": "flex w-full"}, SimpleTable(rows=rows))


@component
def delete_epic_area(set_delete_name):
    name_to_delete, set_name_to_delete = use_state("")

    def delete_epic(event):
        api = f"{base_url}/api/epics/?epic_name={name_to_delete}"
        response = requests.delete(api)
        set_delete_name(name_to_delete)
        print(name)

    inp_delete_name = Input(set_value=set_name_to_delete, label="delete epic input")
    btn = html.button(
        {
            "class": "relative w-fit h-fit px-2 py-1 text-lg border text-gray-50  border-secondary-200",
            "onClick": delete_epic,
        },
        "Submit",
    )
    return Column(Row(inp_delete_name), Row(btn))
