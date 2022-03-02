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

from config import base_url


@component
def page():
    username, set_username = use_state("")
    name, set_name = use_state("")
    surname, set_surname = use_state("")
    email, set_email = use_state("")
    submitted_surname, set_submitted_surname = use_state("")
    deleted_user, set_deleted_user = use_state("")
    return Container(
        Row(
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
            )
        ),
        Column(
            Row(list_users(submitted_surname)),
        ),
        Row(delete_user(set_deleted_user)),
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

    inp_username = Input(set_value=set_username, label="username")
    inp_name = Input(set_value=set_name, label="name")
    inp_surname = Input(set_value=set_surname, label="surname")
    inp_email = Input(set_value=set_email, label="email")
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
def list_users(submitted_surname):
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
    return html.div({"class": "flex w-full"}, SimpleTable(rows=rows))


@component
def delete_user(set_delete_user):
    delete_user, set_delete_user = use_state("")

    def delete_user(event):
        api = f"{base_url}/api/users?username={delete_user}"
        response = requests.delete(api)
        set_deleted_user(delete_user)

    inp_username = Input(set_value=set_delete_user, label="delete user (username)")
    btn = html.button(
        {
            "class": "relative w-fit h-fit px-2 py-1 text-lg border text-gray-50  border-secondary-200",
            "onClick": delete_user,
        },
        "Submit",
    )
    return Column(Row(inp_username), Row(btn))
