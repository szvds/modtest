import discord
from discord.ext import commands
import asyncio
import config as db
from datetime import datetime


def get_prefix(bot, message):
    if message.guild is None:
        return commands.when_mentioned_or("/")(bot, message)
    result = db.guildscol.find_one({"guild": message.guild.id})
    if result is not None:
        return commands.when_mentioned_or(*result["prefix"])(bot, message)
    elif result is None:
        db.guildscol.insert_one({"guild": message.guild.id,
                                 "prefix": "/",
                                 "staffRoles": [None],
                                 "modRoles": [None],
                                 "warningLimit": None,
                                 "warningAction": None,
                                 "muteRole": None
                                 })
        return commands.when_mentioned_or("/")(bot, message)


extensions = ["utility", "moderation", "scanning"]
bot = commands.Bot(command_prefix=get_prefix, case_insensitive=True)
bot.remove_command("help")
db.launch_time = datetime.utcnow()


@bot.event
async def on_ready():
    print("I am running as: " + bot.user.name)
    print("My id is: " + str(bot.user.id))
    print("----------------")


@bot.event
async def on_command_error(ctx, error):
    if (isinstance(error, commands.CommandNotFound) or isinstance(error, commands.BadArgument) or
            isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.MissingPermissions) or
            isinstance(error, commands.BotMissingPermissions) or isinstance(error, commands.CheckFailure) or
            isinstance(error, commands.CheckFailure)):
        return
    elif isinstance(error, commands.NoPrivateMessage):
        await ctx.send(f"<:no:484017898730291211>/{ctx.command} cannot be used in Private Messages.")
    else:
        embed = discord.Embed(title=f"Error in command {ctx.command.qualified_name.lower()}", description=f"{type(error).__name__}: `{error}`\n")
        await bot.get_channel(479996891115945996).send(embed=embed)


async def status():  # cycle between status messages.
    await bot.wait_until_ready()
    while not bot.is_closed():
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"over {len(bot.users)} users"))
        await asyncio.sleep(15)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"over {len(bot.guilds)} servers"))
        await asyncio.sleep(15)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"over {len(bot.channels)} channels"))
        await asyncio.sleep(15)
bot.loop.create_task(status())


async def mutes():
    await bot.wait_until_ready()
    while not bot.is_closed():
        result = db.memberscol.find({})
        for member in result:
            if member["warnTime"] > datetime.datetime.now():
                asyncio.sleep((datetime.datetime.now() - member["warnTime"]).total_seconds())
                print("Test")
bot.loop.create_task(mutes())


@bot.command()
async def prefix(ctx, *, prefix: str=None):
    if prefix is None:
        prefix = db.guildscol.find_one({"guild": ctx.guild.id})["prefix"]
        await ctx.send(f"The current server prefix is `{prefix}`")
        return
    elif len(prefix) > 7:
        await ctx.send("<:no:484017898730291211>The maximum prefix length is 7 characters.")
    elif ctx.message.author.guild_permissions.administrator or ctx.message.author.guild_permissions.owner:
        result = db.guildscol.find_one({"guild": ctx.guild.id})
        result["prefix"] = prefix
        db.guildscol.replace_one({"guild": ctx.guild.id}, result)
        await ctx.send("<:yes:484017899065835521>Successfully changed the bot prefix to `{}`".format(prefix))
    else:
        await ctx.send("<:no:484017898730291211>You must be an Administator or the Owner of the server to change the bot prefix.")


@bot.command(pass_context=True)
async def load(ctx, *, extension_name: str=None):
    if extension_name is None:
        await ctx.send("<:no:484017898730291211> You must specify the extension to reload.")
        return
    if ctx.message.author.id == 158594933274574849:
        try:
            bot.load_extension(extension_name)
            extensions.append(extension_name)
            await ctx.send(f"<:yes:484017899065835521>Successfully loaded extension `{extension_name}`")
        except Exception as e:
            if type(e).__name__ != "Forbidden":
                print('{}: {}'.format(type(e).__name__, e))
                await ctx.send(f"<:no:460791849393848320>There was an error while loading the extension: \n```\n"
                               f"{type(e).__name__}: {e}\n```")


@bot.command(pass_context=True)
async def unload(ctx, *, extension_name: str=None):
    if extension_name is None:
        await ctx.send("<:no:484017898730291211> You must specify the extension to reload.")
    if ctx.message.author.id == 158594933274574849:
        bot.unload_extension(extension_name)
        extensions.remove(extension_name)
        await ctx.send(f"<:yes:484017899065835521>Successfully unloaded the extension `{extension_name}`")


@bot.command(pass_context=True)
async def reload(ctx, *, extension: str=None):
    if ctx.message.author.id == 158594933274574849:
        if extension is None:
            await ctx.send("<:no:484017898730291211> You must specify the extension to reload.")
            return
        try:
            bot.unload_extension(extension)
            extensions.remove(extension_name)
            bot.load_extension(extension)
            extensions.append(extension_name)
            await ctx.send(f"<:yes:484017899065835521>Successfully reloaded extension `{extension}`")
        except Exception as e:
            if type(e).__name__ != "Forbidden":
                print('{}: {}'.format(type(e).__name__, e))
                await ctx.send(f"<:no:484017898730291211> There was an error while reloading the extension: \n```\n"
                               f"{type(e).__name__}: {e}\n```")


@bot.command(pass_context=True)
async def restart(ctx):
    if ctx.message.author.id == 158594933274574849:
        for ext in extensions:
            bot.unload_extension(ext)
            bot.load_extension(ext)
        await ctx.send("<:yes:484017899065835521>Successfully restarted the bot.")


if __name__ == "__main__":
    for ext in extensions:
        try:
            bot.load_extension(ext)
            print(f"Loaded extension {ext}")
        except Exception as e:
            print(f"There was an error while loading the extension: \n{type(e).__name__}: {e}\n")

bot.run('REMOVED', bot=True, reconnect=True)
