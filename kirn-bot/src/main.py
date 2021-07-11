import discord
from discord.utils import get
from discord.ext.commands import has_permissions, MissingPermissions

import json
import os
from discord.ext import commands

import database.models
import database.admindb
import math as m
from discord.ext.commands.errors import BotMissingPermissions


async def get_prefix(bot, message):
    return commands.when_mentioned_or(database.admindb.get_prefix(message.guild.id))(bot, message)

intents = discord.Intents().all()
bot = commands.Bot(command_prefix=get_prefix, intents=intents)


@bot.event
async def on_command_error(ctx: commands.Context, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Command is missing arguments 😪')
        return

    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        return

    if isinstance(error, commands.CheckFailure):
        await ctx.send("You do not have permission to use this command.")
        return

    if isinstance(error, commands.BotMissingPermissions):
        missing = [perm.replace('_', ' ').replace(
            'guild', 'server').title() for perm in error.missing_perms]
        if len(missing) > 2:
            fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
        else:
            fmt = ' and '.join(missing)
        _message = 'I need the **{}** permission(s) to run this command.'.format(
            fmt)
        await ctx.send(_message)
        return

    if isinstance(error, commands.DisabledCommand):
        await ctx.send('This command has been disabled.')
        return

    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send("This command is on cooldown, please retry in {}s.".format(m.ceil(error.retry_after)))
        return

    if isinstance(error, commands.MissingPermissions):
        missing = [perm.replace('_', ' ').replace(
            'guild', 'server').title() for perm in error.missing_perms]
        if len(missing) > 2:
            fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
        else:
            fmt = ' and '.join(missing)
        _message = 'You need the **{}** permission(s) to use this command.'.format(
            fmt)
        await ctx.send(_message)
        return

    if isinstance(error, BotMissingPermissions):
        await ctx.send("Bot is missing permissions")
        return

    print(error)
    await ctx.send('An unknown error has occured 👀')

# Loop to look through cogs folder and load all cogs contained within it
for filename in os.listdir(os.path.join(os.path.dirname(__file__), 'cogs')):
    if filename.endswith('.py'):
        # splicing cuts 3 last characters aka .py
        bot.load_extension(f'cogs.{filename[:-3]}')


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

bot.run(os.getenv('BOT_TOKEN'))
