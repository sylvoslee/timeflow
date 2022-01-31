from idom import html, run, use_state, component, event, vdom, EventHandler
from idom.server.sanic import PerClientStateServer
from idom.web import module_from_url, export

from components.sidebar import Sidebar


@component
def page():

    current_page, set_current_page = use_state("page1")

    return html.div({"class": "flex"}, Sidebar(current_page, set_current_page))
