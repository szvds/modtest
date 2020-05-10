import discord
from discord.ext import commands
import psutil
import datetime
import config as config


class Utility():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["information", "botinfo", "bot-info"])
    async def info(self, ctx):
        embed = discord.Embed(title="", description=f"", timestamp=datetime.datetime.utcnow(), colour=0x00988E)
        embed.add_field(name="Servers", value=f"{len(self.bot.guilds)}", inline=True)
        embed.add_field(name="Users", value=f"{len(self.bot.users)}", inline=True)
        embed.add_field(name="Owner", value=f"{self.bot.get_user(158594933274574849)}", inline=True)
        embed.add_field(name="CPU usage", value=f"{round(psutil.cpu_percent())}%", inline=True)
        embed.add_field(name="Memory usage", value=f"{psutil.virtual_memory()[2]}%", inline=True)
        embed.add_field(name="Disk usage", value=f"{psutil.disk_usage('/')[3]}%", inline=True)
        embed.add_field(name="Support", value="[Click here!](https://discord.gg/H8aQtny)", inline=True)
        embed.add_field(name="Invite", value="[Click here!](https://discordapp.com/api/oauth2/authorize?client_id=460501449172844545&permission"
                                             "s=1580592199&scope=bot)", inline=True)
        embed.add_field(name="Website", value=f"[Coming soon!](https://google.com/)", inline=True)
        embed.set_author(name="Bot information", icon_url="https://goo.gl/UPQ42W")

        delta_uptime = datetime.datetime.utcnow() - config.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        if (days == 0):
            days = ""
        elif (days == 1):
            days = str(days) + " day,"
        else:
            days = str(days) + " days,"

        if (hours == 0):
            hours = ""
        elif (hours == 1):
            hours = str(hours) + " hour and"
        else:
            hours = str(hours) + " hours and"
        if (minutes == 0):
            seconds = str(seconds) + " seconds"
            minutes = ""
        elif (minutes == 1):
            minutes = str(minutes) + " minute"
            seconds = ""
        else:
            minutes = str(minutes) + " minutes"
            seconds = ""
        embed.set_footer(text=f"Uptime: {days} {hours} {minutes}{seconds}")
        await ctx.send(embed=embed)

    @commands.command(aliases=["pong", "rtt", "lag"])
    async def ping(self, ctx):
        embed = discord.Embed(title="", description=f":ping_pong: Ping: {round(self.bot.latency*1000)}ms", colour=0x00988E)
        msg = await ctx.send(embed=embed)
        embed = discord.Embed(title="", description=f":ping_pong: Ping: {round(self.bot.latency*1000)}ms\n:hearts: Heartbeat: "
                                                    f"{round((datetime.datetime.utcnow()-msg.created_at).total_seconds()*100)}ms", colour=0x00988E)
        await msg.edit(embed=embed)

    @commands.command(aliases=["onlinetime", "up-time", "online-time"])
    async def uptime(self, ctx):
        delta_uptime = datetime.datetime.utcnow() - config.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        if (days == 0):
            days = ""
        elif (days == 1):
            days = str(days) + " day, "
        else:
            days = str(days) + " days, "

        if (hours == 0):
            hours = ""
        elif (hours == 1):
            hours = str(hours) + " hour and "
        else:
            hours = str(hours) + " hours and "
        if (minutes == 0):
            seconds = str(seconds) + " seconds"
            minutes = ""
        elif (minutes == 1):
            minutes = str(minutes) + " minute"
            seconds = ""
        else:
            minutes = str(minutes) + " minutes"
            seconds = ""
        await ctx.send(f"Uptime: {days}{hours}{minutes}{seconds}")

# settings
    @commands.guild_only()
    @commands.group(invoke_without_command=True)
    async def settings(self, ctx):
        embed = discord.Embed(title="", description=f"• {ctx.prefix}settings staff-roles\n"
                                                    f"- Returns the staff-roles help.\n"
                                                    f"• {ctx.prefix}settings mod-roles\n"
                                                    f"- Returns the mod-roles help.", colour=0x00988E)
        embed.set_author(name="Settings", icon_url="https://cdn.discordapp.com/attachments/463758511776595998/480298814599725057/Cog.png")
        await ctx.send(embed=embed)

# SETTINGS STAFFROLE COMMAND -------------------------------
# settings staffrole
    @commands.guild_only()
    @settings.group(aliases=["staff-role", "staff-roles", "staffroles"], invoke_without_command=True)
    async def staffrole(self, ctx):
        embed = discord.Embed(title="", description=f"• {ctx.prefix}settings staff-roles set `<@role | role | None>`\n"
                                                    f"- Changes the staff-role and removes all previous staff-roles.\n"
                                                    f"• {ctx.prefix}settings staff-roles add `<@role | role>`\n"
                                                    f"- Adds a staff-role, does not remove any roles.\n"
                                                    f"• {ctx.prefix}settings staff-roles delete `<@role | role>`\n"
                                                    f"- Adds a staff-role.\n"
                                                    f"• {ctx.prefix}settings staff-roles list\n"
                                                    f"- Lists all the server's staff roles.", colour=0x00988E)
        embed.set_author(name="Settings", icon_url="https://cdn.discordapp.com/attachments/463758511776595998/480298814599725057/Cog.png")
        await ctx.send(embed=embed)

# settings staffrole set
    @commands.guild_only()
    @staffrole.command(aliases=["set", "set-role", "set-roles", "setroles"])
    async def setrole(self, ctx, *role):
        role = " ".join(role)
        try:
            role = await commands.RoleConverter().convert(ctx, role)
        except Exception:
            await ctx.send("<:no:484017898730291211>Invaild role. Roles *are* case sensitive!")
        if ctx.author.guild_permissions.administrator:
            result = config.guildscol.find_one({"guild": ctx.guild.id})
            if len(result["staffRoles"]) > 30:
                await ctx.send("<:no:484017898730291211>Iris stores a maximum of 30 roles per server at one time. There's a good reason for this!")
            if result is not None:
                result["staffRoles"] = role
            else:
                result = ({"guild": ctx.message.guild.id,
                           "prefix": "/",
                           "staffRoles": [role.id],
                           "modRoles": [None],
                           "warningLimit": None,
                           "warningAction": None,
                           "muteRole": None
                           })
            config.guildscol.replace_one({"guild": ctx.guild.id}, result)
            embed = discord.Embed(title="", description=f"<:yes:484017899065835521>Successfully set the staff role to `{role.name}`",
                                  timestamp=datetime.datetime.utcnow(), colour=0x00988E)
            embed.set_footer(text=f"By {ctx.author}")
            await ctx.send(embed=embed)
        else:
            await ctx.send("<:no:484017898730291211>You are lacking `ADMINISTRATOR` permission.")

    @setrole.error
    async def setrole_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Usage", description=f"{ctx.prefix}settings staff-role set `<@role | role>`\n", colour=0x00988E)
            embed.add_field(name="Info:", value="Changes the staff-role and removes all previous staff-roles. Requires `ADMINSTRATOR` permission.")
            embed.set_footer(text="<Required> [Optional]")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("<:no:484017898730291211>Invaild role. Roles *are* case sensitive!")

# settings staffrole add
    @commands.guild_only()
    @staffrole.command(aliases=["add", "add-role", "addroles", "add-roles"])
    async def addrole(self, ctx, *role):
        role = " ".join(role)
        try:
            role = await commands.RoleConverter().convert(ctx, role)
        except Exception:
            await ctx.send("<:no:484017898730291211>Invaild role. Roles *are* case sensitive!")
        if ctx.author.guild_permissions.administrator:
            result = config.guildscol.find_one({"guild": ctx.guild.id})
            if len(result["staffRoles"]) > 30:
                await ctx.send("<:no:484017898730291211>Iris stores a maximum of 30 roles per server at one time. There's a good reason for this!")
            if role.id in result["staffRoles"]:
                currentRoles = []
                for roleID in result["staffRoles"]:
                    try:
                        currentRoles.append(discord.utils.get(ctx.guild.roles, id=roleID).name)
                    except Exception:
                        pass
                currentRoles = "`, `".join(currentRoles)
                await ctx.send(f"<:no:484017898730291211>That role has already been added.\nCurrent staff roles: `{currentRoles}`")
                return
            if result is not None:
                result["staffRoles"].append(role.id)
            else:
                result = ({"guild": ctx.message.guild.id,
                           "prefix": "/",
                           "staffRoles": [role.id],
                           "modRoles": [None],
                           "warningLimit": None,
                           "warningAction": None,
                           "muteRole": None
                           })
            config.guildscol.replace_one({"guild": ctx.guild.id}, result)
            currentRoles = []
            for roleID in result["staffRoles"]:
                try:
                    currentRoles.append(discord.utils.get(ctx.guild.roles, id=roleID).name)
                except Exception:
                    pass
            currentRoles = "`, `".join(currentRoles)
            embed = discord.Embed(title="", description=f"<:yes:484017899065835521>Successfully added `{role.name}` to the staff roles.\n Current "
                                                        f"roles: `{currentRoles}`",
                                  timestamp=datetime.datetime.utcnow(), colour=0x00988E)
            embed.set_footer(text=f"By {ctx.author}")
            await ctx.send(embed=embed)
        else:
            await ctx.send("<:no:484017898730291211>You are lacking `ADMINISTRATOR` permission.")

    @addrole.error
    async def addrole_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Usage", description=f"{ctx.prefix}settings staff-role add `<@role | role>`\n", colour=0x00988E)
            embed.add_field(name="Info:", value="Adds a staff-role, does not remove any roles. Requires `ADMINSTRATOR` permission.")
            embed.set_footer(text="<Required> [Optional]")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("<:no:484017898730291211>Invaild role. Roles *are* case sensitive!")

# settings staffrole del
    @commands.guild_only()
    @staffrole.command(aliases=["del-role", "del", "remove", "delroles", "del-roles"])
    async def delrole(self, ctx, *role):
        role = " ".join(role)
        try:
            role = await commands.RoleConverter().convert(ctx, role)
        except Exception:
            await ctx.send("<:no:484017898730291211>Invaild role. Roles *are* case sensitive!")
        if ctx.author.guild_permissions.administrator:
            result = config.guildscol.find_one({"guild": ctx.guild.id})
            if len(result["staffRoles"]) > 30:
                await ctx.send("<:no:484017898730291211>Iris stores a maximum of 30 roles per server at one time. There's a good reason for this!")
            if role.id not in result["staffRoles"]:
                currentRoles = []
                for roleID in result["staffRoles"]:
                    try:
                        currentRoles.append(discord.utils.get(ctx.guild.roles, id=roleID).name)
                    except Exception:
                        pass
                currentRoles = "`, `".join(currentRoles)
                await ctx.send(f"<:no:484017898730291211>That role doesn't exist in the staffrole list.\nCurrent staffroles: `{currentRoles}`")
                return
            result["staffRoles"].remove(role.id)
            config.guildscol.replace_one({"guild": ctx.guild.id}, result)
            currentRoles = []
            for roleID in result["staffRoles"]:
                try:
                    currentRoles.append(discord.utils.get(ctx.guild.roles, id=roleID).name)
                except Exception:
                    pass
            currentRoles = "`, `".join(currentRoles)
            embed = discord.Embed(title="", description=f"<:yes:484017899065835521>Successfully deleted `{role.name}`.\nCurrent staff roles: "
                                                        f"`{currentRoles}`",
                                  timestamp=datetime.datetime.utcnow(), colour=0x00988E)
            embed.set_footer(text=f"By {ctx.author}")
            await ctx.send(embed=embed)
        else:
            await ctx.send("<:no:484017898730291211>You are lacking `ADMINISTRATOR` permission.")

    @delrole.error
    async def delrole_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Usage", description=f"{ctx.prefix}staff-role de `<@role | role>`\n", colour=0x00988E)
            embed.add_field(name="Info:", value="Changes the staff-role and removes all previous staff-roles. Requires `ADMINSTRATOR` permission.")
            embed.set_footer(text="<Required> [Optional]")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("<:no:484017898730291211>Invaild role. Roles *are* case sensitive!")

# settings staffrole list
    @commands.guild_only()
    @staffrole.command(aliases=["list", "list-roles", "show", "display", "listroles"])
    async def listrole(self, ctx):
        result = config.guildscol.find_one({"guild": ctx.guild.id})
        currentRoles = []
        for roleID in result["staffRoles"]:
            try:
                currentRoles.append(discord.utils.get(ctx.guild.roles, id=roleID).name)
            except Exception:
                pass
        currentRoles = "`, `".join(currentRoles)
        if currentRoles == "":
            currentRoles = f"No staff roles on this server. Add some with {ctx.prefix}staff-role add `<@role | role>`!"
        embed = discord.Embed(title=f"{ctx.guild.name} staff roles:", description=f"`{currentRoles}`", colour=0x00988E,
                              timestamp=datetime.datetime.utcnow())
        await ctx.send(embed=embed)

# STAFFROLE COMMAND -------------------------------------------
# staffrole
    @commands.guild_only()
    @commands.group(aliases=["staff-role", "staff-roles", "staffrole"], invoke_without_command=True)
    async def staffroles(self, ctx):
        embed = discord.Embed(title="", description=f"• {ctx.prefix}settings staff-roles set `<@role | role | None>`\n"
                                                    f"- Changes the staff-role and removes all previous staff-roles.\n"
                                                    f"• {ctx.prefix}settings staff-roles add `<@role | role>`\n"
                                                    f"- Adds a staff-role, does not remove any roles.\n"
                                                    f"• {ctx.prefix}settings staff-roles delete `<@role | role>`\n"
                                                    f"- Removes a staff-role.\n"
                                                    f"• {ctx.prefix}settings staff-roles list\n"
                                                    f"- Lists all the server's staff roles.", colour=0x00988E)
        embed.set_author(name="Settings", icon_url="https://cdn.discordapp.com/attachments/463758511776595998/480298814599725057/Cog.png")
        await ctx.send(embed=embed)

# staffrole set
    @commands.guild_only()
    @staffroles.command(aliases=["set", "set-role", "set-roles", "setrole"])
    async def setroles(self, ctx, *role):
        role = " ".join(role)
        try:
            role = await commands.RoleConverter().convert(ctx, role)
        except Exception:
            await ctx.send("<:no:484017898730291211>Invaild role. Roles *are* case sensitive!")
        if ctx.author.guild_permissions.administrator:
            result = config.guildscol.find_one({"guild": ctx.guild.id})
            if len(result["staffRoles"]) > 30:
                await ctx.send("<:no:484017898730291211>Iris stores a maximum of 30 roles per server at one time. There's a good reason for this!")
            if result is not None:
                result["staffRoles"] = role
            else:
                result = ({"guild": ctx.message.guild.id,
                           "prefix": "/",
                           "staffRoles": [role.id],
                           "modRoles": [None],
                           "warningLimit": None,
                           "warningAction": None,
                           "muteRole": None
                           })
            config.guildscol.replace_one({"guild": ctx.guild.id}, result)
            embed = discord.Embed(title="", description=f"<:yes:484017899065835521>Successfully set the staff role to `{role.name}`",
                                  timestamp=datetime.datetime.utcnow(), colour=0x00988E)
            embed.set_footer(text=f"By {ctx.author}")
            await ctx.send(embed=embed)
        else:
            await ctx.send("<:no:484017898730291211>You are lacking `ADMINISTRATOR` permission.")

# staffrole set
    @setroles.error
    async def setroles_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Usage", description=f"{ctx.prefix}staff-role set `<@role | role>`\n", colour=0x00988E)
            embed.add_field(name="Info:", value="Changes the staff-role and removes all previous staff-roles. Requires `ADMINSTRATOR` permission.")
            embed.set_footer(text="<Required> [Optional]")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("<:no:484017898730291211>Invaild role. Roles *are* case sensitive!")

# staffrole add
    @commands.guild_only()
    @staffroles.command(aliases=["add", "add-role", "addrole", "add-roles"])
    async def addroles(self, ctx, *role):
        role = " ".join(role)
        try:
            role = await commands.RoleConverter().convert(ctx, role)
        except Exception:
            await ctx.send("<:no:484017898730291211>Invaild role. Roles *are* case sensitive!")
        if ctx.author.guild_permissions.administrator:
            result = config.guildscol.find_one({"guild": ctx.guild.id})
            if len(result["staffRoles"]) > 30:
                await ctx.send("<:no:484017898730291211>Iris stores a maximum of 30 roles per server at one time. There's a good reason for this!")
            if role.id in result["staffRoles"]:
                currentRoles = []
                for roleID in result["staffRoles"]:
                    try:
                        currentRoles.append(discord.utils.get(ctx.guild.roles, id=roleID).name)
                    except Exception:
                        pass
                currentRoles = "`, `".join(currentRoles)
                if currentRoles == "":
                    currentRoles = "No staff roles in this server."
                else:
                    currentRoles = f"Current staff roles: `{currentRoles}`"
                await ctx.send(f"<:no:484017898730291211>That role has already been added.\n{currentRoles}")
                return
            if result is not None:
                result["staffRoles"].append(role.id)
            else:
                result = ({"guild": ctx.message.guild.id,
                           "prefix": "/",
                           "staffRoles": [role.id],
                           "modRoles": [None],
                           "warningLimit": None,
                           "warningAction": None,
                           "muteRole": None
                           })
            config.guildscol.replace_one({"guild": ctx.guild.id}, result)
            currentRoles = []
            for roleID in result["staffRoles"]:
                try:
                    currentRoles.append(discord.utils.get(ctx.guild.roles, id=roleID).name)
                except Exception:
                    pass
            currentRoles = "`, `".join(currentRoles)
            if currentRoles == "":
                currentRoles = "No staff roles in this server."
            else:
                currentRoles = f"Current staff roles: `{currentRoles}`"
            embed = discord.Embed(title="", description=f"<:yes:484017899065835521>Successfully added `{role.name}` to the staff roles.\n"
                                                        f"{currentRoles}",
                                  timestamp=datetime.datetime.utcnow(), colour=0x00988E)
            embed.set_footer(text=f"By {ctx.author}")
            await ctx.send(embed=embed)
        else:
            await ctx.send("<:no:484017898730291211>You are lacking `ADMINISTRATOR` permission.")

    @addroles.error
    async def addroles_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Usage", description=f"{ctx.prefix}staff-role add `<@role | role>`\n", colour=0x00988E)
            embed.add_field(name="Info:", value="Adds a staff-role, does not remove any roles. Requires `ADMINSTRATOR` permission.")
            embed.set_footer(text="<Required> [Optional]")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("<:no:484017898730291211>Invaild role. Roles *are* case sensitive!")

# staffrole del
    @commands.guild_only()
    @staffroles.command(aliases=["del-role", "del", "remove", "delrole", "del-roles"])
    async def delroles(self, ctx, *role):
        role = " ".join(role)
        try:
            role = await commands.RoleConverter().convert(ctx, role)
        except Exception:
            await ctx.send("<:no:484017898730291211>Invaild role. Roles *are* case sensitive!")
        if ctx.author.guild_permissions.administrator:
            result = config.guildscol.find_one({"guild": ctx.guild.id})
            if len(result["staffRoles"]) > 30:
                await ctx.send("<:no:484017898730291211>Iris stores a maximum of 30 roles per server at one time. There's a good reason for this!")
            if role.id not in result["staffRoles"]:
                currentRoles = []
                for roleID in result["staffRoles"]:
                    try:
                        currentRoles.append(discord.utils.get(ctx.guild.roles, id=roleID).name)
                    except Exception:
                        pass
                currentRoles = "`, `".join(currentRoles)
                if currentRoles == "":
                    currentRoles = "No staff roles in this server."
                else:
                    currentRoles = f"Current staff roles: `{currentRoles}`"
                await ctx.send(f"<:no:484017898730291211>That role doesn't exist in the staffrole list.\n{currentRoles}")
                return
            result["staffRoles"].remove(role.id)
            config.guildscol.replace_one({"guild": ctx.guild.id}, result)
            currentRoles = []
            for roleID in result["staffRoles"]:
                try:
                    currentRoles.append(discord.utils.get(ctx.guild.roles, id=roleID).name)
                except Exception:
                    pass
            currentRoles = "`, `".join(currentRoles)
            if currentRoles == "":
                currentRoles = "No staff roles in this server."
            else:
                currentRoles = f"Current staff roles: `{currentRoles}`"
            embed = discord.Embed(title="", description=f"<:yes:484017899065835521>Successfully deleted `{role.name}`.\n{currentRoles}",
                                  timestamp=datetime.datetime.utcnow(), colour=0x00988E)
            embed.set_footer(text=f"By {ctx.author}")
            await ctx.send(embed=embed)
        else:
            await ctx.send("<:no:484017898730291211>You are lacking `ADMINISTRATOR` permission.")

    @delroles.error
    async def delroles_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Usage", description=f"{ctx.prefix}staff-role set `<@role | role>`\n", colour=0x00988E)
            embed.add_field(name="Info:", value="Adds a staff-role, does not remove any roles. Requires `ADMINSTRATOR` permission.")
            embed.set_footer(text="<Required> [Optional]")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("<:no:484017898730291211>Invaild role. Roles *are* case sensitive!")

# staffrole list
    @commands.guild_only()
    @staffroles.command(aliases=["list", "list-roles", "show", "display", "listroles"])
    async def list_staff_roles(self, ctx):
        result = config.guildscol.find_one({"guild": ctx.guild.id})
        currentRoles = []
        for roleID in result["staffRoles"]:
            try:
                currentRoles.append(discord.utils.get(ctx.guild.roles, id=roleID).name)
            except Exception:
                pass
        currentRoles = "`, `".join(currentRoles)
        if currentRoles == "":
            currentRoles = "No staff roles in this server."
        else:
            currentRoles = f"Current staff roles: `{currentRoles}`"
        embed = discord.Embed(title=f"{ctx.guild.name} staff roles:", description=f"`{currentRoles}`", colour=0x00988E,
                              timestamp=datetime.datetime.utcnow())
        await ctx.send(embed=embed)

# SETTINGS MODROLE COMMAND ------------------------------------
# settings modrole
    @commands.guild_only()
    @settings.group(aliases=["mod-role", "mod-roles", "modroles"], invoke_without_command=True)
    async def modrole(self, ctx):
        embed = discord.Embed(title="", description=f"• {ctx.prefix}settings mod-roles set `<@role | role | None>`\n"
                                                    f"- Changes the mod-role and removes all previous mod-roles.\n"
                                                    f"• {ctx.prefix}settings mod-roles add `<@role | role>`\n"
                                                    f"- Adds a mod-role, does not remove any roles.\n"
                                                    f"• {ctx.prefix}settings mod-roles delete `<@role | role>`\n"
                                                    f"- Adds a mod-role.\n"
                                                    f"• {ctx.prefix}settings mod-roles list\n"
                                                    f"- Lists all the server's mod roles.", colour=0x00988E)
        embed.set_author(name="Settings", icon_url="https://cdn.discordapp.com/attachments/463758511776595998/480298814599725057/Cog.png")
        await ctx.send(embed=embed)

# settings modrole set
    @commands.guild_only()
    @modrole.command(aliases=["set", "set-role", "set-roles", "setroles"])
    async def setRole(self, ctx, *role):
        role = " ".join(role)
        try:
            role = await commands.RoleConverter().convert(ctx, role)
        except Exception:
            await ctx.send("<:no:484017898730291211>Invaild role. Roles *are* case sensitive!")
        if ctx.author.guild_permissions.administrator:
            result = config.guildscol.find_one({"guild": ctx.guild.id})
            if len(result["modRoles"]) > 30:
                await ctx.send("<:no:484017898730291211>Iris stores a maximum of 30 roles per server at one time. There's a good reason for this!")
            result["modRoles"] = [role.id]
            config.guildscol.replace_one({"guild": ctx.guild.id}, result)
            embed = discord.Embed(title="", description=f"<:yes:484017899065835521>Successfully set the mod role to `{role.name}`",
                                  timestamp=datetime.datetime.utcnow(), colour=0x00988E)
            embed.set_footer(text=f"By {ctx.author}")
            await ctx.send(embed=embed)
        else:
            await ctx.send("<:no:484017898730291211>You are lacking `ADMINISTRATOR` permission.")

    @setRole.error
    async def setRole_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Usage", description=f"{ctx.prefix}settings mod-role set `<@role | role>`\n", colour=0x00988E)
            embed.add_field(name="Info:", value="Changes the mod-role and removes all previous mod-roles. Requires `ADMINSTRATOR` permission.")
            embed.set_footer(text="<Required> [Optional]")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("<:no:484017898730291211>Invaild role. Roles *are* case sensitive!")

# settings modrole add
    @commands.guild_only()
    @modrole.command(aliases=["add", "add-role", "addroles", "add-roles"])
    async def addRole(self, ctx, *role):
        role = " ".join(role)
        try:
            role = await commands.RoleConverter().convert(ctx, role)
        except Exception:
            await ctx.send("<:no:484017898730291211>Invaild role. Roles *are* case sensitive!")
        if ctx.author.guild_permissions.administrator:
            result = config.guildscol.find_one({"guild": ctx.guild.id})
            if len(result["modRoles"]) > 30:
                await ctx.send("<:no:484017898730291211>Iris stores a maximum of 30 roles per server at one time. There's a good reason for this!")
            if role.id in result["modRoles"]:
                currentRoles = []
                for roleID in result["modRoles"]:
                    try:
                        currentRoles.append(discord.utils.get(ctx.guild.roles, id=roleID).name)
                    except Exception:
                        pass
                currentRoles = "`, `".join(currentRoles)
                if currentRoles == "":
                    currentRoles = "No mod roles in this server."
                else:
                    currentRoles = f"Current mod roles: {currentRoles}"
                await ctx.send(f"<:no:484017898730291211>That role has already been added.\n{currentRoles}")
                return
            if result is not None:
                result["modRoles"].append(role.id)
            else:
                result = ({"guild": ctx.message.guild.id,
                           "prefix": "/",
                           "staffRoles": [None],
                           "modRoles": [role.id],
                           "warningLimit": None,
                           "warningAction": None,
                           "muteRole": None
                           })
            config.guildscol.replace_one({"guild": ctx.guild.id}, result)
            currentRoles = []
            for roleID in result["modRoles"]:
                try:
                    currentRoles.append(discord.utils.get(ctx.guild.roles, id=roleID).name)
                except Exception:
                    pass
            currentRoles = "`, `".join(currentRoles)
            if currentRoles == "":
                currentRoles = "No mod roles in this server."
            else:
                currentRoles = f"Current mod roles: `{currentRoles}`"
            embed = discord.Embed(title="", description=f"<:yes:484017899065835521>Successfully added `{role.name}` to the mod roles.\n"
                                                        f"{currentRoles}`",
                                  timestamp=datetime.datetime.utcnow(), colour=0x00988E)
            embed.set_footer(text=f"By {ctx.author}")
            await ctx.send(embed=embed)
        else:
            await ctx.send("<:no:484017898730291211>You are lacking `ADMINISTRATOR` permission.")

    @addRole.error
    async def addRole_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Usage", description=f"{ctx.prefix}settings mod-role add `<@role | role>`\n", colour=0x00988E)
            embed.add_field(name="Info:", value="Adds a mod-role, does not remove any roles. Requires `ADMINSTRATOR` permission.")
            embed.set_footer(text="<Required> [Optional]")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("<:no:484017898730291211>Invaild role. Roles *are* case sensitive!")

# settings modrole del
    @commands.guild_only()
    @modrole.command(aliases=["del-role", "del", "remove", "delrole", "del-roles"])
    async def delRole(self, ctx, *role):
        role = " ".join(role)
        try:
            role = await commands.RoleConverter().convert(ctx, role)
        except Exception:
            await ctx.send("<:no:484017898730291211>Invaild role. Roles *are* case sensitive!")
        if ctx.author.guild_permissions.administrator:
            result = config.guildscol.find_one({"guild": ctx.guild.id})
            if len(result["modRoles"]) > 30:
                await ctx.send("<:no:484017898730291211>Iris stores a maximum of 30 roles per server at one time. There's a good reason for this!")
            if role.id not in result["modRoles"]:
                currentRoles = []
                for roleID in result["modRoles"]:
                    try:
                        currentRoles.append(discord.utils.get(ctx.guild.roles, id=roleID).name)
                    except Exception:
                        pass
                currentRoles = "`, `".join(currentRoles)
                if currentRoles == "":
                    currentRoles = "No mod roles in this server."
                else:
                    currentRoles = f"Current mod roles: `{currentRoles}`"
                await ctx.send(f"<:no:484017898730291211>That role doesn't exist in the modrole list.\n{currentRoles}")
                return
            result["modRoles"].remove(role.id)
            config.guildscol.replace_one({"guild": ctx.guild.id}, result)
            currentRoles = []
            for roleID in result["modRoles"]:
                try:
                    currentRoles.append(discord.utils.get(ctx.guild.roles, id=roleID).name)
                except Exception:
                    pass
            currentRoles = "`, `".join(currentRoles)
            if currentRoles == "":
                currentRoles = "No mod roles in this server."
            else:
                currentRoles = f"Current mod roles: `{currentRoles}`"
            embed = discord.Embed(title="", description=f"<:yes:484017899065835521>Successfully deleted `{role.name}`.\n"
                                                        f"{currentRoles}",
                                  timestamp=datetime.datetime.utcnow(), colour=0x00988E)
            embed.set_footer(text=f"By {ctx.author}")
            await ctx.send(embed=embed)
        else:
            await ctx.send("<:no:484017898730291211>You are lacking `ADMINISTRATOR` permission.")

    @delRole.error
    async def delRole_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Usage", description=f"{ctx.prefix}mod-role de `<@role | role>`\n", colour=0x00988E)
            embed.add_field(name="Info:", value="Changes the mod-role and removes all previous mod-roles. Requires `ADMINSTRATOR` permission.")
            embed.set_footer(text="<Required> [Optional]")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("<:no:484017898730291211>Invaild role. Roles *are* case sensitive!")

# settings modrole list
    @commands.guild_only()
    @modrole.command(aliases=["list", "list-roles", "show", "display", "listroles"])
    async def listRole(self, ctx):
        result = config.guildscol.find_one({"guild": ctx.guild.id})
        currentRoles = []
        for roleID in result["modRoles"]:
            try:
                currentRoles.append(discord.utils.get(ctx.guild.roles, id=roleID).name)
            except Exception:
                pass
        currentRoles = "`, `".join(currentRoles)
        if currentRoles == "":
            currentRoles = "No mod roles in this server."
        else:
            currentRoles = f"Current mod roles: {currentRoles}"
        embed = discord.Embed(title=f"{ctx.guild.name} mod roles:", description=f"{currentRoles}", colour=0x00988E,
                              timestamp=datetime.datetime.utcnow())
        await ctx.send(embed=embed)

# MODROLE COMMAND ------------------------------------
# modrole
    @commands.guild_only()
    @commands.group(aliases=["mod-role", "mod-roles", "modrole"], invoke_without_command=True)
    async def modRoles(self, ctx):
        embed = discord.Embed(title="", description=f"• {ctx.prefix}mod-roles set `<@role | role | None>`\n"
                                                    f"- Changes the mod-role and removes all previous mod-roles.\n"
                                                    f"• {ctx.prefix}mod-roles add `<@role | role>`\n"
                                                    f"- Adds a mod-role, does not remove any roles.\n"
                                                    f"• {ctx.prefix}mod-roles delete `<@role | role>`\n"
                                                    f"- Removes a mod-role.\n"
                                                    f"• {ctx.prefix}mod-roles list\n"
                                                    f"- Lists all the server's mod roles.", colour=0x00988E)
        embed.set_author(name="Settings", icon_url="https://cdn.discordapp.com/attachments/463758511776595998/480298814599725057/Cog.png")
        await ctx.send(embed=embed)

# modrole set
    @commands.guild_only()
    @modRoles.command(aliases=["set-role", "set", "setrole"])
    async def setRoles(self, ctx, *role):
        role = " ".join(role)
        try:
            role = await commands.RoleConverter().convert(ctx, role)
        except Exception:
            await ctx.send("<:no:484017898730291211>Invaild role. Roles *are* case sensitive!")
        if ctx.author.guild_permissions.administrator:
            result = config.guildscol.find_one({"guild": ctx.guild.id})
            if len(result["modRoles"]) > 30:
                await ctx.send("<:no:484017898730291211>Iris stores a maximum of 30 roles per server at one time. There's a good reason for this!")
            result["modRoles"] = [role.id]
            config.guildscol.replace_one({"guild": ctx.guild.id}, result)
            embed = discord.Embed(title="", description=f"<:yes:484017899065835521>Successfully set the mod role to `{role.name}`",
                                  timestamp=datetime.datetime.utcnow(), colour=0x00988E)
            embed.set_footer(text=f"By {ctx.author}")
            await ctx.send(embed=embed)
        else:
            await ctx.send("<:no:484017898730291211>You are lacking `ADMINISTRATOR` permission.")

    @setRoles.error
    async def setRoles_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Usage", description=f"{ctx.prefix}mod-role set `<@role | role>`\n", colour=0x00988E)
            embed.add_field(name="Info:", value="Changes the mod-role and removes all previous mod-roles. Requires `ADMINSTRATOR` permission.")
            embed.set_footer(text="<Required> [Optional]")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("<:no:484017898730291211>Invaild role. Roles *are* case sensitive!")

# modrole add
    @commands.guild_only()
    @modRoles.command(aliases=["add-role", "add", "addrole"])
    async def addRoles(self, ctx, *role):
        role = " ".join(role)
        try:
            role = await commands.RoleConverter().convert(ctx, role)
        except Exception:
            await ctx.send("<:no:484017898730291211>Invaild role. Roles *are* case sensitive!")
        if ctx.author.guild_permissions.administrator:
            result = config.guildscol.find_one({"guild": ctx.guild.id})
            if len(result["modRoles"]) > 30:
                await ctx.send("<:no:484017898730291211>Iris stores a maximum of 30 roles per server at one time. There's a good reason for this!")
            if role.id in result["modRoles"]:
                currentRoles = []
                for roleID in result["modRoles"]:
                    try:
                        currentRoles.append(discord.utils.get(ctx.guild.roles, id=roleID).name)
                    except Exception:
                        pass
                currentRoles = "`, `".join(currentRoles)
                if currentRoles == "":
                    currentRoles = "No mod roles in this server."
                else:
                    currentRoles = f"Current mod roles: `{currentRoles}`"
                await ctx.send(f"<:no:484017898730291211>That role has already been added.\n{currentRoles}")
                return
            result["modRoles"].append(role.id)
            config.guildscol.replace_one({"guild": ctx.guild.id}, result)
            currentRoles = []
            for roleID in result["modRoles"]:
                try:
                    currentRoles.append(discord.utils.get(ctx.guild.roles, id=roleID).name)
                except Exception:
                    pass
            currentRoles = "`, `".join(currentRoles)
            embed = discord.Embed(title="", description=f"<:yes:484017899065835521>Successfully added `{role.name}` to the mod roles.\n Current "
                                                        f"roles: `{currentRoles}`",
                                  timestamp=datetime.datetime.utcnow(), colour=0x00988E)
            embed.set_footer(text=f"By {ctx.author}")
            await ctx.send(embed=embed)
        else:
            await ctx.send("<:no:484017898730291211>You are lacking `ADMINISTRATOR` permission.")

    @addRoles.error
    async def addRoles_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Usage", description=f"{ctx.prefix}mod-role add `<@role | role>`\n", colour=0x00988E)
            embed.add_field(name="Info:", value="Adds a mod-role, does not remove any roles. Requires `ADMINSTRATOR` permission.")
            embed.set_footer(text="<Required> [Optional]")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("<:no:484017898730291211>Invaild role. Roles *are* case sensitive!")

# modrole del
    @commands.guild_only()
    @modRoles.command(aliases=["del-role", "del", "delete", "deleterole", "delete-role", "delrole", "remove"])
    async def delRoles(self, ctx, *role):
        role = " ".join(role)
        try:
            role = await commands.RoleConverter().convert(ctx, role)
        except Exception:
            await ctx.send("<:no:484017898730291211>Invaild role. Roles *are* case sensitive!")
        if ctx.author.guild_permissions.administrator:
            result = config.guildscol.find_one({"guild": ctx.guild.id})
            if len(result["modRoles"]) > 30:
                await ctx.send("<:no:484017898730291211>Iris stores a maximum of 30 roles per server at one time. There's a good reason for this!")
            if role.id not in result["modRoles"]:
                currentRoles = []
                for roleID in result["modRoles"]:
                    try:
                        currentRoles.append(discord.utils.get(ctx.guild.roles, id=roleID).name)
                    except Exception:
                        pass
                currentRoles = "`, `".join(currentRoles)
                await ctx.send(f"<:no:484017898730291211>That role doesn't exist in the modrole list.\nCurrent mod roles: `{currentRoles}`")
                return
            result["modRoles"].remove(role.id)
            config.guildscol.replace_one({"guild": ctx.guild.id}, result)
            currentRoles = []
            for roleID in result["modRoles"]:
                try:
                    currentRoles.append(discord.utils.get(ctx.guild.roles, id=roleID).name)
                except Exception:
                    pass
            currentRoles = "`, `".join(currentRoles)
            embed = discord.Embed(title="", description=f"<:yes:484017899065835521>Successfully deleted `{role.name}`.\nCurrent mod roles: "
                                                        f"`{currentRoles}`",
                                  timestamp=datetime.datetime.utcnow(), colour=0x00988E)
            embed.set_footer(text=f"By {ctx.author}")
            await ctx.send(embed=embed)
        else:
            await ctx.send("<:no:484017898730291211>You are lacking `ADMINISTRATOR` permission.")

    @delRoles.error
    async def delRoles_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Usage", description=f"{ctx.prefix}mod-role set `<@role | role>`\n", colour=0x00988E)
            embed.add_field(name="Info:", value="Adds a mod-role, does not remove any roles. Requires `ADMINSTRATOR` permission.")
            embed.set_footer(text="<Required> [Optional]")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("<:no:484017898730291211>Invaild role. Roles *are* case sensitive!")

# modrole list
    @commands.guild_only()
    @modRoles.command(aliases=["list"])
    async def listRoles(self, ctx):
        result = config.guildscol.find_one({"guild": ctx.guild.id})
        currentRoles = []
        for roleID in result["modRoles"]:
            try:
                currentRoles.append(discord.utils.get(ctx.guild.roles, id=roleID).name)
            except Exception:
                pass
        currentRoles = "`, `".join(currentRoles)
        if currentRoles == "":
            currentRoles = "No mod roles in this server."
        else:
            currentRoles = f"Current staff roles: `{currentRoles}`"
        embed = discord.Embed(title=f"{ctx.guild.name} mod roles:", description=f"{currentRoles}", colour=0x00988E,
                              timestamp=datetime.datetime.utcnow())
        await ctx.send(embed=embed)

# SETTINGS WARNING COMMAND ------------------------

# settings warning
    @commands.guild_only()
    @settings.group(aliases=["warnings", "warn"], invoke_without_command=True)
    async def warning(self, ctx):
        embed = discord.Embed(title="", description=f"• {ctx.prefix}settings warnings limit `<number | None>`\n"
                                                    f"- Sets the maximum amount of warnings before the `action` is executed.\n"
                                                    f"• {ctx.prefix}settings warnings action `<ban | kick | mute | None>`\n"
                                                    f"- Sets the action to execute when a member reaches `limit` warnings.\n", colour=0x00988E)
        embed.set_author(name="Settings", icon_url="https://cdn.discordapp.com/attachments/463758511776595998/480298814599725057/Cog.png")
        await ctx.send(embed=embed)

# settings warning limit
    @commands.guild_only()
    @warning.command(aliases=["set-limit", "setlimit"])
    async def limit(self, ctx, limit: str):
        if ctx.author.guild_permissions.administrator:
            if limit.lower() in ["no", "none", "remove", "unlimited", "false", "not", "f", "n"]:
                limit = None
            else:
                try:
                    int(limit)
                except Exception:
                    await ctx.send("<:no:484017898730291211>Invaild limit. Possible values: `1-30 | remove`")
                    return
            if ctx.author.guild_permissions.administrator:
                result = config.guildscol.find_one({"guild": ctx.guild.id})
                if result is not None:
                    prevlimit = result["warningLimit"]
                    result["warningLimit"] = int(limit)
                else:
                    prevlimit = None
                    result = ({"guild": ctx.guild.id,
                               "prefix": "/",
                               "staffRoles": [None],
                               "modRoles": [None],
                               "warningLimit": limit,
                               "warningAction": None,
                               "muteRole": None
                               })
                config.guildscol.replace_one({"guild": ctx.guild.id}, result, True)
                if prevlimit is not None:
                    embed = discord.Embed(title="", description=f"<:yes:484017899065835521> Successfully changed the warning limit to `{limit}`\n"
                                                                f"Previous: `{prevlimit}`",
                                          colour=0x00988E)
                    embed.set_footer(text=f"By: {ctx.author}")
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(title="", description=f"<:yes:484017899065835521> Successfully set the warning limit to `{limit}`",
                                          colour=0x00988E)
                    embed.set_footer(text=f"By: {ctx.author}")
                    await ctx.send(embed=embed)
        else:
            await ctx.send("<:no:484017898730291211>You are lacking `ADMINISTRATOR` permission.")

    async def on_guild_remove(self, guild):
        config.guildscol.delete_many({"guild": guild.id})
        config.memberscol.delete_many({"guild": guild.id})

# settings warning action
    @commands.guild_only()
    @warning.command(aliases=["set-action", "setaction"])
    async def action(self, ctx, action: str):
        if ctx.author.guild_permissions.administrator:
            if action.lower() in ["ban", "banuser"]:
                action = "ban"
            elif action.lower() in ["kick", "kickuser"]:
                action = "ban"
            elif action.lower() in ["mute", "muteuser"]:
                action = "kick"
            else:
                await ctx.send()
            result = config.guildscol.find_one({"guild": ctx.guild.id})
            if result is not None:
                prevaction = result["warningAction"]
                result["warningAction"] = action
            else:
                prevaction = None
                result = ({"guild": ctx.guild.id,
                           "prefix": "/",
                           "staffRoles": [None],
                           "modRoles": [None],
                           "warningLimit": None,
                           "warningAction": action,
                           "muteRole": None
                           })
            config.guildscol.replace_one({"guild": ctx.guild.id}, result, True)
            if prevaction is not None:
                    embed = discord.Embed(title="", description=f"<:yes:484017899065835521> Successfully changed the warning action to `{action}`\n"
                                                                f"Previous: `{prevaction}`",
                                          colour=0x00988E)
                    embed.set_footer(text=f"By: {ctx.author}")
                    await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="", description=f"<:yes:484017899065835521> Successfully set the warning limit to `{action}`",
                                      colour=0x00988E)
                embed.set_footer(text=f"By: {ctx.author}")
                await ctx.send(embed=embed)
        else:
            await ctx.send("<:no:484017898730291211>You are lacking `ADMINISTRATOR` permission.")

# muterole
    @commands.guild_only()
    @settings.command(aliases=["mute-role"])
    async def muterole(self, ctx, *role):
        role = " ".join(role)
        if role in ["no", "none", "remove", "unlimited", "false", "not", "f", "n"]:
            role = None
        else:
            try:
                role = await commands.RoleConverter().convert(ctx, role)
            except Exception:
                await ctx.send("<:no:484017898730291211>Invaild role. Roles *are* case sensitive!")
        if ctx.author.guild_permissions.administrator:
            result = config.guildscol.find_one({"guild": ctx.guild.id})
            if result is not None:
                result["muteRole"] = role.id
            else:
                result = ({"guild": ctx.guild.id,
                           "prefix": "/",
                           "staffRoles": [None],
                           "modRoles": [None],
                           "warningLimit": None,
                           "warningAction": None,
                           "muteRole": role.id
                           })
            config.guildscol.replace_one({"guild": ctx.guild.id}, result, True)
            embed = discord.Embed(title="", description=f"<:yes:484017899065835521> Successfully set the mute role to `{role.name}`",
                                  colour=0x00988E)
            embed.set_footer(text=f"By: {ctx.author}")
            await ctx.send(embed=embed)
        else:
            await ctx.send("<:no:484017898730291211>You are lacking `ADMINISTRATOR` permission.")

    @commands.guild_only()
    @commands.command(aliases=["mute-role"])
    async def muteRole(self, ctx, *role):
        role = " ".join(role)
        if role in ["no", "none", "remove", "unlimited", "false", "not", "f", "n"]:
            role = None
        else:
            try:
                role = await commands.RoleConverter().convert(ctx, role)
            except Exception:
                await ctx.send("<:no:484017898730291211>Invaild role. Roles *are* case sensitive!")
        if ctx.author.guild_permissions.administrator:
            result = config.guildscol.find_one({"guild": ctx.guild.id})
            if result is not None:
                result["muteRole"] = role.id
            else:
                result = ({"guild": ctx.guild.id,
                           "prefix": "/",
                           "staffRoles": [None],
                           "modRoles": [None],
                           "warningLimit": None,
                           "warningAction": None,
                           "muteRole": role.id
                           })
            config.guildscol.replace_one({"guild": ctx.guild.id}, result, True)
            embed = discord.Embed(title="", description=f"<:yes:484017899065835521> Successfully set the mute role to `{role.name}`",
                                  colour=0x00988E)
            embed.set_footer(text=f"By: {ctx.author}")
            await ctx.send(embed=embed)
        else:
            await ctx.send("<:no:484017898730291211>You are lacking `ADMINISTRATOR` permission.")


def setup(bot):
    bot.add_cog(Utility(bot))
