import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f"✅ 봇이 로그인되었습니다: {bot.user}")
    activity = discord.Game(name="집사랑 주인님 대접하는 중")
    await bot.change_presence(status=discord.Status.online, activity=activity)

@bot.command()
async def 환영(ctx, *members: discord.Member):
    if len(members) == 0:
        await ctx.send("❗ 최소 1명에서 최대 3명까지 멘션해주세요!")
        return
    if len(members) > 3:
        await ctx.send("❗ 최대 3명까지만 멘션할 수 있어요!")
        return

    mentions = " ".join(member.mention for member in members)
    message = (
        f"# <a:84931announcement:1381626468735385600>   {mentions} 님 환영합니다!\n\n"
        f"<a:51047animatedarrowwhite:1381626541150175332>   {mentions} 님 𝐌𝐀𝐈𝐃 𝐌𝐨𝐨𝐍에 오신 것을 환영합니다!\n\n"
        f"<a:51047animatedarrowwhite:1381626541150175332> <#1381621263730086060> 에서 규칙을 꼭 확인해주세요!\n"
        f"<:6430pinkribbon:1381626681357238452>   규칙을 읽지 않아 생기는 불이익은 책임지지 않아요!\n\n"
        f"<a:51047animatedarrowwhite:1381626541150175332> 적응이 어렵다면 <@&1381621262291570842> 를 맨션해주세요!\n\n"
        f"<:3141coquettebow:1381626675489669220> 앞으로 잘 부탁드려요!\n"
        f"<@&1381621262291570844>")
    await ctx.send(message)

bot.run(os.environ['TOKEN2'])
