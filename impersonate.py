async def impersonate(
    message_author, message_channel, message_content, message_attachment=None
):
    webhook = await message_channel.create_webhook(name=message_author.name)

    await webhook.send(
        message_content,
        username=message_author.name,
        avatar_url=message_author.avatar_url,
        files=message_attachment,
    )

    await webhook.delete()
