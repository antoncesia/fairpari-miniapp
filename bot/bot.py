"""Telegram-бот FairPari (прототип) — путь пользователя до Mini App по брифу.

Шаги (см. карту бота, разделы С-xx / В-xx):
  1. Профиль бота: About и Description на 4 языках (С-07).
  2. /start [ref] — реф-метка вебмастера запоминается при первом входе и не перезаписывается (В-08).
  3. Язык — по языку Telegram; если язык не из списка — экран «👇 Choose a language» (В-07, решение прототипа).
     Сменить язык — команда /language (где разместить смену — открытый вопрос В-07).
  4. Главное меню: картинка + текст одним сообщением, [Имя] — имя в Telegram (С-08), суммы по языку (С-09),
     кнопки «Регистрация 🔥» → Mini App, «FairPari Channel 📢» по языку, «Поддержка 🆘» (С-10).
  5. После регистрации Mini App открывает бота по ссылке ?start=reg_done → кнопка становится «Играть ▶️»,
     через 5 минут — «Приветственный бонус», один раз (С-13). В боевой версии статус даёт бэкенд по initData.
  Бонусы пн/чт/пт не отправляются (С-14).

Запуск: bot/run.sh (токен — в bot/.env, в репозиторий не попадает).
"""
import asyncio
import logging
import os
import pathlib
import sqlite3
import time
from typing import Optional
from urllib.parse import urlencode

from aiogram import Bot, Dispatcher, F, types
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.types import (BotCommand, BotCommandScopeDefault, FSInputFile, InlineKeyboardButton,
                           InlineKeyboardMarkup, WebAppInfo)

import texts as T

ROOT = pathlib.Path(__file__).resolve().parent


def load_env() -> None:
    env = ROOT / ".env"
    if env.exists():
        for line in env.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


load_env()
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
APP_URL = os.environ.get("APP_URL", "https://antoncesia.github.io/fairpari-miniapp/").rstrip("/") + "/"
BONUS_DELAY_SEC = int(os.environ.get("BONUS_DELAY_SEC", "300"))
DEFAULT_REF = os.environ.get("DEFAULT_REF", "ref_339")
SYNC_PROFILE = os.environ.get("SYNC_PROFILE", "1") == "1"

MEDIA_MENU = ROOT / "media" / "main_menu.png"
MEDIA_BONUS = ROOT / "media" / "welcome_bonus.jpg"
SERVICE_ARGS = {"reg_done", "auth_ok"}

log = logging.getLogger("fairpari-bot")
dp = Dispatcher()
BOT_USERNAME = ""
_file_ids: dict = {}

# ---------------- хранилище ----------------
DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)
db = sqlite3.connect(DATA / "bot.sqlite")
db.row_factory = sqlite3.Row
db.executescript("""
CREATE TABLE IF NOT EXISTS users(
  id INTEGER PRIMARY KEY, first_name TEXT, lang TEXT, ref TEXT,
  created_at INTEGER, registered_at INTEGER, bonus_due_at INTEGER, bonus_sent_at INTEGER, blocked_at INTEGER);
CREATE TABLE IF NOT EXISTS events(user_id INTEGER, kind TEXT, ts INTEGER, meta TEXT);
""")
db.commit()


def now() -> int:
    return int(time.time())


def event(uid: int, kind: str, meta: str = "") -> None:
    db.execute("INSERT INTO events VALUES (?,?,?,?)", (uid, kind, now(), meta))
    db.commit()


def get_user(uid: int) -> Optional[sqlite3.Row]:
    return db.execute("SELECT * FROM users WHERE id=?", (uid,)).fetchone()


def ensure_user(u: types.User, ref: Optional[str]) -> sqlite3.Row:
    row = get_user(u.id)
    if row is None:
        db.execute("INSERT INTO users(id, first_name, ref, created_at) VALUES (?,?,?,?)",
                   (u.id, u.first_name, ref or DEFAULT_REF, now()))
        event(u.id, "start_first", ref or DEFAULT_REF)
    else:
        # первая реф-метка не перезаписывается — защита sub_id вебмастера (В-08)
        db.execute("UPDATE users SET first_name=?, ref=COALESCE(ref, ?), blocked_at=NULL WHERE id=?",
                   (u.first_name, ref or DEFAULT_REF, u.id))
        event(u.id, "start_again", ref or "")
    db.commit()
    return get_user(u.id)


def lang_from_telegram(code: Optional[str]) -> Optional[str]:
    code = (code or "").lower()
    for lang in T.LANGS:
        if code.startswith(lang):
            return lang
    return None


# ---------------- клавиатуры ----------------
def app_url(row: sqlite3.Row) -> str:
    return APP_URL + "?" + urlencode({"ref": row["ref"] or DEFAULT_REF, "lang": row["lang"] or T.DEFAULT_LANG, "bot": BOT_USERNAME})


def menu_keyboard(row: sqlite3.Row) -> InlineKeyboardMarkup:
    lang = row["lang"] or T.DEFAULT_LANG
    b = T.BUTTONS[lang]
    # «Играть ▶️»: ссылка для зарегистрированных не дана (В-12) — пока ведёт в тот же Mini App
    main_text = b["play"] if row["registered_at"] else b["register"]
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=main_text, web_app=WebAppInfo(url=app_url(row)))],
        [InlineKeyboardButton(text=b["channel"], url=T.CHANNELS[lang]),
         InlineKeyboardButton(text=b["support"], url=T.SUPPORT_URL)],
    ])


def lang_keyboard() -> InlineKeyboardMarkup:
    btn = [InlineKeyboardButton(text=T.LANG_NAMES[l], callback_data="lang:" + l) for l in T.LANGS]
    return InlineKeyboardMarkup(inline_keyboard=[btn[:2], btn[2:]])


async def send_photo_cached(bot: Bot, chat_id: int, path: pathlib.Path, **kw) -> None:
    key = path.name
    photo = _file_ids.get(key) or FSInputFile(path)
    msg = await bot.send_photo(chat_id, photo, **kw)
    if key not in _file_ids and msg.photo:
        _file_ids[key] = msg.photo[-1].file_id


async def send_menu(bot: Bot, chat_id: int, row: sqlite3.Row) -> None:
    lang = row["lang"] or T.DEFAULT_LANG
    sport, casino = T.BONUS[lang]
    caption = T.MENU[lang].format(name=row["first_name"] or "", sport=sport, casino=casino)
    await send_photo_cached(bot, chat_id, MEDIA_MENU, caption=caption, reply_markup=menu_keyboard(row))
    event(row["id"], "menu_shown", lang)


# ---------------- обработчики ----------------
@dp.message(CommandStart())
async def on_start(msg: types.Message, command: CommandObject, bot: Bot) -> None:
    arg = (command.args or "").strip()
    u = msg.from_user
    if arg in SERVICE_ARGS:
        row = ensure_user(u, None)
        if not row["registered_at"]:
            due = now() + BONUS_DELAY_SEC if arg == "reg_done" else None
            db.execute("UPDATE users SET registered_at=?, bonus_due_at=COALESCE(bonus_due_at, ?) WHERE id=?",
                       (now(), due, u.id))
            db.commit()
            event(u.id, arg)
        row = get_user(u.id)
        if not row["lang"]:
            db.execute("UPDATE users SET lang=? WHERE id=?", (lang_from_telegram(u.language_code) or T.DEFAULT_LANG, u.id))
            db.commit()
            row = get_user(u.id)
        await send_menu(bot, msg.chat.id, row)
        return

    row = ensure_user(u, arg or None)
    if not row["lang"]:
        lang = lang_from_telegram(u.language_code)
        if lang is None:  # язык Telegram не из списка — просим выбрать (В-07)
            await msg.answer(T.CHOOSE_LANG[T.DEFAULT_LANG], reply_markup=lang_keyboard())
            event(u.id, "lang_prompt", u.language_code or "")
            return
        db.execute("UPDATE users SET lang=? WHERE id=?", (lang, u.id))
        db.commit()
        event(u.id, "lang_auto", lang)
        row = get_user(u.id)
    await send_menu(bot, msg.chat.id, row)


@dp.message(Command("language"))
async def on_language(msg: types.Message) -> None:
    row = get_user(msg.from_user.id)
    lang = (row["lang"] if row and row["lang"] else None) or T.DEFAULT_LANG
    await msg.answer(T.CHOOSE_LANG[lang], reply_markup=lang_keyboard())


@dp.callback_query(F.data.startswith("lang:"))
async def on_lang_pick(cb: types.CallbackQuery, bot: Bot) -> None:
    lang = cb.data.split(":", 1)[1]
    if lang not in T.LANGS:
        await cb.answer()
        return
    ensure_user(cb.from_user, None)
    db.execute("UPDATE users SET lang=? WHERE id=?", (lang, cb.from_user.id))
    db.commit()
    event(cb.from_user.id, "lang_set", lang)
    await cb.answer(T.LANG_NAMES[lang])
    try:
        await cb.message.delete()
    except TelegramBadRequest:
        pass
    await send_menu(bot, cb.message.chat.id, get_user(cb.from_user.id))


@dp.my_chat_member()
async def on_member(upd: types.ChatMemberUpdated) -> None:
    status = upd.new_chat_member.status
    if status == "kicked":
        db.execute("UPDATE users SET blocked_at=? WHERE id=?", (now(), upd.from_user.id))
        db.commit()
        event(upd.from_user.id, "blocked")
    elif status == "member":
        event(upd.from_user.id, "unblocked")


# ---------------- приветственный бонус ----------------
async def bonus_loop(bot: Bot) -> None:
    while True:
        rows = db.execute("SELECT * FROM users WHERE bonus_due_at IS NOT NULL AND bonus_due_at<=? "
                          "AND bonus_sent_at IS NULL AND blocked_at IS NULL", (now(),)).fetchall()
        for row in rows:
            lang = row["lang"] or T.DEFAULT_LANG
            kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=T.BUTTONS[lang]["bonus"], url=T.WELCOME_BONUS_URL)]])
            try:
                await send_photo_cached(bot, row["id"], MEDIA_BONUS, caption=T.WELCOME_BONUS[lang], reply_markup=kb)
                db.execute("UPDATE users SET bonus_sent_at=? WHERE id=?", (now(), row["id"]))
                event(row["id"], "welcome_bonus_sent", lang)
            except TelegramForbiddenError:
                db.execute("UPDATE users SET blocked_at=? WHERE id=?", (now(), row["id"]))
                event(row["id"], "blocked")
            except Exception:  # не роняем цикл из-за одного пользователя
                log.exception("welcome bonus failed for %s", row["id"])
            db.commit()
        await asyncio.sleep(15)


# ---------------- профиль бота ----------------
async def sync_profile(bot: Bot) -> None:
    await bot.set_my_short_description(T.ABOUT[T.DEFAULT_LANG])
    await bot.set_my_description(T.DESCRIPTION[T.DEFAULT_LANG])
    await bot.set_my_commands([BotCommand(command=c, description=d) for c, d in T.COMMANDS[T.DEFAULT_LANG].items()],
                              scope=BotCommandScopeDefault())
    for lang in T.LANGS + ("ru",):
        await bot.set_my_short_description(T.ABOUT[lang], language_code=lang)
        await bot.set_my_description(T.DESCRIPTION[lang], language_code=lang)
        if lang in T.COMMANDS:
            await bot.set_my_commands([BotCommand(command=c, description=d) for c, d in T.COMMANDS[lang].items()],
                                      scope=BotCommandScopeDefault(), language_code=lang)
    log.info("Профиль бота обновлён: About, Description, команды")


async def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    if not BOT_TOKEN:
        raise SystemExit("Нет BOT_TOKEN: впишите токен в bot/.env (см. bot/.env.example)")
    T.check_limits()
    bot = Bot(BOT_TOKEN)
    global BOT_USERNAME
    me = await bot.get_me()
    BOT_USERNAME = me.username
    log.info("Бот @%s запущен, Mini App: %s", BOT_USERNAME, APP_URL)
    if SYNC_PROFILE:
        await sync_profile(bot)
    asyncio.create_task(bonus_loop(bot))
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
