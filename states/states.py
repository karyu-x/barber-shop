from aiogram.fsm.state import State, StatesGroup


class userst(StatesGroup):
    language = State()
    phone = State()
    fio = State()
    conf = State()
    menu = State()
    change_language = State()
    location = State()
    barber_contact = State()
    book_barber = State()
    conf_time = State()
    conf_time_and_menu = State()
    test_month = State()
    orderhistory = State()
    noorderback = State()
    orderhistory_back = State()
    description_cancel = State()



class adminst(StatesGroup):
    main_menu = State()

    new_post_menu = State()
    post_description = State()
    post_photo = State()
    post_button = State()
    post_confirm = State()
    post_confirm_next = State()

    bron_menu = State()
    bron_today_menu = State()
    bron_info_menu = State()
    bron_others_menu = State()
    bron_otherday_menu = State()
    bron_others_cancel_menu = State()
    bron_cancel_reason_menu = State()
    bron_cancel_day_reason = State()

    analytics = State()

    language = State()