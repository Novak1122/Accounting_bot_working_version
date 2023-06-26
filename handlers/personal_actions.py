import logging
from aiogram import types
import re
from bot import botdb
from dispatcher import dp


@dp.message_handler(commands="start")
async def start(message: types.Message):
    if not botdb.user_exist(message.from_user.id):
        botdb.add_user(message.from_user.id)
    users = botdb.get_users()
    logging.info(f"Users: {users}")
    await message.bot.send_message(chat_id=message.from_user.id, text="""Добро пожаловать! 
    [Как пользоваться ботом]
    /start – начало роботы с ботом
    Для внесения расходов используйте одну из команд - /spent, /s, !spent, !s
    Для внесения доходов используйте следующие команды - /earned, /e, !earned, !e
    К примеру :
    !spent 100
    /earned 300
    Для того что б посмотреть историю внесенных данных используйте одну из команд – /history, /h, !history, !h
    Если необходимо узнать историю операций за день/неделю/месяц, используйте такие команды:
    !h day
    !h week
    !h month""")


@dp.message_handler(commands=("spent", "earned", "s", "e"), commands_prefix="/!")
async def start(message: types.Message):
    cmd_variants = (('/spent', '/s', '!spent', '!s'), ('/earned', '/e', '!earned', '!e'))
    operation = '-' if message.text.startswith(cmd_variants[0]) else '+'

    value = message.text
    for i in cmd_variants:
        for j in i:
            value = value.replace(j, '').strip()

    if len(value):
        x = re.findall(r"\d+(?:.\d+)?", value)
        if len(x):
            value = float(x[0].replace(',', '.'))

            botdb.add_record(message.from_user.id, operation, value)

            if operation == '-':
                await message.reply("✅ Запись о <u><b>расходе</b></u> успешно внесена!")
            else:
                await message.reply("✅ Запись о <u><b>доходе</b></u> успешно внесена!")
        else:
            await message.reply("Не удалось определить сумму!")
    else:
        await message.reply("Не введена сумма!")


@dp.message_handler(commands=("history", "h"), commands_prefix="/!")
async def start(message: types.Message):
    cmd_variants = ('/history', '/h', '!history', '!h')
    within_als = {
        "day": ('today', 'day', 'сегодня', 'день'),
        "week": ('week', 'неделю'),
        "month": ('month', 'месяц'),
    }

    cmd = message.text
    for r in cmd_variants:
        cmd = cmd.replace(r, '').strip()

    within = 'day'
    if len(cmd):
        for k in within_als:
            for als in within_als[k]:
                if (als == cmd):
                    within = k

    records = botdb.get_records(message.from_user.id, within)

    if len(records):
        answer = f"🕘 История операций за {within_als[within][-1]}\n\n"

        for r in records:
            answer += "<b>" + ("➖ Расход" if not r[2] else "➕ Доход") + "</b>"
            answer += f" - {r[3]}"
            answer += f" <i>({r[4]})</i>\n"

        await message.reply(answer)
    else:
        await message.reply("Записей не обнаружено!")
