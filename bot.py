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

    if message.author == client.user:
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

    elif is_valid_keyword(message.content.split()[0]):
        keyword = message.content.split()[0]
        channel = client.get_channel(int(get_channel_id(keyword)))

        modified_message = ""

        if message.reference:
            reply_message_id = int(message.reference.message_id)
            reply_message = await message.channel.fetch_message(reply_message_id)
            modified_message = (
                f"**{reply_message.author.name}**\n{reply_message.content}"
            )
            await channel.send(modified_message)
            if reply_message.attachments:
                for attachment in reply_message.attachments:
                    file = await attachment.to_file()
                    await channel.send(file=file)
        else:
            modified_message = f"**{message.author.name}**\n{message.content[len(message.content.split()[0]) + 1:]}"
            await channel.send(modified_message)
            if message.attachments:
                for attachment in message.attachments:
                    file = await attachment.to_file()
                    await channel.send(file=file)

        await message.delete()

    elif message.content.startswith(".add"):
        keyword = message.content.split()[1]

        if keyword:
            add_keyword(keyword, int(message.channel.id))
            await message.add_reaction("✅")


load_dotenv()
client.run(os.getenv("DISCORD_TOKEN"))
