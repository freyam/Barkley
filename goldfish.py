import json
import discord


async def remind(user_id, task):
    with open("tasks.json", "r") as f:
        user_tasks = json.load(f)
        if user_id in user_tasks:
            user_tasks[user_id]["n_tasks"] += 1
            user_tasks[user_id]["tasks"].append(
                [user_tasks[user_id]["n_tasks"], task, "False"]
            )
        else:
            user_tasks[user_id] = {"n_tasks": 1, "tasks": [[1, task, "False"]]}

    with open("tasks.json", "w") as f:
        json.dump(user_tasks, f)


async def complete(user_id, task_id):
    with open("tasks.json", "r") as f:
        user_tasks = json.load(f)
        if user_id in user_tasks:
            for task in user_tasks[user_id]["tasks"]:
                if task_id == task[0]:
                    print(task)
                    task[2] = "True"

    with open("tasks.json", "w") as f:
        json.dump(user_tasks, f)


async def goldfish(user_id):
    with open("tasks.json", "r") as f:
        user_tasks = json.load(f)
        if user_id in user_tasks:
            goldfish_embed = discord.Embed(title="Goldfish")
            for task in user_tasks[user_id]["tasks"]:
                if task[2] == "True":
                    name = f"~~Task {task[0]}~~"
                    value = f"~~{task[1]}~~"
                else:
                    name = f"Task {task[0]}"
                    value = task[1]

                goldfish_embed.add_field(
                    name=name,
                    value=value,
                    inline=False,
                )
    return goldfish_embed


async def clear(user_id, task_id):
    with open("tasks.json", "r") as f:
        user_tasks = json.load(f)
        if user_id in user_tasks:
            for task in user_tasks[user_id]["tasks"]:
                if task_id == task[0]:
                    user_tasks[user_id]["tasks"].remove(task)
                    user_tasks[user_id]["n_tasks"] -= 1

    with open("tasks.json", "w") as f:
        json.dump(user_tasks, f)
