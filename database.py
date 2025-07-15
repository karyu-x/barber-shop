import json
from datetime import datetime
from decouple import config
import requests


BASE_URL = config('BASE_URL')


def create_user(phone, fio, telegram_id, lang):
    """
    Attempts to register a new user.
    Returns a tuple: (success, message)
    """
    url = f"{BASE_URL}/api/auth/register/"

    # This line is fragile. It's better to ensure the correct lang code ('uz', 'ru') is passed directly.
    # For now, let's assume it works as intended.
    if " " in lang:
         lang = lang.split(" ")[1]

    payload = {
        "phone_number": phone,
        "first_name": fio,
        "telegram_id": telegram_id,
        "user_lang": lang
    }

    try:
        response = requests.post(url=url, data=payload)

        if response.status_code == 201:
            print("User created successfully.")
            return (True, "User created.")

        # Check for the specific validation error
        if response.status_code == 400:
            error_data = response.json()
            if 'telegram_id' in error_data and "already exist" in error_data['telegram_id'][0]:
                print("User already exists.")
                # You might want to log the user in or retrieve their data here instead.
                return (False, "User already exists.")
            else:
                # Handle other possible 400 errors
                print(f"Bad Request: {error_data}")
                return (False, f"Invalid data: {error_data}")

        # Handle other HTTP errors
        print(f"An error occurred: {response.status_code}")
        return (False, f"Server error: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"A network error occurred: {e}")
        return (False, "Network error.")



def update_user_lang(telegram_id, new_lang):
    """
    Updates the language of a user by their Telegram ID.
    Returns a tuple: (success, message)
    """
    url = f"{BASE_URL}/api/auth/update_lang/{telegram_id}/"


    if " " in new_lang:
        new_lang = new_lang.split(" ")[1]

    payload = {
        "user_lang": new_lang
    }
    try:
        response = requests.patch(url, json=payload)
        if response.status_code in [200, 202]:
            return True, "User language updated successfully."
        else:
            return False, f"Failed to update language. Status: {response.status_code}, Response: {response.text}"
    except Exception as e:
        return False, f"Request failed with exception: {str(e)}"



def get_user_by_telegram_id():
    """
    Checks if a user with the given Telegram ID exists.
    Returns a dictionary: {'exists': bool, 'data': user_data or message}
    """
    url = f"{BASE_URL}/api/auth/users/"  # Telegram ID ni url-ga qo'shamiz

    try:
        response = requests.get(url)
        if response.status_code == 200:
            user_data = response.json()
            users = {}
            for i in user_data:
                users[int(i["telegram_id"])] = i["user_lang"]
            return users
        elif response.status_code == 404:
            return {
                'exists': False,
                'data': 'User not found'  # Foydalanuvchi topilmadi
            }
        else:
            return {
                'exists': False,
                'data': f"Unexpected response: {response.status_code} - {response.text}"  # Xato javobni qaytarish
            }
    except Exception as e:
        return {
            'exists': False,
            'data': f"Request failed: {str(e)}"
        }


def current_day():
    url = f"{BASE_URL}/api/bookings/available-slots/?date={datetime.today().date()}&service_id={1}"
    response = requests.get(url=url)
    res = response.json()
    return res["slots"]



def booked_time(tg_id, time, service):
    url = f"{BASE_URL}/api/bookings/"
    payload = {
        "telegram_id": tg_id,
        "start_time": time,
        "service": service
    }
    headers = {"Content-Type": "application/json"}  # qo‘shib ko‘ring

    # print("Payload:", payload)

    try:
        response = requests.post(url, json=payload, headers=headers)
        # print("Response status:", response.status_code)
        # print("Response text:", response.text)

        if response.status_code == 201:
            return True
        elif response.status_code == 404:
            return {'exists': False, 'data': 'User not found'}
        else:
            return {
                'exists': False,
                'data': f"Unexpected response: {response.status_code} - {response.text}"
            }
    except Exception as e:
        return {'exists': False, 'data': f"Request failed: {str(e)}"}




def get_brons_all():
    url = f"{BASE_URL}/api/bookings/"
    response = requests.get(url)
    bron_base = {}

    if response.status_code == 200:
        for booking in response.json():
            start_time = booking.get("start_time")
            if not start_time:
                continue

            start_dt = datetime.fromisoformat(start_time)
            date_str = start_dt.strftime("%d-%m")
            time_str = start_dt.strftime("%H:%M")

            user_info = booking.get("user", "")
            if " - " in user_info:
                name, phone, tg_id = user_info.split(" - ")
            else:
                name, phone = user_info, ""

            bron_base[booking["id"]] = {
                "name": name.strip(),
                "phone": phone.strip(),
                "tg_id": tg_id.strip(),
                "date": date_str,
                "time": time_str,
                "summa": int(float(booking["service"]["price"])),
                "status": 0 if booking["status"] == "CONFIRMED" else 1
            }
    else:
        print(f"❌ Failed to get bookings: {response.status_code}")
    return bron_base




def booking_history_user(tg_id):
    url = f"{BASE_URL}/api/bookings/booking-history/?telegram_id={tg_id}"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"❌ Error: {response.status_code}")
        return [], {}

    data = response.json()

    confirmed_data = [item for item in data if item.get('status') == 'CONFIRMED' and 'start_time' in item]

    total = [item['start_time'] for item in confirmed_data]
    total.sort(key=lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M"))

    id_to_time = {item['id']: item['start_time'] for item in confirmed_data if 'id' in item and 'start_time' in item}

    tg_id_to_ids = {tg_id: id_to_time}

    print(f"keldi:{total}\n{tg_id_to_ids}")
    return total, tg_id_to_ids


def send_cancel_request(pk, tg_id, cancel_reason):
    url = f"{BASE_URL}/api/bookings/{pk}/cancel/"
    payload = {
        "telegram_id": tg_id,
        "cancel_reason": cancel_reason  # foydalanuvchining sababi
    }
    try:
        response = requests.post(url, json=payload)
        print(response.text)
        if response.status_code == 200:
            print("✅ Success: Booking canceled.")
            return True
        else:
            print(f"❌ Error: {response.status_code}, {response.text}")
            return False
    except Exception as e:
        print(f"⚠️ Exception: {e}")
        return False


#################################################################################################

def get_user_all():
    url = f"{BASE_URL}/api/auth/users/"
    response = requests.get(url)
    users = response.json()
    data_base = {}

    for user in users:
        telegram_id = user.get("telegram_id")
        if telegram_id:
            lang_code = str(user.get("user_lang", "")).lower()

            if lang_code == "uz":
                lang = "🇺🇿 uz"
            elif lang_code == "ru":
                lang = "🇷🇺 ru"
            else:
                lang = "🇺🇸 en"

            data_base[telegram_id] = {
                "fio": user.get("first_name", "NoName"),
                "phone": user.get("phone_number", "NoPhone"),
                "lang": lang,
                "is_staff": int(user.get("is_staff", False))
            }

    return data_base


def get_client_all():
    url = f"{BASE_URL}/api/auth/users/client/"
    response = requests.get(url)
    data_base = {}

    if response.status_code == 200:
        for user in response.json():
            telegram_id = user.get("telegram_id")
            if telegram_id:
                data_base[telegram_id] = {
                    "fio": user.get("first_name"),
                    "phone": user.get("phone_number"),
                    "lang": "🇺🇿 uz" if user.get("user_lang") == "uz" else (
                        "🇷🇺 ru" if user.get("user_lang") == "ru" else "🇺🇸 en"
                    ),
                    "is_staff": 1 if user.get("is_staff") == True else 0
                }
    else:
        print(f"❌ Failed to get users: {response.status_code}")

    return data_base


def get_brons_all():
    url = f"{BASE_URL}/api/bookings/"
    response = requests.get(url)
    bron_base = {}

    if response.status_code == 200:
        for booking in response.json():
            start_time = booking.get("start_time")
            if not start_time:
                continue

            start_dt = datetime.fromisoformat(start_time)
            date_str = start_dt.strftime("%d-%m")
            time_str = start_dt.strftime("%H:%M")

            user_info = booking.get("user", "")
            if " - " in user_info:
                name, phone, tg_id = user_info.split(" - ")
            else:
                name, phone = user_info, ""

            bron_base[booking["id"]] = {
                "name": name.strip(),
                "phone": phone.strip(),
                "tg_id": int(tg_id),
                "date": date_str,
                "time": time_str,
                "summa": int(float(booking["service"]["price"])),
                "status": 0 if booking["status"] == "CONFIRMED" else 1
            }
    else:
        print(f"❌ Failed to get bookings: {response.status_code}")

    return bron_base

def parse_date_flex(date_str):
    current_year = datetime.now().year
    for fmt in ("%m-%d", "%d-%m"):
        try:
            return datetime.strptime(date_str, fmt).replace(year=current_year)
        except ValueError:
            continue
    raise ValueError(f"❌ Неизвестный формат даты: {date_str}")


def bron_cancel_time_range(date, start_time, end_time, tg_id, reason="OTMEN VAQTLA"):
    print(date)
    url = f"{BASE_URL}/api/bookings/cancel-time-range/?telegram_id={tg_id}"

    try:
        date_obj = parse_date_flex(date)
        dates = date_obj.strftime("%Y-%m-%d")
    except Exception as e:
        return False, print(f"❌ Неверный формат даты: {e}")

    if isinstance(start_time, datetime):
        start_time = start_time.strftime("%H:%M")
    if isinstance(end_time, datetime):
        end_time = end_time.strftime("%H:%M")

    payload = {
        "date": dates,
        "from_time": start_time,  
        "to_time": end_time,
        "reason": reason
    }

    try:
        response = requests.post(url, json=payload, timeout=5)
        print(f"📥 Status code: {response.status_code}")
        print(f"📥 Response text: {response.text}")

        if response.status_code in [200, 202]:
            return True
        else:
            return False
    except Exception as e:
        return False


def bron_cancel_date(date_str_dd_mm, tg_id, reason="OTMEN KUN"):
    url = f"{BASE_URL}/api/bookings/cancel-day/?telegram_id={tg_id}"

    try:
        date_obj = datetime.strptime(date_str_dd_mm, "%d-%m")
        date_obj = date_obj.replace(year=datetime.now().year)
        formatted_date = date_obj.strftime("%Y-%m-%d")
    except ValueError as e:
        return False

    payload = {
        "date": formatted_date,  
        "reason": reason,
    }

    try:
        response = requests.post(url, json=payload)
        if response.status_code in [200, 202]:
            return True
        else:
            return False
    except Exception as e:
        return False


def update_user_lang(telegram_id, new_lang):
    url = f"{BASE_URL}/api/auth/update_lang/{telegram_id}/"

    if " " in new_lang:
        new_lang = new_lang.split(" ")[1]

    payload = {
        "user_lang": new_lang
    }
    try:
        response = requests.patch(url, json=payload)
        if response.status_code in [200, 202]:
            return True, "User language updated successfully."
        else:
            return False, f"Failed to update language. Status: {response.status_code}, Response: {response.text}"
    except Exception as e:
        return False, f"Request failed with exception: {str(e)}"