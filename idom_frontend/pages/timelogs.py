import asyncio
from cProfile import label
import json
from idom import html, run, use_state, component, event, vdom
import requests
from sanic import Sanic, response
from black import click

from components.input import Input, Selector
from components.layout import Row, Column, Container
from components.lists import ListSimple
from components.table import SimpleTable

base_url = "http://127.0.0.1:8000"


@component
def page():
    name, set_name = use_state("")
    work_area, set_work_area = use_state("")
    client_id, set_client_id = use_state("")
    submitted_name, set_submitted_name = use_state("")
    is_changed, set_is_changed = use_state(False)
    placeholder = "select year"

    return Container(
        create_epic_form(
            placeholder,
            name,
            set_name,
            work_area,
            set_work_area,
            client_id,
            set_client_id,
            set_submitted_name,
        ),
        # Column(
        #     Row(list_epics(submitted_name)),
        # ),
        # Row(delete_epic(set_delete_name)),
    )


@component
def create_epic_form(
    placeholder,
    name,
    set_name,
    work_area,
    set_work_area,
    client_id,
    set_client_id,
    set_submitted_name,
):
    @event(prevent_default=True)
    async def handle_submit(event):
        data = {"name": name, "work_area": work_area, "client_id": client_id}
        print("here", data)
        response = requests.post(
            f"{base_url}/api/epics",
            data=json.dumps(data),
            headers={"accept": "application/json", "Content-Type": "application/json"},
        )
        set_submitted_name(name)

    selector = Selector(placeholder)
    inp_name = Input(value=name, set_value=set_name, label="name")
    inp_work_area = Input(value=work_area, set_value=set_work_area, label="work_area")
    inp_client_id = Input(value=client_id, set_value=set_client_id, label="client_id")
    btn = html.button(
        {
            "class": "relative w-fit h-fit px-2 py-1 text-lg border text-gray-50  border-secondary-200",
            "onClick": handle_submit,
        },
        "Submit",
    )

    return Column(
        Row(
            selector,
            inp_name,
            inp_work_area,
            inp_client_id,
        ),
        Row(btn),
    )
