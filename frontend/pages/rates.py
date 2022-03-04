import asyncio
from cProfile import label
import json
from idom import html, run, use_state, component, event, vdom
import requests
from sanic import Sanic, response
from black import click
from datetime import datetime

from components.input import Input, Selector, Selector2
from components.layout import Row, Column, Container
from components.lists import ListSimple
from components.table import SimpleTable
from components.controls import SubmitButton
from pages.data import (
    clients_names,
    client_name_by_epic_id,
    username,
    year_month_dict_list,
    to_rate,
    forecast_by_user_epic_year_month,
    forecast_deletion,
    months_start,
    rates_by_user_client_date,
)

from pages.utils import month_start_to_str, far_date, date_str_to_date
from config import base_url


@component
def page():
    user_id, set_user_id = use_state("")
    client_id, set_client_id = use_state("")
    month_start, set_month_start = use_state("")
    amount, set_amount = use_state("")
    updated_rate, set_updated_rate = use_state("")
    on_submit, set_on_submit = use_state(True)
    return Container(
        Row(
            create_rates_form(
                user_id,
                set_user_id,
                client_id,
                set_client_id,
                month_start,
                set_month_start,
                amount,
                set_amount,
                on_submit,
                set_on_submit,
            )
        ),
        Column(
            Row(rates_table(user_id, client_id, month_start)),
        ),
        # Row(update_rate(set_updated_rate)),
    )


@component
def create_rates_form(
    user_id,
    set_user_id,
    client_id,
    set_client_id,
    month_start,
    set_month_start,
    amount,
    set_amount,
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

    @event(prevent_default=True)
    async def handle_submit(event):
        """
        schema:
        {
        "user_id": 0,
        "client_id": 0,
        "valid_from": "2022-03-03",
        "valid_to": "2022-03-03",
        "amount": 0,
        "created_at": "2022-03-03T16:02:57.934Z",
        "updated_at": "2022-03-03T16:02:57.934Z",
        "is_active": true
        }
        """
        ms_str = month_start_to_str(month_start)
        selected_date = date_str_to_date(ms_str)
        to_rate(
            user_id=user_id,
            client_id=client_id,
            valid_from=str(selected_date),
            valid_to=str(far_date),
            amount=amount,
            created_at=str(datetime.now()),
            updated_at=str(datetime.now()),
            is_active=True,
        )
        if on_submit:
            set_on_submit(False)
        else:
            set_on_submit(True)

    selector_user_id = Selector2(set_value=set_user_id, data=username())

    selector_client_id = Selector2(
        set_value=set_client_id,
        data=clients_names(),
    )
    selector_month_start = Selector2(
        set_value=set_month_start,
        data=months_start(),
    )
    inp_amount = Input(set_amount, label="amount in EUR")

    is_disabled = True
    if user_id != "" and client_id != "" and month_start != "" and amount != "":
        is_disabled = False

    btn = SubmitButton(is_disabled, handle_submit)

    return Column(
        Row(selector_user_id, selector_client_id, selector_month_start, inp_amount),
        Row(btn),
    )


@component
def rates_table(user_id, client_id, month_start):
    """Generates a table component with forecast days by year and month

    Args:
        user_id (int): the id of the user for which the forecast is for
        epic_id (int): the id of the epic for which the forecast is for
        year_month (str): the year_month combined for which the forecast is for

    Returns:
        list of filtered forecasts
    """
    ms_str = month_start_to_str(month_start)
    rows = rates_by_user_client_date(user_id=user_id, client_id=client_id, date=ms_str)
    return html.div({"class": "flex w-full"}, SimpleTable(rows))


# @component
# def update_rate(set_updated_rate):
#     rate_to_update, set_rate_to_update = ("")
#     new_amount, set_new_amount = ("")

#     def handle_delete(event):
#         forecast_deletion(forecast_to_delete)
#         set_deleted_forecast(forecast_to_delete)

#     inp_forecast = Input(
#         set_value=set_new_amount,
#         label="forecast id to delete",
#     )
#     btn = html.button(
#         {
#             "class": "relative w-fit h-fit px-2 py-1 text-lg border text-gray-50  border-secondary-200",
#             "onClick": handle_delete,
#         },
#         "Delete",
#     )
#     return Column(Row(inp_forecast), Row(btn))
