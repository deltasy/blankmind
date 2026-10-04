import disnake
from disnake.ext import commands
from traceback import format_exc as error
import asyncio
import subprocess
from os import listdir as dirs

from actions.buttons import buttonClick
from functions.page1 import getSv
from mongo import udb

def readComs(mode='no errors'):
  folder = 'commands'
  for filename in dirs(folder):
    if filename.endswith('.py'):
      module_name = filename[:-3]
      module_path = f'{folder}.{module_name}'

      try:
        command_module = __import__(module_path, fromlist=[''])
        if hasattr(command_module, 'command'):
          command_module.command(bot)
      except:
        if mode == 'errors':
          print(f'Command imports -> {error()}\n-----')

intents = disnake.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='>', intents=intents)

@bot.event
async def on_ready():
  print('CORP started!')
  readComs()

  getSv(bot)


  """
  with open('bot_display2.gif', 'rb') as avatar:
    await bot.user.edit(avatar=avatar.read()) 
  """

  #await initial(bot)

  await bot.change_presence(activity=disnake.Activity(type=disnake.ActivityType.custom, name="Blank Mind", state="💠 Guilds Bot"))

  #await manualrank()

readComs('errors')





async def manualrank():
  cHall = bot.get_channel(1233830022473711636) # DAILY GUILD RANK
		  
  svguild = cHall.guild
	
  by_level = [fhFilter(i + 1) for i in range(2)]

  grank = []

  best_guild = by_level[::-1][0][::-1][0]
	
  for guilds in by_level[::-1]:
    for guild in guilds[::-1]:
      grank.append(f"<@&{guild['guild_role']}> ➜ **{round(sum(guild['bank']['contributors'].values()), 1)}** <:blank:1124439750208655500>")

  grank[0] = '# :trophy: ' + grank[0]
  grank[1] = '## :second_place: ' + grank[1]
  grank[2] = '## :third_place: ' + grank[2] + '\n▬▬▬▬▬▬▬'

  gembed = disnake.Embed(
    description='\n'.join(grank),
    colour=svguild.get_role(best_guild['guild_role']).colour
	  
  )

  await cHall.purge(limit=None)
  await cHall.send(embed=gembed)
  await cHall.send(f'# <a:animated_fire:1216782884036280390> **{best_guild["guild_name"]} is dominating the hall!**')


def fhFilter(lvl):
  pipeline = [
        {"$match": {"level": lvl, "ugid": {"$exists": True}}},
        {"$addFields": {
            "total_contributors": {
                "$sum": {
                    "$map": {
                        "input": {"$objectToArray": "$bank.contributors"},
                        "in": "$$this.v"
                    }
                }
            }
        }},
        {"$sort": {"total_contributors": 1}} 
  ]

	
  return list(udb.aggregate(pipeline))



async def initial(bot):
    emb1 = disnake.Embed(
      description=f'## 💠 GUILD COMMANDS',
      colour = 0xFFFFFF
    )
    emb2 = disnake.Embed(
      description=f'## ✅ </guild create:1220132312554147962> **(Costs 100 <:blank:1124439750208655500>)**\n> Create your own guild. You will earn a guild statistics tab, a custom role, and will be able to invite other users. **Your guild members can enter your private room without you needing to invite them with </room:1225204130730217545>**',
      colour = 0x33FF33
    )
    emb3 = disnake.Embed(
      description=f'## ✅ </guild invite:1220132312554147962> **(Costs 5 <:blank:1124439750208655500>)**\n> Invites a user to your guild. You can only invite one user at a time and you will spend blanks even if they do not accept the invitation.',
      colour = 0x33FF33
    )
    emb4 = disnake.Embed(
      description=f'## ✅ </guild leave:1220132312554147962>\n> Makes you leave your current guild',
      colour = 0x33FF33
    )
    emb5 = disnake.Embed(
      description=f'## ✅ </guild kick:1220132312554147962>\n> Kicks a user from your guild',
      colour = 0x33FF33
    )

    embn1 = disnake.Embed(
      description=f'## <:MP_LOCK:1230985696353714237> 💠 GUILD COMMANDS\n> Unlocks with a <@&1230869225640562698>',
      colour = 0xed3325
    )
	
    chats = getSv(['cCommands_MPnull', 'cCommands_MPlow', 'cCommands_MPmed', 'cCommands'])

    all_embeds = [
      [[embn1]],
      [[embn1]],
      [[embn1]],
      [[emb1, emb2, emb3, emb4, emb5]],
    ]

    async def multichat(chat, aindex, this_embeds):
      try:
        await chat.purge(limit=None)

        with open('corp.gif', 'rb') as file: corp = disnake.File(file)
        await chat.send(file=corp)
		  
        for i, embeds in enumerate(this_embeds[aindex]): 
          try: await chat.send(embeds=embeds)
          except: 
            try: await chat.send(file=embeds)
            except: pass
				
          try: 
            if i + 1 < len(this_embeds[aindex]): await chat.send('‎\n\n‎')
          except: print(error())

        with open('divider_down.png', 'rb') as file: div_down = disnake.File(file)
        await chat.send(file=div_down)
        await chat.send("‎\n‎\n‎\n‎")

        if aindex >= len(all_embeds) - 1: await chat.send('<-C->')

      except: print(error())

    try: [asyncio.create_task(multichat(chat, u, all_embeds)) for u, chat in enumerate(chats)]
    except: print(error())

@bot.listen("on_button_click")
async def btn(inter: disnake.MessageInteraction):
  await buttonClick(inter, bot)

bot.run('T')