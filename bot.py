from dotenv import load_dotenv
import os
import discord
import json

# prefix = "."

client = discord.Client()


def enable_tag(receiver, sender):
    
    with open("users.json", "r") as f:
        users = json.load(f)
        print("entered enable")
        
        if(users.get(sender) is None):
            users[sender] = []
            # print(users)
        if(receiver not in users.get(sender)):
            users.get(sender).append(receiver)
    with open("users.json", "w") as f:
        json.dump(users, f)
    print("done enabling...")


def disable_tag(receiver, sender):
    with open("users.json", "r") as f:
        users = json.load(f)
        if (receiver in users.get(sender)):
                users.get(sender).remove(receiver)

    with open("users.json", "w") as f:
        json.dump(users, f)


def generate_tag(sender):
    with open("users.json", "r") as f:
        users = json.load(f)
        message = ""
        print(users)
        for receiver in users.get(sender):
            print("receiver = " + receiver)
            message += "<@!{receiver}> " 

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
            massage = generate_tag(message.author.id)
            await message.channel.send(massage)
            await message.add_reaction("✅")
    elif message.content.startswith('.disable pings'):
        receiver = message.author.id
        sender = get_sender(message.content.split()[2])
        if (sender):
            await message.channel.send(f"{receiver} removed from {sender}'s tag list.")
            await message.add_reaction("✅")
            disable_tag(receiver, sender)

load_dotenv()
client.run(os.getenv("DISCORD_TOKEN"))
