import asyncio
from cProfile import label
import json
from black import click
from idom import html, run, use_state, component, event, vdom
from idom.server.sanic import PerClientStateServer
import requests
from pathlib import Path
from sanic import Sanic, response

from components.input import Input
from components.layout import Row, Column
from components.lists import ListSimple

base_url = "http://127.0.0.1:8000"


@component
def create_user():
    username, set_username = use_state("")
    name, set_name = use_state("")
    surname, set_surname = use_state("")
    email, set_email = use_state("")
    submitted_surname, set_submitted_surname = use_state("")
    return html.div(
        {"class": "bg-primary-500"},
        html.div(html.link({"href": "/static/tailwind.css", "rel": "stylesheet"})),
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
        Column(Row(list_users(submitted_surname))),
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
def list_users(surname):
    api = f"{base_url}/api/users/lists/surname"
    response = requests.get(api)
    lis = []
    for item in response.json():
        lis.append(html.li(item))
    return ListSimple(items=response.json())


# run(create_user, port=8001)

app = Sanic(__name__)
HERE = Path(__file__).parent
app.static("/static", str(HERE / "tailwind/build"))
PerClientStateServer(
    create_user,
    {
        "redirect_root_to_index": False,
    },
    app,
)
app.run(
    host="0.0.0.0",
    port=8001,
    workers=1,
    debug=True,
)
