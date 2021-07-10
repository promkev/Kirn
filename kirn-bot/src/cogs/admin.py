import discord
from discord.ext import commands
import os
import database.models
import database.admindb
import typing


class Admin(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.db = database.models.db

    async def cog_check(self, ctx: commands.Context):
        # Check if the user has the administrator permission
        return ctx.author.guild_permissions.administrator

    @commands.command(brief="Add one or more courses")
    async def addcourse(self, ctx: commands.Context, *args):
        arg_list: list = list(args)
        response: str = ""
        try:
            db_return: str = database.admindb.add_course(
                arg_list, ctx.guild.id)
            response = response + db_return + "\n"
        except BaseException as e:
            print(e)
        await ctx.message.channel.send(response)

    @commands.command(brief="Remove one or more courses")
    async def removecourse(self, ctx: commands.Context, *args: list):
        arg_list: list = list(args)
        response: str = ""
        try:
            db_return: str = database.admindb.remove_course(
                arg_list, ctx.guild.id)
            response = response + db_return + "\n"
        except BaseException as e:
            print(e)
        await ctx.message.channel.send(response)

    def get_templates(self) -> typing.List[str]:
        templates: typing.List[str] = []
        for filename in os.listdir(os.path.join(os.path.dirname(__file__), '..', 'templates')):
            if filename.endswith('.txt'):
                templates.append(filename[:-4])
        return templates

    @commands.command(brief="List all available templates")
    async def templatelist(self, ctx):
        response: str = "**Template List**\n"
        for template in self.get_templates():
            response = response + template + "\n"
        await ctx.message.channel.send(response)

    @commands.command(brief="Add all courses in a template")
    async def addtemplate(self, ctx: commands.Context, arg):
        response: str = ""
        if arg in self.get_templates():
            courses: typing.List[str] = []
            try:
                with open(os.path.join(os.path.dirname(__file__), '..', 'templates', arg + '.txt')) as fp:
                    line = fp.readline()
                    while line:
                        courses.append(line.strip())
                        line = fp.readline()
                    database.admindb.add_course(courses, ctx.guild.id)
            except BaseException as e:
                print(e)
            response = response + "✅ Added template " + arg
        else:
            response = response + "❌ Template does not exist"
        await ctx.message.channel.send(response)

    @commands.command(brief="Remove all courses associated with a template")
    async def removetemplate(self, ctx: commands.Context, arg):
        response: str = ""
        if arg in self.get_templates():
            courses: typing.List[str] = []
            try:
                with open(os.path.join(os.path.dirname(__file__), '..', 'templates', arg + '.txt')) as fp:
                    line = fp.readline()
                    while line:
                        courses.append(line.strip())
                        line = fp.readline()
                    database.admindb.remove_course(courses, ctx.guild.id)
            except BaseException as e:
                print(e)
            response = response + "✅ Removed template " + arg
        else:
            response = response + "❌ Template does not exist"
        await ctx.message.channel.send(response)

    @commands.command(brief="Change the server's prefix")
    async def setprefix(self, ctx: commands.Context, arg):
        database.admindb.set_prefix(ctx.guild.id, arg)
        await ctx.message.channel.send("Changed prefix to " + arg)

    @commands.command(brief="Change a course's category", description="\nIf your category has multiple words, use quotation marks as such: \"category name\"\n\nExample: \n$setcategory \"General Electives\" PHYS-204\n$setcategory PHYS PHYS-204")
    async def setcategory(self, ctx: commands.Context, *args):
        arg_list: list = list(args)
        new_category: str = ""
        # Determine new category
        if arg_list[0][0] == "\"":
            i: int = 0
            found: bool = False
            temp: str = ""
            # Find last word
            for arg in arg_list:
                i = i + 1
                temp = temp + arg
                if arg[-1] == "\"":
                    found = True
                    break
            if found == True:
                new_category = temp[1:-1]
            else:
                new_category = arg_list[0]
        else:
            new_category = arg_list[0]
        response: str = "Changed the following courses' category to " + new_category + ":\n"
        try:
            db_return: str = database.admindb.course_category(new_category,
                                                              arg_list[1:], ctx.guild.id)
            response = response + db_return + "\n"
            for arg in arg_list[1:]:
                if database.admindb.course_exists(arg, ctx.guild.id):
                    category = discord.utils.get(
                        ctx.guild.categories, name=new_category)
                    channel = discord.utils.get(
                        ctx.guild.channels, name=arg.lower())
                    if channel == None:
                        break
                    if category is None:
                        category = await ctx.guild.create_category(name=new_category)
                    await channel.edit(category=category)

        except BaseException as e:
            print(e)
        await ctx.message.channel.send(response)

    @commands.command()
    async def adminls(self, ctx):
        courses = database.admindb.course_list(ctx.guild.id)
        courses = sorted(courses, key=lambda i: i['course_name'])
        prefixes: typing.List[str] = []
        message: typing.List[str] = []
        for course in courses:
            new_msg = course["course_name"] + " | " + course["category"] + "\n"
            message.append(new_msg)
        optimized_message: typing.List[str] = []
        i: int = 0
        optimized_message.append("__Course List__ (course_name | category)\n")
        for x in message:
            if len(optimized_message[i]) + len(x) >= 2000:
                i = i + 1
                optimized_message.append(x)
            else:
                optimized_message[i] = optimized_message[i] + x
        for x in optimized_message:
            await ctx.message.channel.send(x)


def setup(client):
    client.add_cog(Admin(client))
