
import discord
from discord.ext import commands
import os
import database.admindb
import utilities.course


async def join_course(course: str, guild: discord.Guild, user: discord.User, client: discord.Client):
    category_name = database.admindb.get_course(
        course, guild.id)["category"]
    # Get or create original category
    category = discord.utils.get(
        guild.categories, name=category_name)

    if category is None:
        category = await guild.create_category(name=category_name)

    # Get or create second category if there are already over 50 channels in the original
    category = discord.utils.get(
        guild.categories, name=category_name)

    if category is None:
        category = await guild.create_category(name=category_name)

    channel = discord.utils.get(
        guild.channels, name=course.lower())

    if channel is None:
        channel = await guild.create_text_channel(course, category=category)
        await channel.set_permissions(guild.default_role, read_messages=False)
        await channel.set_permissions(client.user, read_messages=True)

    if channel.overwrites_for(user).read_messages == None:
        await channel.set_permissions(user, read_messages=True)

    await channel.send(user.mention + ' joined the chat.')


async def generate_course_invite(course: str, guild: discord.Guild, client: discord.Client):
    category_name = database.admindb.get_course(
        course, guild.id)["category"]
    # Get or create original category
    category = discord.utils.get(
        guild.categories, name=category_name)

    if category is None:
        category = await guild.create_category(name=category_name)

    # Get or create second category if there are already over 50 channels in the original
    category = discord.utils.get(
        guild.categories, name=category_name)

    if category is None:
        category = await guild.create_category(name=category_name)

    channel = discord.utils.get(
        guild.channels, name=course.lower())

    if channel is None:
        channel = await guild.create_text_channel(course, category=category)
        await channel.set_permissions(guild.default_role, read_messages=False)
        await channel.set_permissions(client.user, read_messages=True)

    link = await channel.create_invite(max_age=300)
    return link.url
