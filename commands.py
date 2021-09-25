from discord.utils import get
from tag import *
from organize import *
from impersonate import *
from utils import *


async def dot_listen(message):
    receiver = message.author.id
    sender = get_sender(message.content.split()[1])

    if sender is None:
        return

    enable_ping(receiver, sender)
    await message.add_reaction("✅")


async def dot_ghost(message):
    receiver = message.author.id
    sender = get_sender(message.content.split()[1])

    if sender is None:
        return

    disable_ping(receiver, sender)
    await message.add_reaction("✅")


async def dot_dot(message):
    sender_id = message.author.id
    message_with_tags = generate_tag(sender_id)
    if message_with_tags:
        await message.delete()
        bot_tag = await message.channel.send(message_with_tags)
        await bot_tag.delete()


async def dot_add(message):
    keyword = message.content.split()[1]

    if keyword:
        add_keyword(keyword, int(message.channel.id))
        await message.add_reaction("✅")


async def dot_organize(client, message):
    keyword = message.content.split()[0]
    message_channel = client.get_channel(int(get_channel_id(keyword)))

    if message.reference:
        reply_message = await message.channel.fetch_message(
            message.reference.message_id
        )

        message_author = reply_message.author
        message_content = reply_message.content
        message_attachment = (
            [await attch.to_file() for attch in reply_message.attachments]
            if reply_message.attachments
            else []
        )

        if len(message.content.split()) > 1 and message.content.split()[1] == "-":
            await reply_message.delete()
    else:
        message_author = message.author
        message_content = f"{message.content[len(message.content.split()[0]) + 1:]}"
        message_attachment = (
            [await attch.to_file() for attch in message.attachments]
            if message.attachments
            else []
        )

    await impersonate(
        message_author, message_channel, message_content, message_attachment
    )

    await message.delete()


async def dot_jay(client, message, server_id):
    msg_split = message.content.split()

    user = message.author

    if len(msg_split) == 2:
        user = message.mentions[0]

    guild = client.get_guild(server_id)
    Jay = get(guild.roles, name="Jay")

    if Jay in user.roles:
        await user.remove_roles(Jay)
    else:
        await user.add_roles(Jay)

    await message.delete()


async def dot_lorem_ipsum(message):
    message_content = get_lorem()
    await impersonate(message.author, message.channel, message_content, None)
    await impersonate(message.author, message.channel, message_content, None)
    await impersonate(message.author, message.channel, message_content, None)
