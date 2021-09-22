from tag import *
from organize import *
from impersonate import *

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
    channel = client.get_channel(int(get_channel_id(keyword)))

    modified_message = ""

    if message.reference:
        reply_message_id = int(message.reference.message_id)
        reply_message = await message.channel.fetch_message(reply_message_id)
        modified_message = f"**{reply_message.author.name}**\n{reply_message.content}"
        bot_message = await channel.send(modified_message)
        await impersonate(bot_message, reply_message.author)

        if reply_message.attachments:
            for attachment in reply_message.attachments:
                file = await attachment.to_file()
                bot_message = await channel.send(file=file)
                await impersonate(bot_message, reply_message.author)
    else:
        modified_message = f"**{message.author.name}**\n{message.content[len(message.content.split()[0]) + 1:]}"
        bot_message = await channel.send(modified_message)
        await impersonate(bot_message, message.author)
        if message.attachments:
            for attachment in message.attachments:
                file = await attachment.to_file()
                bot_message = await channel.send(file=file)
                await impersonate(bot_message, message.author)

    await message.delete()
