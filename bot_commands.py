import discord
import league
import asyncio
import os
from discord.ext import commands
from dotenv import load_dotenv



intents = discord.Intents.all()
intents.message_content = True
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
bot = commands.Bot(command_prefix='^', intents=intents)


@bot.command(name="test")
@commands.has_permissions(administrator=True)
async def test(ctx):
    await ctx.send("jg gap")

@bot.command(name="doxx-them")
@commands.has_permissions(administrator=True)
async def get_summoner_info(ctx, summoner_name, tag):
    api = os.getenv('API_KEY')
    summoner_info = league.get_summoner_info(summoner_name, tag, api)
    await ctx.send(summoner_info)

@bot.command(name="tenDeaths?")
@commands.has_permissions(administrator=True)
async def get_last_match(ctx, summoner_name, tag):
    api = os.getenv('API_KEY')
    summoner_info = league.get_summoner_info(summoner_name, tag, api)
    puid = summoner_info['puuid']
    match = league.get_last_match(puid, api)
    for part in match.participants:
        if part.puid == puid:
            match = part
            break
    await ctx.send("Yes" if (match.deaths >= 10) else "No")

@bot.command(name="get-match")
@commands.has_permissions(administrator=True)
async def get_match(ctx, summoner_name, tag):
    api = os.getenv('API_KEY')
    summoner_info = league.get_summoner_info(summoner_name, tag, api)
    puid = summoner_info['puuid']
    match = league.get_last_match(puid, api)
    await ctx.send(match)
    
bot.run(TOKEN)