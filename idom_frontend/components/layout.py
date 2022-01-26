from typing import Any, Callable, List
from idom import html


def Column(*args: html):
    return html.div({"class": "flex flex-col space-y-2 pl-2 pr-4 mt-2"}, args)


def Row(*args: html):
    return html.div({"class": "flex flex-col md:flex-row space-x-4"}, args)
