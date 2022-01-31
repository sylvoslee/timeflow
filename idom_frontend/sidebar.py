from idom import html, run, use_state, component, event, vdom, EventHandler
from idom.server.sanic import PerClientStateServer
from idom.web import module_from_url, export

from main import page as user_page
from components.layout import Column, Row
from components.sidebar import Sidebar


@component
def page():

    current_page, set_current_page = use_state("Users")
    pages = ["Users", "Timelogs", "Epics", "Clients"]

    timelogs_page = html.h1(
        {"class": "text-white"}, "Timelogs Page, not implemented yet"
    )
    epics_page = html.h1({"class": "text-white"}, "Epics Page, not implemented yet")

    print("here", current_page)

    if current_page == "Users":
        current_page_component = user_page()
    elif current_page == "Timelogs":
        current_page_component = timelogs_page
    elif current_page == "Epics":
        current_page_component = epics_page

    return html.div(
        {"class": "flex w-full"},
        Sidebar(current_page, set_current_page, pages=pages, title="Timesheets UI"),
        Column(Row(current_page_component)),
    )
