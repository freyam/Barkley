from dotenv import load_dotenv
import os
import discord
import json
from discord.ext.commands import Bot
bot = Bot(".")
client = discord.Client()


def log(message):
    print(message)

@bot.command()
async def test(ctx):
    await ctx.send("Command executed")

def enable_ping(receiver, sender):
    sender_key = str(sender)

    with open("users.json", "r") as f:
        users = json.load(f)

        users[sender_key] = users.get(sender_key) or []

        if receiver not in users.get(sender_key):
            users.get(sender_key).append(receiver)

    with open("users.json", "w") as f:
        json.dump(users, f)


def disable_ping(receiver, sender):
    sender_key = str(sender)

    with open("users.json", "r") as f:
        users = json.load(f)

        if receiver in users.get(sender_key):
            users.get(sender_key).remove(receiver)

    with open("users.json", "w") as f:
        json.dump(users, f)


def generate_tag(sender) -> str:
    sender_key = str(sender)
    message = ""

    with open("users.json", "r") as f:
        users = json.load(f)
        users[sender_key] = users.get(sender_key) or []

        receivers = users.get(sender_key)
        for receiver in receivers:
            message += f"<@!{receiver}> "

    with open("users.json", "w") as f:
        json.dump(users, f)

    return message


def get_sender(sender_msg) -> str:
    sender_id = str(sender_msg)

    if sender_msg.startswith("<@!") and sender_msg.endswith(">"):
        sender_id = sender_id[3:]
        sender_id = sender_id[: len(sender_id) - 1]
    elif sender_msg.startswith("<@") and sender_msg.endswith(">"):
        sender_id = sender_id[2:]
        sender_id = sender_id[: len(sender_id) - 1]
    else:
        sender_id = None

    return sender_id


def is_operation(possible_command):
    '''
    docstring chutiya
    '''
    with open("channels.json", "r") as f:
        channels = json.load(f)
        keywords = channels.get("keywords")
        if(keywords.get(possible_command) is not None):
            return 1

        return 0


def add_operation(operation, channel_input):
    '''
    some bs
    '''
    channel = int(channel_input)
    with open("channels.json", "r") as f:
        channel_dict = json.load(f)
        keywords = channel_dict.get("keywords")
        keywords[operation] = channel

    with open("channels.json", "w") as f:
        json.dump(channel_dict, f)


def get_channel_id(command):
    with open("channels.json", "r") as f:
        channels = json.load(f)
        keywords = channels.get("keywords")
        return keywords.get(command) 

@client.event
async def on_ready():
    log("Tagomatic has been unleashed!")


@client.event
async def on_message(message):
    log(f"{message.channel}: {message.author}: {message.content}")

    if message.author == client.user:
        # await message.delete()
        print()

    elif message.content.startswith(".listen"):
        receiver = message.author.id
        sender = get_sender(message.content.split()[1])

        if not sender:
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

    elif message.content == '.':
        sender_id = message.author.id
        bot_ping = generate_tag(sender_id)
        if bot_ping:
            await message.delete()
            await message.channel.send(bot_ping)
    
    elif(is_operation(message.content.split()[0]) == 1):
        await message.delete()
        print("valid operation encountered")
        author_x = ""
        message_x = ""
        
        if message.reference:
            
            message_id = int(message.reference.message_id)
            messagee = await message.channel.fetch_message(message_id)
            author_x = f"**{messagee.author.name}**: "
            message_x += f"{messagee.content}"
            # log(messagee.content)
            
        else:
            author_x = f"**{message.author.name}**: "
            message_x += message.content[len(message.content.split()[0]) + 1:]

        channel_id = int(get_channel_id(message.content.split()[0]))
        channel = client.get_channel(channel_id)

        if(message_x and message_x != ""):
            await channel.send(author_x + message_x)

    elif message.content.startswith(".add"):
        channel_id = int(message.channel.id)
        command = message.content.split()[1]

        if(command and command != ""):
            print("command: ", command)
            add_operation(command, channel_id)

        await message.add_reaction("✅")

load_dotenv()
client.run(os.getenv("DISCORD_TOKEN"))
