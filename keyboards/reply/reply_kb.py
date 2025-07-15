import calendar
from datetime import datetime, timedelta

from aiogram.types import KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder

import config as cf
import database as db

def start_key():
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(KeyboardButton(text=f"🇺🇸 en"), KeyboardButton(text=f"🇺🇿 uz"),KeyboardButton(text=f"🇷🇺 ru"))
    keyboard.adjust(3)
    return keyboard.as_markup(resize_keyboard=True)


def ask_phone(lang):
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(KeyboardButton(text=cf.get_text(lang, 'buttons', 'contact'),request_contact=True))
    keyboard.adjust(1)
    return keyboard.as_markup(resize_keyboard=True)


def conf(lang):
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(KeyboardButton(text=cf.get_text(lang, 'buttons', 'confirm')), KeyboardButton(text=cf.get_text(lang, 'buttons', 'rejected')))
    keyboard.adjust(2)
    return keyboard.as_markup(resize_keyboard=True)


def menu(lang):
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(KeyboardButton(text=cf.get_text(lang, 'buttons', 'booking')), KeyboardButton(text=cf.get_text(lang, 'buttons', 'location')),
                 KeyboardButton(text=cf.get_text(lang, 'buttons', 'contactwithbarber')),KeyboardButton(text=cf.get_text(lang, 'buttons', 'change_language')),
                 KeyboardButton(text=cf.get_text(lang, 'buttons', 'myorders')))
    keyboard.adjust(2)
    return keyboard.as_markup(resize_keyboard=True)


languages = ["🇺🇸 en","🇺🇿 uz","🇷🇺 ru"]

def change_language(lang):
    keyboard = ReplyKeyboardBuilder()
    for i in languages:
        keyboard.row(KeyboardButton(text=str(i)))
    keyboard.add(KeyboardButton(text=cf.get_text(lang, 'buttons', 'back')))
    keyboard.adjust(3)
    return keyboard.as_markup(resize_keyboard=True)


def back(lang):
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(KeyboardButton(text=cf.get_text(lang, 'buttons', 'back')))
    keyboard.adjust(1)
    return keyboard.as_markup(resize_keyboard=True)


def book_barber(lang):
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(KeyboardButton(text=cf.get_text(lang, 'buttons', 'today')), KeyboardButton(text=cf.get_text(lang, 'buttons', 'another_day')),
                         KeyboardButton(text=cf.get_text(lang, 'buttons', 'back')))
    keyboard.adjust(2,1)
    return keyboard.as_markup(resize_keyboard=True)


def book_time(lang):
    keyboard = ReplyKeyboardBuilder()
    hour = db.current_day()
    for i in hour:
        keyboard.row(KeyboardButton(text=f'⏱️{i}'))
    keyboard.add(KeyboardButton(text=cf.get_text(lang, 'buttons', 'back')))
    keyboard.adjust(3)
    return keyboard.as_markup(resize_keyboard=True)


def confirmation_time(lang):
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(KeyboardButton(text=cf.get_text(lang, 'buttons', 'confirm')), KeyboardButton(text=cf.get_text(lang, 'buttons', 'rejected')),
                 KeyboardButton(text=cf.get_text(lang, 'buttons', 'back')))
    keyboard.adjust(2,1)
    return keyboard.as_markup(resize_keyboard=True)


def sana_va_hafta_kunlari(lang):
    kunlar_dict = {
        "🇺🇿 uz": ['Dushanba', 'Seshanba', 'Chorshanba', 'Payshanba', 'Juma', 'Shanba', 'Yakshanba'],
        "🇷🇺 ru": ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье'],
        "🇺🇸 en": ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    }

    hafta_kunlari = kunlar_dict[lang]  # lang har doim to‘g‘ri uzatiladi deb hisoblaymiz

    ertaga = datetime.now() + timedelta(days=1)
    oy_oxiri = ertaga.replace(day=calendar.monthrange(ertaga.year, ertaga.month)[1])

    sana_dict = {}
    sana = ertaga

    while sana <= oy_oxiri:
        format_sana = sana.strftime("%d-%m")  # masalan: "14-07"
        hafta_kuni = hafta_kunlari[sana.weekday()]
        sana_dict[format_sana] = hafta_kuni
        sana += timedelta(days=1)

    return sana_dict


def test_month(lang):
    keyboard = ReplyKeyboardBuilder()
    kunlar = sana_va_hafta_kunlari(lang)

    for sana, hafta_kuni in kunlar.items():
        keyboard.row(KeyboardButton(text=f"🗒 {sana} - {hafta_kuni}"))

    keyboard.add(KeyboardButton(text=cf.get_text(lang, 'buttons', 'back')))
    keyboard.adjust(2)

    return keyboard.as_markup(resize_keyboard=True)


def check_brons_otherday(day):
    bron = db.get_brons_all()

    start_time = datetime.strptime("09:00", "%H:%M")
    end_time = datetime.strptime("21:00", "%H:%M")

    all_slots = []
    current = start_time
    while current <= end_time:
        all_slots.append(current.strftime("%H:%M"))
        current += timedelta(minutes=30)

    taken_slots = [v["time"] for v in bron.values() if v["date"] == day]
    slots = [t for t in all_slots if t not in taken_slots]

    return slots


def book_time_and_data(lang,day):
    keyboard = ReplyKeyboardBuilder()
    hour = check_brons_otherday(day)
    for i in hour:
        keyboard.row(KeyboardButton(text=f"⏱️ {i}"))
    keyboard.add(KeyboardButton(text=cf.get_text(lang, 'buttons', 'back')))
    keyboard.adjust(3)
    return keyboard.as_markup(resize_keyboard=True)


def history(lang):
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(KeyboardButton(text=cf.get_text(lang, 'buttons', 'history_btn')), KeyboardButton(text=cf.get_text(lang, 'buttons', 'cancel_booking')),
                 KeyboardButton(text=cf.get_text(lang, 'buttons', 'back')))
    keyboard.adjust(2)
    return keyboard.as_markup(resize_keyboard=True)


def book_time_and_dates(lang, times):
    keyboard = ReplyKeyboardBuilder()

    for time_str in times:
        # Agar vaqt jarayonda bo'lsa, ⌛ emoji qo'shamiz
        time_dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M")
        now = datetime.now()

        if time_dt >= now:  # Agar vaqt hali kelmagan bo'lsa
            emoji = "⌛"
            keyboard.row(KeyboardButton(text=f"{emoji} {time_str}"))

    # "Back" tugmasini qo'shamiz
    keyboard.add(KeyboardButton(text=cf.get_text(lang, 'buttons', 'back')))
    keyboard.adjust(2)  # Tugmalarni 3 ta ustunda joylashtiramiz

    return keyboard.as_markup(resize_keyboard=True)

###################################################################################################################

# BACK MENU
def back_menu(lang):
    keyboard = ReplyKeyboardBuilder()
    keyboard.row(KeyboardButton(text=cf.get_text(lang, "buttons", "back")))
    return keyboard.as_markup(resize_keyboard=True, input_field_placeholder=cf.translations['input'])


# CONFIRM REJECT MENU
def confirm_reject(lang):
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(KeyboardButton(text=cf.get_text(lang, "buttons", "confirm")), KeyboardButton(text=cf.get_text(lang, "buttons", "rejected")))
    keyboard.row(KeyboardButton(text=cf.get_text(lang, "buttons", "back")))
    return keyboard.as_markup(resize_keyboard=True, input_field_placeholder=cf.translations['input'])

# ADMIN MAIN_MENU
def admin_main_menu(lang):
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(
        KeyboardButton(text=cf.get_text(lang, "buttons", "admin_btn_1")),
        KeyboardButton(text=cf.get_text(lang, "buttons", "admin_btn_5")),
        KeyboardButton(text=cf.get_text(lang, "buttons", "admin_btn_2")),
        # KeyboardButton(text=cf.get_text(lang, "buttons", "admin_btn_7")),
        # KeyboardButton(text=cf.get_text(lang, "buttons", "admin_btn_3")),
        KeyboardButton(text=cf.get_text(lang, "buttons", "admin_btn_4")),
        # KeyboardButton(text=cf.get_text(lang, "buttons", "admin_btn_6")),
    )                
    keyboard.adjust(2)
    return keyboard.as_markup(resize_keyboard=True, input_field_placeholder=cf.translations['input'])


# ADMIN NEW POST MENU
def admin_new_post_menu(lang):
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(
        KeyboardButton(text=cf.get_text(lang, "buttons", "admin_btn_0_1")), KeyboardButton(text=cf.get_text(lang, "buttons", "admin_btn_0_2")),
        KeyboardButton(text=cf.get_text(lang, "buttons", "admin_btn_0_3")), KeyboardButton(text=cf.get_text(lang, "buttons", "admin_btn_0_4"))
    )
    keyboard.adjust(2)
    keyboard.row(KeyboardButton(text=cf.get_text(lang, "buttons", "back")))
    return keyboard.as_markup(resize_keyboard=True, input_field_placeholder=cf.translations['input'])


# ADMIN POST CONFIRM MENU
def admin_post_confirm(lang):
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(
        KeyboardButton(text=cf.get_text(lang, "buttons", "admin_btn_0_4_1")), KeyboardButton(text=cf.get_text(lang, "buttons", "admin_btn_0_4_2"))
    )
    keyboard.row(KeyboardButton(text=cf.get_text(lang, "buttons", "back")))
    return keyboard.as_markup(resize_keyboard=True, input_field_placeholder=cf.translations['input'])


# ADMIN BRON_MENU 
def admin_bron_menu(lang):
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(
        KeyboardButton(text=cf.get_text(lang, "buttons", "admin_btn_1_1")), KeyboardButton(text=cf.get_text(lang, "buttons", "admin_btn_1_2"))
    )
    keyboard.row(KeyboardButton(text=cf.get_text(lang, "buttons", "back")))
    return keyboard.as_markup(resize_keyboard=True, input_field_placeholder=cf.translations['input'])


# ADMIN BRON_TODAY
def admin_bron_today_menu(lang):
    today = cf.check_brons_today()
    keyboard = ReplyKeyboardBuilder()
    for i in today:
        keyboard.add(KeyboardButton(text=f"⏱️ {i}"))
    keyboard.adjust(3)
    keyboard.row(KeyboardButton(text=cf.get_text(lang, "buttons", "back")))
    return keyboard.as_markup(resize_keyboard=True, input_field_placeholder=cf.translations['input'])


# ADMIN BRON_OTHERS
def admin_bron_others_menu(lang):
    others = cf.check_brons_others(lang)
    keyboard = ReplyKeyboardBuilder()
    for date, day in others.items():
        keyboard.add(KeyboardButton(text=f"🗓 {date} - {day}"))
    keyboard.adjust(1, 3)
    keyboard.row(KeyboardButton(text=cf.get_text(lang, "buttons", "back")))
    return keyboard.as_markup(resize_keyboard=True, input_field_placeholder=cf.translations['input'])


# ADMIN BRON OTHERDAY MENU
def admin_bron_otherday_menu(lang, day):
    otherday = cf.check_brons_otherday(day)
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(KeyboardButton(text=f"{day} - {cf.get_text(lang, 'buttons', 'admin_btn_1_1_2')}"))
    for i in otherday:
        keyboard.add(KeyboardButton(text=f"⏱️ {i}"))
    keyboard.adjust(1, 3)
    keyboard.row(KeyboardButton(text=cf.get_text(lang, "buttons", "back")))
    return keyboard.as_markup(resize_keyboard=True, input_field_placeholder=cf.translations['input'])


# ADMIN ANALYTIC_MENU
def admin_analytic_menu(lang):
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(
        KeyboardButton(text=cf.get_text(lang, "buttons", "admin_btn_2_1")), KeyboardButton(text=cf.get_text(lang, "buttons", "admin_btn_2_2")),
        KeyboardButton(text=cf.get_text(lang, "buttons", "admin_btn_2_3"))
    )
    keyboard.adjust(2, 1)
    keyboard.row(KeyboardButton(text=cf.get_text(lang, "buttons", "back")))
    return keyboard.as_markup(resize_keyboard=True, input_field_placeholder=cf.translations['input'])


# ADMIN CANCEL_MENU
def admin_cancel_menu(lang):
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(
        KeyboardButton(text=cf.get_text(lang, "buttons", "admin_btn_1_1")), KeyboardButton(text=cf.get_text(lang, "buttons", "admin_btn_1_2"))
    )
    keyboard.row(KeyboardButton(text=cf.get_text(lang, "buttons", "back")))
    return keyboard.as_markup(resize_keyboard=True, input_field_placeholder=cf.translations['input'])


# ADMIN LANGUAGE_MENU 
def admin_language_menu(lang):
    keyboard = ReplyKeyboardBuilder()
    for i in cf.languages:
        keyboard.add(KeyboardButton(text=i))
    keyboard.adjust(3)
    keyboard.row(KeyboardButton(text=cf.get_text(lang, "buttons", "back")))
    return keyboard.as_markup(resize_keyboard=True, input_field_placeholder=cf.translations['input'])


# ADMIN POISK USER
def admin_poisk_user(lang):
    keyboard = ReplyKeyboardBuilder()
    keyboard.row(KeyboardButton(text=cf.get_text(lang, "buttons", "back")))
    return keyboard.as_markup(resize_keyboard=True, input_field_placeholder=cf.translations['input'])