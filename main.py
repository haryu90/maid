import os
import discord
from discord.ext import commands, tasks
import asyncio

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# 점수를 저장할 딕셔너리
user_scores = {}
# 음성 채널에 입장한 사용자 추적
voice_channel_users = {}

# 점수 증가 주기를 1분으로 설정 (60초)
@tasks.loop(seconds=60)
async def increase_scores():
    for user_id in voice_channel_users.copy():
        # 1분마다 점수 1점씩 증가
        user_scores[user_id] = user_scores.get(user_id, 0) + 1

# 봇이 준비되었을 때 호출
@bot.event
async def on_ready():
    print(f"✅ 봇이 로그인되었습니다: {bot.user}")
    activity = discord.Game(name="집사랑 주인님 대접하는 중")
    await bot.change_presence(status=discord.Status.online, activity=activity)
    increase_scores.start()  # 주기적인 점수 증가 시작

# 사용자가 음성 채널에 입장할 때
@bot.event
async def on_voice_state_update(member, before, after):
    if after.channel and not before.channel:  # 음성 채널에 입장했을 때
        voice_channel_users[member.id] = True
    elif before.channel and not after.channel:  # 음성 채널을 나갔을 때
        if member.id in voice_channel_users:
            del voice_channel_users[member.id]

# 점수 확인 명령어
@bot.command(name="음챗")
async def check_score(ctx, member: discord.Member = None):
    if member is None:
        # 본인의 점수를 확인
        score = user_scores.get(ctx.author.id, 0)
        await ctx.send(f"{ctx.author.mention}님의 현재 점수는 {score}점입니다.")
    else:
        # 멘션한 사람의 점수를 확인
        score = user_scores.get(member.id, 0)
        await ctx.send(f"{member.mention}님의 현재 점수는 {score}점입니다.")

# 점수 리셋 명령어
@bot.command(name="리셋")
async def reset_scores(ctx):
    user_scores.clear()
    voice_channel_users.clear()
    await ctx.send("모든 사용자의 점수가 리셋되었습니다.")

# 환영 메시지 명령어
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
