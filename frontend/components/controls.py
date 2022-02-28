


    # wrap this inside a Button component
    button_is_active = True
    if user_id == "" or epic_id == "" or year_month == "" or days == "":
        button_is_active = False

    button_status = "text-gray-50  border-secondary-200"
    if button_is_active is False:
        button_status = "text-gray-500  border-gray-500"

    btn = html.button(
        {
            "class": f"relative w-fit h-fit px-2 py-1 text-lg border {button_status}",
            "onClick": handle_submit,
            "disabled": True,
        },
        "Submit",
    )
    # end of wrap