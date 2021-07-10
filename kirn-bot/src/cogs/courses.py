import discord
from discord.ext import commands
import os
import database.admindb


class Courses(commands.Cog):
    courses: list = []

    def __init__(self, client):
        self.client = client

    @commands.command(brief="Join a course channel", description="Join a course channel")
    async def join(self, ctx: commands.Context, *, arg):
        course = arg.upper()
        if database.admindb.course_exists(course, ctx.guild.id):
            category_name = database.admindb.get_course(
                course, ctx.guild.id)["category"]
            print(category_name)
            # Get or create original category
            category = discord.utils.get(
                ctx.guild.categories, name=category_name)

            if category is None:
                category = await ctx.guild.create_category(name=category_name)

            # Get or create second category if there are already over 50 channels in the original
            category = discord.utils.get(
                ctx.guild.categories, name=category_name)
            if category is None:
                category = await ctx.guild.create_category(name=category_name)

            channel = discord.utils.get(
                ctx.guild.channels, name=course.lower())

            if channel is None:
                channel = await ctx.guild.create_text_channel(course, category=category)
                await channel.set_permissions(ctx.guild.default_role, read_messages=False)
                await channel.set_permissions(self.client.user, read_messages=True)

            if channel.overwrites_for(ctx.message.author).read_messages == None:
                await channel.set_permissions(ctx.message.author, read_messages=True)

            await ctx.message.channel.send('✅ Got it! Gave ' + ctx.message.author.mention + ' access to #' + course.lower() + '.')

            await channel.send(ctx.message.author.mention + ' joined the chat.')

        else:
            await ctx.message.channel.send('Course does not exist 🤦‍♀️')

    @commands.command(brief="Leave a course channel")
    async def leave(self, ctx: commands.Context, *, arg):
        course = arg.upper()
        if database.admindb.course_exists(course, ctx.guild.id):
            channel = discord.utils.get(
                ctx.guild.channels, name=course.lower())
            if channel.overwrites_for(ctx.message.author).read_messages != None:
                await channel.set_permissions(
                    ctx.message.author, read_messages=None)
                await ctx.message.channel.send("✅ Got it! Removed " + ctx.message.author.mention + "'s access to #" + course.lower() + ".")
            else:
                await ctx.message.channel.send(ctx.message.author.mention + ", you are not in #" + course.lower() + " " + "😩")

        else:
            await ctx.message.channel.send('Course does not exist 🤦‍♀️')

    @commands.command(brief="List all available course channels")
    async def ls(self, ctx):
        courses = database.admindb.course_list(ctx.guild.id)
        prefixes: typing.List[str] = []
        message: typing.List[str] = []
        # Parse the different prefixes
        [prefixes.append(course["course_name"].split('-')[0])
            for course in courses if course["course_name"].split('-')[0] not in prefixes]
        # Go through each prefix and find
        for prefix in prefixes:
            prefix_courses: typing.List[str] = []
            [prefix_courses.append(course["course_name"].split('-')[1])
                for course in courses if course["course_name"].split('-')[0] == prefix]
            prefix_msg: str = ""
            prefix_msg = prefix_msg + "**" + prefix + "**: `"
            prefix_courses.sort()
            for course in prefix_courses:
                prefix_msg = prefix_msg + course + ", "
            prefix_msg = prefix_msg[:len(prefix_msg) - 2] + "`\n"
            message.append(prefix_msg)
        optimized_message: typing.List[str] = []
        i: int = 0
        optimized_message.append("__Course List__\n")
        for x in message:
            if len(optimized_message[i]) + len(x) >= 2000:
                i = i + 1
                optimized_message.append(x)
            else:
                optimized_message[i] = optimized_message[i] + x
        for x in optimized_message:
            await ctx.message.channel.send(x)


def setup(client):
    client.add_cog(Courses(client))
