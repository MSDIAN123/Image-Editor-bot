
from pyrogram import filters
from szbot import sz
import os
import json
import requests
from pyrogram.types import (CallbackQuery, InlineKeyboardButton,
                            InlineQueryResultArticle, InlineQueryResultPhoto,
                            InputTextMessageContent)
from pykeyboard import InlineKeyboard
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import traceback
from pyrogram.errors import UserNotParticipant          
from szbot.plugins.channel import  *


picmebtns = InlineKeyboardMarkup(
            [       
                [
                    InlineKeyboardButton("Pic me", callback_data="picme me"),
                    InlineKeyboardButton("Hq logo", callback_data="picme hql") 
                ],
                [
                    InlineKeyboardButton("Logo", callback_data="picme new"),
                    InlineKeyboardButton("Wallpaper", callback_data="picme wall")           
                ],   
            ]
        )

async def inline_help_func():
    answerss = [
        InlineQueryResultArticle(
            title="Button Menu",
            description="logo create tool Available",
            input_message_content=InputTextMessageContent(
                """
**Now You can Create your Image Useing Me!**

✪ Pic me : Capture Your Profile Picture.
✪ Hq logo : Create your own hq logo.
✪ Logo : create your own logo.
✪ Wallpaper : Get some new wallpapers.           
                """
            ),
            thumb_url="data:image/jpeg;base64,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",
            reply_markup=picmebtns,
        ),
    ]
    return answerss


@sz.on_inline_query()
async def inline_query_handler(client, query):
    try:
        text = query.query.strip().lower()
        answers = []
        if text.strip() == "":
            answerss = await inline_help_func()
            await client.answer_inline_query(
                query.id, results=answerss, cache_time=10
            )
        elif text.split()[0] == "Logo":
            if len(text.split()) < 3:
                return await client.answer_inline_query(
                    query.id,
                    results=answers,
                    switch_pm_text="Logo",
                )   
        elif text.split()[0] == "hqlogo":
            if len(text.split()) < 3:
                return await client.answer_inline_query(
                    query.id,
                    results=answers,
                    switch_pm_text="Hqlogo",
                )    
        elif text.split()[0] == "wall":
            if len(text.split()) < 3:
                return await client.answer_inline_query(
                    query.id,
                    results=answers,
                    switch_pm_text="wall",
                )
    except Exception as e:
        e = traceback.format_exc()
        return answers
