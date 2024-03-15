import discord
from discord import app_commands
from discord.ext import tasks
from datetime import datetime
import os
from keep_alive import keep_alive
from zoneinfo import ZoneInfo
import psutil
import aiohttp

client = discord.Client(intents=discord.Intents.default())
tree = app_commands.CommandTree(client=client)
JIHOU_CHANNEL_ID = 1208730354656084008 #チャンネルID

@client.event
async def setup_hook():
    loop.start()

@client.event
async def on_ready():
    await tree.sync()
    print("起動!")
    await client.change_presence(activity=discord.Game(name="幻塔"))

@tree.command(name="ping", description="pingを計測します")
async def ping(interaction: discord.Interaction):
	ping = client.latency
	cpu_percent = psutil.cpu_percent()
	mem = psutil.virtual_memory() 
	embed = discord.Embed(title="Ping", description=f"Ping : {ping*1000}ms\nCPU : {cpu_percent}%\nMemory : {mem.percent}%", color=discord.Colour.gold())
	embed.set_thumbnail(url=client.user.display_avatar.url)
	await interaction.response.send_message(embed=embed)

@tree.command(name="genshin_userinfo", description="UIDからユーザーの情報を確認できます")
async def ping(interaction: discord.Interaction, uid: str):
    await interaction.response.defer()
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://enka.network/api/uid/{uid}') as response:
            if response.status != 404:
                user = await response.json()
            else:
                embed = discord.Embed(title="ユーザーが見つかりませんでした。", description="UIDが間違っていないか、確認してください。")
                await interaction.followup.send()
    embed = discord.Embed(title=f"{user['playerInfo']['nickname']} の情報",description=f"レベル: **{user['playerInfo']['level']}**\n自己紹介: \n```\n{user['playerInfo']['signature']}\n```")

# 60秒に一回ループ
@tasks.loop(seconds=60)
async def loop():
    # 現在の時刻
    now = datetime.now(ZoneInfo("Asia/Tokyo")).strftime('%H:%M')
    if now == '00:00':
        channel = client.get_channel(JIHOU_CHANNEL_ID)
        await channel.send('https://cdn.discordapp.com/attachments/1208773839023247390/1216853798086246471/AP1GczNYgiHoE-mNro7tzg-rB65rTJ-CfPC98xw2hDvNFzRx6RDVs794Xee_Www1200-h675-s-no.png?ex=6601e669&is=65ef7169&hm=bc216034890394dc50482395cb8b776b5bf7f6257da343a50b8133abff2b739a&')

keep_alive()
client.run(os.getenv("discord"))
