# bot.py
from logging import StrFormatStyle
import os
import random

import discord
from discord import permissions
from discord.client import Client
from dotenv import load_dotenv
from discord.ext import commands
import requests
from requests import get
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import datetime
from discord import FFmpegPCMAudio
from discord.utils import get
from discord import TextChannel
from googletrans import Translator, constants
import json
from textblob import TextBlob
import urllib
from youtube_dl import YoutubeDL
from pycoingecko import CoinGeckoAPI
import time
import discordhex


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
cg = CoinGeckoAPI()

def get(element:str):
  path = os.path.abspath("./conf.json")
  with open(path, "r") as read_file:
    content = json.load(read_file)
  return content[element]
  
intents = discord.Intents.all()
client = discord.Client(intents=intents)
permissions = discord.Permissions.all()
bot = commands.Bot(command_prefix='?', intents=intents, help_command=None, allowed_mentions=discord.AllowedMentions(everyone=False, users=True, roles=False), permissions=permissions)
time = datetime.datetime.utcnow()
# set permissions

# flag = True

# @bot.event 
# async def on_message(message):
#     if(message.content.startswith('?')):
#         if(message.content == '?'):
#             return
#         if(message.content == '?eth'):
#             price = get_token_price('ethereum')
#             await message.channel.send('ETH: Rp.' + str(price))
#         elif(message.content == '?btc'):
#             price = get_token_price('bitcoin')
#             await message.channel.send('BTC: Rp.' + str(price))
#         elif(message.content == '?doge'):
#             price = get_token_price('bitcoin')
#             await message.channel.send('DOGE: Rp.' + str(price))

#         else:
#             token_name = message.content.replace('$', '')
#             try:
#                 price = get_token_price(token_name)
#                 await message.channel.send(token_name.upper() + ': $' + str(price))

#             except Exception as e:
#                 print('Error: ', end =''), print(e)
#                 await message.channel.send('Unable to fetch price, please use full token name!')

#     if(message.content.startswith('?')):
#         global task
#         global flag
        
#     if(message.content == '?'):
#         return

#     if(message.content == '?reset'):
#         await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='all the coins'))
#         await message.channel.send('Resetting the monitor!')
#         tasks.cancel()
#         flag = True

#     else:
#         token_name = message.content.replace('?', '')
#         try:
#             if(flag):
#                 price = cg.get_price(ids=token_name.lower(), vs_currencies='idr')[token_name.lower()]['idr']
#                 task =  asyncio.Task(monitor(token_name))
#                 await message.channel.send('Now monitoring ' + token_name)
#                 flag = False
#             else:
#                 await message.channel.send('Error: cannot monitor two coins at once. ?reset first!')
        
#         except Exception as e:
#             print('Error: ', end =''), print(e)
#             await message.channel.send('Unable to monitor... please use full token name!')

# def get_token_price(id):
#     id = id.lower()
#     t = time.localtime()
#     logging_time = time.strftime('%I:%M:%S %p', t)
#     price = cg.get_price(ids=id, vs_currencies='idr')[id]['idr']
#     print('[' + logging_time + ']: ' + str(id) + ': Rp.' + str(price))
#     return price
    
# async def monitor(token_name):
#     while (True):
#         t = time.localtime()
#         logging_time = time.strftime('%I:%M:%S %p', t)

#         price = cg.get_price(ids=token_name.lower(), vs_currencies='idr')[token_name.lower()]['idr']
#         print('[' + logging_time + ']: ', end= '')
#         print('Monitoring ', end='')
#         print(token_name + ': $' + str(price))
#         await changeWatching(price)
#         await asyncio.sleep(10)

# async def changeWatching(price):
#     await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='$' + str(price)))

@bot.event
async def on_ready():
    print(f'{bot.user.name} dh login')

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, Welcome aboard!'
    )

# check song from spotify
@bot.command(name='check', help='Check song from spotify')
async def check_song(ctx, song_name: str):
    url = 'https://api.spotify.com/v1/search?q=' + song_name + '&type=track'
    response = requests.get(url, headers={"Authorization": "Bearer " + get('SPOTIFY_TOKEN')})
    data = response.json()
    try:
        title = data['tracks']['items'][0]['name']
        artist = data['tracks']['items'][0]['artists'][0]['name']
        album = data['tracks']['items'][0]['album']['name']
        preview_url = data['tracks']['items'][0]['preview_url']
        await ctx.send(f'Title: {title}\nArtist: {artist}\nAlbum: {album}\nPreview: {preview_url}')
    except Exception as e:
        print(e)
        await ctx.send('Song not found!')

#info bot   
@bot.command(name='infobot', help='Show bot info')
async def info(ctx):
    embed = discord.Embed(title='Info', color=discord.Color.dark_blue())
    embed.add_field(name='Bot name', value=bot.user.name, inline=False)
    embed.add_field(name='Bot ID', value=bot.user.id, inline=False)
    embed.add_field(name='Bot prefix', value='?', inline=False)
    #created at
    embed.add_field(name='Created at', value=bot.user.created_at.strftime("%d/%m/%Y"), inline=False)
    embed.set_thumbnail(url=bot.user.avatar_url)
    # footer made by @Tartaglia with url
    await ctx.send(embed=embed)




@bot.command(name='rickroll', help='Rickrolls the user')
async def rickroll(ctx):
    embed=discord.Embed(title="Get Rickrolled, lmao!", url="", description="**That's the Handsome Rick Astley**", color=0x966908)
    embed.set_image(url="https://c.tenor.com/u9XnPveDa9AAAAAM/rick-rickroll.gif")
    await ctx.reply(embed=embed) 

# cry command
@bot.command(name='cry', help='Sends a crying emoji')
async def cry(ctx):
    embed=discord.Embed(title="Meme Flip :", url="", description="You made me cry, you dumb", color=0xd69a00)
    embed.set_thumbnail(url="https://c.tenor.com/vM2hP3AsiP8AAAAM/%E0%A4%87%E0%A4%AE%E0%A5%8B%E0%A4%9C%E0%A5%80-%E0%A4%B0%E0%A5%8B%E0%A4%A8%E0%A4%BE.gif")
    await ctx.reply(embed=embed)
    
# Info Server command
@bot.command(name='info', help='Shows the server info')
async def info(ctx):
    embed=discord.Embed(title="Server Info", url="", description="Here is the server info", color=0xd69a00)
    embed.add_field(name="Server Name", value=ctx.guild.name, inline=False)
    embed.add_field(name="Server ID", value=ctx.guild.id, inline=False)
    embed.add_field(name="Server Owner", value=ctx.guild.owner, inline=False)
    embed.add_field(name="Server Region", value=ctx.guild.region, inline=False)
    # created_at dd/mm/yyyy
    embed.add_field(name="Server Created", value=ctx.guild.created_at.strftime("%d/%m/%Y"), inline=False)
    embed.add_field(name="Server Member Count", value=ctx.guild.member_count, inline=False)
    embed.add_field(name="Server Role Count", value=len(ctx.guild.roles), inline=False)
    embed.add_field(name="Server Emote Count", value=len(ctx.guild.emojis), inline=False)
    # get avatar server
    embed.set_thumbnail(url=ctx.guild.icon_url)
    await ctx.send(embed=embed)

# Info User with avatar command
@bot.command(name='userinfo', help='Gives info about the user')
async def userinfo(ctx, member: discord.Member):
    embed=discord.Embed(title="User Info", url="", color=0xd69a00)
    embed.add_field(name="Name", value=member.name, inline=False)
    embed.add_field(name="ID", value=member.id, inline=False)
    embed.add_field(name="Nickname", value=member.nick, inline=False)
    roles = [role for role in member.roles[1:]]
    embed.add_field(name=f'Roles ({len(roles)}):', value="".join([role.mention + "|" for role in roles]), inline=False)
    embed.add_field(name="Created At", value=member.created_at.strftime("%d/%m/%Y"), inline=False)
    embed.add_field(name="Joined At", value=member.joined_at.strftime("%d/%m/%Y"), inline=False)
    #status
    if member.status == discord.Status.online:
        embed.add_field(name="Status", value="Online", inline=False)
    elif member.status == discord.Status.offline:
        embed.add_field(name="Status", value="Offline", inline=False)
    elif member.status == discord.Status.idle:
        embed.add_field(name="Status", value="Idle", inline=False)
    elif member.status == discord.Status.dnd:
        embed.add_field(name="Status", value="Do Not Disturb", inline=False)
    #game
    if member.activity:
        if member.activity.type == discord.ActivityType.playing:
            embed.add_field(name="Playing", value=member.activity.name, inline=False)
        elif member.activity.type == discord.ActivityType.streaming:
            embed.add_field(name="Streaming", value=member.activity.name, inline=False)
        elif member.activity.type == discord.ActivityType.listening:
            embed.add_field(name="Listening", value=member.activity.name, inline=False)
        elif member.activity.type == discord.ActivityType.watching:
            embed.add_field(name="Watching", value=member.activity.name, inline=False)
    else:
        embed.add_field(name="Playing", value="None", inline=False)
    # Status Premium
    if member.premium_since:
        embed.add_field(name="Premium since", value=member.premium_since, inline=False)
    else:
        embed.add_field(name="Premium since", value="None", inline=False)
    
    embed.set_thumbnail(url=member.avatar_url)
    await ctx.reply(embed=embed)

# covid-19 in indonesiacommand
@bot.command(name='covid', help='Gives info about covid-19 in indonesia')
async def covid(ctx):
    url = "https://api.kawalcorona.com/indonesia"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
    embed=discord.Embed(title="Covid-19 in Indonesia", url="", description="Here is the covid-19 in Indonesia", color=0xd69a00)
    embed.add_field(name="Positif", value=data[0]['positif'], inline=False)
    embed.add_field(name="Sembuh", value=data[0]['sembuh'], inline=False)
    embed.add_field(name="Meninggal", value=data[0]['meninggal'], inline=False)
    embed.add_field(name="Dirawat", value=data[0]['dirawat'], inline=False)
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/746165212586768586/746165212586768586.png")
    await ctx.reply(embed=embed)

# wikipedia https://id.wikipedia.org/api/rest_v1/page/summary/
@bot.command(name='wiki', help='Gives info about wikipedia')
async def wiki(ctx, *, search):
    url = "https://id.wikipedia.org/api/rest_v1/page/summary/{}".format(search)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
    if data['type'] == 'disambiguation':
        embed=discord.Embed(title="Wikipedia", url="", description="Here is the wikipedia", color=0xd69a00)
        embed.add_field(name="Disambiguation", value="Please choose one of the following", inline=False)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/746165212586768586/746165212586768586.png")
        await ctx.reply(embed=embed)
        for item in data['redirects']:
            embed=discord.Embed(title="Wikipedia", url="", description="Here is the wikipedia", color=0xd69a00)
            embed.add_field(name="Disambiguation", value=item['to'], inline=False)
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/746165212586768586/746165212586768586.png")
            await ctx.reply(embed=embed)
    else:
        embed=discord.Embed(title="Wikipedia", url="", description=data['title'], color=0xd69a00)
        embed.add_field(name="Deskripsi", value=data['extract'], inline=False)
        embed.set_image(url=data['originalimage']['source'])
        embed.add_field(name="URL", value=data['content_urls']['desktop']['page'], inline=False)
        # set footer by user
        embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)

#server icon command
@bot.command(name='servericon', help='Gives the server icon')
async def servericon(ctx):
    embed=discord.Embed(title="Server Icon", url="", color=0xd69a00)
    embed.set_image(url=ctx.guild.icon_url)
    await ctx.reply(embed=embed)

#avatar member command
@bot.command(name='avatar', help='Gives the avatar of the member')
async def avatar(ctx, member: discord.Member):
    embed=discord.Embed(title="Avatar", url="", color=0xd69a00)
    embed.set_image(url=member.avatar_url)
    await ctx.reply(embed=embed)

# purge message command
@bot.command(name='purge', delete_after=3)
@commands.has_permissions(manage_messages=True)
async def purge(ctx, limit=100, member: discord.Member=None):
    await ctx.message.delete()
    msg = []
    try:
        limit = int(limit)
    except:
        return await ctx.send("Please pass in an integer as limit")
    if not member:
        await ctx.channel.purge(limit=limit)
        return await ctx.send(f"Purged {limit} messages", delete_after=3)
    async for m in ctx.channel.history():
        if len(msg) == limit:
            break
        if m.author == member:
            msg.append(m)
    await ctx.channel.delete_messages(msg)
    await ctx.send(f"Purged {limit} messages of {member.mention}", delete_after=3)
    

# get list trending movie command
@bot.command(name='trending', help='Gives the list of trending movies')
async def trending(ctx):
    url = "https://api.themoviedb.org/3/trending/movie/week?api_key=b4f4d1c2f91c4d46cc9f8dfd603919ff"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
    embed=discord.Embed(title="Trending Movies", url="", description="Here is the list of trending movies", color=0xd69a00)
    for i in range(len(data['results'])):
        embed.add_field(name=f'{i+1} - {data["results"][i]["title"]}', value=f'Rating: {data["results"][i]["vote_average"]}', inline=False)
        #release date
        embed.add_field(name="Release Date", value=data["results"][i]["release_date"], inline=False)
    await ctx.reply(embed=embed)

# get movie info command
@bot.command(name='movie', help='Gives the info of the movie')
async def movie(ctx, *, movie: str):
    url = "https://api.themoviedb.org/3/search/movie?api_key=b4f4d1c2f91c4d46cc9f8dfd603919ff&language=en-US&query=" + movie + "&page=1&include_adult=false"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
    embed=discord.Embed(title="Movie Info", url="", color=0xd69a00)
    embed.add_field(name="Title", value=data['results'][0]['title'], inline=False)
    embed.add_field(name="Overview", value=data['results'][0]['overview'], inline=False)
    embed.add_field(name="Rating", value=data['results'][0]['vote_average'], inline=False)
    embed.add_field(name="Release Date", value=data['results'][0]['release_date'], inline=False)
    # thumbnail
    embed.set_thumbnail(url=f"https://image.tmdb.org/t/p/w500{data['results'][0]['poster_path']}")
    await ctx.reply(embed=embed)

# get random meme
@bot.command(name='meme', help='Gives a random meme')
async def meme(ctx):
    url = "https://meme-api.herokuapp.com/gimme"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
    embed=discord.Embed(title="Meme", url="", color=0xd69a00)
    embed.set_image(url=data['url'])
    await ctx.reply(embed=embed)

# filter avatar to grey
@bot.command(name='grey', help='Gives the avatar of the member with the specified filter')
async def avatarfilter(ctx, member: discord.Member):
    embed=discord.Embed(title="Avatar", url="", color=0xd69a00)
    embed.set_image(url=f"https://res.cloudinary.com/demo/image/fetch/w_200,e_grayscale/{member.avatar_url}?size=1024")
    await ctx.reply(embed=embed)

# filter avatar to 90 degrees
@bot.command(name='flip', help='Gives the avatar of the member with the specified filter')
async def avatarfilter(ctx, member: discord.Member):
    embed=discord.Embed(title="Avatar", url="", color=0xd69a00)
    embed.set_image(url=f"https://res.cloudinary.com/demo/image/fetch/w_200,a_90/{member.avatar_url}?size=1024")
    await ctx.reply(embed=embed)

# get today's date
@bot.command(name='today', help='Gives the current date')
async def date(ctx):
    embed=discord.Embed(title="Date", url="", color=0xd69a00)
    # get day
    embed.add_field(name="Day", value=datetime.datetime.now().strftime("%A"), inline=False)
    embed.add_field(name="Today's Date", value=datetime.datetime.now().strftime("%d-%m-%Y"), inline=False)
    # get time
    embed.add_field(name="Time", value=datetime.datetime.now().strftime("%H:%M:%S"), inline=False)
    await ctx.reply(embed=embed)

# respond message member
@bot.command(name='pungky')
async def respond(ctx):
    await ctx.reply(f'lom mndi')

# mention member with message
@bot.command(name='mention')
async def mention(ctx, member: discord.Member):
    await ctx.reply(f'{member.mention} bau')

@bot.command(name='sa')
async def respond(ctx):
    await ctx.reply(f'♥♥♥♥♥♥♥')

# afk and if user typing, back to normal
@bot.command(name='afk')
async def afk(ctx, *, reason: str):
    await ctx.send(f"{ctx.author.mention} is now AFK. {reason}")
    await ctx.trigger_typing()
    await ctx.send(f"{ctx.author.mention} is back!")

# get weather 
@bot.command(name='weather', help='Gives the weather')
async def weather(ctx, *, city: str):
    url = "https://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=32b2bc6c49f9407597e4139767efaee8"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
    embed=discord.Embed(title="Weather", url="", color=0xd69a00)
    # reqested by author name, avatar, time
    embed.set_footer(text=ctx.author.name, icon_url = ctx.author.avatar_url)
    embed.add_field(name="City", value=city, inline=False)
    embed.add_field(name="Temperature", value=data['main']['temp']-273.15, inline=False)
    embed.add_field(name="Description", value=data['weather'][0]['main'], inline=False)
    embed.add_field(name="Wind Speed", value=data['wind']['speed'], inline=False)
    embed.add_field(name="Humidity", value=data['main']['humidity'], inline=False)
    embed.add_field(name="Pressure", value=data['main']['pressure'], inline=False)
    #timezome
    embed.add_field(name="Timezone", value=data['timezone'], inline=False)
    # set thumbnail
    embed.set_thumbnail(url=f"https://openweathermap.org/img/w/{data['weather'][0]['icon']}.png")
    await ctx.reply(embed=embed)

# get random quote
@bot.command(name='quote', help='Gives a random quote')
async def quote(ctx):
    url = "https://api.forismatic.com/api/1.0/?method=getQuote&lang=en&format=json"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
    embed=discord.Embed(title="", url="", color=0xd69a00)
    
    embed.add_field(name="Quote", value=data["*quoteText*"], inline=False)
    embed.add_field(name="Author", value=data["quoteAuthor"], inline=False)
    await ctx.reply(embed=embed)

# get pokemon info
@bot.command(name='pokemon', help='Gives the pokemon info')
async def pokemon(ctx, *, pokemon: str):
    url = "https://pokeapi.co/api/v2/pokemon/" + pokemon
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
    embed=discord.Embed(title="Pokemon", url="", color=0xd69a00)
    # get pokemon name uppercase
    embed.add_field(name="Name", value=data['name'].upper(), inline=False)
    embed.add_field(name="Weight", value=data['weight'], inline=False)
    embed.add_field(name="Height", value=data['height'], inline=False)
    embed.add_field(name="Abilities", value=data['abilities'][0]['ability']['name'], inline=False)
    embed.add_field(name="Type", value=data['types'][0]['type']['name'].upper(), inline=False)
    embed.add_field(name="Type", value=data['types'][1]['type']['name'].upper(), inline=False)
    # thumbnail
    embed.set_thumbnail(url=f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{data['id']}.png")
    await ctx.reply(embed=embed)

# translate text id to english
@bot.command(name='translate', help='Translate text to english')
async def translate(ctx, *, text: str):
    translator = Translator()
    result = translator.translate(text, src='id', dest='en')
    embed=discord.Embed(title="Translation", url="", color=0xd69a00)
    embed.add_field(name="Translated Text", value=result.text, inline=False)
    await ctx.reply(embed=embed)

# send random anime gif
@bot.command(name='animegif', help='Send random anime gif')
async def gif(ctx):
    url = "https://api.tenor.com/v1/random?q=anime&key=LIVDSRZULELA"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
    embed=discord.Embed(title="GIF", url="", color=0xd69a00)
    embed.set_image(url=data['results'][0]['media'][0]['gif']['url'])
    await ctx.reply(embed=embed)

# send color
@bot.command(name='randomcolor', help='Send random color')
async def color(ctx):
    embed=discord.Embed(title="", url="", color=0xd69a00)
    embed.set_footer(text="Random Color")
    embed.set_image(url=f"https://dummyimage.com/200x200/{random.randint(0,16777215)}/ffffff.png&text={random.randint(0,16777215)}")
    embed.add_field(name="Color", value=f"#{random.randint(0,16777215):06x}", inline=False)
    await ctx.reply(embed=embed)


#ping and latency
@bot.command(name='ping', help='Ping the bot')
async def ping(ctx):
    
    embed=discord.Embed(title="", url="", color=0xd69a00)
    embed.set_footer(text=f"{ctx.author.name}", icon_url = ctx.author.avatar_url)
    embed.add_field(name="Ping", value=f"{round(bot.latency * 1000)}ms", inline=False)
    await ctx.reply(embed=embed)


@bot.command(name='woi')
async def respond(ctx):
    if ctx.author.id == 325260673015873548:
        await ctx.send("woi jg")
    else:
        await ctx.send("yem l")

#fun commands
@bot.command(name='roll')
async def roll(ctx, dice: str):
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)


@bot.command(name='say', delete_after=0)
async def say(ctx, *, text: str):
    await ctx.send(text)


#game commands

@bot.command(name='dice')
async def dice(ctx):
    choices = ['1', '2', '3', '4', '5', '6']
    await ctx.send(f'{random.choice(choices)}')

@bot.command(name='batuguntingkertas')
async def rps(ctx, *, choice: str):
    rps = ["batu", "gunting", "kertas"]
    choice = choice.lower()
    if choice in rps:
        bot = random.choice(rps)
        if bot == choice:
            await ctx.send("seri")
        elif bot == "batu" and choice == "gunting":
            await ctx.send("l mng")
        elif bot == "gunting" and choice == "kertas":
            await ctx.send("l mng")
        elif bot == "kertas" and choice == "batu":
            await ctx.send("l mng")
        else:
            await ctx.send("l klh")
    else:
        await ctx.send("slh")

@bot.command(name='joke', help='sends a joke')
async def joke(ctx):
    url = "https://official-joke-api.appspot.com/random_joke"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
    embed=discord.Embed(title="Joke", url="", color=0xd69a00)
    embed.add_field(name="Setup", value=data['setup'], inline=False)
    embed.add_field(name="Punchline", value=data['punchline'], inline=False)
    await ctx.reply(embed=embed)

#pretty embed for help
@bot.command(name='help')
async def help(ctx):
    embed = discord.Embed()
    # set author
    embed.set_author(name=bot.user.name + ' • Help', url="", icon_url = bot.user.avatar_url)
    embed.set_thumbnail(url=bot.user.avatar_url)
    embed.add_field(name = '__**Mods**__', value= "`ping`, `info`, `userinfo` <user>, `servericon`, `avatar`", inline = True)
    embed.add_field(name = '__**Fun**__', value = "`pokemon` <name>, `animegif`, `flip` <user>, `grey` <user>, `meme`, ", inline = True)
    embed.add_field(name = '__**Utilities**__', value = "`weater` <city>, `randomcolor`, `translate` <text>, `quote`, `today`, `movie`, `trending`, `wiki` <text>, `covid`", inline = True)
    
    # embed.add_field(name = 'Red Team ', value = "Something", inline = True)
    # embed.add_field(name = 'Champion', value = "Something", inline = True)
    # embed.add_field(name = 'Rank', value = "Something", inline = True)
    embed.set_footer(text=ctx.author.name, icon_url = ctx.author.avatar_url)    
    await ctx.send(embed=embed)




@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')

bot.run(TOKEN)