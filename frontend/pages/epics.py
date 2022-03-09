import asyncio
from cProfile import label
import json
from idom import html, run, use_state, component, event, vdom
import requests
from sanic import Sanic, response
from black import click
from datetime import datetime

from components.input import Input, Selector2, SelectorDropdownKeyValue, Selector
from components.layout import Row, Column, Container
from components.lists import ListSimple
from components.table import SimpleTable
from components.controls import Button
from config import base_url

from data.teams import teams_id_name
from data.sponsors import sponsors_id_name
from data.common import year_month_dict_list, days_in_month


@component
def page():
    short_name, set_short_name = use_state("")
    name, set_name = use_state("")
    team_id, set_team_id = use_state("")
    sponsor_id, set_sponsor_id = use_state("")

    year_month, set_year_month = use_state("")
    day, set_day = use_state("")

    # submitted_name, set_submitted_name = use_state("")
    # is_changed, set_is_changed = use_state(False)
    # delete_name, set_delete_name = use_state("")

    return Container(
        create_epic_form(
            short_name,
            set_short_name,
            name,
            set_name,
            team_id,
            set_team_id,
            sponsor_id,
            set_sponsor_id,
            year_month,
            set_year_month,
            day,
            set_day
            # set_submitted_name,
        ),
        # Column(
        #     Row(list_epics(submitted_name)),
        # ),
        # Row(delete_epic(set_delete_name)),
    )


@component
def create_epic_form(
    short_name,
    set_short_name,
    name,
    set_name,
    team_id,
    set_team_id,
    sponsor_id,
    set_sponsor_id,
    year_month,
    set_year_month,
    day,
    set_day
    # set_submitted_name,
):
    """
    post endpoint: /api/epics
    schema: {
    "name": "string",
    "active": True
    "created_at": "2022-02-17T15:31:39.103Z",
    "updated_at": "2022-02-17T15:31:39.103Z"
    }"""

    @event(prevent_default=True)
    async def handle_submit(event):
        data = {
            "name": name,
            "active": True,
            "created_at": str(datetime.now()),
            "updated_at": str(datetime.now()),
        }
        response = requests.post(
            f"{base_url}/api/epics",
            data=json.dumps(data),
            headers={"accept": "application/json", "Content-Type": "application/json"},
        )
        set_submitted_name(name)

    inp_short_name = Input(set_short_name, "epics short name")
    inp_name = Input(set_name, "epics full name")
    selector_team = Selector2(set_team_id, teams_id_name())
    selector_sponsor = Selector2(set_sponsor_id, sponsors_id_name())
    selector_start_month = Selector2(
        set_year_month, year_month_dict_list(label="select start month")
    )
    selector_start_day = Selector2(set_day, days_in_month(label="select start day"))
    # is_disabled = True
    # if name != "" and  != "" and  != "":
    is_disabled = False
    btn = Button(is_disabled, handle_submit, label="Submit")

    return Column(
        Row(
            inp_short_name,
            inp_name,
            selector_team,
            selector_sponsor,
            selector_start_month,
            selector_start_day,
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

    inp_delete_name = Input(set_value=set_name_to_delete, label="delete epic input")
    btn = html.button(
        {
            "class": "relative w-fit h-fit px-2 py-1 text-lg border text-gray-50  border-secondary-200",
            "onClick": delete_epic,
        },
        "Submit",
    )
    return Column(Row(inp_delete_name), Row(btn))
