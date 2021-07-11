from aiohttp import web
from discord.ext import commands, tasks
import discord
import os
import aiohttp
import database.admindb
import utilities.course

app = web.Application()
routes = web.RouteTableDef()


class APIServer(commands.Cog):

    def __init__(self, client):

        self.client = client
        self.web_server.start()

        @routes.post('/join')
        async def join_course_api(request):
            if request.headers.get('Authorization') == os.getenv('API_TOKEN'):
                body = await request.json()
                guild_id = body['guildId']
                course_name = body['courseName'].upper()
                user_id = body['userId']
                print(int(guild_id))
                guild = self.client.get_guild(int(guild_id))
                if guild is None:
                    return web.json_response({
                        "success": False,
                        "code": 0,
                        "extra": ""
                    })

                if database.admindb.course_exists(course_name, guild_id):

                    user = guild.get_member(int(user_id))
                    if user is None:

                        return web.json_response({
                            "success": False,
                            "code": 1,
                            "extra": await utilities.course.generate_course_invite(
                                course_name, guild, self.client)
                        })

                    await utilities.course.join_course(
                        course_name, guild, user, self.client)

                    return web.json_response({
                        "success": True,
                        "code": 0,
                        "extra": ""
                    })
                else:
                    return web.json_response({
                        "success": False,
                        "code": 1,
                        "extra": ""
                    })

        self.webserver_port = os.environ.get('PORT', 5000)
        app.add_routes(routes)

    @commands.command()
    async def helloworld(self, ctx: commands.Context):
        await ctx.message.channel.send("test123")

    @tasks.loop()
    async def web_server(self):
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, host='0.0.0.0', port=self.webserver_port)
        await self.client.wait_until_ready()
        await site.start()

    @web_server.before_loop
    async def web_server_before_loop(self):
        await self.client.wait_until_ready()


def setup(client):
    client.add_cog(APIServer(client))
