from dotenv import load_dotenv
import os
import discord
import requests

from tag import *
from organize import *

client = discord.Client()


def log(message):
    print(message)


@client.event
async def on_ready():
    log("He is a dog, and a butler. Who wouldn't love him?")


@client.event
async def on_message(message):
    log(f"{message.channel}: {message.author}: {message.content}")

    if message.attachments:
        attachment_message = ""

        for attachment in message.attachments:
            attachment_message += (
                f"**{message.author.name} sent `{attachment.filename}`**\n"
                f"`{float(attachment.size)/1000} KB`\n"
                f"{message.attachments[0].url}\n"
            )

        if message.content != "":
            attachment_message += message.content

        await message.channel.send(attachment_message)

    elif message.author == client.user:
        return

    elif message.content.startswith(".listen"):
        receiver = message.author.id
        sender = get_sender(message.content.split()[1])

        if sender is None:
            return

        enable_ping(receiver, sender)
        await message.add_reaction("✅")

    elif message.content.startswith(".ghost"):
        receiver = message.author.id
        sender = get_sender(message.content.split()[1])

        if not sender:
            return

        disable_ping(receiver, sender)
        await message.add_reaction("✅")

    elif message.content == ".":
        sender_id = message.author.id
        message_with_tags = generate_tag(sender_id)
        if message_with_tags:
            await message.delete()
            await message.channel.send(message_with_tags)

    elif is_valid_keyword(message.content.split()[0]) == 1:
        modified_message = ""

        if message.reference:
            reply_message_id = int(message.reference.message_id)
            reply_message = await message.channel.fetch_message(reply_message_id)
            modified_message = (
                f"**{reply_message.author.name}**\n{reply_message.content}"
            )
        else:
            modified_message = f"**{message.author.name}**\n{message.content[len(message.content.split()[0]) + 1:]}"

        keyword = message.content.split()[0]

        channel_id = int(get_channel_id(keyword))
        channel = client.get_channel(channel_id)

        if modified_message != "":
            await message.delete()
            await channel.send(modified_message)

    elif message.content.startswith(".add"):
        keyword = message.content.split()[1]

        if keyword:
            add_keyword(keyword, int(message.channel.id))
            await message.add_reaction("✅")


load_dotenv()
client.run(os.getenv("DISCORD_TOKEN"))
