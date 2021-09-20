from dotenv import load_dotenv
import os
import discord
import json

# prefix = "."

client = discord.Client()


def enable_tag(receiver, sender):
    sender_key = str(sender)
    with open("users.json", "r") as f:
        users = json.load(f)
        # print("entered enable")
        
        if(users.get(sender_key) is None):
            users[sender_key] = []
            # print(users)
        if(receiver not in users.get(sender_key)):
            users.get(sender_key).append(receiver)
    with open("users.json", "w") as f:
        json.dump(users, f)
    # print("done enabling...")


def disable_tag(receiver, sender):
    sender_key = str(sender)
    with open("users.json", "r") as f:
        users = json.load(f)
        print(users)
        if (receiver in users.get(sender_key)):
                users.get(sender_key).remove(receiver)

    with open("users.json", "w") as f:
        json.dump(users, f)


def generate_tag(sender):
    sender_key = str(sender)
    with open("users.json", "r") as f:
        users = json.load(f)
        message = ""
        print(users.get(sender_key))
        for receiver in users.get(sender_key):
            print("receiver = " + str(receiver))
            message += f"<@!{receiver}> " 

    return message


def get_sender(sender_msg):
    sender_id = sender_msg
    if sender_id.startswith('<@!') and sender_id.endswith('>'):
        sender_id = sender_id[3:]
        sender_id = sender_id[:len(sender_id) - 1]
    elif sender_id.startswith('<@') and sender_id.endswith('>'):
        sender_id = sender_id[2:]
        sender_id = sender_id[:len(sender_id) - 1]
    else:
        sender_id = None

    return sender_id


@client.event
async def on_ready():
    print("bot started.")



@client.event
async def on_message(message):
    print("message received")
    if message.content.startswith('.enable pings'):
    # if message.content.startswith('sa'):
        print("enabling pings...")
        receiver = message.author.id
        sender = get_sender(message.content.split()[2])
        # print(sender)
        if (sender):
            enable_tag(receiver, sender)
            # massage = generate_tag(message.author.id)
            # await message.channel.send(massage)
            await message.add_reaction("✅")
    elif message.content.startswith('.disable pings'):
        receiver = message.author.id
        sender = get_sender(message.content.split()[2])
        if (sender):
            await(await message.channel.send(f"<@!{receiver}> removed from <@!{sender}>'s tag list.")).delete(delay=3)
            await message.delete()
            await message.add_reaction("✅")
            disable_tag(receiver, sender)
    else:
        sender = message.author.id
        if (sender):
            massage = generate_tag(message.author.id)
            await message.channel.send(massage)


load_dotenv()
client.run(os.getenv("DISCORD_TOKEN"))
