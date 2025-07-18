import json
import calendar

from decouple import config
from datetime import datetime, timedelta

import database as db

TOKEN = "7795978174:AAGKf_gTcERLyS5JgDeliiTL8_gf5nnnUuA"

def admins():
    users = db.get_user_all()
    ad_list = []
    for id, staff in users.items():
        if staff['is_staff'] == 1:
            ad_list.append(id)
    return ad_list

languages = ["🇺🇿 uz", "🇷🇺 ru", "🇺🇸 en"]

with open("data.json", "r", encoding="utf-8") as file:
    translations = json.load(file)

def get_text(lang, category, key):
    return translations.get(lang, {}).get(category, {}).get(key, f"[{key}]")


def check_bron_user_info(time=None, bron_id=None):
    brons = db.get_brons_all()
    users = db.get_user_all()
    
    for id, i in brons.items():
        if (time and i.get('time') == time) or (bron_id and str(id) == str(bron_id)):
            tg_id = i.get("tg_id")
            user_data = users.get(tg_id, {})
            user_info = {
                "id": id,
                "name": i.get("name"),
                "phone": i.get("phone"),
                "tg_id": tg_id,
                "time": i.get("time"),
                "lang": user_data.get("lang", "🇺🇿 uz")
            }
            return user_info
    return {}


def check_brons_today():
    bron = db.get_brons_all()
    now = datetime.now().replace(second=0, microsecond=0)

    if now.hour < 9:
        return []

    today_str = now.strftime("%d-%m")
    end_time = now.replace(hour=21, minute=0)

    hour = now.hour
    minute = now.minute

    if minute == 0:
        minute = 0
    elif minute < 30:
        minute = 30
    else:
        hour += 1
        minute = 0
        if hour >= 24:
            return []

    all_slots = []
    current_slot = now.replace(hour=hour, minute=minute)

    while current_slot <= end_time:
        time_str = current_slot.strftime("%H:%M")
        all_slots.append(time_str)
        current_slot += timedelta(minutes=30)

    taken_slots = [i["time"] for i in bron.values() if i["date"] == today_str and i['status'] == 0]
    free_slots = [t + (" ✅" if t in taken_slots else "") for t in all_slots]

    return free_slots


def check_brons_others(lang):
    today = datetime.now()
    tomorrow = today + timedelta(days=1)

    last_day = calendar.monthrange(tomorrow.year, tomorrow.month)[1]
    end_date = tomorrow.replace(day=last_day)

    week_days_dict = {
        "🇺🇿 uz": ['Dushanba', 'Seshanba', 'Chorshanba', 'Payshanba', 'Juma', 'Shanba', 'Yakshanba'],
        "🇷🇺 ru": ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье'],
        "🇺🇸 en": ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    }
    week_days = week_days_dict.get(lang, [])

    date_dict = {}
    date = tomorrow
    while date <= end_date:
        key = date.strftime("%d-%m")
        value = week_days[date.weekday()]
        date_dict[key] = value
        date += timedelta(days=1)

    return date_dict


def check_brons_otherday(day):
    bron = db.get_brons_all()

    start_time = datetime.strptime("09:00", "%H:%M")
    end_time = datetime.strptime("21:00", "%H:%M")

    all_slots = []
    current = start_time
    while current <= end_time:
        all_slots.append(current.strftime("%H:%M"))
        current += timedelta(minutes=30)

    taken_slots = [v["time"] for v in bron.values() if v["date"] == day and v['status'] == 0]
    slots = [t + (" ✅" if t in taken_slots else "") for t in all_slots]

    return slots
