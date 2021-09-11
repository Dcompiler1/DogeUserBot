# @DogeUserBot - < https://t.me/DogeUserBot >
# Copyright (C) 2021 - DOG-E
# All rights reserved.
#
# This file is a part of < https://github.com/DOG-E/DogeUserBot >
# Please read the GNU Affero General Public License in;
# < https://www.github.com/DOG-E/DogeUserBot/blob/DOGE/LICENSE/ >
# ================================================================
from asyncio import sleep
from os import remove

from ..helpers.utils.format import md_to_text, paste_message
from .data import _sudousers_list


async def eor(
    event,
    text,
    parse_mode=None,
    link_preview=None,
    file_name=None,
    aslink=False,
    deflink=False,
    noformat=False,
    linktext=None,
    caption=None,
):  # sourcery no-metrics
    sudo_users = _sudousers_list()
    link_preview = link_preview or False
    reply_to = await event.get_reply_message()
    if len(text) < 4096 and not deflink:
        parse_mode = parse_mode or "md"
        if event.sender_id in sudo_users:
            if reply_to:
                return await reply_to.reply(
                    text,
                    parse_mode=parse_mode,
                    link_preview=link_preview,
                )
            return await event.reply(
                text,
                parse_mode=parse_mode,
                link_preview=link_preview,
            )
        await event.edit(
            text,
            parse_mode=parse_mode,
            link_preview=link_preview,
        )
        return event
    if not noformat:
        text = md_to_text(text)
    if aslink or deflink:
        linktext = linktext or "Message was to big so pasted to bin"
        response = await paste_message(text, pastetype="s")
        text = linktext + f" [here]({response})"
        if event.sender_id in sudo_users:
            if reply_to:
                return await reply_to.reply(text, link_preview=link_preview)
            return await event.reply(text, link_preview=link_preview)
        await event.edit(text, link_preview=link_preview)
        return event
    file_name = file_name or "@DogeUserBot.txt"
    caption = caption or None
    with open(file_name, "w+") as output:
        output.write(text)
    if reply_to:
        await reply_to.reply(caption, file=file_name)
        await event.delete()
        return remove(file_name)
    if event.sender_id in sudo_users:
        await event.reply(caption, file=file_name)
        await event.delete()
        return remove(file_name)
    await event.client.send_file(
        event.chat_id,
        file_name,
        caption=caption,
    )
    await event.delete()
    remove(file_name)


async def edl(
    event,
    text,
    time=None,
    parse_mode=None,
    link_preview=None,
):
    sudo_users = _sudousers_list()
    parse_mode = parse_mode or "md"
    link_preview = link_preview or False
    time = time or 10
    if event.sender_id in sudo_users:
        reply_to = await event.get_reply_message()
        dogevent = (
            await reply_to.reply(
                text,
                link_preview=link_preview,
                parse_mode=parse_mode,
            )
            if reply_to
            else await event.reply(
                text,
                link_preview=link_preview,
                parse_mode=parse_mode,
            )
        )
    else:
        dogevent = await event.edit(
            text,
            link_preview=link_preview,
            parse_mode=parse_mode,
        )
    await sleep(time)
    return await dogevent.delete()
