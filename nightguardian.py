import discord
import datetime
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)


@bot.event
async def on_ready():
    print(f'Bot has connected successfully with name: {bot.user.name}')


@bot.group()
async def crew(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send('Invalid crew command. Use "/crew help" for more information.')


@crew.command()
async def help(ctx):
    message = "```"
    message += "=== Welcome to NightGuardian Bot === \n"
    message += "List Command: \n"
    message += "- /crew todo : use to see what to do today. \n"
    message += "- /crew addtodo [works] : add to do to day ! \n"
    message += "- /crew check [numbers] : check done works \n"
    message += "- /crew reset : reset to do list ! \n"
    message += "- /crew date : Date and countdown !"
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


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.lower() == 'hello':
        await message.channel.send(f'Have a good day {message.author.mention}')

    await bot.process_commands(message)


@bot.command()
@commands.is_owner()
async def reload(ctx, extension):
    await bot.reload_extension(f"cogs.{extension}")
    embed = discord.Embed(title='Reload', description=f'{extension} successfully reloaded', color=0xff00c8)
    await ctx.send(embed=embed)

# Run bot
bot.run('MTEyODM3NTU2MDY1ODIyNzMwMQ.GE_c7L.aLXY_kdVhagiRlkk0IANZBVwGC6-visz9BngjM')
