from idom import component, html
from typing import Callable


@component
def SubmitButton(is_disabled: bool, handle_submit: Callable):
    button_status = "text-gray-50  border-secondary-200"
    if is_disabled is False:
        button_status = "relative w-fit h-fit px-2 py-1 text-lg border text-gray-50 border-secondary-200 hover:bg-gray-50 hover:text-primary-500"
    return html.button(
        {
            "class": f"relative w-fit h-fit px-2 py-1 text-lg border {button_status}",
            "onClick": handle_submit,
            "disabled": is_disabled,
        },
        "Submit",
    )
