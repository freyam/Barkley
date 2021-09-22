async def impersonate(message, person):
    print("name =" + person.name)
    webhook = await message.channel.create_webhook(name=person.name)
    await webhook.send(
        str(message.content), username=person.name, avatar_url=person.avatar_url)

    webhooks = await message.channel.webhooks()
    for webhook in webhooks:
        await webhook.delete()
    await message.delete()

