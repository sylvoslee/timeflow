import asyncio
from cProfile import label
import json
from black import click
from idom import html, run, use_state, component, event, vdom
from idom.server.sanic import PerClientStateServer
import requests
from sanic import Sanic, response

from components.input import Input
from components.layout import Row, Column, Container
from components.lists import ListSimple
from components.table import SimpleTable

base_url = "http://127.0.0.1:8000"


@component
def page():
    username, set_username = use_state("")
    name, set_name = use_state("")
    surname, set_surname = use_state("")
    email, set_email = use_state("")
    submitted_surname, set_submitted_surname = use_state("")
    is_changed, set_is_changed = use_state(False)

    return Container(
        create_user_form(
            username,
            set_username,
            name,
            set_name,
            surname,
            set_surname,
            email,
            set_email,
            set_submitted_surname,
        ),
        Column(
            Row(list_users(submitted_surname, is_changed)),
        ),
        Row(delete_user(is_changed, set_is_changed)),
    )


@component
def create_user_form(
    username,
    set_username,
    name,
    set_name,
    surname,
    set_surname,
    email,
    set_email,
    set_submitted_surname,
):
    """
    endpoint: /api/users
    schema: {
      "username": "string",
      "name": "string",
      "surname": "string",
      "email": "string"
    }"""

    @event(prevent_default=True)
    async def handle_submit(event):
        data = {"username": username, "name": name, "surname": surname, "email": email}
        print("here", data)
        response = requests.post(
            f"{base_url}/api/users",
            data=json.dumps(data),
            headers={"accept": "application/json", "Content-Type": "application/json"},
        )
        set_submitted_surname(surname)

    inp_username = Input(value=username, set_value=set_username, label="username")
    inp_name = Input(value=name, set_value=set_name, label="name")
    inp_surname = Input(value=surname, set_value=set_surname, label="surname")
    inp_email = Input(value=email, set_value=set_email, label="email")
    btn = html.button(
        {
            "class": "relative w-fit h-fit px-2 py-1 text-lg border text-gray-50  border-secondary-200",
            "onClick": handle_submit,
        },
        "Submit",
    )

    return Column(
        Row(
            inp_username,
            inp_name,
            inp_surname,
            inp_email,
        ),
        Row(btn),
    )


@component
def list_users(surname, is_changed):
    api = f"{base_url}/api/users"
    response = requests.get(api)

    rows = []
    for item in response.json():
        d = {
            "name": item["name"],
            "surname": item["surname"],
            "username": item["username"],
            "email": item["email"],
        }
        rows.append(d)
    return SimpleTable(rows=rows)


@component
def delete_user(is_changed, set_is_changed):
    username, set_username = use_state("")

    def delete_user(event):
        api = f"{base_url}/api/users?username={username}"
        response = requests.delete(api)
        set_is_changed(True)

    inp_username = Input(
        value=username, set_value=set_username, label="delete user input"
    )
    btn = html.button(
        {
            "class": "relative w-fit h-fit px-2 py-1 text-lg border text-gray-50  border-secondary-200",
            "onClick": delete_user,
        },
        "Submit",
    )
    return Column(Row(inp_username), Row(btn))


# run(create_user, port=8001)
