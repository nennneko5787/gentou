import discord
from discord.ext import tasks
from datetime import datetime
import os
from keep_alive import keep_alive

client = discord.Client(intents=discord.Intents.all())
JIHOU_CHANNEL_ID = 1208730354656084008 #チャンネルID

@client.event
async def setup_hook():
    loop.start()

@client.event
async def on_ready():
    print("起動!")
    await client.change_presence(activity=discord.Game(name="幻塔"))

# 60秒に一回ループ
@tasks.loop(seconds=60)
async def loop():
    # 現在の時刻
    now = datetime.now().strftime('%H:%M')
    if now == '00:00':
        channel = client.get_channel(JIHOU_CHANNEL_ID)
        await channel.send('https://cdn.discordapp.com/attachments/1208773839023247390/1216853798086246471/AP1GczNYgiHoE-mNro7tzg-rB65rTJ-CfPC98xw2hDvNFzRx6RDVs794Xee_Www1200-h675-s-no.png?ex=6601e669&is=65ef7169&hm=bc216034890394dc50482395cb8b776b5bf7f6257da343a50b8133abff2b739a&')

keep_alive()
client.run(os.getenv("discord"))
