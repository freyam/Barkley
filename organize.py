import json

def is_valid_keyword(user_channel) -> bool:
    with open("channels.json", "r") as f:
        channels = json.load(f)

        if channels.get("keywords").get(user_channel):
            return True
        else:
            return False


def add_keyword(operation, user_channel):
    channel = int(user_channel)

    with open("channels.json", "r") as f:
        channels = json.load(f)

        keywords = channels.get("keywords")
        keywords[operation] = channel

    with open("channels.json", "w") as f:
        json.dump(channels, f)


def get_channel_id(keyword):
    with open("channels.json", "r") as f:
        channels = json.load(f)

        return channels.get("keywords").get(keyword)
