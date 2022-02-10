from idom import html, run, use_state, component, event, vdom, EventHandler
from idom.web import module_from_url, export
from pages.users import page as users_page
from pages.clients import page as clients_page
from pages.epics import page as epics_page
from pages.timelogs import page as timelogs_page

from components.layout import Column, Row, FlexContainer
from components.sidebar import Sidebar


@component
def page():

    current_page, set_current_page = use_state("Timelogs")
    pages = ["Users", "Timelogs", "Epics", "Clients"]

    print("here", current_page)
    if current_page == "Users":
        current_page_component = users_page(key="users_page")
    elif current_page == "Epics":
        current_page_component = epics_page(key="epics_page")
    elif current_page == "Timelogs":
        current_page_component = timelogs_page(key="timelogs_page")
    elif current_page == "Clients":
        current_page_component = clients_page(key="clients_page")
    else:
        current_page_component = html.h1(
            {"class": "text-white"}, "Test Page, not implemented yet"
        )

    return html.div(
        {"class": "flex w-full"},
        Sidebar(current_page, set_current_page, pages=pages, title="Timesheets UI"),
        FlexContainer(current_page_component),
    )
