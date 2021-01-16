import discord
from discord.ext import commands, tasks
import os
import json
import math
import random
from embed import assembleEmbed
import math
import datetime
from datetime import date
import asyncio
import re

intents = discord.Intents.default()
intents.members = True 
client = commands.Bot(command_prefix='.', case_insensitive=True, intents=intents)

@client.event
async def on_ready():
  print("bunnie bot online")
  changeBotStatus.start()

@client.event
async def on_message(message):
  if message.author.bot:
    return
  else:
    with open("afk.json","r") as f:
      data = json.load(f)
    mentions = [str(user.id) for user in message.mentions]
    for key in data.keys():
      if key in mentions:
        user = client.get_user(key)
        embed = discord.Embed(
          description = f"<@!{key}> is AFK: {data[key][0]}",
          color = 0x2f3136
        )
        await message.channel.send(embed=embed)
        break
        return
      elif str(message.author.id) == key:
        data.pop(key)
        with open("afk.json","w") as f:
          json.dump(data, f)
        embed = discord.Embed(
          description = f"<@!{key}> is no longer AFK.",
          color = 0x2f3136
        )
        await message.channel.send(embed=embed, delete_after=3)
        break
        return
  if message.content == f"<@!{client.user.id}>":
    channel = message.channel
    await channel.send(f'My prefix is `.`')
  if 'welcome' in message.content.lower():
    await message.channel.send('welcome to bunnie! <a:sbunbundraw:775877819238580225>')
  if 'goodnight' in message.content.lower():
    await message.channel.send('sleep well <a:sbunbunsleep:725853912426610688>')
  if message.content == 'hi':
    if 'hi' in message.content.lower():
      await message.channel.send('hihi <a:sbunbunstare:756938352690987018>')
  await client.process_commands(message)


time_regex = re.compile(r"(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {"h": 3600, "s": 1, "m": 60, "d": 86400}

def convert(argument):
    args = argument.lower()
    matches = re.findall(time_regex, args)
    time = 0
    for key, value in matches:
        try:
            time += time_dict[value] * float(key)
        except KeyError:
            raise commands.BadArgument(
                f"{value} is an invalid time key! s|m|h|d are valid arguments"
            )
        except ValueError:
            raise commands.BadArgument(f"{key} is not a number!")
    return round(time)

@client.command()
@commands.guild_only()
@commands.has_role(799797776133259345)
async def mute(ctx, member: discord.Member, time=None): 
  if time == None:
    role_to_add = ctx.guild.get_role(783204673594458132)
    await member.add_roles(role_to_add)
  else:
    duration = convert(time)
    role_to_add = ctx.guild.get_role(783204673594458132)
    await member.add_roles(role)
    embed = discord.Embed(
      description = f'<:zpinkyes:746751022315208884> {member.mention} has been muted!',
      color = 0x2f3136)
    await ctx.send(embed=embed)
    await asyncio.sleep(duration)

@client.command()
@commands.guild_only()
async def afk(ctx,* ,reason="a mysterious reason"):
  embed = discord.Embed(
    description = f"`{ctx.author}` is now AFK.",
    color = 0x2f3136
  )
  await ctx.send(embed=embed)
  with open("afk.json","r") as f:
      data = json.load(f)
  data[str(ctx.author.id)] = []
  data[str(ctx.author.id)].append(reason)
  with open("afk.json","w") as f:
      json.dump(data, f)

@client.command()
@commands.guild_only()
@commands.has_role(799797776133259345)
async def pm(ctx, member: discord.Member):
  role_to_add = ctx.guild.get_role(705463198811422750)
  if role_to_add in member.roles:
    await member.add_roles(role_to_add)
    await ctx.send(f'{member} has been pmed!')
    embed = discord.Embed(
      description = f'<:zpinkyes:746751022315208884> {member.mention} has been made a pm!!',
      color = 0x2f3136)
    await ctx.send(embed=embed)
  else:
    await member.remove_role(role_to_add)
    embed = discord.Embed(
      description = f'<:zpinkyes:746751022315208884>{member.mention} un-pmed!',
      color = 0x2f3136)
    await ctx.send(embed=embed)

@client.command()
@commands.guild_only()
@commands.has_role(799797776133259345)
async def role(ctx, member: discord.Member, role: discord.Role):
  if role in member.roles:
    await member.remove_roles(role)
    embed = discord.Embed(
      description = f'<:zpinkyes:746751022315208884> {role} has been removed from {member.mention}!',
      color = 0x2f3136)
    await ctx.send(embed=embed)
  else:
    await member.add_roles(role)
    embed = discord.Embed(
      description = f'<:zpinkyes:746751022315208884> {role} has been added to {member.mention}!',
      color = 0x2f3136)
    await ctx.send(embed=embed)

@client.command()
@commands.guild_only()
async def suggest(ctx, *, suggestion):
  author = ctx.message.author
  today = date.today()
  d1 = today.strftime("%m/%d/%Y")
  embed = discord.Embed(
    title='Server Suggestion:',
    description=suggestion,
    colour=0x2f3136)
  embed.set_footer(text="ID: " + str(ctx.author.id) + " • " + str(d1))
  channel = client.get_channel(727674621666525197)
  msg = await channel.send(embed=embed)
  await msg.add_reaction('✅')
  await msg.add_reaction('❌')
  embed.set_author(name=str(author),icon_url=ctx.author.avatar_url)
  embed = discord.Embed(
    description = f'<:zpinkyes:746751022315208884> suggestion submitted!',
    color = 0x2f3136)
  await ctx.send(embed=embed)


@client.command()
@commands.guild_only()
async def embed(ctx, *, embed):
  title, description = embed.split(" // ")
  embed = discord.Embed(
    title=f'{title}',
    description=f'{description}',
    color = 0x2f3136)
  await ctx.send(embed=embed)

@client.command()
@commands.guild_only()
async def iembed(ctx, url):
  embed = discord.Embed(color = 0x2f3136)
  embed.set_image(url=f'{url}')
  await ctx.send(embed=embed)

@client.command()
@commands.guild_only()
async def say(ctx,*,input):
  embed = discord.Embed(
    description = input,
    color = 0x2f3136
  )
  await ctx.send(embed=embed)

@tasks.loop(hours=0.25)
async def changeBotStatus():
  guild = client.get_guild(705463198756634704)
  member_count = len([m for m in guild.members if not m.bot])
  statuses = [
    {"type": "watching", "message": "over discord.gg/flower"},
    {"type": "playing", "message": "destiny with matt"},
    {"type": "watching", "message": f"{member_count} softies"}
  ]
  botStatus = statuses[math.floor(random.random() * len(statuses))]
  if botStatus["type"] == "playing":
    await client.change_presence(activity=discord.Game(name=botStatus["message"]))
  elif botStatus["type"] == "watching":
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=botStatus["message"]))
  print("bot status changed to message")

@client.event
async def on_member_join(member):
  channel = client.get_channel(740015490851799040)
  embed = discord.Embed(
    title = 'welcome to bunnie!',
    description = '・<#705463199129927751>\n・<#705463199129927753>\n・<#705463199129927754>\n・<#728245554638749766>',
    color = 0x2f3136)
  embed.set_footer(text='wear ur mask + wash ur hands', icon_url='https://cdn.discordapp.com/emojis/781322093752483850.png?v=1')
  embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/763645027938598912.gif?v=1')
  await channel.send(f'{member.mention} <@&705463198790451274>', embed=embed)
  try:
    await member.send('''♡ᵎ・floral network
・thank you for joining (user)! don't forget to check out the servers below
https://discord.gg/2RRWDwgPHy
https://discord.gg/uEZHdEehAj''')
  except: 
    print('dm msg failed')

@client.command()   
@commands.guild_only()
@commands.has_role(799797776133259345)
async def ban(ctx, member : discord.Member, *, reason = None):
  await member.ban(reason=reason)
  await ctx.message.delete()
  embed = discord.Embed(
    description = f'<:zpinkyes:746751022315208884> {member.mention} has been banned!',
    color = 0x2f3136)
  await ctx.send(embed=embed)

@client.command()   
@commands.guild_only()
@commands.has_role(799797776133259345)
async def kick(ctx, member : discord.Member, *, reason = None):
  await member.kick(reason=reason)
  embed = discord.Embed(
    description = f'<:zpinkyes:746751022315208884>{member.mention} has been kicked!',
    color = 0x2f3136)
  await ctx.send(embed=embed)

@client.command()
@commands.guild_only()
async def cembed(ctx, *, jsonInput):
    """Helps to create an embed to be sent to a channel."""
    jso = json.loads(jsonInput)
    title = jso['title'] if 'title' in jso else ""
    desc = jso['description'] if 'description' in jso else ""
    titleUrl = jso['titleUrl'] if 'titleUrl' in jso else ""
    hexcolor = jso['hexColor'] if 'hexColor' in jso else "#C7B1A3"
    webcolor = jso['webColor'] if 'webColor' in jso else ""
    thumbnailUrl = jso['thumbnailUrl'] if 'thumbnailUrl' in jso else ""
    authorName = jso['authorName'] if 'authorName' in jso else ""
    authorUrl = jso['authorUrl'] if 'authorUrl' in jso else ""
    authorIcon = jso['authorIcon'] if 'authorIcon' in jso else ""
    if 'author' in jso:
        authorName = ctx.message.author.name
        authorIcon = ctx.message.author.avatar_url_as(format="jpg")
    fields = jso['fields'] if 'fields' in jso else ""
    footerText = jso['footerText'] if 'footerText' in jso else ""
    footerUrl = jso['footerUrl'] if 'footerUrl' in jso else ""
    imageUrl = jso['imageUrl'] if 'imageUrl' in jso else ""
    
    embed = assembleEmbed(
        title=title,
        desc=desc,
        titleUrl=titleUrl,
        hexcolor=hexcolor,
        webcolor=webcolor,
        thumbnailUrl=thumbnailUrl,
        authorName=authorName,
        authorUrl=authorUrl,
        authorIcon=authorIcon,
        fields=fields,
        footerText=footerText,
        footerUrl=footerUrl,
        imageUrl=imageUrl
    )
    await ctx.send(embed=embed)

@client.event
async def on_command_error(ctx, error):
  if isinstance(error, discord.ext.commands.UnexpectedQuoteError) or isinstance(error, discord.ext.commands.InvalidEndOfQuotedStringError):
    embed = discord.Embed(
    description = f"<:zpinkno:746751048252784700> It appears that your quotation marks are misaligned, and I can't read your query.",
    color = 0x2f3136)
    return await ctx.send(embed=embed)
  if isinstance(error, discord.ext.commands.ExpectedClosingQuoteError):
    embed = discord.Embed(
    description = f"<:zpinkno:746751048252784700> I was expecting you were going to close out your command with a quote somewhere.",
    color = 0x2f3136)
    return await ctx.send(embed=embed)
  if isinstance(error, discord.ext.commands.CommandNotFound):
    return
  else:
    print("ERROR:")
    print(error)
    embed = discord.Embed(
    description = f'<:zpinkno:746751048252784700> {error}',
    color = 0x2f3136)
    await ctx.send(embed=embed)
    return

@client.command()
@commands.guild_only()
#@commands.has_role(799797776133259345)
async def close(ctx, reason = None):
  channel_id = ctx.channel.id
  def check(message):
    return message.author == ctx.author and message.channel == ctx.channel and message.content.lower() == "yes"
  try:
    with open('data.json') as f:
        data = json.load(f)
    if ctx.channel.id in data["ticket-channel-ids"]:
      await ctx.send('Are you sure you want to close this ticket? Reply with `yes` if you are sure.')
      await client.wait_for('message', check=check, timeout=60)
      f = open(f"{ctx.channel.name}.txt", 'w')
      messages = await ctx.channel.history().flatten()
      data = list(map(lambda m: str(m.author) + ": " + m.content, messages))
      f.write("\n".join(data))
      f.close()
      await ctx.channel.delete()
      channel = client.get_channel(734724557965099069)
      await channel.send(file = discord.File(f'{ctx.channel.name}.txt'))
      os.remove(f'{ctx.channel.name}.txt')
      embed = discord.Embed(
        title = 'Ticket Closed',
        description = f'**Closed by: ** {ctx.author} \n **Name:** {ctx.channel.name} \n **Channel ID: ** {ctx.channel.id}',
        color = 0x2c2f33)
      await channel.send(embed=embed)
      index = data["ticket-channel-ids"].index(channel_id)
      del data["ticket-channel-ids"][index]
      with open('data.json', 'w') as f:
        json.dump(data, f)
    else:
      embed = discord.Embed(
      description = f'<:zpinkno:746751048252784700> Please pick a ticket channel to close!',
      color = 0x2f3136)
      await ctx.send(embed=embed)
  except asyncio.TimeoutError:
    embed = discord.Embed(
    description = f'<:zpinkno:746751048252784700> You have run out of time to close this ticket.',
    color = 0x2f3136)
    await ctx.send(embed=embed)
client.remove_command('help')

@client.command()
@commands.guild_only()
async def help(ctx):
  embed = discord.Embed(
    title = "<a:zpinknotepad:730651604050772019> bunnie's help panel",
    description = '''__**<:bunnieheartdontsteal:781322093752483850> basics**__ \n`・afk`\n`・say`\n`・suggest`\n`・role`\n`・ping`\n \n__**<:bunnieheartdontsteal:781322093752483850> utilities**__\n`・ban`\n`・kick`\n`・mute`\n`・unmute`\n`・pm`\n \n __**<:bunnieheartdontsteal:781322093752483850> other**__\n`・edit`\n`・close`\n`・embed`\n`・iembed`\n`・cembed`\n''',
    color = 0x2f3136)  
  await ctx.send(embed=embed)

@client.command()
@commands.guild_only()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

@client.command()
@commands.has_role(799797776133259345)
async def edit(ctx, *, msg):
  await ctx.message.delete()
  with open('data.json') as f:
    data = json.load(f)
  if ctx.channel.id in data["ticket-channel-ids"]:
    channel = ctx.channel
    await channel.edit(name=f'{msg}')
    embed = discord.Embed(
    description = f'<:zpinkyes:746751022315208884> Edited to {msg}',
    color = 0x2f3136)
    await ctx.send(embed=embed)
  else:
    embed = discord.Embed(
    description = f'<:zpinkno:746751048252784700> Edit a ticket channel dummy.',
    color = 0x2f3136)

@client.event
async def on_raw_reaction_add(payload):
  guild = discord.utils.get(client.guilds, id=payload.guild_id)
  member = guild.get_member(payload.user_id)
  if payload.message_id == 799135110674382848 and payload.emoji.id == 799133549214433280:
    category = discord.utils.get(guild.categories, id=705463198849171556)
    ticketchannel = await guild.create_text_channel(name=f'ticket {member.name}', category=category)
    await ticketchannel.set_permissions(payload.member, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)
    g = discord.utils.get(guild.roles, name='softies')
    await ticketchannel.set_permissions(g, send_messages=False, read_messages=False, read_message_history=False)
    embed = discord.Embed(
      title = 'help',
      description = f'''thank you for creating a ticket! staff will be with you shortly
<:zzillegal:733335340701450240>・if you are reporting a server, member, dm advertiser, etc. please provide an explanation, proof, and id(s)''',
      color = 0x2c2f33)
    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/705463200388481079/799122322068996096/746559229871259668_50.gif')
    await ticketchannel.send(member.mention ,embed=embed)
    with open("data.json") as f:
        data = json.load(f)
    data["ticket-channel-ids"].append(ticketchannel.id)
    with open("data.json", 'w') as f:
        json.dump(data, f)


@client.command()
@commands.has_role(799797776133259345)
async def unmute(ctx, member: discord.Member):
  role = ctx.guild.get_role(783204673594458132)
  embed = discord.Embed(
    description = f'<:zpinkyes:746751022315208884> {member.mention} has been muted!',
    color = 0x2f3136)
  await ctx.send(embed=embed)
  await member.remove_roles(role)

client.run(cofig.token)
