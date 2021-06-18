import discord
from replit import db
from discord.ext import commands
import datetime
import asyncio
import time

class todolist(commands.Cog):
  def __init__(self, client):
    self.client = client
    self.client.loop.create_task(self.background_task())

  @commands.Cog.listener()
  async def on_reaction_add(self, reaction, user):
    channel = reaction.message.channel
    emoji = str(reaction.emoji)
    if user.bot:
      return
    if emoji == "<:deletesign:853677705861267456>" and str(reaction.message.author) == "MyTodoList#7809":
      data = str(reaction.message.content).split("\n")
      for x in range(len(data)):
        data[x] = data[x].split(": ")
      tabel = list(db.keys())
      for x in tabel:
        if db[x][0] == data[1][1] and db[x][1] == data[2][1] and db[x][2] == data[3][1]:
          del db[x]
          await channel.send("```Data berhasil dihapus```")
          return

  @commands.command()
  async def help(self, ctx):
    context = """```List of Commands!
1. t!ping                         
    = return ping
2. t!all                          
    = return all of registered tasks
3. t!add <nama> <tanggal> <waktu> 
    = If you want to input a task
4. t!clear <number>               
    = If you want to delete messages regardless if you have the permission or not 
    (Use it wisely!!!)
    (Example: t!clear 3, it gonna clear 3 messages above this command)
5. t!help                         
    = Show this messages```"""
    await ctx.send(context)

  @commands.command()
  async def ping(self, ctx):
    # await ctx.send(str(round(self.client.latency * 100)) + "ms")
    ping = str(round(self.client.latency * 100)) + " ms"
    embed=discord.Embed(color=0xff0000)
    embed.add_field(name="Ping " + str(ctx.author), value=ping, inline=False)
    await ctx.send(embed=embed)

  @commands.command()
  async def all(self, ctx):
    data = list(db.keys())
    if len(data) == 0:
      await ctx.send("```Data masih kosong```")
    else:
      count = 1
      for x in data:
        print(db[x])
        tanggalwaktu_deadline = str(db[x][1]) + " " + str(db[x][2])
        tanggalwaktu_deadline = datetime.datetime.strptime(tanggalwaktu_deadline, '%d/%m/%Y %H:%M:%S')
        tanggalwaktu_sekarang = datetime.datetime.now()
        sisa = str(tanggalwaktu_deadline - tanggalwaktu_sekarang).split()
        if len(sisa) == 1:
          sisa_waktu = sisa[0][0:8]
          await ctx.send("**" + "Task " + str(count) + "**")
          data = await ctx.send("```Nama\t\t\t\t\t\t\t: {}\nTanggal Deadline\t\t\t\t: {}\nWaktu Deadline\t\t\t\t  : {}\nSisa Waktu\t\t\t\t\t  : {}```".format(count, db[x][0], db[x][1], db[x][2], sisa_waktu))
        else:
          sisa_hari = sisa[0] + " " + sisa[1]
          sisa_waktu = sisa[2][0:8]
          data = await ctx.send("**Task {}**\n```Nama\t\t\t\t\t\t\t: {}\nTanggal Deadline\t\t\t\t: {}\nWaktu Deadline\t\t\t\t  : {}\nSisa Waktu\t\t\t\t\t  : {}```".format(count, db[x][0], db[x][1], db[x][2], (sisa_hari + " " + sisa_waktu)))
        count += 1
        emoji = "<:deletesign:853677705861267456>"
        await data.add_reaction(emoji)
        
  @commands.command()
  async def add(self, ctx, nama, tanggal, waktu):      
    data = list(db.keys())
    for x in data:
      # print(db[x])
      if nama == db[x][0] and tanggal == db[x][1] and waktu == db[x][2]:
        await ctx.send("Data sudah pernah dimasukkan, jika ingin mengubah silahkan gunakan t!update sesuai dengan panduan di dalam t!help")
        return
    db[str(len(db.keys()) + 1)] = [nama, tanggal, waktu]
    await ctx.send("Data telah dimasukkan")

  @commands.command()
  async def clear(self, ctx, amount=100):
    channel = ctx.message.channel
    messages = []
    async for message in channel.history(limit=amount + 1):
      messages.append(message)
    await channel.delete_messages(messages)
    msg = await ctx.send('Messaged deleted.')
    time.sleep(5)
    await msg.delete()

  async def reminder(self):
    await self.client.wait_until_ready()  # Make sure your guild cache is ready so the channel can be found via get_channel
    ctx = self.client.get_channel(821985835032510467) # Note: It's more efficient to do bot.get_guild(guild_id).get_channel(channel_id) as there's less looping involved, but just get_channel still works fine
    data = list(db.keys())
    if len(data) == 0:
      await ctx.send("```Data masih kosong```")
    else:
      count = 1
      for x in data:
        tanggalwaktu_deadline = str(db[x][1]) + " " + str(db[x][2])
        tanggalwaktu_deadline = datetime.datetime.strptime(tanggalwaktu_deadline, '%d/%m/%Y %H:%M:%S')
        tanggalwaktu_sekarang = datetime.datetime.now()
        sisa = str(tanggalwaktu_deadline - tanggalwaktu_sekarang).split()
        if len(sisa) == 1:
          sisa_waktu = sisa[0][0:8]
          await ctx.send("**" + "Task " + str(count) + "**")
          data = await ctx.send("```Nama\t\t\t\t\t\t\t: {}\nTanggal Deadline\t\t\t\t: {}\nWaktu Deadline\t\t\t\t  : {}\nSisa Waktu\t\t\t\t\t  : {}```".format(count, db[x][0], db[x][1], db[x][2], sisa_waktu))
        else:
          sisa_hari = sisa[0] + " " + sisa[1]
          sisa_waktu = sisa[2][0:8]
          data = await ctx.send("**Task {}**\n```Nama\t\t\t\t\t\t\t: {}\nTanggal Deadline\t\t\t\t: {}\nWaktu Deadline\t\t\t\t  : {}\nSisa Waktu\t\t\t\t\t  : {}```".format(count, db[x][0], db[x][1], db[x][2], (sisa_hari + " " + sisa_waktu)))
        count += 1
        emoji = "<:deletesign:853677705861267456>"
        await data.add_reaction(emoji)

  async def background_task(self):
    now = datetime.datetime.now()
    if now.time() > datetime.time(13, 0, 0):  # Make sure loop doesn't start after {WHEN} as then it will send immediately the first time as negative seconds will make the sleep yield instantly
      tomorrow = datetime.datetime.combine(now.date() + datetime.timedelta(days=1), datetime.time(0))
      seconds = (tomorrow - now).total_seconds()  # Seconds until tomorrow (midnight)
      await asyncio.sleep(seconds)   # Sleep until tomorrow and then the loop will start 
    while True:
      now = datetime.datetime.now() # You can do now() or a specific timezone if that matters, but I'll leave it with utcnow
      target_time = datetime.datetime.combine(now.date(), datetime.time(13, 0, 0))  # 6:00 PM today (In UTC)
      seconds_until_target = (target_time - now).total_seconds()
      await asyncio.sleep(seconds_until_target)  # Sleep until we hit the target time
      await self.reminder()  # Call the helper function that sends the message
      tomorrow = datetime.datetime.combine(now.date() + datetime.timedelta(days=1), datetime.time(0))
      seconds = (tomorrow - now).total_seconds()  # Seconds until tomorrow (midnight)
      await asyncio.sleep(seconds)   # Sleep until tomorrow and then the loop will start a new iteration
    
def setup(client):
  client.add_cog(todolist(client))