import asyncio
from cProfile import label
import json
from idom import html, run, use_state, component, event, vdom
import requests
from sanic import Sanic, response
from black import click

from components.input import (
    Input,
    Selector,
    SelectorDropdownList,
    SelectorDropdownKeyValue,
    AutoSelect,
)
from components.layout import Row, Column, Container
from components.lists import ListSimple
from components.table import SimpleTable
from config import base_url


@component
def page():
    year_month, set_year_month = use_state("")
    days, set_days = use_state("")
    user_id, set_user_id = use_state("")
    epic_id, set_epic_id = use_state("")
    client_id, set_client_id = use_state("")
    deleted_forecst, set_deleted_forecast = use_state("")
    is_true, set_is_true = use_state(True)
    print(client_id)
    return Container(
        create_forecast_form(
            year_month,
            set_year_month,
            days,
            set_days,
            user_id,
            set_user_id,
            epic_id,
            set_epic_id,
            client_id,
            set_client_id,
            is_true,
            set_is_true,
        ),
        Column(
            Row(list_forecasts(is_true, user_id, epic_id, year_month)),
        ),
        Row(delete_forecast_input(set_deleted_forecast)),
    )


@component
def create_forecast_form(
    year_month,
    set_year_month,
    days,
    set_days,
    user_id,
    set_user_id,
    epic_id,
    set_epic_id,
    client_id,
    set_client_id,
    is_true,
    set_is_true,
):
    """
        schema:
    {
      "user_id": 0,
      "epic_id": 0,
      "client_id": 0,
      "days": 0,
      "month": 0,
      "year": 0
    }
    """

    @event(prevent_default=True)
    async def handle_submit(event):
        # set_client_id(r_value)
        a = year_month
        year = a[:4]
        month = a[5:7]

        year_int = int(year)
        month_int = int(month)
        data = {
            "user_id": user_id,
            "epic_id": epic_id,
            "client_id": client_id,
            "month": month_int,
            "year": year,
            "days": days,
        }
        response = requests.post(
            f"{base_url}/api/forecasts",
            data=json.dumps(data),
            headers={"accept": "application/json", "Content-Type": "application/json"},
        )
        if is_true:
            set_is_true(False)
        else:
            set_is_true(True)

    # year and month dropdown list
    # fmt: off
    year_month_list = [
    "2022_01","2022_02","2022_03","2022_04","2022_05",
    "2022_06","2022_07","2022_08","2022_09","2022_10","2022_11", "2022_12"
    ]
    # fmt: on
    year_month_dropdown_list = SelectorDropdownList(year_month_list)

    # days dropdown list
    forecast_days_nr = range(1, 30)
    forecast_days_list = []
    for n in forecast_days_nr:
        forecast_days_list.append(n)

    days_dropdown_list = SelectorDropdownList(forecast_days_list)
    # hours dropdown list
    # fmt: off
    h = ["07", "08", "09", "10", "11", "12", "13", "14", "15", "16", 
        "17", "18", "19", "20", "21", "22"]
    q = ["00", "15", "30", "45"]
    # fmt: on

    hours_list = []
    for n in h:
        for m in q:
            hours = f"{n}:{m}"
            hours_list.append(hours)

    hours_dropdown_list = SelectorDropdownList(hours_list)

    # username dropdown list
    api_username = f"{base_url}/api/users"
    response_username = requests.get(api_username)

    username_rows = []
    for item in response_username.json():
        d = {item["username"]: item["id"]}
        username_rows.append(d)

    username_dropdown_list = SelectorDropdownKeyValue(rows=username_rows)

    # epic name dropdown list
    api_epic_name = f"{base_url}/api/epics/active"
    response_epic_name = requests.get(api_epic_name)

    epic_name_rows = []
    for item in response_epic_name.json():
        d = {item["name"]: item["id"]}
        epic_name_rows.append(d)

    epic_name_dropdown_list = SelectorDropdownKeyValue(rows=epic_name_rows)

    # client name dropdown list
    api_client_name = f"{base_url}/api/epics/{epic_id}/client-name"
    response_client_name = requests.get(api_client_name)
    r = response_client_name.json()
    client_name = r.get("name")
    client_id = r.get("id_1")
    option = html.option({"value": f"{client_id}"}, client_name)
    selector_user_id = Selector(
        set_value=set_user_id,
        placeholder="select user",
        dropdown_list=username_dropdown_list,
    )

    selector_epic_id = Selector(
        set_value=set_epic_id,
        placeholder="select epic",
        dropdown_list=epic_name_dropdown_list,
    )
    selector_client_id = AutoSelect(set_value=set_client_id, option=option)

    selector_year_month = Selector(
        set_value=set_year_month,
        placeholder="select a month",
        dropdown_list=year_month_dropdown_list,
    )

    selector_days = Selector(
        set_value=set_days,
        placeholder="select forecast days",
        dropdown_list=days_dropdown_list,
    )

    btn = html.button(
        {
            "class": "relative w-fit h-fit px-2 py-1 text-lg border text-gray-50  border-secondary-200",
            "onClick": handle_submit,
        },
        "Submit",
    )

    return Column(
        Row(
            selector_user_id,
            selector_epic_id,
            selector_client_id,
            selector_year_month,
            selector_days,
        ),
        Row(btn),
    )


@component
def list_forecasts(is_true, user_id, epic_id, year_month):

    year = year_month[:4]
    month = year_month[5:7]
    rows = []
    if user_id != "" and epic_id != "" and year_month != "":
        api = f"{base_url}/api/forecasts/users/{user_id}/epics/{epic_id}/year/{year}/month/{month}"
        print(api)
        response = requests.get(api)
        print(response.json())
        for item in response.json():
            d = {
                "year": item["year"],
                "month": item["month"],
                "days": item["days"],
            }
            rows.append(d)

    elif user_id != "" and epic_id != "" and year_month == "":
        api = f"{base_url}/api/forecasts/users/{user_id}/epics/{epic_id}"
        print(api)
        response = requests.get(api)
        print(response.json())
        for item in response.json():
            d = {
                "month": item["month"],
                "days": item["days"],
            }
            rows.append(d)
    elif user_id != "" and epic_id == "" and year_month != "":
        api = (
            f"{base_url}/api/forecasts/users/{user_id}/epics/year/{year}/month/{month}"
        )
        print(api)
        response = requests.get(api)
        print(response.json())
        for item in response.json():
            d = {
                "epic name": item["name"],
                "year": item["year"],
                "month": item["month"],
                "days": item["days"],
            }
            rows.append(d)
    return html.div({"class": "flex w-full"}, SimpleTable(rows=rows))


@component
def delete_forecast_input(set_deleted_forecast):
    forecast_to_delete, set_forecast_to_delete = use_state("")

    def handle_delete(event):
        api = f"{base_url}/api/forecasts/?forecast_id={forecast_to_delete}"

        response = requests.delete(api)
        set_deleted_forecast(forecast_to_delete)

    inp_forecast = Input(
        set_value=set_forecast_to_delete,
        label="forecast id to delete",
    )
    btn = html.button(
        {
            "class": "relative w-fit h-fit px-2 py-1 text-lg border text-gray-50  border-secondary-200",
            "onClick": handle_delete,
        },
        "Submit",
    )
    return Column(Row(inp_forecast), Row(btn))
