from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

import config as cf

# ADMIN POST BUTTONS
def admin_post_button(buttons):
    inline_keyboard = InlineKeyboardBuilder()
    for i in buttons:
        inline_keyboard.add(InlineKeyboardButton(text=i['text'], url=i['url']))
    return inline_keyboard.as_markup()


# ADMIN BRON INFO MENU
def admin_bron_info_menu(lang, bron_id, tg_id):
    inline_keyboard = InlineKeyboardBuilder()
    inline_keyboard.add(
        InlineKeyboardButton(text=cf.get_text(lang, "buttons", "admin_btn_1_1_0"), url=f"tg://user?id={tg_id}"),
        InlineKeyboardButton(text=cf.get_text(lang, "buttons", "admin_btn_1_1_1"), callback_data=f"remind_{bron_id}"), 
        InlineKeyboardButton(text=cf.get_text(lang, "buttons", "admin_btn_1_1_2"), callback_data=f"cancel_{bron_id}")
    )
    inline_keyboard.adjust(1)
    return inline_keyboard.as_markup()


# ADMIN BRON CANCEL MENU
def admin_bron_cancel_menu(lang):
    inline_keyboard = InlineKeyboardBuilder()
    inline_keyboard.add(
        InlineKeyboardButton(text=cf.get_text(lang, "buttons", "reason_no_show"), callback_data="reason_no_show"),
        InlineKeyboardButton(text=cf.get_text(lang, "buttons", "reason_by_user"), callback_data="reason_by_user"),
        InlineKeyboardButton(text=cf.get_text(lang, "buttons", "reason_technical"), callback_data="reason_technical"),
        InlineKeyboardButton(text=cf.get_text(lang, "buttons", "reason_other"), callback_data="reason_other"),
        InlineKeyboardButton(text=cf.get_text(lang, "buttons", "back"), callback_data="back")    
    )
    inline_keyboard.adjust(1)
    return inline_keyboard.as_markup()