from datetime import datetime

import keyboards.reply.reply_kb as kb_r

import states.states as st
import config as cf
import database as db


async def ask_phone(bot, message, state):
    user_id = message.from_user.id
    if message.text in {"🇺🇸 en":"🇺🇸 en", "🇺🇿 uz":"🇺🇿 uz", "🇷🇺 ru":"🇷🇺 ru"}:
        await state.update_data(language=message.text)
        data = await state.get_data()
        lang = data['language']
        await bot.send_message(chat_id=user_id,text=cf.get_text(lang, 'message_text', 'contact'), reply_markup=kb_r.ask_phone(lang))
        await state.set_state(st.userst.phone)


async def check_phone(bot, message, state):
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data['language']
    if message.contact:
        await state.update_data(phone=message.contact.phone_number)
        await bot.send_message(chat_id=user_id,text=cf.get_text(lang, 'message_text', 'user_info'), reply_markup=kb_r.ReplyKeyboardRemove())
        await state.set_state(st.userst.fio)
    else:
        text = message.text
        if message.text.startswith("+998") and len(text) == 13 and text[1:].isdigit():
            await state.update_data(phone=message.text)
            await bot.send_message(chat_id=user_id,text=cf.get_text(lang, 'message_text', 'user_info'), reply_markup=kb_r.ReplyKeyboardRemove())
            await state.set_state(st.userst.fio)
        else:
            await bot.send_message(chat_id=user_id,text=cf.get_text(lang, 'message_text', 'error_phone'))


async def fio_user(bot, message, state):
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data['language']
    ok = True
    for i in message.text:
        if not i.isalpha():
            await bot.send_message(chat_id=user_id,text=cf.get_text(lang, 'message_text', 'error_name'))
            ok = False
            break
    if ok:
        await state.update_data(user_name=message.text)
        msg_text = (
            f"{cf.get_text(lang, 'message_text', 'show_info')}\n"
            f"{cf.get_text(lang, 'message_text', 'phone')} {data['phone']}\n"
            f"{cf.get_text(lang, 'message_text', 'name')} {message.text}"
        )

        await bot.send_message(chat_id=user_id,text=msg_text, reply_markup=kb_r.conf(lang))
        await state.set_state(st.userst.conf)


async def conf(bot, message, state):
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data['language']
    if message.text == cf.get_text(lang, "buttons", "confirm"):
        if db.create_user(data["phone"],data["user_name"],str(user_id),lang):
            await bot.send_message(chat_id=user_id, text=cf.get_text(lang, 'message_text', 'main_menu_text'),reply_markup=kb_r.menu(lang))
            await state.set_state(st.userst.menu)

    elif message.text == cf.get_text(lang, "buttons", "rejected"):
        await bot.send_message(chat_id=user_id, text=cf.translations['start'], reply_markup=kb_r.start_key(), parse_mode='HTML')
        await state.set_state(st.userst.language)


async def menu(bot, message, state):
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data['language']
    if message.text == cf.get_text(lang, "buttons", "change_language"):
        await bot.send_message(chat_id=user_id, text=cf.get_text(lang, 'message_text', 'change_language'),reply_markup=kb_r.change_language(lang))
        await state.set_state(st.userst.change_language)
    elif message.text == cf.get_text(lang, "buttons", "location"):
        await bot.send_location(chat_id=user_id, latitude=41.331411, longitude=69.252588)
        await bot.send_message(chat_id=user_id, text=cf.get_text(lang, 'message_text', 'location'),reply_markup=kb_r.back(lang))
        await state.set_state(st.userst.location)
    elif message.text == cf.get_text(lang, "buttons", "contactwithbarber"):
        await bot.send_message(chat_id=user_id,text=cf.get_text(lang, 'message_text', 'barber_info'), reply_markup=kb_r.back(lang))
        await state.set_state(st.userst.barber_contact)
    elif message.text == cf.get_text(lang, "buttons", "booking"):
        await bot.send_message(chat_id=user_id, text=cf.get_text(lang, 'message_text', 'book_barber'),reply_markup=kb_r.book_barber(lang))
        await state.set_state(st.userst.book_barber)
    elif message.text == cf.get_text(lang, "buttons", "myorders"):
        await bot.send_message(chat_id=user_id, text=cf.get_text(lang, 'message_text', 'history'),reply_markup=kb_r.history(lang))
        await state.set_state(st.userst.orderhistory)
    elif message.text == cf.get_text(lang, "buttons", "services"):
        await bot.send_message(chat_id=user_id, text=cf.get_text(lang, "message_text", "services"))


async def cancel_and_history(bot, message, state):
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data['language']

    if message.text == cf.get_text(lang, "buttons", "back"):
        await bot.send_message(chat_id=user_id, text=cf.get_text(lang, 'message_text', 'main_menu_text'),
                               reply_markup=kb_r.menu(lang))
        await state.set_state(st.userst.menu)

    elif message.text == cf.get_text(lang, "buttons", "history_btn"):
        times, detailed_info = db.booking_history_user(user_id)
        print(times)

        if times:
            all_time = ""
            now = datetime.now()

            for time_str in times:
                if isinstance(time_str, list):
                    time_str = time_str[0]

                time_dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M")
                emoji = "⌛" if time_dt >= now else "✅"

                all_time += f"{emoji} {time_str}\n\n"

            msg_text = cf.get_text(lang, 'message_text', 'all_time_booked') + "\n\n" + all_time
            await bot.send_message(chat_id=user_id, text=msg_text)
            await state.set_state(st.userst.orderhistory)

        else:
            await bot.send_message(chat_id=user_id, text=cf.get_text(lang, 'message_text', 'noorders'),
                                reply_markup=kb_r.back(lang))
            await state.set_state(st.userst.orderhistory)

    elif message.text == cf.get_text(lang, "buttons", "cancel_booking"):
        times,dict_with_id = db.booking_history_user(user_id)
        ongoing_times = [time for time in times if datetime.strptime(time, "%Y-%m-%d %H:%M") >= datetime.now()]

        if ongoing_times:
            keyboard = kb_r.book_time_and_dates(lang, ongoing_times)
            msg_text = cf.get_text(lang, 'message_text', 'choose_time_cancel')  # "❌ Buyurtmani bekor qilish"
            await bot.send_message(chat_id=user_id, text=msg_text, reply_markup=keyboard)
        else:
            await bot.send_message(chat_id=user_id, text=cf.get_text(lang, 'message_text', 'noorder_user'),reply_markup=kb_r.back(lang))
        await state.set_state(st.userst.orderhistory_back)


cancel_list_time = []
async def show_time_to_cancel(bot, message, state):
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data['language']
    if message.text == cf.get_text(lang, "buttons", "back"):
        await bot.send_message(chat_id=user_id, text=cf.get_text(lang, 'message_text', 'history'),
                               reply_markup=kb_r.history(lang))
        await state.set_state(st.userst.orderhistory)
    elif message.text.startswith("⌛ "):
        cancel_list_time.append(message.text[2:].strip())
        print(f"cancel_list_time:{cancel_list_time}")
        await bot.send_message(chat_id=user_id, text=cf.get_text(lang, 'message_text', 'description_cancel'),reply_markup=kb_r.ReplyKeyboardRemove())
        await state.set_state(st.userst.description_cancel)


async def send_cancel_time(bot, message, state):
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data['language']
    print(f"message.text:{message.text}")

    times, dict_with_id = db.booking_history_user(user_id)

    cancel = cancel_list_time[0] 
    cancel_list_time.clear()
    print(cancel)
    res = dict_with_id[user_id]
    for k, v in res.items():
        if v == cancel:
            pk = k  
            print(f"{v} == {cancel}")
            print(f"Bekor qilinadigan PK: {pk}")

            if db.send_cancel_request(pk, user_id, message.text):
                await bot.send_message(chat_id=user_id, text=cf.get_text(lang, 'message_text', 'success'))
                await bot.send_message(chat_id=user_id, text=cf.get_text(lang, 'message_text', 'main_menu_text'),reply_markup=kb_r.menu(lang))
                await state.set_state(st.userst.menu)
            else:
                await bot.send_message(chat_id=user_id, text=cf.get_text(lang, 'message_text', 'error_with_cancel'))


async def change_lang_and_menu(bot, message, state):
    user_id = message.from_user.id
    l_list = {"🇺🇸 en","🇺🇿 uz","🇷🇺 ru"}
    if message.text in l_list:
        for i in l_list:
            if message.text == i:
                await state.update_data(language=message.text)
                db.update_user_lang(user_id, message.text)
                await bot.send_message(chat_id=user_id, text=cf.get_text(message.text, 'message_text', 'main_menu_text'),reply_markup=kb_r.menu(message.text))
                await state.set_state(st.userst.menu)
                break
    else:
        data = await state.get_data()
        lang = data['language']
        if message.text == cf.get_text(lang, "buttons", "back"):
            await bot.send_message(chat_id=user_id, text=cf.get_text(lang, 'message_text', 'main_menu_text'),reply_markup=kb_r.menu(lang))
            await state.set_state(st.userst.menu)


async def back_location(bot, message, state):
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data['language']
    if message.text == cf.get_text(lang, "buttons", "back"):
        await bot.send_message(chat_id=user_id, text=cf.get_text(lang, 'message_text', 'main_menu_text'), reply_markup=kb_r.menu(lang))
        await state.set_state(st.userst.menu)


async def back_contact(bot, message, state):
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data['language']
    if message.text == cf.get_text(lang, "buttons", "back"):
        await bot.send_message(chat_id=user_id, text=cf.get_text(lang, 'message_text', 'main_menu_text'), reply_markup=kb_r.menu(lang))
        await state.set_state(st.userst.menu)


async def barber_book(bot, message, state):
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data['language']
    if message.text == cf.get_text(lang, "buttons", "back"):
        await bot.send_message(chat_id=user_id, text=cf.get_text(lang, 'message_text', 'main_menu_text'), reply_markup=kb_r.menu(lang))
        await state.set_state(st.userst.menu)
    elif message.text == cf.get_text(lang, "buttons", "today"):
        await bot.send_message(chat_id=user_id, text=cf.get_text(lang, 'message_text', 'today_book'),reply_markup=kb_r.book_time(lang))
        await state.set_state(st.userst.conf_time)
    elif message.text == cf.get_text(lang, "buttons", "another_day"):
        await bot.send_message(chat_id=user_id, text=cf.get_text(lang, 'message_text', 'today_book'),
                               reply_markup=kb_r.test_month(lang))
        await state.set_state(st.userst.test_month)


dates = []
async def confirmation_time_1(bot, message, state):
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data['language']
    another_day = message.text.split(" ")
    if another_day[0].startswith("🗒") and another_day[1][:2].isdigit() and another_day[2] == '-' and another_day[3].isalpha():
        dates.append(another_day[1])
        await bot.send_message(chat_id=user_id, text=cf.get_text(lang, 'message_text', 'today_book'),
                               reply_markup=kb_r.book_time_and_data(lang,another_day[1]))
        await state.set_state(st.userst.conf_time)
    if message.text == cf.get_text(lang, "buttons", "back"):
        await bot.send_message(chat_id=user_id, text=cf.get_text(lang, 'message_text', 'book_barber'),reply_markup=kb_r.book_barber(lang))
        await state.set_state(st.userst.book_barber)


async def confirmation_time_2(bot, message, state):
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data['language']
    text = message.text
    splt = text.split(":")
    if text.startswith("⏱️") and splt[1].isdigit():
        if len(dates) == 1:
            msg_text = (
                f"{cf.get_text(lang, 'message_text', 'conf_time')}\n🗓 {dates[0] + '-' + str(datetime.today().date())[:4]}\n{message.text}"
            )
            dates.append(message.text[2:])
        else:
            dates.append(message.text[1:])
            msg_text = (
                f"{cf.get_text(lang, 'message_text', 'conf_time')}\n{message.text}"
            )
        await bot.send_message(chat_id=user_id, text=msg_text, reply_markup=kb_r.confirmation_time(lang))
        await state.set_state(st.userst.conf_time_and_menu)
    elif message.text == cf.get_text(lang, "buttons", "back"):
        await bot.send_message(chat_id=user_id, text=cf.get_text(lang, 'message_text', 'book_barber'),reply_markup=kb_r.book_barber(lang))
        await state.set_state(st.userst.book_barber)


async def confirmation_time_menu(bot, message, state):
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data['language']
    if message.text == cf.get_text(lang, "buttons", "confirm"):
        print(dates)
        if len(dates) == 1:
            # Tozalash:
            import re
            time_match = re.search(r"\d{2}:\d{2}", dates[0])
            if time_match:
                clean_time = time_match.group()
            else:
                await bot.send_message(chat_id=user_id, text="❌ Noto‘g‘ri vaqt formati!")
                return

            # Matnni formatlash
            text = cf.get_text(lang, 'message_text', 'booked_user')
            msg_text = text.format(time=clean_time)

            times = f"{datetime.today().date()} {clean_time}"

            if db.booked_time(str(user_id), times, 1):
                await bot.send_location(chat_id=user_id, latitude=41.328093, longitude=69.336579)
                await bot.send_message(chat_id=user_id, text=msg_text)
                await bot.send_message(
                    chat_id=user_id,
                    text=cf.get_text(lang, 'message_text', 'main_menu_text'),
                    reply_markup=kb_r.menu(lang)
                )
                await state.set_state(st.userst.menu)
                dates.clear()

        else:
            text = cf.get_text(lang, 'message_text', 'booked_user')
            formatted_time = f"{datetime.now().year}-{dates[0]} {dates[1]}"
            msg_text = text.format(time=formatted_time)
            day = dates[0].split("-")
            times = str(datetime.today().date())[:4] + "-" + day[1] + "-" + day[0] + dates[1]
            if db.booked_time(user_id,  times, 1):
                await bot.send_location(chat_id=user_id, latitude=41.331411, longitude=69.252588)
                await bot.send_message(chat_id=user_id, text=msg_text)
                await bot.send_message(chat_id=user_id, text=cf.get_text(lang, 'message_text', 'main_menu_text'),
                                       reply_markup=kb_r.menu(lang))
                await state.set_state(st.userst.menu)
                dates.clear()