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
    submitted_name, set_submitted_name = use_state("")
    year_month, set_year_month = use_state("")
    day, set_day = use_state("")
    user_id, set_user_id = use_state("")
    epic_id, set_epic_id = use_state("")
    start_time, set_start_time = use_state("")
    end_time, set_end_time = use_state("")
    client_id, set_client_id = use_state("")
    delete_timelog, set_delete_timelog = use_state("")
    return Container(
        create_timelog_form(
            year_month,
            set_year_month,
            day,
            set_day,
            user_id,
            set_user_id,
            epic_id,
            set_epic_id,
            start_time,
            set_start_time,
            end_time,
            set_end_time,
            client_id,
            set_client_id
            # set_submitted_name,
        ),
        Column(
            Row(list_timelogs(user_id)),
        ),
        Row(delete_timelogs(set_delete_timelog)),
    )


@component
def create_timelog_form(
    year_month,
    set_year_month,
    day,
    set_day,
    user_id,
    set_user_id,
    epic_id,
    set_epic_id,
    start_time,
    set_start_time,
    end_time,
    set_end_time,
    client_id,
    set_client_id
    # set_submitted_name,
):
    """
    schema:
    {
    "user_id": 0,
    "start_time": "string",
    "end_time": "string",
    "client_id": 0,
    "epic_id": 0,
    "count_hours": 0,
    "count_days": 0,
    "month": 0,
    "year": 0
    }
    """

    @event(prevent_default=True)
    async def handle_submit(event):
        a = year_month
        year_a_cut = a[:4]
        month_a_cut = a[5:7]

        year = int(year_a_cut)
        month = int(month_a_cut)

        data = {
            "start_time": start_time,
            "end_time": end_time,
            "user_id": user_id,
            "client_id": client_id,
            "epic_id": epic_id,
            "count_hours": 0,
            "count_days": 0,
            "month": month,
            "year": year,
        }
        print("timelog post json", data)
        response = requests.post(
            f"{base_url}/api/timelogs",
            data=json.dumps(data),
            headers={"accept": "application/json", "Content-Type": "application/json"},
        )
        # set_submitted_name(name)

    # year and month dropdown list
    year_month_dropdown_list = (
        html.option({"value": "2022_01"}, "2022_01"),
        html.option({"value": "2022_02"}, "2022_02"),
        html.option({"value": "2022_03"}, "2022_03"),
        html.option({"value": "2022_04"}, "2022_04"),
        html.option({"value": "2022_05"}, "2022_05"),
        html.option({"value": "2022_06"}, "2022_06"),
        html.option({"value": "2022_07"}, "2022_07"),
        html.option({"value": "2022_08"}, "2022_08"),
        html.option({"value": "2022_09"}, "2022_09"),
        html.option({"value": "2022_10"}, "2022_10"),
        html.option({"value": "2022_11"}, "2022_11"),
        html.option({"value": "2022_12"}, "2022_12"),
    )

    # days dropdown list
    month_days_nr = range(1, 32)
    month_days_list = []
    for n in month_days_nr:
        month_days_list.append(n)

    days_dropdown = []
    for n in month_days_list:
        a = html.option({"value": f"{n}"}, n)
        days_dropdown.append(a)
        days_dropdown_list = tuple(days_dropdown)

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
    hours_dropdown = []
    for n in hours_list:
        a = html.option({"value": f"{n}"}, n)
        hours_dropdown.append(a)
        hours_dropdown_list = tuple(hours_dropdown)

    selector_year_month = Selector(
        value=year_month,
        set_value=set_year_month,
        placeholder="select a month",
        dropdown_list=year_month_dropdown_list,
    )

    selector_days = Selector(
        value=day,
        set_value=set_day,
        placeholder="select a day",
        dropdown_list=days_dropdown_list,
    )

    selector_start_time = Selector(
        value=start_time,
        set_value=set_start_time,
        placeholder="select start time",
        dropdown_list=hours_dropdown_list,
    )
    selector_end_time = Selector(
        value=end_time,
        set_value=set_end_time,
        placeholder="select end time",
        dropdown_list=hours_dropdown_list,
    )

    inp_user_id = Input(value=user_id, set_value=set_user_id, label="user id")
    inp_epic_id = Input(value=epic_id, set_value=set_epic_id, label="epic id")
    inp_client_id = Input(value=client_id, set_value=set_client_id, label="client id")
    btn = html.button(
        {
            "class": "relative w-fit h-fit px-2 py-1 text-lg border text-gray-50  border-secondary-200",
            "onClick": handle_submit,
        },
        "Submit",
    )

    return Column(
        Row(
            inp_user_id,
            inp_epic_id,
            inp_client_id,
            selector_year_month,
            selector_days,
            selector_start_time,
            selector_end_time,
        ),
        Row(btn),
    )


@component
def list_timelogs(user_id):
    api = f"{base_url}/api/timelogs"
    response = requests.get(api)

    rows = []
    for item in response.json():
        d = {
            "user_id": item["user_id"],
            "epic_id": item["epic_id"],
            "start_time": item["start_time"],
            "end_time": item["end_time"],
            "count_hours": item["count_hours"],
            "count_days": item["count_days"],
            "month": item["month"],
            "year": item["year"],
        }
        rows.append(d)
    return html.div({"class": "flex w-full"}, SimpleTable(rows=rows))


@component
def delete_timelogs(set_delete_timelog):
    year_month, set_year_month = use_state("")
    day, set_day = use_state("")
    user_id, set_user_id = use_state("")
    epic_id, set_epic_id = use_state("")
    start_time, set_start_time = use_state("")
    end_time, set_end_time = use_state("")
    client_id, set_client_id = use_state("")

    def delete_timelog(event):
        api = f"{base_url}/api/users?username={username}"
        response = requests.delete(api)

    year_month_dropdown_list = (
        html.option({"value": "2022_01"}, "2022_01"),
        html.option({"value": "2022_02"}, "2022_02"),
        html.option({"value": "2022_03"}, "2022_03"),
        html.option({"value": "2022_04"}, "2022_04"),
        html.option({"value": "2022_05"}, "2022_05"),
        html.option({"value": "2022_06"}, "2022_06"),
        html.option({"value": "2022_07"}, "2022_07"),
        html.option({"value": "2022_08"}, "2022_08"),
        html.option({"value": "2022_09"}, "2022_09"),
        html.option({"value": "2022_10"}, "2022_10"),
        html.option({"value": "2022_11"}, "2022_11"),
        html.option({"value": "2022_12"}, "2022_12"),
    )

    # days dropdown list
    month_days_nr = range(1, 32)
    month_days_list = []
    for n in month_days_nr:
        month_days_list.append(n)

    days_dropdown = []
    for n in month_days_list:
        a = html.option({"value": f"{n}"}, n)
        days_dropdown.append(a)
        days_dropdown_list = tuple(days_dropdown)

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
    hours_dropdown = []
    for n in hours_list:
        a = html.option({"value": f"{n}"}, n)
        hours_dropdown.append(a)
        hours_dropdown_list = tuple(hours_dropdown)

    selector_year_month = Selector(
        value=year_month,
        set_value=set_year_month,
        placeholder="select a month",
        dropdown_list=year_month_dropdown_list,
    )

    selector_days = Selector(
        value=day,
        set_value=set_day,
        placeholder="select a day",
        dropdown_list=days_dropdown_list,
    )

    selector_start_time = Selector(
        value=start_time,
        set_value=set_start_time,
        placeholder="select start time",
        dropdown_list=hours_dropdown_list,
    )
    selector_end_time = Selector(
        value=end_time,
        set_value=set_end_time,
        placeholder="select end time",
        dropdown_list=hours_dropdown_list,
    )

    inp_user_id = Input(value=user_id, set_value=set_user_id, label="user id")
    inp_epic_id = Input(value=epic_id, set_value=set_epic_id, label="epic id")
    inp_client_id = Input(value=client_id, set_value=set_client_id, label="client id")
    btn = html.button(
        {
            "class": "relative w-fit h-fit px-2 py-1 text-lg border text-gray-50  border-secondary-200",
            "onClick": delete_timelog,
        },
        "Submit",
    )

    return Column(
        Row(
            inp_user_id,
            inp_epic_id,
            inp_client_id,
            selector_year_month,
            selector_days,
            selector_start_time,
            selector_end_time,
        ),
        Row(btn),
    )
