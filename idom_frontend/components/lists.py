from typing import Any, Callable, List
from idom import html


def ListSimple(items: List[Any]):
    li_items = []
    for item in items:
        li_items.append(
            html.li(
                {"class": "p-2"},
                html.p({"class": "bg-secondary-300 pl-1"}, item),
            )
        )
    return html.ul(li_items)


def ListCards(items: List[Any]):

    l_items = []
    for item in items:
        l_items.append(html.div({"class": "font-medium"}, item))

    return html.ul(
        {"class": "flex flex-col p-4"},
        html.li(
            {"class": "border-gray-400 flex flex-row"},
            html.div(
                {
                    "class": "select-none flex flex-1 items-center p-4 transition duration-500 ease-in-out transform hover:-translate-y-2 rounded-2xl border-2 p-6 hover:shadow-2xl secondary-200"
                },
                html.div(
                    {"class": "flex-1 pl-1 mr-16"},
                    l_items,
                ),
            ),
        ),
    )
