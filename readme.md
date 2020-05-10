<h1>Setup</h1>
Requirements:
<ul>
	<li>discord.py rewrite</li>
	<li>python 3.6</li>
	<li>mongodb</li>
	<li>update MONGOSTRING in config.py</li>
	<li>run bot.py</li>
	
<h1>Iris Bot</h1>
A simple discord bot with moderation features.
<h3>Admin commands</h3>
<ul>
	<li>load [module] - loads a module</li>
	<li>unload [module] - unloads a module</li>
	<li>reload [module] - unloads and then loads a module</li>
	<li>restart - reloads all modules</li>
</ul>
<h3>Server Moderation commands</h3>
<ul>
	<li>warn [user] [warning] - Adds a warning to the database and DMs the user with the warning.</li>
	<li>warnings [user] - fetches a user's warnings from the database.</li>
	<li>warnings add [user] [warning] - alias for "warn" <br>
	Aliases: "warn", "addwarning", "warnuser", "warningadd", "warnadd", "addwarn"</li>
	<li>warnings listwarnings [user] - alias for "warnings" <br>
	Aliases: "list", "listwarns", "warnlist"</li>
	<li>warnings delete [user] [warning id] - deletes a warning from the database <br>
	Aliases: "remove", "del", "erase", "delwarning", "delwarn", "warndel", "warningdel"</li>
	<li>warnings clear [user] - deletes all a user's warnings <br>
	Aliases: "clean", "clearwarnings", "clearwarns", "warningsclear", "warnsclear"</li>
	<hr>
	<li>purge [amount] - deletes the previous <i>amount</i> of messages in a channel <br>
	Aliases: "purgemessages", "purgemsgs", "prune"</li>
	<li>purge member [user] [amount] - deletes an <i>amount</i> of messages sent by a <i>user</i> in the channel <br>
	Aliaes: "user"</li>
	<li>purge bots [amount] - deletes an <i>amount</i> of messages sent by bots in the channel</li>
	<li>purge contains [phrase] [amount] - deletes an <i>amount</i> of messages containing the <i>phrase</i> in the channel <br>
	Aliases: "contents"</li>
	<li>purge embed [amount] - deletes an <i>amount</i> of messages containing embeds <br>
	Aliases: "embeds"</li>
	<li>purge beginswith [phrase] [amount] - deletes an <i>amount</i> of messages starting with the <i>phrase</i> in the channel <br>
	Aliases: "startswith", "prefix"</li>
	<li>purge endswith [phrase] [amount] - deletes an <i>amount</i> of messages ending with the <i>phrase</i> in the channel <br>
	Aliases: "finisheswith", "suffix"</li>
	<li>purge notcontains [phrase] [amount] - deletes an <i>amount</i> of messages not containing the <i>phrase</i> in the channel <br>
	Aliases: "not", "doesn't contain", "nocontains"</li>
	<li>purge mentions [user] [amount] - deletes an <i>amount</i> of messages mentioning <i>user</i> in the channel <br>
	Aliases: "mentionsuser", "mentionsmember"</li>
	<hr>
	<p class="warning">Warning: Not functional</p>
	<li>mute [user] [time] - mutes a user <br> 
	Aliases: "muteuser", "mute-user"</li>
</ul>
<h3>Utility commands</h3>
<ul>
	<li>info - provides information about the bot</li>
	<li>uptime - shows how long the bot has been online (the restart command doesn't affect this)</li>
</ul>
<h3>Settings commands</h3>
<ul>
	<li>settings - shows where to find staff role/mod role help</li>
	<li>settings staff-role [role] - shows which commands can change the staffroles.<br>
	Aliases: "staff-role", "staff-roles", "staffroles"<li>
	<li>settings staff-roles set [role] - changes the staff-role and removes all previous staff-roles. <br>
	Aliases: "set", "set-role", "set-roles", "setroles"</li>
	<li>settings staff-roles add [role] - cdds a staff-role, does not remove any roles.
	Aliases: "add", "add-role", "addroles", "add-roles"</li>
	<li>settings staff-role delete [role] - cemoves a staff role.<br>
	Aliases: "del-role", "del", "remove", "delroles", "del-roles"</li>
	<li>settings staff-role list - lists the staffroles. <br>
	Aliases: "staff-role", "staff-roles", "staffrole"</li>
	<hr>
	<li>settings mod-role [role] - shows which commands can change the modroles.<br>
	Aliases: "mod-role", "mod-roles", "modroles"<li>
	<li>settings mod-roles set [role] - changes the mod-role and removes all previous mod-roles. <br>
	Aliases: "set", "set-role", "set-roles", "setroles"</li>
	<li>settings mod-roles add [role] - cdds a mod-role, does not remove any roles.
	Aliases: "add", "add-role", "addroles", "add-roles"</li>
	<li>settings mod-role delete [role] - cemoves a mod role.<br>
	Aliases: "del-role", "del", "remove", "delroles", "del-roles"</li>
	<li>settings mod-role list - lists the modroles. <br>
	Aliases: "mod-role", "mod-roles", "modrole"</li>
	<hr>
	<li>settings mute-role [role] - sets the role which will be added to a user when they are muted<br>
	Aliases: "muterole"</li>
</ul>
	
