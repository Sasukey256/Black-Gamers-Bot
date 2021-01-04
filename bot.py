import discord
from discord.ext import commands
from random import choice, randint
from time import sleep
import sqlite3 as sqlite

yesnolist = ['Ja', 'Nein', 'Vielleicht', 'Wahrscheinlich', 'Wahrscheinlich nicht']
ssplist = ['Schere', 'Stein', 'Papier']

client = commands.Bot(command_prefix='.')
client.remove_command('help')

# Database Setup

sql = """
    CREATE TABLE IF NOT EXISTS warnsystem (
        user text NOT NULL,
        reason text NOT NULL
    )
"""

conn = sqlite.connect("database.db")
curs = conn.cursor()

curs.execute(sql)
conn.commit()

# Events

@client.event
async def on_ready():
    print('Bot wurde erfolgreich gestartet.')

# Commands

@client.command()
async def help(ctx, page=1):
    if page == 1:
        embedVar = discord.Embed(title="Befehlsliste 1 ~ BlackGamers", description="Hier findest du Befehle dieses Bots", color=0x2c3e50)
        embedVar.add_field(name="`.help`", value="Zeig eine Liste an Befehlen dieses Bots an", inline=True)
        embedVar.add_field(name="`.8ball [Frage]`", value="Frage den Bot eine Ja/Nein Frage und er antwortet", inline=True)
        embedVar.add_field(name="`.clear [Anzahl]`", value="Lösche eine Anzahl an Nachrichten (Team)", inline=True)
        embedVar.add_field(name="`.kick @user [Grund]`", value="Kicke ein Mitglied vom Server (für immer)", inline=True)
        embedVar.add_field(name="`.ban @user [Grund]`", value="Banne ein Mitglied vom Server (für immer) (Team)", inline=True)
        embedVar.add_field(name="`.mute @user [Grund]`", value="Mute ein Mitglied auf dem Server (für immer) (Team)", inline=True)
        embedVar.add_field(name="`.announce [Text]`", value="Schicke einen Text als Embed durch den Bot (Team)", inline=True)
        embedVar.add_field(name="`.links`", value="Siehe unsere Social Media Links an", inline=True)
        embedVar.add_field(name="`.quellcode`", value="Lies den Quellcode dieses Bots nach", inline=True)
        await ctx.send(embed=embedVar)
    elif page == 2:
        embedVar = discord.Embed(title='Befehlsliste 2 ~ BlackGamers', description='Hier findest du Befehle dieses Bots', color=0x2c3e50)
        embedVar.add_field(name='`.serverinfo`', value='Lass dir eine Info über den Server anzeigen', inline=True)
        embedVar.add_field(name='`.serverinfo @user`', value='Lass dir eine Info über ein Mitglied anzeigen', inline=True)
        embedVar.add_field(name='`.avatar @user`', value='Lass dir das Profilbild eines Mitglied anzeigen', inline=True)
        embedVar.add_field(name='`.nick [Name]`', value='Gib einem Mitglied einen neuen Nickname (Team)', inline=True)
        embedVar.add_field(name='`.ssp [Schere/Stein/Papier]`', value='Spiele Schere, Stein, Papier mit dem Bot', inline=True)
        embedVar.add_field(name='`.dm @user [Nachricht]`', value='Schicke einem Mitglied eine Privatnachricht (Team)', inline=True)
        embedVar.add_field(name='`.ping`', value='Lass dir den Ping des Bots in einem Embed anzeigen', inline=True)
        embedVar.add_field(name='`.warn @user [Grund]`', value='Verwarne ein Mitglied (Team)', inline=True)
        embedVar.add_field(name='`.checkwarns @user`', value='Siehe dir die Warns eines Mitgliedes an (Team)', inline=True)
        await ctx.send(embed=embedVar)
    else:
        embedVar = discord.Embed(title='Fehler: Befehlsliste', description='Schreibe entweder `1` oder `2` hinter den Helf Befehl')
        await ctx.send(embed=embedVar)

@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    await ctx.send(choice(yesnolist))

@client.command(aliases=['purge', 'deletebulk'])
async def clear(ctx, amount=0):
    if amount != 0:
        await ctx.channel.purge(limit=amount)
    else:
        embedVar = discord.Embed(title='Fehler: Clear', description='Bitte gib eine Anzahl an Nachrichten an, die gelöscht werden sollen.', color=0xe74c3c)
        await ctx.send(embed=embedVar)

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    embedVar = discord.Embed(title='Ban Befehl', description='Das Mitglied {0} wurde wegen {1} gekickt'.format(member, reason), color=0xe74c3c)
    await ctx.send(embed=embedVar)

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    embedVar = discord.Embed(title='Ban Befehl', description='Das Mitglied {0} wurde wegen {1} gebannt'.format(member, reason), color=0xe74c3c)
    await ctx.send(embed=embedVar)

@client.command()
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name='Muted')

    if not mutedRole:
        mutedRole = await guild.create_role(name='Muted')

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)

    await member.add_roles(mutedRole, reason=reason)
    embedVar = discord.Embed(title='Mute Befehl', description='Das Mitglied {0} wurde wegen {1} gemutet'.format(member, reason), color=0xe74c3c)
    await ctx.send(embed=embedVar)

@client.command()
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member : discord.Member):
    mutedRole = discord.utils.get(ctx.guild.roles, name='Muted')

    await member.remove_roles(mutedRole)
    embedVar = discord.Embed(title='Unmute Befehl', description='{0} wurde entmutet'.format(member), color=0xe74c3c)
    await ctx.send(embed=embedVar)

@client.command(aliases=['send'])
@commands.has_permissions(manage_messages=True)
async def announce(ctx, *, message=None):
    if message != None:
        await ctx.channel.purge(limit=1)
        embedVar = discord.Embed(title='Annoucement Befehl', description='{}'.format(message), color=0xe74c3c)
        await ctx.send(embed=embedVar)
    else:
        await ctx.channel.purge(limit=1)
        embedVar = discord.Embed(title='Fehler: Annoucement', description='Bitte schreibe einen Text, wenn du diesen Befehl benutzt', color=0xe74c3c)
        await ctx.send(embed=embedVar)

@client.command()
async def links(ctx):
    embedVar = discord.Embed(title='Liste wichtiger Links', description='Hier findest du alle wichtigen Links', color=0xe74c3c)
    embedVar.add_field(name='Website', value='[Klicke Hier](https://blackgamers.tk)', inline=True)
    embedVar.add_field(name='Discord', value='[Klicke Hier](https://discord.gg/VC9ftrdTqg)', inline=True)
    embedVar.add_field(name='GitHub (Programmierer)', value='[Klicke Hier](https://www.github.com/Sasukey256/)', inline=True)
    await ctx.send(embed=embedVar)

@client.command(aliases=['sourcecode', 'code'])
async def quellcode(ctx):
    embedVar = discord.Embed(title='Quellcode dieses Bots', description='[https://github.com/Sasukey256/Black-Gamers-Bot/upload)', color=0xe74c3c)
    await ctx.send(embed=embedVar)

@client.command()
async def serverinfo(ctx):
    name = str(ctx.guild.name)
    id = str(ctx.guild.id)
    region = str(ctx.guild.region)
    memberCount = str(ctx.guild.member_count)
    icon = str(ctx.guild.icon_url)
   
    embedVar = discord.Embed(title="Server Information", description="Hier findest du eine Serverinfo", color=0xe74c3c)
    embedVar.set_thumbnail(url=icon)
    embedVar.add_field(name="Server ID", value=id, inline=True)
    embedVar.add_field(name="Region", value=region, inline=True)
    embedVar.add_field(name="Mitgliederanzahl", value=memberCount, inline=True)

    await ctx.send(embed=embedVar)

@client.command()
async def userinfo(ctx, member : discord.Member):
    avatar_url = member.avatar_url
    username = member
    id = member.id
    roles = [role for role in member.roles]

    embedVar = discord.Embed(title="Userinfo Befehl", description="Hier ist eine Information über das erwähnte Mitglied", color=0xe74c3c)
    embedVar.set_thumbnail(url=avatar_url)
    embedVar.add_field(name="Name", value=str(username), inline=True)
    embedVar.add_field(name="ID", value=str(id), inline=True)
    embedVar.add_field(name="Top Rolle", value=str(member.top_role.mention), inline=True)
    embedVar.add_field(name=f"Rollen ({len(roles)})", value=', '.join([role.mention for role in roles]), inline=True)

    await ctx.send(embed=embedVar)

@client.command()
async def avatar(ctx, member : discord.Member):
    avatar_url = member.avatar_url
    embedVar = discord.Embed(title="{}'s Avatar".format(member), color=0xbe2edd)
    embedVar.set_image(url=avatar_url)
    await ctx.send(embed=embedVar)
    
@client.command()
async def ssp(ctx, *, wahl):
    wahl_bot = choice(ssplist)
    if wahl == "Schere" or wahl == "Stein" or wahl == "Papier":
        await ctx.send(wahl_bot)
    else:
        await ctx.send("Bitte schreibe `Schere`, `Stein` oder `Papier` um zu spielen")

@client.command(aliases=['pn','pm', 'private'])
@commands.has_permissions(manage_messages=True)
async def dm(ctx, member : discord.Member, *, text):
    embedVar1 = discord.Embed(title="Dm Befehl", description=f"Die Nachricht wurde erfolgreich an {member} gesendet.", color=0xbe2edd)
    embedVar2 = discord.Embed(title="Nachricht vom Server **🖤BlackGamers🖤**", description=text, color=0xbe2edd)
    
    await member.send(embed=embedVar2)
    await ctx.send(embed=embedVar1)

@client.command(aliases=['changenick'])
@commands.has_permissions(manage_nicknames=True)
async def nick(ctx, member : discord.Member, *, nick):
    await member.edit(nick=nick)
    embedVar = discord.Embed(title="Nick Befehl", description=f"Der Nickname von {member} wurde zu {nick} geändert", color=0xbe2edd)
    
    await ctx.send(embed=embedVar)

@client.command(aliases=['latency'])
async def ping(ctx):
    await ctx.send(f"Mein Ping ist **{round(client.latency * 1000)}ms**")

@client.command()
@commands.has_permissions(kick_members=True)
async def warn(ctx, member : discord.Member, *, reason):

    user = str(member.id)

    sql = "INSERT INTO warnsystem VALUES ('{0}', '{1}')".format(user, reason)
    curs.execute(sql)
    conn.commit()

    embedBuild = discord.Embed(
        title = "Warn Befehl",
        description = f"Das Mitglied {member} wurde wegen {reason} verwarnt",
        color = 0xe74c3c
    )

    await ctx.send(embed=embedBuild)

    embedBuild = discord.Embed (
        title = "Verwarnung auf **🖤BlackGamers🖤**",
        description = f"Du wurdest auf **🖤BlackGamers🖤** wegen `{reason}` verwarnt",
        color=0xe74c3c
    )

    await member.send(embed=embedBuild)

@client.command(aliases=['seewarns', 'warns', 'infractions'])
@commands.has_permissions(kick_members=True)
async def checkwarns(ctx, member : discord.Member):

    user = member.id

    sql = f"SELECT * FROM warnsystem where user={user}"
    curs.execute(sql)
    
    warns = curs.fetchall()
    warns2 = []

    for i in warns:
        for j in i:
            warns2.append(j)

    while warns2.count(f"{user}"):
        warns2.remove(f"{user}")

    reasons = ", ".join(warns2)

    embedBuild = discord.Embed(
        title = "Checkwarns Befehl",
        description = f"Warns von **{member}** ({len(warns2)}): {reasons}",
        color = 0xe74c3c
    )

    await ctx.send(embed=embedBuild)

client.run('Enter Token here')
