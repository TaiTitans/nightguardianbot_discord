import discord
from discord.ext import commands
import datetime
import asyncio
import sqlite3

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)

todos = []
user_stats = {}  # Dictionary để lưu trữ thông tin người dùng

# Database connection
def create_connection():
    return sqlite3.connect('user_stats.db')

# Database connection
connection = sqlite3.connect('user_stats.db')
cursor = connection.cursor()

# Create the user_stats table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_stats (
        user_id INTEGER PRIMARY KEY,
        chat_experience INTEGER DEFAULT 0,
        voice_time INTEGER DEFAULT 0
    )
''')

# Save changes and close the connection
connection.commit()
connection.close()
# Ranks and the required XP to reach each rank
ranks = [
    {"name": "Bronze", "required_xp": 10},
    {"name": "Silver", "required_xp": 70},
    {"name": "Gold", "required_xp": 150},
    {"name": "Platinum", "required_xp": 400},
    {"name": "Diamond", "required_xp": 3000},
    {"name": "Master", "required_xp": 9999},
]





@bot.event
async def on_ready():
    print(f'Bot has connected successfully with name: {bot.user.name}')
    await setup_sleep_reminders()
    bot.loop.create_task(setup_voice_time_reset())
    await initialize_user_stats()

async def initialize_user_stats():
    # Get all user IDs from the Discord server
    guild = bot.get_guild(1115810115820466177)  # Replace YOUR_GUILD_ID with your actual guild ID
    if guild is not None:
        for member in guild.members:
            user_id = member.id
            user_stats.setdefault(user_id, {'chat_experience': 0, 'voice_time': datetime.timedelta()})

async def setup_sleep_reminders():
    while True:
        now = datetime.datetime.now()

        # Chào buổi sáng lúc 7 giờ sáng
        if now.hour == 7 and now.minute == 0:
            await greet_morning()

        # Nhắc ngủ sớm lúc 0 giờ
        if now.hour == 0 and now.minute == 0:
            await remind_to_sleep()

        # Reset kinh nghiệm chat sau 24 giờ
        reset_user_experience()

        await asyncio.sleep(60)  # Kiểm tra mỗi phút

async def greet_morning():
    guild = bot.get_guild(1115810115820466177)  # Thay YOUR_GUILD_ID bằng ID của server Discord
    if guild is not None:
        channel = bot.get_channel(1123811119912460330)  # Thay YOUR_CHANNEL_ID bằng ID của kênh Discord
        if channel is not None:
            await channel.send(f"{channel.mention} It's time to go to bed early. Have a good night's sleep! @everyone")

async def remind_to_sleep():
    guild = bot.get_guild(1115810115820466177)  # Thay YOUR_GUILD_ID bằng ID của server Discord
    if guild is not None:
        channel = bot.get_channel(1123811119912460330)  # Thay YOUR_CHANNEL_ID bằng ID của kênh Discord
        if channel is not None:
            await channel.send(f"{channel.mention} Good Morning <3 . Have A Good Day ! @everyone")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    introductions = {
        'hello': f'Have a good day {message.author.mention}',
        'taititans': f'Good boy . He is a programmer from Vietnam and very handsome. ~.~ {message.author.mention}',
        'goodnight': f'Goodnight <3 {message.author.mention}',
        'who are lili': f'She is the captain of the ship, and a kind and hardworking girl. <3 {message.author.mention}',
        'who are nabi': f'She is a cute girl and a good girl. <3 {message.author.mention}',
        'who are vas': f'They have personality and good at math {message.author.mention}',
        'who are bella': f'She is a smart girl who knows many languages. {message.author.mention}',
        'who are princessjo': f'A hardworking girl. Cheerful and friendly. I think she will become an excellent lawyer. {message.author.mention}',
        'who are genos': f'A strong boy and a friendly guy. {message.author.mention}',
        'who are david': f'An American guy who is serious and ready to help people. {message.author.mention}',
        'who are akari': f'A Japanese girl who is happy and loves to learn. {message.author.mention}',
        'who are naya': f'A mysterious girl. {message.author.mention}',
        'who are thai': f'Luffy Boyyyyyyyyy. {message.author.mention}',
        'who are timina': f'Was a friend of Nabi and she was very interesting and cool :3 {message.author.mention}'
    }

    content = message.content.lower()
    if content in introductions:
        await message.channel.send(introductions[content])

    await bot.process_commands(message)

    # Cập nhật kinh nghiệm chat của người dùng
    connection = create_connection()
    update_user_chat_experience(message.author.id, connection)
    connection.close()
@bot.event
async def on_voice_state_update(member, before, after):
    if member == bot.user:
        return

    # Cập nhật thời gian tham gia kênh thoại của người dùng
    connection = create_connection()
    update_user_voice_time(member.id, before.channel, after.channel, connection)
    connection.close()
@bot.group()
async def crew(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send('Invalid crew command. Use "!crew help" for more information.')

@crew.command()
async def help(ctx):
    message = "```"
    message += "=== Welcome to NightGuardian Bot Version 1.5=== \n"
    message += "List Command: \n"
    message += "- !crew todo : use to see what to do today. \n"
    message += "- !crew addtodo [works] : add to do to day ! \n"
    message += "- !crew check [numbers] : check done works \n"
    message += "- !crew reset : reset to do list ! \n"
    message += "- !crew date : Date and countdown ! \n"
    message += "- !crew pomodoro [cycles] [duration] : start [cycles] Pomodoro cycles, each lasting [duration] minutes. \n"
    message += "- !crew rank : Show your current rank and XP. \n"
    message += "- !crew rankinfo : Show the list of ranks and XP required to achieve each rank. \n"
    message += "- !crew toprank : Show the top-ranking users based on XP. \n"
    message += "- !crew worktoday : Display your focused work time today. "
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
        if 0 < numbers <= len(todos):
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

# Cập nhật kinh nghiệm chat của người dùng
def reset_user_experience():
    # Remove users whose last chat time is older than 24 hours
    now = datetime.datetime.now()
    user_ids_to_remove = [user_id for user_id, stats in user_stats.items() if now - stats.get('last_chat_time', now) >= datetime.timedelta(hours=24)]
    for user_id in user_ids_to_remove:
        user_stats.pop(user_id, None)

def update_user_chat_experience(user_id, connection):
    now = datetime.datetime.now()
    if user_id not in user_stats:
        user_stats[user_id] = {'chat_experience': 0, 'last_chat_time': now}
    else:
        # Check if last chat time is from a different day
        if now.date() > user_stats[user_id]['last_chat_time'].date():
            user_stats[user_id]['chat_experience'] = 0  # Reset chat experience for the new day
        user_stats[user_id]['chat_experience'] += 1
    user_stats[user_id]['last_chat_time'] = now

    connection = sqlite3.connect('user_stats.db')
    with connection:
        cursor = connection.cursor()

        # Update the user's chat_experience in the database
        cursor.execute('''
            INSERT OR REPLACE INTO user_stats (user_id, chat_experience)
            VALUES (?, COALESCE((SELECT chat_experience FROM user_stats WHERE user_id = ?) + 1, 1))
        ''', (user_id, user_id))

    # Save changes and close the connection
    connection.commit()
    connection.close()

def reset_user_chat_experience_daily():
    # Reset chat experience for all users daily
    now = datetime.datetime.now()
    for user_id, stats in user_stats.items():
        if now.date() > stats.get('last_chat_time', now).date():
            stats['chat_experience'] = 0
        stats['last_chat_time'] = now

def get_user_chat_experience(user_id):
    return user_stats.get(user_id, {}).get('chat_experience', 0)

def update_user_voice_time(user_id, before_channel, after_channel, connection):
    now = datetime.datetime.now()
    if user_id not in user_stats:
        user_stats[user_id] = {'voice_time': datetime.timedelta(), 'in_voice_channel': False, 'last_voice_join_time': None}

    if before_channel is not None and after_channel is None:
        # User left the voice channel
        start_time = user_stats[user_id].get('last_voice_join_time')
        if start_time is not None and user_stats[user_id]['in_voice_channel']:
            # If the user was previously in a voice channel, update the voice time
            voice_time = now - start_time
            user_stats[user_id]['voice_time'] += voice_time
            user_stats[user_id]['in_voice_channel'] = False
    elif before_channel is None and after_channel is not None:
        # User joined the voice channel
        user_stats[user_id]['in_voice_channel'] = True
        user_stats[user_id]['last_voice_join_time'] = now

    # Update the user's voice_time in the database
    with connection:
        cursor = connection.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO user_stats (user_id, voice_time)
            VALUES (?, COALESCE((SELECT voice_time FROM user_stats WHERE user_id = ?) + ?, ?))
        ''', (user_id, user_id, user_stats[user_id]['voice_time'].total_seconds() // 60, user_stats[user_id]['voice_time'].total_seconds() // 60))

    # Save changes and close the connection
    connection.commit()
    connection.close()

async def setup_voice_time_reset():
    while True:
        reset_user_voice_time_daily()
        await asyncio.sleep(86400)  # Run every 24 hours to reset voice time

def reset_user_voice_time_daily():
    now = datetime.datetime.now()
    for user_id, stats in user_stats.items():
        if 'last_voice_join_time' in stats:
            last_voice_join_time = stats['last_voice_join_time']
            if last_voice_join_time.date() < now.date():
                stats['voice_time'] = datetime.timedelta()
                stats['in_voice_channel'] = False
def get_user_voice_time(user_id):
    now = datetime.datetime.now()
    if user_id in user_stats:
        last_voice_join_time = user_stats[user_id].get('last_voice_join_time')
        if last_voice_join_time is not None:
            # If the user is still in the voice channel, consider the time until now
            voice_time = user_stats[user_id]['voice_time']
            if user_stats[user_id]['in_voice_channel']:
                voice_time += now - last_voice_join_time
            return voice_time.total_seconds() // 60  # Convert to minutes
    return 0

def get_user_rank(user_id):
    xp = get_user_chat_experience(user_id)
    current_rank = None
    next_rank = None
    for rank in ranks:
        if xp >= rank['required_xp']:
            current_rank = rank
        else:
            next_rank = rank
            break
    return current_rank, next_rank


@crew.command()
async def rank(ctx):
    user_id = ctx.author.id
    current_rank, next_rank = get_user_rank(user_id)
    if current_rank:
        xp = get_user_chat_experience(user_id)
        xp_needed = next_rank['required_xp'] - xp if next_rank else 0
        await ctx.send(
            f'{ctx.author.mention}, your current rank is ***{current_rank["name"]}*** with {xp} XP. You need ***{xp_needed}*** XP to reach the next rank.')

        if next_rank and xp >= next_rank['required_xp']:
            await ctx.send(f'Congratulations {ctx.author.mention}! You have reached the rank of  ***{next_rank["name"]}***')
    else:
        await ctx.send(f'{ctx.author.mention}, you are currently unranked.You have reached the rank of  ***{next_rank["name"]}***')

@crew.command()
async def rankinfo(ctx):
    message = "```"
    message += "=== Ranks and Required XP ===\n"
    for rank in ranks:
        message += f"{rank['name']}: {rank['required_xp']} XP\n"
    message += "```"
    await ctx.send(message)

@crew.command()
async def toprank(ctx):
    top_users = sorted(user_stats.items(), key=lambda x: x[1]['chat_experience'], reverse=True)[:10]
    if not top_users:
        await ctx.send("The Top Ranking Users table is empty.")
        return

    message = "```"
    message += "=== Top Ranking Users ===\n"
    for index, (user_id, stats) in enumerate(top_users):
        member = ctx.guild.get_member(user_id)
        if member is not None:
            current_rank, _ = get_user_rank(user_id)
            message += f"{index + 1}. {member.display_name} (Rank: {current_rank['name']}, XP: {stats['chat_experience']})\n"
        else:
            # The member is not found in the guild, handle this case accordingly
            message += f"{index + 1}. User with ID {user_id} is not found in the guild.\n"
    message += "```"
    await ctx.send(message)

@crew.command()
async def worktoday(ctx):
    user_id = ctx.author.id
    voice_time = get_user_voice_time(user_id)
    await ctx.send(f'Your voice time today: {voice_time} minutes.{ctx.author.mention}')

# Run bot
bot.run('MTEyODM3NTU2MDY1ODIyNzMwMQ.G_0J9q.AbtTdtBSjGz6xnUXU0_-Z8n37-I8b0oOEkY8z4')