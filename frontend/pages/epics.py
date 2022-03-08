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
from components.controls import Button
from config import base_url


@component
def page():
    name, set_name = use_state("")
    work_area, set_work_area = use_state("")
    client_id, set_client_id = use_state("")
    submitted_name, set_submitted_name = use_state("")
    is_changed, set_is_changed = use_state(False)
    delete_name, set_delete_name = use_state("")
    print(name)

    return Container(
        create_epic_form(
            name,
            set_name,
            work_area,
            set_work_area,
            client_id,
            set_client_id,
            set_submitted_name,
        ),
        Column(
            Row(list_epics(submitted_name)),
        ),
        Row(delete_epic(set_delete_name)),
    )


@component
def create_epic_form(
    name,
    set_name,
    work_area,
    set_work_area,
    client_id,
    set_client_id,
    set_submitted_name,
):
    """
    post endpoint: /api/epics
    schema: {
    "name": "string",
    "work_area": "string",
    "client_id": 0
    "active": True
    "created_at": "2022-02-17T15:31:39.103Z",
    "updated_at": "2022-02-17T15:31:39.103Z"
    }"""

    @event(prevent_default=True)
    async def handle_submit(event):
        data = {
            "name": name,
            "work_area": work_area,
            "client_id": client_id,
            "active": True,
            "created_at": str(datetime.now()),
            "updated_at": str(datetime.now()),
        }
        print("here", data)
        response = requests.post(
            f"{base_url}/api/epics",
            data=json.dumps(data),
            headers={"accept": "application/json", "Content-Type": "application/json"},
        )
        set_submitted_name(name)

    api_client_name = f"{base_url}/api/clients/active"
    response_client_name = requests.get(api_client_name)

    client_name_rows = []
    for item in response_client_name.json():
        d = {item["name"]: item["id"]}
        client_name_rows.append(d)

    client_name_dropdown_list = SelectorDropdownKeyValue(rows=client_name_rows)
    selector_client_name = Selector(
        set_value=set_client_id,
        placeholder="select client",
        dropdown_list=client_name_dropdown_list,
    )

    inp_name = Input(set_value=set_name, label="name")
    inp_work_area = Input(set_value=set_work_area, label="work_area")
    is_disabled = True
    if name != "" and work_area != "" and client_id != "":
        is_disabled = False

    btn = Button(is_disabled, handle_submit, label="Submit")

    return Column(
        Row(
            inp_name,
            inp_work_area,
            selector_client_name,
        ),
        Row(btn),
    )


@component
def list_epics(submitted_name):
    api = f"{base_url}/api/epics/active"
    response = requests.get(api)

    rows = []
    for item in response.json():
        d = {
            "name": item["name"],
            "work_area": item["work_area"],
            "client_id": item["client_id"],
        }
        rows.append(d)
    return html.div({"class": "flex w-full"}, SimpleTable(rows=rows))


@component
def delete_epic(set_delete_name):
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
