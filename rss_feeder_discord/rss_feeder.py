import discord
from discord.ext import commands, tasks
import feedparser
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_BOT_TOKEN')
GUILD_ID = os.getenv('DISCORD_GUILD_ID')
CHANNEL_ID = os.getenv('DISCORD_CHANNEL_ID')

if not TOKEN:
    raise ValueError("DISCORD_BOT_TOKEN is not set in the .env file")
if not GUILD_ID:
    raise ValueError("DISCORD_GUILD_ID is not set in the .env file")
if not CHANNEL_ID:
    raise ValueError("DISCORD_CHANNEL_ID is not set in the .env file")

GUILD_ID = int(GUILD_ID)
CHANNEL_ID = int(CHANNEL_ID)

# Intentsの設定
intents = discord.Intents.default()
intents.message_content = True

# intentsを渡してBotを作成
bot = commands.Bot(command_prefix='!', intents=intents)

rss_feeds = []
latest_entries = {}

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    check_feed.start()

@bot.command()
async def addfeed(ctx, url: str):
    # TODO: save on sqlite3? user info, channel info
    print("addfeed called")
    if url not in rss_feeds:
        rss_feeds.append(url)
        await ctx.send(f"RSS feed {url} has been added!")
    else:
        await ctx.send(f"RSS feed {url} is already in the list!")

@bot.command()
async def removefeed(ctx, url: str):
    if url in rss_feeds:
        rss_feeds.remove(url)
        latest_entries.pop(url, None)  # remove the latest entry for this feed if it exists
        await ctx.send(f"RSS feed {url} has been removed!")
    else:
        await ctx.send(f"RSS feed {url} is not in the list!")

@bot.command()
async def debugfeed(ctx):
    await ctx.send(f"chu!")
    for feed_url in rss_feeds:
        feed = feedparser.parse(feed_url)
        print(json.dumps(feed, indent=2))
        entry = feed.entries[0]

        if latest_entries.get(feed_url) == entry.link:
            continue

        guild = discord.utils.get(bot.guilds, id=GUILD_ID)
        if not guild:
            continue

        channel = guild.get_channel(CHANNEL_ID)
        if not channel:
            continue

        await channel.send(f"**{entry.title}**\n{entry.link}")
        latest_entries[feed_url] = entry.link

import json
@tasks.loop(minutes=10)
async def check_feed():
    for feed_url in rss_feeds:
        feed = feedparser.parse(feed_url)
        print(json.dumps(feed, indent=2))
        entry = feed.entries[0]

        if latest_entries.get(feed_url) == entry.link:
            continue

        guild = discord.utils.get(bot.guilds, id=GUILD_ID)
        if not guild:
            continue

        channel = guild.get_channel(CHANNEL_ID)
        if not channel:
            continue

        await channel.send(f"**{entry.title}**\n{entry.link}")
        latest_entries[feed_url] = entry.link

bot.run(TOKEN)
