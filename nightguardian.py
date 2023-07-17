import discord
from discord.ext import commands
import datetime
import asyncio
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

todos = []

@bot.event
async def on_ready():
    print(f'Bot has connected successfully with name: {bot.user.name}')
    await setup_sleep_reminders()

async def setup_sleep_reminders():
    while True:
        now = datetime.datetime.now()

        # Chào buổi sáng lúc 7 giờ sáng
        if now.hour == 7 and now.minute == 0:
            await greet_morning()

        # Nhắc ngủ sớm lúc 0 giờ
        if now.hour == 0 and now.minute == 0:
            await remind_to_sleep()

        await asyncio.sleep(60)  # Kiểm tra mỗi phút

async def greet_morning():
    guild = bot.get_guild(1115810115820466177)  # Thay YOUR_GUILD_ID bằng ID của server Discord
    if guild is not None:
        channel = bot.get_channel(1123811119912460330)  # Thay YOUR_CHANNEL_ID bằng ID của kênh Discord
        if channel is not None:
            await channel.send(f"{channel.mention} It's time to go to bed early. Have a good night's sleep!")

async def remind_to_sleep():
    guild = bot.get_guild(1115810115820466177)  # Thay YOUR_GUILD_ID bằng ID của server Discord
    if guild is not None:
        channel = bot.get_channel(1123811119912460330)  # Thay YOUR_CHANNEL_ID bằng ID của kênh Discord
        if channel is not None:
            await channel.send(f"{channel.mention} Good Morning <3 . Have A Good Day !")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.lower() == 'hello':
        await message.channel.send(f'Have a good day {message.author.mention}')
    if message.content.lower() == 'taititans':
        await message.channel.send(f'He is a goodboy <3')

    await bot.process_commands(message)

@bot.group()
async def crew(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send('Invalid crew command. Use "!crew help" for more information.')

@crew.command()
async def help(ctx):
    message = "```"
    message += "=== Welcome to NightGuardian Bot Version 1.0=== \n"
    message += "List Command: \n"
    message += "- !crew todo : use to see what to do today. \n"
    message += "- !crew addtodo [works] : add to do to day ! \n"
    message += "- !crew check [numbers] : check done works \n"
    message += "- !crew reset : reset to do list ! \n"
    message += "- !crew date : Date and countdown ! \n"
    message += "- !crew pomodoro [cycles] [duration] : start [cycles] Pomodoro cycles, each lasting [duration] minutes."
    message += "```"
    await ctx.send(message)

@crew.command()
async def date(ctx):
    now = datetime.datetime.now()
    new_year = datetime.datetime(now.year + 1, 1, 1)
    countdown = new_year - now
    message = "```"
    message += f"Today is {now.strftime('%d/%m/%Y')}\n"
    message += f"Countdown to New Year: {countdown.days} days"
    message += "```"
    await ctx.send(message)

@crew.command()
async def addtodo(ctx, *, works):
    todos.append(works)
    await ctx.send(f'Task "{works}" has been added to the To-Do list.')

@crew.command()
async def todo(ctx):
    if len(todos) > 0:
        todo_list = '\n'.join(todos)
        message = "```"
        message += "=-= To-Do List =-= \n"
        message += f"{todo_list}\n"
        message += "```"
        await ctx.send(message)
    else:
        await ctx.send('**The To-Do list is empty.**')

@crew.command()
async def check(ctx, numbers):
    try:
        numbers = int(numbers)
        if numbers > 0 and numbers <= len(todos):
            done_tasks = todos[:numbers]
            todos[:] = todos[numbers:]
            done_list = '\n'.join(done_tasks)
            await ctx.send(f'**Completed Tasks:**\n{done_list}')
        else:
            await ctx.send('Invalid number. Please specify a valid number of tasks.')
    except ValueError:
        await ctx.send('Invalid number. Please specify a valid number of tasks.')

@crew.command()
async def reset(ctx):
    todos.clear()
    await ctx.send('The To-Do list has been reset.')

@crew.command()
async def pomodoro(ctx, cycles: int, duration: int):
    for _ in range(cycles):
        work_duration = duration * 60
        break_duration = 5 * 60  # 5 minutes break

        await ctx.send(f'Pomodoro session started for {duration} minutes.')
        await ctx.send(f'Work phase started. {ctx.author.mention}')
        await asyncio.sleep(work_duration)
        await ctx.send(f'{ctx.author.mention}, take a break!')
        await asyncio.sleep(break_duration)
        await ctx.send(f'{ctx.author.mention}, break is over. Back to work!')
# Run bot

port = int(os.environ.get("PORT", 5000))
bot.run('MTEyODM3NTU2MDY1ODIyNzMwMQ.GrVjQE._K1rOsoxcVI1EwU_-QShjcOVRkZVxe9zP0e_ZQ', port=port)
