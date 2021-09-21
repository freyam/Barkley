import json


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