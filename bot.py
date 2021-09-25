from dotenv import load_dotenv
import os
import discord

from commands import *

client = discord.Client()


def log(message):
    print(message)


@client.event
async def on_ready():
    log("He is a dog, and a butler. Who wouldn't love him?")


@client.event
async def on_message(message):
    log(f"#{message.channel} ({message.author}) {message.content}")

    if message.author.id == client.user.id or message.webhook_id:
        return

    if message.content == "which barkley":
        await message.channel.send(f"{os.uname()[1]}")
    elif message.content.startswith(".listen"):
        await dot_listen(message)
    elif message.content.startswith(".ghost"):
        await dot_ghost(message)
    elif message.content == ".":
        await dot_dot(message)
    elif message.content.startswith(".j"):
        await dot_jay(client, message, message.guild.id)
    elif message.content.startswith(".add"):
        await dot_add(message)
    elif message.content == "lorem":
        await dot_lorem_ipsum(message)
    elif is_valid_keyword(message.content.split()[0]):
        await dot_organize(client, message)


load_dotenv()
client.run(os.getenv("DISCORD_TOKEN"))
