import discord
from discord.ext import commands, tasks
import feedparser
import os
from dotenv import load_dotenv
import sqlite3

load_dotenv()

TOKEN = os.getenv('DISCORD_BOT_TOKEN')

if not TOKEN:
    raise ValueError("DISCORD_BOT_TOKEN is not set in the .env file")
# TODO: show help
# TIP: https://rss.app

def init_db():
    conn = sqlite3.connect('rss_feeds.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS feeds
                 (user_id INTEGER, channel_id INTEGER, feed_url TEXT, latest_entry TEXT)''')

    conn.commit()
    conn.close()

init_db()

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
    conn = sqlite3.connect('rss_feeds.db')
    c = conn.cursor()
    
    # Check if feed already exists for this user
    c.execute("SELECT * FROM feeds WHERE user_id=? AND feed_url=?", (ctx.author.id, url))
    if c.fetchone():
        await ctx.send("This feed is already added.")
        return

    c.execute("INSERT INTO feeds (user_id, channel_id, feed_url, latest_entry) VALUES (?, ?, ?, ?)",
              (ctx.author.id, ctx.channel.id, url, ""))

    conn.commit()
    conn.close()

    await ctx.send(f"RSS feed {url} has been added to channel {ctx.channel.name}!")

@bot.command()
async def removefeed(ctx, url: str):
    conn = sqlite3.connect('rss_feeds.db')
    c = conn.cursor()
    
    # Check if feed exists for this user
    c.execute("SELECT * FROM feeds WHERE user_id=? AND feed_url=?", (ctx.author.id, url))
    if c.fetchone():
        c.execute("DELETE FROM feeds WHERE user_id=? AND feed_url=?", (ctx.author.id, url))
        conn.commit()
        await ctx.send(f"RSS feed {url} has been removed!")
    else:
        await ctx.send(f"RSS feed {url} is not in the list!")

    conn.close()

@bot.command()
async def resetfeed(ctx, member: discord.Member):
    conn = sqlite3.connect('rss_feeds.db')
    c = conn.cursor()
    
    # Delete all feeds for the mentioned user
    c.execute("DELETE FROM feeds WHERE user_id=?", (member.id,))
    conn.commit()
    conn.close()

    await ctx.send(f"All RSS feeds for {member.mention} have been removed!")

@bot.command()
async def debugfeed(ctx):
    await ctx.send(f"chu!")
    conn = sqlite3.connect('rss_feeds.db')
    c = conn.cursor()

    c.execute("SELECT * FROM feeds")
    feeds = c.fetchall()

    for feed in feeds:
        user_id, channel_id, feed_url, latest_entry = feed
        fetched_feed = feedparser.parse(feed_url)

        if fetched_feed.entries and fetched_feed.entries[0].link != latest_entry:
            channel = bot.get_channel(channel_id)
            user = await bot.fetch_user(user_id)
            await channel.send(f"{user.mention} **{fetched_feed.entries[0].title}**\n{fetched_feed.entries[0].link}")

            c.execute("UPDATE feeds SET latest_entry=? WHERE user_id=? AND feed_url=?", 
                      (fetched_feed.entries[0].link, user_id, feed_url))

    conn.commit()
    conn.close()

@tasks.loop(minutes=10)
async def check_feed():
    conn = sqlite3.connect('rss_feeds.db')
    c = conn.cursor()

    c.execute("SELECT * FROM feeds")
    feeds = c.fetchall()

    for feed in feeds:
        user_id, channel_id, feed_url, latest_entry = feed
        fetched_feed = feedparser.parse(feed_url)

        if fetched_feed.entries and fetched_feed.entries[0].link != latest_entry:
            channel = bot.get_channel(channel_id)
            user = await bot.fetch_user(user_id)
            await channel.send(f"{user.mention} **{fetched_feed.entries[0].title}**\n{fetched_feed.entries[0].link}")

            c.execute("UPDATE feeds SET latest_entry=? WHERE user_id=? AND feed_url=?", 
                      (fetched_feed.entries[0].link, user_id, feed_url))

    conn.commit()
    conn.close()


bot.run(TOKEN)
