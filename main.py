# Context; a bot for simple task management

import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta
import asyncio
import os
from dotenv import load_dotenv
from responses import get_reponse

# Load the token from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Set up the bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

# Dictionary to store reminders
reminders = {}


@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user}')


@bot.command(name='remind')
async def remind(ctx, date: str, time: str, *, event: str):
    # Parse date and time
    reminder_time = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
    current_time = datetime.now()

    if reminder_time < current_time:
        await ctx.send("You can't set a reminder in the past!")
        return

    # Calculate the delay
    delay = (reminder_time - current_time).totalSeconds()

    # Store the reminder
    reminders[(ctx.author.id, reminder_time)] = event

    # Schedule the reminder
    await ctx.send(f"Reminder set for {reminder_time} for event: {event}")
    await asyncio.sleep(delay)
    await ctx.send(f"Reminder: {event}, {ctx.author.mention}")


@bot.command(name='listreminders')
async def list_reminders(ctx):
    user_reminders = [
        f"{time}: {event}" for (user, time), event in reminders.items()
        if user == ctx.author.id
    ]
    if not user_reminders:
        await ctx.send("You have no reminders set.")
    else:
        await ctx.send("\n".join(user_reminders))


@bot.command(name='deletereminder')
async def delete_reminder(ctx, date: str, time: str):
    reminder_time = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
    key = (ctx.author.id, reminder_time)
    if key in reminders:
        del reminders[key]
        await ctx.send("Reminder deleted.")
    else:
        await ctx.send("No reminder found for that date and time.")


bot.run(TOKEN)
