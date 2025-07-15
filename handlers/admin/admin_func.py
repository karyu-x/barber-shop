import asyncio
from datetime import datetime, timedelta

import keyboards.reply.reply_kb as kb_r
import keyboards.inline.inline_kb as kb_i

import states.states as st
import config as cf
import database as db

# ADMIN MAIN_MENU   
async def main_menu(bot, message, state, user_id, lang):
    if message.text == cf.get_text(lang, 'buttons', 'admin_btn_5'):
        await bot.send_message(chat_id=user_id, text=cf.get_text(lang, 'message_text', 'admin_new_post_menu'), reply_markup=kb_r.admin_new_post_menu(lang=lang))
        await state.set_state(st.adminst.new_post_menu)
    elif message.text == cf.get_text(lang, 'buttons', 'admin_btn_1'):
        await bot.send_message(chat_id=user_id, text=cf.get_text(lang, 'message_text', 'admin_bron_menu'), reply_markup=kb_r.admin_bron_menu(lang=lang))
        await state.set_state(st.adminst.bron_menu)
    elif message.text == cf.get_text(lang, "buttons", "admin_btn_2"):
        await bot.send_message(chat_id=user_id, text=cf.get_text(lang, "message_text", "admin_analytic_menu"), reply_markup=kb_r.admin_analytic_menu(lang=lang))
        await state.set_state(st.adminst.analytics)
    elif message.text == cf.get_text(lang, "buttons", "admin_btn_4"):
        await bot.send_message(chat_id=user_id, text=cf.get_text(lang, "message_text", "admin_language_menu"), reply_markup=kb_r.admin_language_menu(lang=lang))
        await state.set_state(st.adminst.language)
    else:
        await bot.send_message(chat_id=user_id, text="eRRoR")


######################################################################
# ADMIN NEW POST MENU
async def new_post_menu(bot, message, state, user_id, lang):
    if message.text == cf.get_text(lang, "buttons", "back"):
        await bot.send_message(chat_id=user_id, text=cf.get_text(lang, "message_text", "admin_main_menu_text"), reply_markup=kb_r.admin_main_menu(lang=lang))
        await state.set_state(st.adminst.main_menu)
    elif message.text == cf.get_text(lang, "buttons", "admin_btn_0_1"):
        await bot.send_message(chat_id=user_id, text=cf.get_text(lang, "message_text", "admin_post_description"), reply_markup=kb_r.back_menu(lang))
        await state.set_state(st.adminst.post_description)
    elif message.text == cf.get_text(lang, "buttons", "admin_btn_0_2"):
        await bot.send_message(chat_id=user_id, text=cf.get_text(lang, "message_text", "admin_post_photo"), reply_markup=kb_r.back_menu(lang))
        await state.set_state(st.adminst.post_photo)
    elif message.text == cf.get_text(lang, "buttons", "admin_btn_0_3"):
        await bot.send_message(chat_id=user_id, text=cf.get_text(lang, "message_text", "admin_post_button"), reply_markup=kb_r.back_menu(lang))
        await state.set_state(st.adminst.post_button)
    elif message.text == cf.get_text(lang, "buttons", "admin_btn_0_4"):
        await bot.send_message(chat_id=user_id, text=cf.get_text(lang, "message_text", "admin_post_confirm"), reply_markup=kb_r.admin_post_confirm(lang))
        await state.set_state(st.adminst.post_confirm)
    else:
        await bot.send_message(chat_id=user_id, text="eRRoR new_post")


# ADMIN POST DESCRIPTION MENU
async def post_description_menu(bot, message, state, user_id, lang):
    if message.text == cf.get_text(lang, "buttons", "back"):
        await bot.send_message(chat_id=user_id, text=cf.get_text(lang, "message_text", "admin_new_post_menu"), reply_markup=kb_r.admin_new_post_menu(lang=lang))
        await state.set_state(st.adminst.new_post_menu)
    else:
        await state.update_data(description=message.text)
        await bot.send_message(chat_id=user_id, text=cf.get_text(lang, "message_text", "post_description_taked"))
        await bot.send_message(chat_id=user_id, text=cf.get_text(lang, "message_text", "admin_new_post_menu"), reply_markup=kb_r.admin_new_post_menu(lang))
        await state.set_state(st.adminst.new_post_menu)

# AMDIN POST PHOTO MENU
async def post_photo_menu(bot, message, state, user_id, lang):
    if message.text == cf.get_text(lang, "buttons", "back"):
        await bot.send_message(chat_id=user_id, text=cf.get_text(lang, "message_text", "admin_new_post_menu"), reply_markup=kb_r.admin_new_post_menu(lang=lang))
        await state.set_state(st.adminst.new_post_menu)
    if message.photo:
        await state.update_data(photo=message.photo[-1].file_id)
        await bot.send_message(chat_id=user_id, text=cf.get_text(lang, "message_text", "post_photo_taked"))
        await bot.send_message(chat_id=user_id, text=cf.get_text(lang, "message_text", "admin_new_post_menu"), reply_markup=kb_r.admin_new_post_menu(lang))
        await state.set_state(st.adminst.new_post_menu)
    else:
        await bot.send_message(chat_id=user_id, text="eRRoR post_photo")


# ADMIN POST BUTTON MENU
async def post_button_menu(bot, message, state, user_id, lang):
    if message.text == cf.get_text(lang, "buttons", "back"):
        await bot.send_message(chat_id=user_id, text=cf.get_text(lang, "message_text", "admin_new_post_menu"), reply_markup=kb_r.admin_new_post_menu(lang=lang))
        await state.set_state(st.adminst.new_post_menu)
        return
    lines = message.text.strip().split("\n")
    buttons = []
    for line in lines:
        parts = line.strip().split(" - ")
        if len(parts) != 2 or not parts[1].strip().startswith("https://"):
            await bot.send_message(chat_id=user_id, text=cf.get_text(lang, "message_text", "admin_post_button_format"))
            return
        buttons.append({"text": parts[0].strip(), "url": parts[1].strip()})

    await state.update_data(buttons=buttons)
    await bot.send_message(chat_id=user_id, text=cf.get_text(lang, "message_text", "post_button_taked"))
    await bot.send_message(chat_id=user_id, text=cf.get_text(lang, "message_text", "admin_new_post_menu"), reply_markup=kb_r.admin_new_post_menu(lang=lang))
    await state.set_state(st.adminst.new_post_menu)


# ADMIN POST CONFIRM MENU
async def post_confirm_menu(bot, message, state, user_id, lang):
    if message.text == cf.get_text(lang, "buttons", "back"):
        await bot.send_message(chat_id=user_id, text=cf.get_text(lang, "message_text", "admin_new_post_menu"), reply_markup=kb_r.admin_new_post_menu(lang=lang))
        await state.set_state(st.adminst.new_post_menu)
    elif message.text == cf.get_text(lang, "buttons", "admin_btn_0_4_1"):
        data = await state.get_data()
        text = data.get("description", "NO MESSAGE")
        photo = data.get("photo", "")
        buttons = data.get("buttons", [])
        if photo:
            await bot.send_photo(chat_id=user_id, photo=photo, caption=text, reply_markup=kb_i.admin_post_button(buttons=buttons))
        else:
            await bot.send_message(chat_id=user_id, text=text, reply_markup=kb_i.admin_post_button(buttons=buttons))
    elif message.text == cf.get_text(lang, "buttons", "admin_btn_0_4_2"):
        await bot.send_message(chat_id=user_id, text=cf.get_text(lang, "message_text", "admin_post_confirm_next"), reply_markup=kb_r.confirm_reject(lang=lang))
        await state.set_state(st.adminst.post_confirm_next)
    else:
        await bot.send_message(chat_id=user_id, text="eRRoR")


# ADMIN POST CONFIRM NEXT MENU
async def post_confirm_next_menu(bot, message, state, clients, user_id, lang):
    data = await state.get_data()
    text = data.get("description", "")
    photo = data.get("photo", "")
    buttons = data.get("buttons", [])
    if message.text == cf.get_text(lang, "buttons", "back"):
        await bot.send_message(chat_id=user_id, text=cf.get_text(lang, "message_text", "admin_post_confirm"), reply_markup=kb_r.admin_post_confirm(lang=lang))
        await state.set_state(st.adminst.post_confirm)
    elif message.text == cf.get_text(lang, "buttons", "confirm"):
        if text or photo or buttons:
            for uid in clients:
                try:
                    if photo:
                        await bot.send_photo(chat_id=uid, photo=photo, caption=text, reply_markup=kb_i.admin_post_button(buttons=buttons))
                    else:
                        await bot.send_message(chat_id=uid, text=text, reply_markup=kb_i.admin_post_button(buttons=buttons))
                except Exception as e:
                    print(f"❗️ Error sending to {uid}: {e}")
            
            await state.clear()
            await bot.send_message(chat_id=user_id, text=cf.get_text(lang, "message_text", "admin_post_sent_succes"))
            await bot.send_message(chat_id=user_id, text=cf.get_text(lang, "message_text", "admin_main_menu_text"), reply_markup=kb_r.admin_main_menu(lang=lang))
            await state.set_state(st.adminst.main_menu)
        else:
            await bot.send_message(chat_id=user_id, text=cf.get_text(lang, "message_text", "admin_post_no_detected"))
    elif message.text == cf.get_text(lang, "buttons", "rejected"):
        if text or photo or buttons:
            await state.clear()
            await bot.send_message(chat_id=user_id, text=cf.get_text(lang, "message_text", "admin_post_cancelled"), reply_markup=kb_r.admin_post_confirm(lang=lang))
            await state.set_state(st.adminst.post_confirm)
        else:
            await bot.send_message(chat_id=user_id, text=cf.get_text(lang, "message_text", "admin_post_no_detected"))
    else:
        await bot.send_message(chat_id=user_id, text="eRRoR confirm next")


######################################################################
# ADMIN BRON MENU
async def bron_menu(bot, message, state, user_id, lang):
    if message.text == cf.get_text(lang, "buttons", "back"):
        await bot.send_message(chat_id=user_id, text=cf.get_text(lang, "message_text", "admin_main_menu_text"), reply_markup=kb_r.admin_main_menu(lang=lang))
        await state.set_state(st.adminst.main_menu)
    elif message.text == cf.get_text(lang, "buttons", "admin_btn_1_1"):
        await bot.send_message(chat_id=user_id, text=cf.get_text(lang, "message_text", "admin_bron_today_menu"), reply_markup=kb_r.admin_bron_today_menu(lang=lang))
        await state.set_state(st.adminst.bron_today_menu)
    elif message.text == cf.get_text(lang, "buttons", "admin_btn_1_2"):
        await bot.send_message(chat_id=user_id, text=cf.get_text(lang, "message_text", "admin_bron_others_menu"), reply_markup=kb_r.admin_bron_others_menu(lang=lang))
        await state.set_state(st.adminst.bron_others_menu)
    else:
        await bot.send_message(chat_id=user_id, text="eRRoR")


# ADMIN BRON TODAY MENU 
async def bron_today_menu(bot, message, state, user_id, lang):
    if message.text == cf.get_text(lang, "buttons", "back"):
        await bot.send_message(chat_id=user_id, text=cf.get_text(lang, "message_text", "admin_bron_menu"), reply_markup=kb_r.admin_bron_menu(lang=lang))
        await state.set_state(st.adminst.bron_menu)
    elif "✅" in message.text.split("⏱️ ")[1] and message.text.split("⏱️ ")[1] in cf.check_brons_today():
        user = cf.check_bron_user_info(time=message.text.split()[1], bron_id=None)
        bron_id = user['id']
        tg_id = user['tg_id']
        name = user['name']
        phone = user['phone']
        msg_text = (
            f"{cf.get_text(lang, 'message_text', 'admin_bron_user_info')}\n\n"
            f"👤 {name}\n"
            f"📞 {phone}\n"
            f"🕒 {message.text.split()[1]}"
        )
        loading_msg = await bot.send_message(chat_id=user_id, text=cf.get_text(lang, "message_text", "admin_bron_poisk"))
        await bot.send_chat_action(chat_id=user_id, action="typing")
        await asyncio.sleep(1)
        await bot.delete_message(chat_id=user_id, message_id=loading_msg.message_id)
        await bot.send_message(chat_id=user_id, text=cf.get_text(lang, "message_text", "admin_bron_found"), reply_markup=kb_r.back_menu(lang=lang))
        await bot.send_message(chat_id=user_id, text=msg_text, reply_markup=kb_i.admin_bron_info_menu(lang=lang, bron_id=bron_id, tg_id=tg_id), parse_mode="HTML")
        await state.update_data(last_state=await state.get_state())
        await state.set_state(st.adminst.bron_info_menu)
    else:
        await bot.send_message(chat_id=user_id, text="eRRoR today")


# ADMIN BRON OTHERS MENU
async def bron_others_menu(bot, message, state, user_id, lang):
    days = cf.check_brons_others(lang)
    if message.text == cf.get_text(lang, "buttons", "back"):
        await bot.send_message(chat_id=user_id, text=cf.get_text(lang, "message_text", "admin_bron_menu"), reply_markup=kb_r.admin_bron_menu(lang=lang))
        await state.set_state(st.adminst.bron_menu)
    else:
        flag = False
        for date, day in days.items():
            if message.text == f"🗓 {date} - {day}":
                flag = True
                await bot.send_message(chat_id=user_id, text=cf.get_text(lang, "message_text", "admin_bron_otherday_menu"), reply_markup=kb_r.admin_bron_otherday_menu(lang=lang, day=date))
                await state.update_data(date=date)
                await state.set_state(st.adminst.bron_otherday_menu)
                break
        if not flag:
            await bot.send_message(chat_id=user_id, text="eRRoR others")


# ADMIN BRON INFO MENU
async def bron_info_menu(bot, message, callback, state, user_id, lang):
    if message:
        if message.text == cf.get_text(lang, "buttons", "back"):
            data = await state.get_data()
            if data['last_state'] == st.adminst.bron_today_menu:
                await bot.send_message(chat_id=user_id, text=cf.get_text(lang, "message_text", "admin_bron_today_menu"), reply_markup=kb_r.admin_bron_today_menu(lang=lang))
                await state.set_state(st.adminst.bron_today_menu)
            elif data['last_state'] == st.adminst.bron_otherday_menu:
                date = data.get('date')
                await bot.send_message(chat_id=user_id, text=cf.get_text(lang, "message_text", "admin_bron_otherday_menu"), reply_markup=kb_r.admin_bron_otherday_menu(lang=lang, day=date))
                await state.set_state(st.adminst.bron_otherday_menu)
        else:
            await bot.send_message(chat_id=user_id, text="eRRor bron info")
    elif callback:
        user = cf.check_bron_user_info(time=None, bron_id=callback.data.split('_')[1])
        user_lang = user["lang"]
        data = await state.get_data()
        date = data.get("date") or datetime.now().strftime("%m-%d")
        start_time = user['time']
        start_dt = datetime.strptime(start_time, "%H:%M")
        end_dt = start_dt + timedelta(minutes=30)
        end_time = end_dt.strftime("%H:%M")
        client_id = user['tg_id']
        if "remind" in callback.data:
            msg_text = (
                f'{cf.get_text(user_lang, "message_text", "admin_bron_remind_send_text")}\n\n'
                f"🕒 {user['time']}"
            )
            await bot.answer_callback_query(callback_query_id=callback.id, text=cf.get_text(lang, "message_text", "admin_bron_remind_text"), show_alert=True)
            await bot.send_message(chat_id=client_id, text=msg_text)
        elif "cancel" in callback.data:
            await state.update_data({"date": date, "start_time": start_dt, "end_time": end_time, "client_id": client_id, "user": user})
            await bot.delete_message(chat_id=user_id, message_id=callback.message.message_id)
            await bot.send_message(chat_id=user_id, text=cf.get_text(lang, "message_text", "admin_choose_cancel_reason"), reply_markup=kb_i.admin_bron_cancel_menu(lang=lang))
            await state.set_state(st.adminst.bron_cancel_reason_menu)
    else:
        await bot.send_message(chat_id=user_id, text="eRRoR MESS | CALL")


# ADMIN BRON CALCEL REASON MENU
async def bron_cancel_reason_menu(bot, callback, state, users, user_id, lang):
    data = await state.get_data()
    calls = {
        "reason_no_show": cf.get_text(lang, "message_text", "reason_no_show"),
        "reason_by_user": cf.get_text(lang, "message_text", "reason_by_user"),
        "reason_technical": cf.get_text(lang, "message_text", "reason_technical")
    }
    if callback.data == "back":
        user = data.get("user")
        bron_id = user['id']
        tg_id = user['tg_id']
        name = user['name']
        phone = user['phone']
        msg_text = (
            f"{cf.get_text(lang, 'message_text', 'admin_bron_user_info')}\n\n"
            f"👤 {name}\n"
            f"📞 {phone}\n"
            f"🕒 {user['time']}"
        )
        await bot.edit_message_text(chat_id=user_id, message_id=callback.message.message_id, text=msg_text, reply_markup=kb_i.admin_bron_info_menu(lang=lang, bron_id=bron_id, tg_id=tg_id))
        await state.set_state(st.adminst.bron_info_menu)
    elif callback.data in calls:
        reason = calls.get(callback.data)
        success = db.bron_cancel_time_range(date=data["date"], start_time=data["start_time"], end_time=data["end_time"], tg_id=user_id, reason=reason)
        lang_client = users[data["client_id"]]['lang']
        if success:
            await bot.edit_message_text(chat_id=user_id, message_id=callback.message.message_id, text=cf.get_text(lang, "message_text", "admin_bron_cancel_text"))
            await bot.send_message(chat_id=data['client_id'], text=cf.get_text(lang_client, "message_text", "admin_bron_cancel_send_text"))
        else:
            await bot.send_message(chat_id=user_id, text="eRRoR Reason")
        if data['last_state'] == st.adminst.bron_today_menu:
            await bot.send_message(chat_id=user_id, text=cf.get_text(lang, "message_text", "admin_bron_today_menu"), reply_markup=kb_r.admin_bron_today_menu(lang=lang))
            await state.set_state(st.adminst.bron_today_menu)
        elif data['last_state'] == st.adminst.bron_otherday_menu:
            date = data.get('date')
            await bot.send_message(chat_id=user_id, text=cf.get_text(lang, "message_text", "admin_bron_otherday_menu"), reply_markup=kb_r.admin_bron_otherday_menu(lang=lang, day=date))
            await state.set_state(st.adminst.bron_otherday_menu)
    elif callback.data == "reason_other":
        await bot.edit_message_text(chat_id=user_id, message_id=callback.message.message_id, text=cf.get_text(lang, "message_text", "admin_bron_reason_other"))
        await state.set_state(st.adminst.bron_cancel_reason_menu)


# ADMIN BRON CANCEL OTHER REASON MENU
async def bron_other_reason_text(bot, message, state, users, user_id, lang):
    data = await state.get_data()
    if message.text == cf.get_text(lang, "buttons", "back"):
        await bot.send_message(chat_id=user_id, text=cf.get_text(lang, "message_text", "admin_bron_cancel_reason_back_text"), reply_markup=kb_i.admin_bron_cancel_menu(lang=lang))
        await state.set_state(st.adminst.bron_info_menu)
        return

    reason_text = message.text.strip()
    success = db.bron_cancel_time_range(
        date=data["date"],
        start_time=data["start_time"],
        end_time=data["end_time"],
        tg_id=message.from_user.id,
        reason=reason_text
    )

    lang_client = users.get(data["client_id"], {}).get("lang", "uz")
    if success:
        await bot.send_message(
            chat_id=user_id,
            text=cf.get_text(lang, "message_text", "admin_bron_cancel_text")
        )
        await bot.send_message(
            chat_id=data["client_id"],
            text=cf.get_text(lang_client, "message_text", "admin_bron_cancel_send_text")
        )
    else:
        await bot.send_message(
            chat_id=user_id,
            text="❌ Ошибка при отмене (Other Reason)"
        )

    if data.get('last_state') == st.adminst.bron_today_menu:
        await bot.send_message(
            chat_id=user_id,
            text=cf.get_text(lang, "message_text", "admin_bron_today_menu"),
            reply_markup=kb_r.admin_bron_today_menu(lang=lang)
        )
        await state.set_state(st.adminst.bron_today_menu)
    elif data.get('last_state') == st.adminst.bron_otherday_menu:
        day = data.get('date')
        await bot.send_message(
            chat_id=user_id,
            text=cf.get_text(lang, "message_text", "admin_bron_otherday_menu"),
            reply_markup=kb_r.admin_bron_otherday_menu(lang=lang, day=day)
        )
        await state.set_state(st.adminst.bron_otherday_menu)


# ADMIN BRON OTHERDAY MENU
async def bron_otherday_menu(bot, message, state, user_id, lang):
    if message.text == cf.get_text(lang, "buttons", "back"):
        await bot.send_message(chat_id=user_id, text=cf.get_text(lang, "message_text", "admin_bron_others_menu"), reply_markup=kb_r.admin_bron_others_menu(lang=lang))
        await state.set_state(st.adminst.bron_others_menu)
    elif message.text == f"{message.text.split()[0]} - {cf.get_text(lang, 'buttons', 'admin_btn_1_1_2')}":
        # db.bron_cancel_date(date_str_dd_mm=message.text.split()[0], tg_id=user_id)
        # await bot.send_message(chat_id=user_id, text=cf.get_text(lang, "message_text", "admin_bron_otherday_cancel_text").format(date=message.text.split()[0]))
        # await bot.send_message(chat_id=user_id, text=cf.get_text(lang, "message_text", "admin_bron_others_menu"), reply_markup=kb_r.admin_bron_others_menu(lang=lang))
        # await state.set_state(st.adminst.bron_others_menu)
        await state.update_data(cancel_day_date=message.text.split()[0])
        await bot.send_message(chat_id=user_id, text=cf.get_text(lang, "message_text", "admin_bron_cancel_day_reason"), reply_markup=kb_r.back_menu(lang=lang))
        await state.set_state(st.adminst.bron_cancel_day_reason)
    elif "⏱️" in message.text:
        if "✅" in message.text:
            user = cf.check_bron_user_info(time=message.text.split()[1], bron_id=None)
            bron_id = user['id']
            tg_id = user['tg_id']
            name = user['name']
            phone = user['phone']
            msg_text = (
                f"{cf.get_text(lang, 'message_text', 'admin_bron_user_info')}\n\n"
                f"👤 {name}\n"
                f"📞 {phone}\n"
                f"🕒 {message.text.split()[1]}"
            )
            loading_msg = await bot.send_message(chat_id=user_id, text=cf.get_text(lang, "message_text", "admin_bron_poisk"))
            await bot.send_chat_action(chat_id=user_id, action="typing")
            await asyncio.sleep(1)
            await bot.delete_message(chat_id=user_id, message_id=loading_msg.message_id)
            await bot.send_message(chat_id=user_id, text=cf.get_text(lang, "message_text", "admin_bron_found"), reply_markup=kb_r.back_menu(lang=lang))
            await bot.send_message(chat_id=user_id, text=msg_text, reply_markup=kb_i.admin_bron_info_menu(lang=lang, bron_id=bron_id, tg_id=tg_id), parse_mode="HTML")
            await state.update_data(last_state=await state.get_state())
            await state.set_state(st.adminst.bron_info_menu)
        else:
            await bot.send_message(chat_id=user_id, text=cf.get_text(lang, "message_text", "admin_bron_otherday_free"))
    else:
        await bot.send_message(chat_id=user_id, text="eRRoR otherday")


# ADMIN BRON CANCEL DAY MENU
async def bron_cancel_day_reason(bot, message, state, user_id, lang):
    user_id = message.from_user.id
    reason = message.text.strip()
    data = await state.get_data()

    if message.text == cf.get_text(lang, "buttons", "back"):
        await bot.send_message(chat_id=user_id, text=cf.get_text(lang, "message_text", "admin_bron_others_menu"), reply_markup=kb_r.admin_bron_others_menu(lang=lang))
        await state.set_state(st.adminst.bron_others_menu)
        return

    success = db.bron_cancel_date(
        date_str_dd_mm=data["cancel_day_date"],
        tg_id=user_id,
        reason=reason
    )

    if success:
        await bot.send_message(chat_id=user_id, text=cf.get_text(lang, "message_text", "admin_bron_otherday_cancel_text").format(date=data["cancel_day_date"]))
    else:
        await bot.send_message(chat_id=user_id, text="❌ Ошибка при отмене бронирования.")

    await bot.send_message(chat_id=user_id, text=cf.get_text(lang, "message_text", "admin_bron_others_menu"), reply_markup=kb_r.admin_bron_others_menu(lang=lang))
    await state.set_state(st.adminst.bron_others_menu)

######################################################################
# ADMIN ANALYTIC MENU
async def analytic_menu(bot, message, state, user_id, lang):
    if message.text == cf.get_text(lang, "buttons", "back"):
        await bot.send_message(chat_id=user_id, text=cf.get_text(lang, "message_text", "admin_main_menu_text"), reply_markup=kb_r.admin_main_menu(lang=lang))
        await state.set_state(st.adminst.main_menu)

    else:
        await bot.send_message(chat_id=user_id, text="eRRoR")

######################################################################
# ADMIN CHANGE_LANGUAGE
async def language_menu(bot, message, state, user_id, lang):
    if message.text == cf.get_text(lang, "buttons", "back"):
        await bot.send_message(chat_id=user_id, text=cf.get_text(lang, 'message_text', "admin_main_menu_text"), reply_markup=kb_r.admin_main_menu(lang=lang))
        await state.set_state(st.adminst.main_menu)
    elif message.text in cf.languages:
        db.update_user_lang(telegram_id=user_id, new_lang=message.text.split()[1])
        await bot.send_message(chat_id=user_id, text=cf.get_text(message.text, "message_text", "admin_main_menu_text"), reply_markup=kb_r.admin_main_menu(lang=message.text))
        await state.update_data(lang=message.text)
        await state.set_state(st.adminst.main_menu)
    else:
        await bot.send_message(chat_id=user_id, text="eRRoR Lang")

######################################################################