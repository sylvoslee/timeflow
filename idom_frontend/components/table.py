from typing import Any, Callable, List
from idom import html


def SimpleTable(rows: List[Any]):
    trs = []
    for row in rows:
        tds = []
        for k in row:
            value = row[k]
            tds.append(html.td({"class": "p-4 w-1/4"}, value))
        trs.append(html.tr({"class": "flex w-full mb-4"}, tds))

    ths = [html.th({"class": "p-4 w-1/4"}, header) for header in rows[0].keys()]
    thead = html.thead(
        {"class": "flex bg-secondary-400 text-white w-full"},
        html.tr({"class": "flex w-full mb-4"}, ths),
    )
    tbody = html.tbody(
        {
            "class": "flex flex-col bg-secondary-200 items-center justify-between overflow-y-scroll w-full"
        },
        trs,
    )
    return html.table({"class": "text-left w-full"}, thead, tbody)


def ClientsTableComponent(rows: List[Any]):
    trs = []
    for row in rows:
        tds = []
        for k in row:
            value = row[k]
            tds.append(html.td({"class": "p-4 w-1/4"}, value))
        trs.append(html.tr({"class": "flex w-full mb-4"}, tds))

    ths = [html.th({"class": "p-4 w-1/4"}, header) for header in rows[0].keys()]
    thead = html.thead(
        {"class": "flex bg-secondary-400 text-white w-full"},
        html.tr({"class": "flex w-full mb-4"}, ths),
    )
    tbody = html.tbody(
        {
            "class": "flex flex-col bg-secondary-200 items-center justify-between overflow-y-scroll w-full"
        },
        trs,
    )
    return html.table({"class": "text-left w-full"}, thead, tbody)
