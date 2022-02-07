from typing import Any, Callable, List
from idom import html, component, use_state
from components.layout import Column, Row


@component
def SimpleTable(rows: List[Any]):
    is_hidden, set_is_hidden = use_state(True)
    page_number, set_page_number = use_state(2)
    print(is_hidden)
    print(f"page number is {page_number}")
    trs = []
    p = page_number
    m = p - 1
    r = 5
    a = m * r
    b = a + r
    for row in rows[a:b]:
        tds = []
        for k in row:
            value = row[k]
            tds.append(html.td({"class": "p-4 w-full"}, value))
        trs.append(html.tr({"class": "flex w-full mb-4"}, tds))

    ths = [html.th({"class": "p-4 w-full"}, header) for header in rows[0].keys()]
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
    tclass = "text-left"
    if is_hidden:
        tclass = "invisible"
    pgnr = "1"
    return Column(
        html.table({"class": tclass}, thead, tbody),
        SimpleTableButton(is_hidden, set_is_hidden),
    )

    # html.a(
    #     {
    #         "href": "#",
    #         "class": "flex px-4 py-2 text-black bg-white rounded-md hover:bg-black hover:text-white",
    #     },
    #     pgnr,
    # html.div(
    #     {"class": "flex items-center space-x-1"},
    # ),
    # justify="justify-between",


@component
def SimpleTableButton(is_hidden, set_is_hidden):
    text, set_text = use_state("show table")

    def show_page(event):
        if is_hidden:
            set_is_hidden(False)
            set_text("hide table")
        else:
            set_is_hidden(True)
            set_text("show table")

    btn = html.button(
        {
            "class": "relative w-fit h-fit px-2 py-1 text-lg border text-gray-50  border-secondary-200",
            "onClick": show_page,
        },
        text,
    )

    return btn
