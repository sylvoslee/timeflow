from typing import Any, Callable, List
from idom import html, component, use_state
from components.layout import Column, Row


def SimpleTable(rows: List[Any]):
    is_hidden, set_is_hidden = use_state(True)
    print(is_hidden)
    trs = []
    for row in rows[:3]:
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
    # if is_hidden == True:
    #     set_is_table_visible("invisible")
    # else:
    #     set_is_table_visible("")
    # tclass = f
    return Column(
        html.table({"class": "text-left"}, thead, tbody),
        SimpleTableButton(is_hidden, set_is_hidden),
    )


@component
def SimpleTableButton(is_hidden, set_is_hidden):
    text, set_text = use_state("show table")

    def show_page(event):
        if is_hidden:
            set_is_hidden(False)
            set_text("unshow table")
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
