from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import  Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import states.states as st
import config as cf
import database as db
import keyboards.reply.reply_kb as kb_r
import keyboards.inline.inline_kb as kb_i
import handlers.user.user_func as us_f
import handlers.admin.admin_func as ad_f


bot = Bot(token=cf.TOKEN)
dp = Dispatcher()
router = Router()

# @router.message(F.sticker)
# async def get_sticker_id(message: Message):
#     await message.reply(f"`{message.sticker.file_id}`")


# @router.message()
# async def cc(message: Message):
#     if message.forward_from:
#         user_id = message.forward_from.id
#         print(f"🔄 ID пересланного пользователя: {user_id}")
#     else:
#         print(f"📥 Это не пересланное сообщение. Ваш ID: {message.from_user.id}")


@router.message(F.text.startswith("/start"))
async def start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    users = db.get_user_all()
    admins = cf.admins()
    if user_id in admins:
        lang = users[user_id]['lang']
        await bot.send_message(chat_id=user_id, text=cf.get_text(lang, 'message_text', 'admin_main_menu_text'), reply_markup=kb_r.admin_main_menu(lang))
        await state.update_data(lang=lang)
        await state.set_state(st.adminst.main_menu)
    elif user_id in users:
        lang = users[user_id]['lang']
        await state.update_data(language=lang)
        await bot.send_message(chat_id=user_id, text=cf.get_text(lang, 'message_text', 'main_menu_text'),reply_markup=kb_r.menu(lang=lang))
        await state.set_state(st.userst.menu)
    else:
        await bot.send_message(chat_id=user_id, text=cf.translations['start'], reply_markup=kb_r.start_key(), parse_mode='HTML')
        await state.set_state(st.userst.language)

###################################################################################################

@router.message(st.userst.language)
async def user_ask_phone(message: Message, state: FSMContext):
    await us_f.ask_phone(bot, message, state)


@router.message(st.userst.phone)
async def user_check_phone(message: Message, state: FSMContext):
    await us_f.check_phone(bot, message, state)


@router.message(st.userst.fio)
async def user_fio_user(message: Message, state: FSMContext):
    await us_f.fio_user(bot, message, state)
    

@router.message(st.userst.conf)
async def user_conf(message: Message, state: FSMContext):
    await us_f.conf(bot, message, state)


@router.message(st.userst.menu)
async def user_menu(message: Message, state: FSMContext):
    await us_f.menu(bot, message, state)


@router.message(st.userst.orderhistory)
async def user_cancel_and_history(message: Message, state: FSMContext):
    await us_f.cancel_and_history(bot, message, state)


@router.message(st.userst.orderhistory_back)
async def user_show_time_to_cancel(message: Message, state: FSMContext):
    await us_f.show_time_to_cancel(bot, message, state)


@router.message(st.userst.description_cancel)
async def user_send_cancel_time(message: Message, state: FSMContext):
    await us_f.send_cancel_time(bot, message, state)


@router.message(st.userst.change_language)
async def user_change_lang_and_menu(message: Message, state: FSMContext):
    await us_f.change_lang_and_menu(bot, message, state)


@router.message(st.userst.location)
async def user_back_location(message: Message, state: FSMContext):
    await us_f.back_location(bot, message, state)


@router.message(st.userst.barber_contact)
async def user_back_contact(message: Message, state: FSMContext):
    await us_f.back_contact(bot, message, state)


@router.message(st.userst.book_barber)
async def user_barber_book(message: Message, state: FSMContext):
    await us_f.barber_book(bot, message, state)


@router.message(st.userst.test_month)
async def user_confirmation_time(message: Message, state: FSMContext):
    await us_f.confirmation_time_1(bot, message, state)


@router.message(st.userst.conf_time)
async def user_confirmation_time(message: Message, state: FSMContext):
    await us_f.confirmation_time_2(bot, message, state)


@router.message(st.userst.conf_time_and_menu)
async def user_confirmation_time_menu(message: Message, state: FSMContext):
    await us_f.confirmation_time_menu(bot, message, state)


###################################################################################################
# ADMIN MAIN_MENU
@router.message(st.adminst.main_menu)
async def admin_menu(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data.get("lang")
    await ad_f.main_menu(bot, message, state, user_id, lang)


# ADMIN NEW POST BUTTON
@router.message(st.adminst.new_post_menu)
async def admin_new_post_menu(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data.get("lang")
    await ad_f.new_post_menu(bot, message, state, user_id, lang)


# ADMIN POST DESCRIPTION MENU
@router.message(st.adminst.post_description)
async def admin_post_description_menu(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data.get("lang")
    await ad_f.post_description_menu(bot, message, state, user_id, lang)


# ADMIN POST PHOTO MENU
@router.message(st.adminst.post_photo)
async def admin_post_photo_menu(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data.get("lang")
    await ad_f.post_photo_menu(bot, message, state, user_id, lang)


# ADMIN POST BUTTON MENU
@router.message(st.adminst.post_button)
async def admin_post_button_menu(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data.get("lang")
    await ad_f.post_button_menu(bot, message, state, user_id, lang)


# ADMIN POST CONFIRM MENU
@router.message(st.adminst.post_confirm)
async def admin_post_confirm_menu(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data.get("lang")
    await ad_f.post_confirm_menu(bot, message, state, user_id, lang)


# ADMIN POST CONFIRM NEXT MENU
@router.message(st.adminst.post_confirm_next)
async def admin_post_confirm_next_menu(message: Message, state: FSMContext):
    user_id = message.from_user.id
    clients = db.get_client_all()
    data = await state.get_data()
    lang = data.get("lang")
    await ad_f.post_confirm_next_menu(bot, message, state, clients, user_id, lang)


# ADMIN FIRST BUTTON
@router.message(st.adminst.bron_menu)
async def admin_bron_menu(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data.get("lang")
    await ad_f.bron_menu(bot, message, state, user_id, lang)


# AMDIN BRON TODAY MENU
@router.message(st.adminst.bron_today_menu)
async def admin_bron_today_menu(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data.get("lang")
    await ad_f.bron_today_menu(bot, message, state, user_id, lang)


# ADMIN BRON INFO MENU
@router.message(st.adminst.bron_info_menu)
async def admin_bron_info_menu(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data.get("lang")
    await ad_f.bron_info_menu(bot, message, callback=None, state=state, user_id=user_id, lang=lang)

@router.callback_query(st.adminst.bron_info_menu)
async def admin_bron_info_menu(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    data = await state.get_data()
    lang = data.get("lang")
    await ad_f.bron_info_menu(bot, message=None, callback=callback, state=state, user_id=user_id, lang=lang)


# ADMIN BRON OTHERS MENU
@router.message(st.adminst.bron_others_menu)
async def admin_bron_others_menu(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data.get("lang")
    await ad_f.bron_others_menu(bot, message, state, user_id, lang)


# ADMIN BRON OTHERDAY MENU
@router.message(st.adminst.bron_otherday_menu)
async def admin_bron_otherday_menu(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data.get("lang")
    await ad_f.bron_otherday_menu(bot, message, state, user_id, lang)


# ADMIN BRON CANCEL REASON MENU
@router.callback_query(st.adminst.bron_cancel_reason_menu)
async def admin_bron_cancel_reason_call_menu(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    users = db.get_user_all()
    data = await state.get_data()
    lang = data.get("lang")
    await ad_f.bron_cancel_reason_menu(bot, callback, state, users, user_id, lang)
    
@router.message(st.adminst.bron_cancel_reason_menu)
async def admin_bron_cancel_reason_msg_menu(message: Message, state: FSMContext):
    user_id = message.from_user.id
    users = db.get_user_all()
    data = await state.get_data()
    lang = data.get("lang")
    await ad_f.bron_other_reason_text(bot, message, state, users, user_id, lang)


# ADMIN BRON CANCEL DAY MENU
@router.message(st.adminst.bron_cancel_day_reason)
async def admin_bron_cancel_day_reason(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data.get("lang")
    await ad_f.bron_cancel_day_reason(bot, message, state, user_id, lang)


# ADMIN SECOND BUTTON
@router.message(st.adminst.analytics)
async def admin_analytic_menu(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data.get("lang")
    await ad_f.analytic_menu(bot, message, state, user_id, lang)


# ADMIN FOURTH BUTTON
@router.message(st.adminst.language)
async def admin_language_menu(message: Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    lang = data.get("lang")
    await ad_f.language_menu(bot, message, state, user_id, lang)