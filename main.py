import os
from keep_alive import keep_alive

keep_alive()

import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f"✅ 봇이 로그인되었습니다: {bot.user}")
    activity = discord.Game(name="집사랑 주인님 대접하는 중")
    await bot.change_presence(status=discord.Status.online, activity=activity)


def has_role_id(role_id: int):

    def predicate(ctx):
        role = discord.utils.get(ctx.author.roles, id=role_id)
        return role is not None

    return commands.check(predicate)


# 예시 역할 ID (실제 역할 ID로 바꿔주세요)
운영진_역할_ID = 1381621262345965610


@bot.command()
@has_role_id(운영진_역할_ID)
async def 환영(ctx, *members: discord.Member):
    if len(members) == 0:
        await ctx.send("❗ 최소 1명에서 최대 3명까지 멘션해주세요!")
        return
    if len(members) > 3:
        await ctx.send("❗ 최대 3명까지만 멘션할 수 있어요!")
        return

    mentions = " ".join(member.mention for member in members)
    message = (
      f"# <a:84931announcement:1381548049527996416>  {mentions} 님 환영합니다!\n\n"
        f"<a:51047animatedarrowwhite:1381548176103968889>  {mentions} 님 𝐌𝐀𝐈𝐃 𝐌𝐨𝐨𝐍에 오신 것을 환영합니다!\n\n"
        f"<a:51047animatedarrowwhite:1381548176103968889> <#1381099323764375672> 에서 규칙을 꼭 확인해주세요!\n"
        f"<:6430pinkribbon:1381548451535523882>  규칙을 읽지 않아 생기는 불이익은 책임지지 않아요!\n\n"
        f"<a:51047animatedarrowwhite:1381548176103968889> 적응이 어렵다면 <@&1381207496341065758>  를 맨션해주세요!\n\n"
        f"<:3141coquettebow:1381626675489669220>  앞으로 잘 부탁드려요!\n"
        f" <@&1381205970163732490> ")
    await ctx.send(message)


@환영.error
async def 환영_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("🚫 이 명령어를 실행할 권한이 없어요!")


bot.run(os.environ['TOKEN2'])
