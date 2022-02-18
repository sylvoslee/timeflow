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

from pages.utils import year_month_list, forecast_days_list, hours_list
from config import base_url


@component
def page():
    year_month, set_year_month = use_state("")
    days, set_days = use_state("")
    user_id, set_user_id = use_state("")
    epic_id, set_epic_id = use_state("")
    client_id, set_client_id = use_state("")
    deleted_forecast, set_deleted_forecast = use_state("")
    on_submit, set_on_submit = use_state(True)
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
            on_submit,
            set_on_submit,
        ),
        Column(
            Row(forecasts_table(user_id, epic_id, year_month)),
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
    on_submit,
    set_on_submit,
):
    """Generates forecast form to submit forecasts and filter forecast by month user and epic

    Args:
        year_month (str): the year_month combined for which the forecast is for
        set_year_month (_type_): function to update year_month state
        days (int): number of forecasted days
        set_days (_type_): function to update days state
        user_id (int): the user id for which the forecast is for
        set_user_id (_type_): function to update user_id state
        epic_id (str): the epic id for which the forecast is for
        set_epic_id (_type_): function to update epic_id state
        client_id (int): the client id for which the forecast is for
        set_client_id (_type_): function to update client_id state
        on_submit (bool): to be switched on submit, triggering render by state change
        set_on_submit (_type_): function to update on_submit state

    Returns:
        _type_: _description_
    """
    print(user_id)

    @event(prevent_default=True)
    async def handle_submit(event):
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

        ym = year_month
        year = ym[:4]
        month = ym[5:7]

        data = {
            "user_id": user_id,
            "epic_id": epic_id,
            "client_id": client_id,
            "month": int(month),
            "year": int(year),
            "days": days,
        }
        print(data)
        response = requests.post(
            f"{base_url}/api/forecasts",
            data=json.dumps(data),
            headers={"accept": "application/json", "Content-Type": "application/json"},
        )
        if on_submit:
            set_on_submit(False)
        else:
            set_on_submit(True)

    api_username = f"{base_url}/api/users"
    response_username = requests.get(api_username)

    username_rows = []
    for item in response_username.json():
        d = {item["username"]: item["id"]}
        username_rows.append(d)

    username_dropdown = SelectorDropdownKeyValue(rows=username_rows)
    selector_user_id = Selector(
        set_value=set_user_id,
        placeholder="select user",
        dropdown_list=username_dropdown,
    )

    api_epic_name = f"{base_url}/api/epics/active"
    response_epic_name = requests.get(api_epic_name)

    epic_name_rows = []
    for item in response_epic_name.json():
        d = {item["name"]: item["id"]}
        epic_name_rows.append(d)

    epic_name_dropdown = SelectorDropdownKeyValue(rows=epic_name_rows)
    selector_epic_id = Selector(
        set_value=set_epic_id,
        placeholder="select epic",
        dropdown_list=epic_name_dropdown,
    )

    api_client_name_id = f"{base_url}/api/epics/{epic_id}/client-name"
    response_client_name_id = requests.get(api_client_name_id)
    r = response_client_name_id.json()
    client_name = r.get("name")
    client_id = r.get("id_1")
    option = html.option({"value": f"{client_id}"}, client_name)
    selector_client_id = AutoSelect(set_value=set_client_id, option=option)

    year_month_dropdown = SelectorDropdownList(year_month_list)
    selector_year_month = Selector(
        set_value=set_year_month,
        placeholder="select a month",
        dropdown_list=year_month_dropdown,
    )

    days_dropdown = SelectorDropdownList(forecast_days_list)
    selector_days = Selector(
        set_value=set_days,
        placeholder="select forecast days",
        dropdown_list=days_dropdown,
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
def forecasts_table(user_id, epic_id, year_month):
    """Generates a table component with forecast days by year and month

    Args:
        user_id (int): the id of the user for which the forecast is for
        epic_id (int): the id of the epic for which the forecast is for
        year_month (str): the year_month combined for which the forecast is for

    Returns:
        _type_: _description_
    """
    ym = year_month
    year = ym[:4]
    month = ym[5:7]
    rows = []
    if user_id != "" and epic_id != "" and year != "" and month != "":
        api = f"{base_url}/api/forecasts/users/{user_id}/epics/{epic_id}/year/{year}/month/{month}"
        response = requests.get(api)
        for item in response.json():
            d = {
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
