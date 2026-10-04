import disnake
from disnake.ext import commands
from json import load as jload
from os import listdir as dirs
from traceback import format_exc as error
import asyncio

from actions.calls import state, callUpdate, mode_format, disableCameradetect, camera_states
from actions.buttons import buttonClick
from actions.dropdown import dropdown

from functions.page1 import getSv, agetSv

from datetime import datetime

with open('jsons/calls.json', 'r') as file: calls = jload(file)

def readComs(mode='errors'):
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
				pass
				if mode == 'errors':
				  print(f'Command imports -> {error()}\n-----')


intents = disnake.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix='>', intents=intents)

@bot.event
async def on_ready():
  #chan = bot.get_channel(1174127784189239377)
  #await chan.send("Crie rascunhos e comece a escrever algum artigo para acrescentar à blankpédia", components=[disnake.ui.Button(label="Gerar rascunho", style=disnake.ButtonStyle.primary, custom_id="new_sketch")])

  """
  with open('cronos_display.gif', 'rb') as avatar:
    await bot.user.edit(avatar=avatar.read()) 
  """

  print('Updated!!')
  readComs('no error')
  
  getSv(bot)
  await agetSv(bot)

  global cCalls, cRoom, cGroup_category, rFocus, cFreearea_category, cCamera, rCinema
  cCalls, cRoom, cGroup_category, rFocus, cFreearea_category, cCamera, rCinema = getSv(['cCalls', 'cRoom', 'cGroup_category', 'rFocus', 'cFreearea_category', 'cCamera', 'rCinema'])

  await callUpdate(cCalls, bot)

  await bot.change_presence(activity=disnake.Activity(type=disnake.ActivityType.custom, name="Blank Mind", state="⌛ Timer Bot"))

  unfocus = bot.get_channel(1227267622911869029)

  embed = disnake.Embed(
    description='🎯** Bugged in focus mode?** Click the button to manually exit focus mode',
    colour=0xFF000D
  )


  """
  eno = disnake.PartialEmoji(animated=False, id='1132703732543529000', name='no')
  await unfocus.send(embed=embed,components=[disnake.ui.Button(label='Sair', emoji=eno, style=disnake.ButtonStyle.danger, custom_id=f"leave_focus")])
  """

readComs()


@bot.event
async def on_message(msg):
  if msg.author.bot and '<-C->' in msg.content: 
    emb1 = disnake.Embed(
      description=f'# :loud_sound: GENERAL COMMANDS',
      colour = 0xFFFFFF
    )
    emb2 = disnake.Embed(
      description=f'## ✅ </room:1225204130730217545>\n> **Only works if you have entered a private call. To create a private call, just connect to <#1126180695019102208>**. After that, you will enter a room that only you have access to. You can use this command to invite new people to your room, so they can also enter.\n\n> For each person in the room, **the <:blank:1124439750208655500> reward per minute increases by 0.01**. If anyone leaves the room, it is destroyed immediately! It\'s a committed study',
      colour = 0x33FF33
    )
    emb3 = disnake.Embed(
      description=f'## ✅ </modelist:1225212116202684508>\n> Opens your modes panel; **Modes are modifiers that can improve your organization and direction in studies:** the modes you choose will activate whenever you enter a call. There are 4 types available:\n\n- :dart: **Focused:** makes most chats temporarily disappear\n\n- :tomato: **Pomodoro:** Activates a rest and study timer chosen by you. **Your time in call will also consider the time you rested**\n\n- :dvd: **Study cycle:** An evolved version of the pomodoro: you can name each step of your cycle, as well as specify cycles for each day of the week. **Cannot be activated along with pomodoro mode.**\n\n- :mountain_snow: **Cave:** An absolute focus mode that isolates you from most chats (distractors) for the amount of days you choose. **Unlike other modes, it is always on and cannot be canceled, even if you are not in a call.**',
      colour = 0x33FF33
    )
	  
    emb4 = disnake.Embed(
      description=f'# :recycle: CYCLE COMMANDS',
      colour = 0xFFFFFF
    )
    emb5 = disnake.Embed(
      description=f'## ✅ </pomodoro set:1225204130730217544>\n> **Adjusts your pomodoro time**. It is activated through the </modelist:1225212116202684508> command',
      colour = 0x33FF33
    )
    emb6 = disnake.Embed(
      description=f'## ✅ </cycle set:1225490700557090857>\n> **Creates a custom study cycle**. It is activated through the </modelist:1225212116202684508> command\n\n> Specify the cycles for each day of the week and the time that will be dedicated to each subject of each cycle. Whenever you finish a subject, the cycle will save your progress even if you leave the call.',
      colour = 0x33FF33
    )
    emb7 = disnake.Embed(
      description=f'## ✅ </cycle today:1225490700557090857>\n> Shows the subjects of today\'s cycle and which ones you have already studied.',
      colour = 0x33FF33
    )





    embm1 = disnake.Embed(
      description=f'# :new: :loud_sound: GENERAL COMMANDS',
      colour = 0xFFFFFF
    )
    embm2 = disnake.Embed(
      description=f'## :new: </room:1225204130730217545>\n> **Only works if you have entered a private call. To create a private call, just connect to <#1126180695019102208>**. After that, you will enter a room that only you have access to. You can use this command to invite new people to your room, so they can also enter.\n\n> For each person in the room, **the <:blank:1124439750208655500> reward per minute increases by 0.01**. If anyone leaves the room, it is destroyed immediately! It\'s a committed study',
      colour = 0x8982C8
    )
    embm3 = disnake.Embed(
      description=f'## <:MP_LOCK:1230985696353714237> </modelist:1225212116202684508>',
      colour = 0xed3325
    )
	  
    embm4 = disnake.Embed(
      description=f'# <:MP_LOCK:1230985696353714237> :recycle: CYCLE COMMANDS\n> Unlock with <@&1230869225640562698>',
      colour = 0xed3325
    )





    embl1 = disnake.Embed(
      description=f'# <:MP_LOCK:1230985696353714237> :loud_sound: GENERAL COMMANDS\n> Unlock with <@&1230869038402375751>',
      colour = 0xed3325
    )
	  
    embl4 = disnake.Embed(
      description=f'# <:MP_LOCK:1230985696353714237> :recycle: CYCLE COMMANDS\n> Unlock with <@&1230869225640562698>',
      colour = 0xed3325
    )


	  

    chats = getSv(['cCommands_MPnull', 'cCommands_MPlow', 'cCommands_MPmed', 'cCommands'])

    all_embeds = [
      [[embl1], [embl4]],
      [[embl1], [embl4]],
      [[embm1, embm2, embm3], [embm4]],
      [[emb1, emb2, emb3], [emb4, emb5, emb6, emb7]],
    ]

    async def multichat(chat, aindex, this_embeds):
      try:
        await chat.purge(limit=1)

        with open('divider_up.png', 'rb') as file: div_up = disnake.File(file)
        await chat.send(file=div_up)
		  
        with open('cronos.gif', 'rb') as file: cronos = disnake.File(file)
        await chat.send(file=cronos)
		  
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
        if aindex >= len(all_embeds) - 1: await chat.send('<-V->')

      except: print(error())

    try: [asyncio.create_task(multichat(chat, u, all_embeds)) for u, chat in enumerate(chats)]
    except: print(error())


@bot.event
async def on_voice_state_update(member, before, after):
  try: category = after.channel.category
  except: category = before.channel.category

  uid = str(member.id)

  if after.channel is not None and after.channel == cCamera:
    with open('jsons/calls.json', 'r') as file: calls = jload(file)
    with open('jsons/callspomo.json', 'r') as file: callspomo = jload(file)

    if after.self_stream == True or after.self_video == True:
      modes = await mode_format(member, str(cCamera.id), uid, 'ignore')
      mode_texts = modes[0]

      if not mode_texts: centralize = 'ㅤ\n' # No study cycles
      else: centralize = ''

      if after.self_stream == True:
        embed = disnake.Embed(
          description=f'{centralize}{member.mention} is sharing screen in <#{1136470255473000480}>\n**<t:{int((datetime.now()).timestamp())}:R>**{mode_texts}',
          colour=0xffffff,
        )
      else:
        embed = disnake.Embed(
          description=f'{centralize}{member.mention} turned on the camera in <#{1136470255473000480}>\n**<t:{int((datetime.now()).timestamp())}:R>**{mode_texts}',
          colour=0xffffff,
        )

      await disableCameradetect(uid)

      try: imgprof = member.avatar.url
      except: imgprof = 'https://assets.mofoprod.net/network/images/discord.width-250.jpg'
      embed.set_thumbnail(url=imgprof)

      await state(member, before, after, [cCalls, cRoom, cGroup_category], bot, 'activated_camera')

      with open('jsons/calls.json', 'r') as file: calls = jload(file)
      with open('jsons/callspomo.json', 'r') as file: callspomo = jload(file)

      if uid in calls: msg = await cCalls.fetch_message(calls[uid][1])
      elif uid in callspomo: msg = await cCalls.fetch_message(callspomo[uid][1])

      try: await msg.edit(embed=embed)
      except: pass

    elif uid in calls or uid in callspomo: # If already activated camera, but now disabled
      if after.self_stream == False and after.self_video == False:
        await member.move_to(None)
  
  elif before.channel == cCamera and uid in camera_states: # Left camera channel before activating camera
     await disableCameradetect(uid)

  if category != cFreearea_category and before.self_stream == after.self_stream and before.self_mute == after.self_mute and before.self_video == after.self_video and before.self_deaf == after.self_deaf:
    if after == cCamera and (after.self_stream == True or after.self_video == True): pass # If still recording/streaming in the camera room, without leaving:
    else: await state(member, before, after, [cCalls, cRoom, cGroup_category], bot)
  elif after.channel and after.channel.id == 1162148851545809078: await member.add_roles(rCinema)
  elif before.channel and before.channel.id == 1162148851545809078: await member.remove_roles(rCinema)

with open('jsons/marks.json', 'r') as file: marks = jload(file)
	
@bot.listen("on_button_click")
async def btn(inter: disnake.MessageInteraction):
  global marks
  await buttonClick(inter, bot)
  with open('jsons/marks.json', 'r') as file: marks = jload(file)


@bot.event
async def on_dropdown(inter: disnake.Interaction):
  await dropdown(inter)

bot.run('T')
