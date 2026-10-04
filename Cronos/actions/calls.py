from json import load as jload, loads as jloads, dump as jdump, dumps as jdumps
from disnake import Embed, PermissionOverwrite as Dperms
from traceback import format_exc as error
from asyncio import sleep as asleep
import asyncio
import pytz
import disnake

from traceback import format_exc as error

from datetime import datetime, timedelta

from functions.page1 import newBlank, getSv, namedisplay, trueFocus
from functions.time import timeString
from commands.pomodoro import ucycles

with open('jsons/calls.json', 'r') as file: cdb = jload(file)
with open('jsons/callgroups.json', 'r') as file: cgdb = jload(file)
with open('jsons/callspomo.json', 'r') as file: cpdb = jload(file)
	

from mongo import udb, readSet

global pomo_tasks, pausewords, camera_states, camera_warn
pomo_tasks, camera_states, pause_words = {}, {}, ['descan', 'pausa']
camera_warn = {}

async def simple_overwrite(user, channel, mode=True):
  if not mode: 
    if type(user) == str: user = await getSv('guild').fetch_member(user)  
    return await channel.set_permissions(user, overwrite=None)

  current_overwrite = channel.overwrites_for(user)
  current_overwrite.update(view_channel=True)

  return await channel.set_permissions(user, overwrite=current_overwrite)


async def disableCameradetect(uid):
  try:
    camera_states[uid].cancel()
    del camera_states[uid]

    try: await camera_warn[uid].delete()
    except: pass

    del camera_warn[uid]
  except: pass

async def mode_format(user, acid, uid, mode=''):
  mode_texts = await detectModes(user, 'get')

  subject, pomo_studytime = None, None
  if 'Pomodoro' in mode_texts: 
    try: pomo_studytime = udb.find_one({'uid': int(uid)})['cycles']['pomodoro'][0]
    except: pomo_studytime = 25
    subject = '📖 Study'
    mode_texts = f'\n\n> {subject}\n> Ends **<t:{int((datetime.now() + timedelta(minutes=pomo_studytime)).timestamp())}:R>**' + mode_texts

    if acid and mode != 'ignore': # If user has pomodoro cycle, start task
      task = asyncio.create_task(nextCycle(uid, pomo_studytime))
      pomo_tasks[uid] = task

  elif 'Cycle' in mode_texts:
    this_day = day_name()

    try:
      with open('jsons/usercycles.json', 'r') as file: ucycles = jload(file)

      klist = list(ucycles['custom_cycles'][uid][this_day].keys())

      if "CHECKPOINTED" in klist:
        subject = ucycles['custom_cycles'][uid][this_day]["CHECKPOINTED"]
        klist.remove("CHECKPOINTED")

      else:

        subject = next(first_key for first_key in klist)
      
      pomo_studytime = ucycles['custom_cycles'][uid][this_day][subject]

      mode_texts = f'\n\n> **{subject}**\n> Ends **<t:{int((datetime.now() + timedelta(hours=pomo_studytime[0], minutes=pomo_studytime[1])).timestamp())}:R>**' + mode_texts

      if acid and mode != 'ignore':
        task = asyncio.create_task(nextCycle(uid, pomo_studytime[0] * 60 + pomo_studytime[1]))
        pomo_tasks[uid] = task

    except: 
      try: # Invalid checkpointed
        del ucycles['custom_cycles'][uid][this_day]["CHECKPOINTED"]
        with open('jsons/usercycles.json', 'w') as file: jdump(ucycles, file, indent=2)
      except: pass

      mode_texts = f'\n\n- You haven\'t configured your cycle for **today ({this_day})** yet. Use the command </cycle set:1225490700557090857>' + mode_texts
  
  return [mode_texts, subject, pomo_studytime]

def day_name():
  fuse = pytz.timezone("America/Sao_Paulo")
  now = datetime.now(fuse)

  # Get current date
  eng_data = now.date().strftime("%A")
  br_data = {"Monday": "Monday", "Tuesday": "Tuesday", "Wednesday": "Wednesday", 'Thursday': "Thursday", 'Friday': 'Friday', 'Saturday': 'Saturday', 'Sunday': 'Sunday'}
  return br_data[eng_data]

async def detectModes(member, oper='active'):
  modes = None
  try:
      if type(member) == int: member = await getSv('guild').fetch_member(member)
      udata = udb.find_one({'uid': member.id})

      if getSv('rCave') in member.roles: return ''
	  
      try:
         mlist = udata['modelist']
         del mlist['caverna']
		  
         modes = [mode for mode, val in mlist.items() if val == 1]
		  
      except: # Never set modes
        udb.update_one({'uid': member.id}, {'$set': {'modelist': {
			'focused': 0,
			'pomodoro': 0,
			'studycycle': 0,
			'cave': 1
        }}})
        return ''
		  

      try:
        study, wait = udata['cycles']['pomodoro']
        pomodisp = f'{study}/{wait}'

      except: # If pomodoro not set, create one
        with open('jsons/usercycles.json', 'r') as file: ucycles = jload(file)
        ucycles['pomodoro'][str(member.id)] = {"📖 Study": 25, "💤 Rest": 5}
        with open('jsons/usercycles.json', 'w') as file: jdump(ucycles, file, indent=2)

        udb.update_one({'uid': member.id}, {
          '$set': {
            'cycles': {
              'pomodoro': [25, 5]
            }
          }
        })
        pomodisp = '25/5'

      connect_messages = {'focused': '🎯 Focused', 'pomodoro': f'🍅 Pomodoro {pomodisp}', 'studycycle': '📀 Custom cycle'}
      
      if oper != 'get':
        rFocus = getSv('rFocus')

        if 'focado' in modes or oper == 'focuschannel':
          if rFocus in member.roles: 
              await member.remove_roles(rFocus)
              await trueFocus(member, 'disable')

          else: 
              await member.add_roles(rFocus)
              await trueFocus(member)
      
  except: print(error())

  if modes: return '\n\n' + ', '.join([f'**{connect_messages[key]}**' for key in connect_messages.keys() if key in modes])
  else: return ''

async def nextCycle(uid, wait):
  await asleep(wait * 60)

  try:

    with open('jsons/callspomo.json', 'r') as file: calls = jload(file)

    ujson = calls[uid]
    cCalls = getSv('cCalls')

    msg = await cCalls.fetch_message(ujson[1])
    old_embed = msg.embeds[0]
    old_description = old_embed.description

    olde_split = old_description.replace('> ', '').split('\n')
    original_stats = olde_split[3:5]

    if any([word for word in pause_words if word in ujson[4].lower()]): # Add finished rest amount
      ujson[5] += ujson[3]

    current_modes = await detectModes(int(uid), 'get')

    with open('jsons/usercycles.json', 'r') as file: ucycles = jload(file)
    
    if 'Pomodoro' in current_modes: current_cycle = ucycles['pomodoro'][uid]
    elif 'Cycle' in current_modes: current_cycle = ucycles['custom_cycles'][uid][day_name()]

    ckeys = list(current_cycle.keys())
    
    if "CHECKPOINTED" in ckeys: ckeys.remove("CHECKPOINTED")

    try:
      ujson[4] = ckeys[ckeys.index(ujson[4]) + 1]
    except: # Cycle restarted
      if 'Cycle' in current_modes:
        old_embed.colour = 0x33FF33
        old_description = old_description.replace(':dvd:', ':dvd: <:yes:1132703714256359584>')

      ujson[4] = ckeys[0]


    ujson[2] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if 'Pomodoro' in current_modes: ujson[3] = current_cycle[ujson[4]] # Next status
    elif 'Cycle' in current_modes: 
      times = current_cycle[ujson[4]]
      ujson[3] = times[0] * 60 + times[1]

    replaces = ['**' + ujson[4] + '**', f'Ends **<t:{int((datetime.now() + timedelta(minutes=ujson[3])).timestamp())}:R>**']

    for i in range(len(replaces)):
      old_description = old_description.replace(original_stats[i], replaces[i])

    new_embed = Embed(
      description=old_description,
      colour=old_embed.colour
    )

    new_embed.set_thumbnail(url=old_embed.thumbnail.url)


    await msg.edit(embed=new_embed)
    ping = await cCalls.send(f'{ujson[4]} <@{uid}>')
    await ping.delete()

    task = asyncio.create_task(nextCycle(uid, ujson[3]))
    pomo_tasks[uid] = task

    with open('jsons/callspomo.json', 'w') as file: jdump(calls, file, indent=2)

  except: print(error())

async def calltime(uid, channel, chat, bot):
  try:
    readSet(int(uid), 'calls.stats', [[0, 0, 0, 0, 0, 0, 0], 0])
    
    statusday = ((datetime.now() - timedelta(hours=3)) - udb.find_one({'semday': {'$exists': True}})['semday']).days
    db = cdb

    suid = str(uid)

    with open('jsons/callspomo.json', 'r') as file: cpdb = jload(file)
    try:
      if suid in cdb:
        msgtimecounter = await chat.fetch_message(cdb[suid][1])

      elif suid in cpdb:
        msgtimecounter = await chat.fetch_message(cpdb[suid][1])

      await msgtimecounter.delete()

    except: pass

    guild = chat.guild
    inCave, cCamera, cFocus = getSv(['cCaveCalls', 'cCamera', 'cFocus'])

    try:
      userobj = await guild.fetch_member(int(uid))
    except:
      print(f'{uid} is an unknown member in calltime')

    if uid in camera_states: # Cancel camera detection timer
      await disableCameradetect(uid)

    if not userobj:
      try: del cdb[suid]
      except: pass
      try: del cpdb[suid]
      except: pass

      with open('jsons/calls.json', 'w') as file: jdump(cdb, file, indent=2)
      with open('jsons/callspomo.json', 'w') as file: jdump(cpdb, file, indent=2)

    if suid in cpdb: # Is a pomodoro
      ujson = cpdb[suid]

      if any([word for word in pause_words if word in ujson[4].lower()]): # If leave during pause, consider current pause as rested time
        ujson[5] += (datetime.now() - datetime.strptime(ujson[2], "%Y-%m-%d %H:%M:%S")).total_seconds() // 60

      if ujson[5] > 10: rest_time = f'\n> 💤 And rested **{timeString(ujson[5])}**'
      else: rest_time = ''

      start_time = datetime.strptime(ujson[0], "%Y-%m-%d %H:%M:%S") + timedelta(minutes=ujson[5]) # Discounting rested time
      totaltime = datetime.now() - start_time
      mins = totaltime.total_seconds() // 60

      try:
        pomo_tasks[suid].cancel()
        del pomo_tasks[suid]
      except: pass

      channel = ujson[6]

    else:
      rest_time = ''
      totaltime = datetime.now() - datetime.strptime(cdb[suid][0], "%Y-%m-%d %H:%M")
      mins = totaltime.total_seconds() // 60

    if channel == None: cinfo = ''
    elif chat == inCave: 
      cinfo = f' in your cave'
      await bot.get_channel(int(channel)).delete()
		
    else: cinfo = f' in <#{channel}>'

    if mins < 10:
      embed = Embed(
        description=f':warning: Stayed **less than 10 minutes**{cinfo}, so received no reward',
        colour=0xed3325,
      )

      delay = 10
    
      msg = await chat.send(f'<@{uid}> **This warning will disappear <t:{int((datetime.now() + timedelta(seconds=delay)).timestamp())}:R>**', embed=embed)
      await msg.delete(delay=delay)

    else:
      try: imgprof = userobj.avatar.url
      except: imgprof = 'https://assets.mofoprod.net/network/images/discord.width-250.jpg'

      if channel and not isinstance(channel, disnake.VoiceChannel) and int(channel) == cCamera.id:
        rew = round(mins * 0.041, 1)
        val = readSet(uid, 'blanks')
    
        valweek = readSet(uid, 'timed.week.blank')

        embed = Embed(
          description=f'ㅤ\nStudied for **{timeString(mins)}** in <#{channel}> with **camera on**\n{newBlank([val, rew])}',
          colour=0x0072DC,
        )
    
        udays = readSet(uid, 'calls.stats', [[0, 0, 0, 0, 0, 0, 0], 0])
        if type(udays) == dict:
          udays = [val for val in udays.values()]

        udb.update_one(
          {'uid': uid},
          {'$inc': {'blanks': rew, 'timed.week.blank': rew, 'timed.week.calls': mins, 'calls.totaltime': mins, 'calls.camera': mins, f'calls.stats.0.{statusday}': mins}, 
            '$max': {'calls.record': mins}
          }
        )

        try: await namedisplay(uid)
        except: print(error())
        
      else:
        rew = round(mins * 0.03, 1)
        val = readSet(uid, 'blanks')
    
        valweek = readSet(uid, 'timed.week.blank')

        embed = Embed(
          description=f'ㅤ\nStudied for **{timeString(mins)}**{cinfo}{rest_time}\n{newBlank([val, rew])}',
          colour=0x0072DC,
        )

        udays = readSet(uid, 'calls.stats', [[0, 0, 0, 0, 0, 0, 0], 0])
        if type(udays) == dict:
          udays = [val for val in udays.values()]

        udb.update_one(
          {'uid': uid},
          {'$inc': {'blanks': rew, 'timed.week.blank': rew, 'timed.week.calls': mins, 'calls.totaltime': mins, f'calls.stats.0.{statusday}': mins}, 
            '$max': {'calls.record': mins}
          }
        )

        try: await namedisplay(uid)
        except: print(error())

      if chat != inCave: embed.set_thumbnail(url=imgprof)
      else: embed.description = embed.description.replace('ㅤ\n', '')
        
      await chat.send(f'<@{uid}>', embed=embed)
    
    try: 
      del cdb[suid]
      with open('jsons/calls.json', 'w') as file: jdump(cdb, file, indent=2)
    except: # User is in cpdb
      try: 
        del cpdb[suid]
        with open('jsons/callspomo.json', 'w') as file: jdump(cpdb, file, indent=2)
      except: pass

    if channel and int(channel) == cFocus.id: asyncio.create_task(detectModes(userobj, 'focuschannel'))

  except: print(error())



async def callgrouptime(uid, channel, chat):
  try:  
    cid = str(channel.id)
	  
    cname = channel.name

    if 'Personal Cave' in cname: chat = getSv('cCaveCalls')

    try:
      msg = await chat.fetch_message(cgdb[cid]['msg'])
    except: return
		
    statusday = ((datetime.now() - timedelta(hours=3)) - udb.find_one({'semday': {'$exists': True}})['semday']).days
    readSet(int(uid), 'calls.stats', [[0, 0, 0, 0, 0, 0, 0], 0])
    del cgdb[cid]['msg']
    
  except: return


  endtime = datetime.now()
  times = [datetime.strptime(i, "%Y-%m-%d %H:%M") for i in list(cgdb[cid].values()) if isinstance(i, str)]

  times.append(endtime)

  try: await msg.delete()
  except: print(error())

  guild = channel.guild

  valid_users = [key for key in cgdb[cid].keys() if key.isdigit()]

  if '🎯' in cname: [asyncio.create_task(detectModes(int(u), 'focuschannel')) for u in valid_users] # Focused private room (All are in focus mode)
  else: [asyncio.create_task(detectModes(int(u))) for u in valid_users] # Normal situation (Only remove those with focus config enabled)


  cMusic = getSv('cMusic')
  [asyncio.create_task(simple_overwrite(u, cMusic, False)) for u in valid_users] # Disable music chat for everyone
	
  guild = channel.guild

  if ((times[len(times) - 1] - times[0]).total_seconds() / 60) < 10:
    embed = Embed(
      colour=0xed3325,
    )

    if len(times) - 1 > 1:
      embed.description = f'> :boom::anger: <@{uid}>\n> :gem: **Bonus: +0.0{len(times) - 2}** <:blank:1124439750208655500>**/min**\n▬▬▬▬▬▬▬▬▬▬▬▬\n:warning: Stayed **less than 10 minutes** connected to **{cname}**, so received no reward'
      await chat.send(', '.join([f'<@{i}>' for i in valid_users]), embed=embed)
      
    else:
      embed.description = f':warning: Stayed **less than 10 minutes** in **{cname}**, so received no reward'
      delay = 10 
      member_display = ', '.join([f'<@{i}>' for i in valid_users])
      msg = await chat.send(member_display + f' **This warning will disappear <t:{int((datetime.now() + timedelta(seconds=delay)).timestamp())}:R>**', embed=embed)
      await msg.delete(delay=delay)

    del cgdb[cid]
    with open('jsons/callgroups.json', 'w') as file: jdump(cgdb, file, indent=2)
    await channel.delete()
 
    return

  else:
    utimes, vault = '', 0.0
    for time in range(len(times)):
      rew = 0
      for i in range(time, len(times)):
        try:
          minterval = ((times[i + 1] - times[i])).total_seconds() // 60
          rew += (0.03 + i * 0.01) * minterval   
        except: break

      try:
        uid2 = int(valid_users[time])
        uvtime = (endtime - times[time]).total_seconds() // 60
  
        val = readSet(uid2, 'blanks')
		
        valweek = readSet(uid, 'timed.week.blank')
      
        utimes += f'<@{uid2}> studied **{timeString(uvtime)}**\n{newBlank([val, rew])}\n▬▬▬▬▬▬\n'

        if '💠' in cname:
          has_guild = udb.find_one({'uid': int(uid2), 'guild': {'$exists': True}})
			
          if has_guild:
            udb.update_one({'ugid': has_guild['guild']}, {'$inc': {'bank.blanks': rew * 0.2, f'bank.contributors.{uid2}': rew * 0.2}})
            vault += rew * 0.2
			  
        udb.update_one(
          {'uid': int(uid2)},
          {'$inc': {'blanks': rew, 'timed.week.blank': rew, 'timed.week.calls': uvtime, 'calls.totaltime': uvtime, f'calls.stats.0.{statusday}': uvtime}, 
          '$max': {'calls.record': uvtime}
          }
        )
		
      except: pass

      try: await namedisplay(int(uid2))
      except: pass

    utimes = utimes[:-7]

    if vault < 0.1: vdisp = ''
    else: vdisp = f'\n> <:guildvault:1233430694231932959> **Vault:** +{round(vault, 1)} <:blank:1124439750208655500>'
  
    if len(times) - 1 > 1:
      utimes = f'### {cname}\n> :boom::anger: <@{uid}>{vdisp}\n> :gem: **Bonus:** +0.0{len(times) - 2} <:blank:1124439750208655500>/min\n▬▬▬▬▬▬▬▬▬▬▬▬\n' + utimes
    else:
      utimes = f'### {cname}{vdisp}\n\n' + utimes
      
    embed = Embed(
      description=utimes,
      colour=0x5865F2,
    )

    if '💠' in cname: embed.set_thumbnail(url='https://media.discordapp.net/attachments/1223022126727041049/1225518032093446224/sala_guilda.png')
    elif '🎯' in cname: embed.set_thumbnail(url='https://media.discordapp.net/attachments/1223022126727041049/1225518031774416987/sala_foco.png')	
    else: embed.set_thumbnail(url='https://media.discordapp.net/attachments/1223022126727041049/1225518032332390470/sala_privada.png')

    await channel.delete()

    await chat.send((', '.join([f'<@{i}>' for i in cgdb[cid]])).replace(' <@guild>,', '').replace(' <@guild>', ''), embed=embed)

    del cgdb[cid]
    with open('jsons/callgroups.json', 'w') as file: jdump(cgdb, file, indent=2)



async def state(user, before, after, chats, bot, mode=''):
  if user.bot: return

  rCave, rFocus, cCaveCalls, cRoom, cCamera, cFocus, cFreearea_category, cCaveCalls, cMusic, rMusibot = getSv(['rCave', 'rFocus', 'cCaveCalls', 'cRoom', 'cCamera', 'cFocus', 'cFreearea_category', 'cCaveCalls', 'cMusic', 'rMusibot'])
	
  cCalls, cRoom, cGroup_category = chats
  guild = cCalls.guild
  uid = str(user.id)

  bcid, acid = None, None
  if after.channel is not None:
    acid = str(after.channel.id)
    if 'Personal Cave' in after.channel.name: 
      cCalls = cCaveCalls

  if before.channel is not None:
    bcid = str(before.channel.id)
    if 'Personal Cave' in before.channel.name: 
      cCalls = cCaveCalls

  if acid == str(cCamera.id) and not mode:
    embed = Embed(
      description=f'{user.mention} connected to <#{1136470255473000480}>.\n\n> **If you don\'t turn on the camera or share screen, you will be disconnected soon.**',
      colour=0xFFBD00
    )
    warn = await cCalls.send(embed=embed)
    task = asyncio.create_task(camera_state(user, 30, warn))
    camera_states[uid], camera_warn[uid] = task, warn
    return

  elif bcid and acid and before.channel == cRoom: return
	
  else:
    mode_texts, subject, pomo_studytime = await mode_format(user, acid, uid)

  try:
    if acid and after.channel.category == cFreearea_category: return
    elif bcid and before.channel.category == cFreearea_category: return

  except: pass

  try:
    with open('jsons/callspomo.json', 'r') as file: cpdb = jload(file)
    if bcid:
      if uid in cdb:
        await calltime(int(uid), bcid, cCalls, bot)
        return asyncio.create_task(detectModes(user))
      
      elif bcid in cgdb: return await callgrouptime(uid, before.channel, cCalls)
      
      elif uid in cpdb:
        if uid in ucycles['custom_cycles']:
          msg = await cCalls.fetch_message(cpdb[uid][1])

          current_stat = msg.embeds[0].description.replace('> ', '').split('\n')[3]

          ucycles['custom_cycles'][uid][day_name()]["CHECKPOINTED"] = current_stat.replace("**", "")
          with open('jsons/usercycles.json', 'w') as file: jdump(ucycles, file, indent=2)

        await calltime(int(uid), bcid, cCalls, bot)
        return asyncio.create_task(detectModes(user))
      

    try: imgprof = user.avatar.url
    except: imgprof = 'https://assets.mofoprod.net/network/images/discord.width-250.jpg'
        
    if acid == str(cRoom.id): # If user created a new private room
      overwrites = {
          guild.default_role: Dperms(connect=False),
          user: Dperms(connect=True),
          rMusibot: Dperms(connect=True),
          rCave: Dperms(view_channel=False),
          rFocus: Dperms(view_channel=False),     
      }


      embed = Embed(
        colour=0xffffff
      )

      # Check if has guild
      guild_user = udb.find_one({'uid': user.id})
      guild_room_exist, uguild = None, None
      try:
        uguild = udb.find_one({'ugid': guild_user['guild']})
        with open('jsons/callgroups.json', 'r') as file: cgdb3 = jload(file)
        guild_room_exist = [i2 for i in cgdb3.values() for i2 in i.values() if i2 == guild_user['guild']]
      except: pass

      if rCave in user.roles:
        vgchannel = await guild.create_voice_channel(f'🗻 ⋯ Personal Cave', category=cGroup_category, overwrites=overwrites)

        embed.description = f'### **{vgchannel.name}**\n{user.mention} entered their cave **<t:{int(datetime.now().timestamp())}:R>**{mode_texts}'

        started = await cCaveCalls.send(embed=embed)
        asyncio.create_task(detectModes(user))

        if 'Pomodoro' in mode_texts or 'Cycle' in mode_texts: # If using a pomodoro
          with open('jsons/callspomo.json', 'r') as file: cpdb = jload(file)

          try:
            if 'Cycle' in mode_texts: pomo_studytime = pomo_studytime[0] * 60 + pomo_studytime[1]

            cpdb[uid] = [datetime.now().strftime("%Y-%m-%d %H:%M:%S"), started.id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), pomo_studytime, subject, 0, vgchannel.id]
            with open('jsons/callspomo.json', 'w') as file: jdump(cpdb, file, indent=2)

          except: # Study cycle not defined for current day
            cdb[uid] = [datetime.now().strftime("%Y-%m-%d %H:%M"), started.id]
            with open('jsons/calls.json', 'w') as file: jdump(cdb, file, indent=2)
        
        else:
          cdb[uid] = [datetime.now().strftime("%Y-%m-%d %H:%M"), started.id]
          with open('jsons/calls.json', 'w') as file: jdump(cdb, file, indent=2)

        return await user.move_to(vgchannel)

      elif uguild and not guild_room_exist: # This guild's room doesn't exist yet
        uguild_role = guild.get_role(uguild['guild_role'])

        overwrites = {
          guild.default_role: Dperms(connect=False),
          user: Dperms(connect=True),
          rMusibot: Dperms(connect=True),
          uguild_role: Dperms(connect=True),
          rCave: Dperms(view_channel=False),
          rFocus: Dperms(view_channel=False)
        }
		  
        vgchannel = await guild.create_voice_channel(f'💠 ⋯ {uguild["guild_name"]}', category=cGroup_category, overwrites=overwrites)
        await asleep(0.5)
        await vgchannel.edit(position=0)

        embed.description = f'### **{vgchannel.name}**\n{user.mention} created the room **<t:{int(datetime.now().timestamp())}:R>**\n▬▬▬▬▬▬▬▬▬▬▬▬\n> **Only members of <@&{uguild["guild_role"]}> can connect**'

        embed.set_thumbnail(url='https://media.discordapp.net/attachments/1223022126727041049/1225518032093446224/sala_guilda.png')
       
        started = await cCalls.send(embed=embed)

        await simple_overwrite(user, cMusic)
		
      else:
        try: uroom_name = next(i for i in user.display_name.split(" ") if i.isaplha()).capitalize()
        except: uroom_name = user.display_name.split(" ")[0]

        modes = await detectModes(user, 'get')

        cdisplay = f'🔒 ⋯ Sala de {uroom_name}'
        if 'Focado' in modes: 
          cdisplay = cdisplay.replace('🔒', '🎯')
          embed.set_thumbnail(url='https://media.discordapp.net/attachments/1223022126727041049/1225518031774416987/sala_foco.png')
        else:
          embed.set_thumbnail(url='https://media.discordapp.net/attachments/1223022126727041049/1225518032332390470/sala_privada.png')

        vgchannel = await guild.create_voice_channel(cdisplay, category=cGroup_category, overwrites=overwrites)

        try: 
          await asleep(0.5)
          fcave_pos = next(cave_pos for cave_pos, channel in enumerate(cGroup_category.channels) if '🗻' in channel.name)
          await vgchannel.edit(position=fcave_pos)
        except: pass

        embed.description = f'### **{vgchannel.name}**\n{user.mention} criou a sala **<t:{int(datetime.now().timestamp())}:R>**\n▬▬▬▬▬▬▬▬▬▬▬▬\nConvide pessoas com `/room` e aumente a recompensa da sala{mode_texts}'

        started = await cCalls.send(embed=embed)
        if 'Focado' not in modes: asyncio.create_task(detectModes(user))

        await simple_overwrite(user, cMusic)



      if uguild and not guild_room_exist and rCave not in user.roles: # Se não existe uma sala de guilda mas tem um usuário da guilda, crie uma
        cgdb[str(vgchannel.id)] = {uid: datetime.now().strftime("%Y-%m-%d %H:%M"), 'msg': started.id, 'guild': guild_user['guild']}

      else: # Padrão
        cgdb[str(vgchannel.id)] = {uid: datetime.now().strftime("%Y-%m-%d %H:%M"), 'msg': started.id}

      with open('jsons/callgroups.json', 'w') as file: jdump(cgdb, file, indent=2)
      await user.move_to(vgchannel)
      return asyncio.create_task(detectModes(user))

    elif acid not in cgdb and acid is not None: # Se não for uma sala privada, é uma sala comum     
      if int(acid) == cFocus.id and 'Focado' not in mode_texts: mode_texts = '\n\n**🎯 Focado**' + mode_texts

      if not mode_texts: centralize = 'ㅤ\n' # Sem ciclos de estudo
      else: centralize = ''

      embed = Embed(
        description=f'{centralize}{user.mention} se conectou a <#{after.channel.id}>\n**<t:{int(datetime.now().timestamp())}:R>**{mode_texts}',
        colour = 0xffffff
      )

      embed.set_thumbnail(url=imgprof)

      started = await cCalls.send(embed=embed)

      if int(acid) == cFocus.id: asyncio.create_task(detectModes(user, 'focuschannel'))
      else: asyncio.create_task(detectModes(user))

      if 'Pomodoro' in mode_texts or 'Ciclo' in mode_texts: # Se estiver usando um pomodoro
        with open('jsons/callspomo.json', 'r') as file: cpdb = jload(file)

        try:
          if 'Ciclo' in mode_texts: pomo_studytime = pomo_studytime[0] * 60 + pomo_studytime[1]

          cpdb[uid] = [datetime.now().strftime("%Y-%m-%d %H:%M:%S"), started.id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), pomo_studytime, subject, 0, acid]
          with open('jsons/callspomo.json', 'w') as file: jdump(cpdb, file, indent=2)
          return

        except: # Ciclo de estudos não definido para o dia atual
          cdb[uid] = [datetime.now().strftime("%Y-%m-%d %H:%M"), started.id]
      
      else:
        cdb[uid] = [datetime.now().strftime("%Y-%m-%d %H:%M"), started.id]
    
    elif acid in cgdb and uid not in cgdb[acid]: # Se user entrar numa sala privada existente
      cgdb[acid][uid] = datetime.now().strftime("%Y-%m-%d %H:%M")
      msg = await cCalls.fetch_message(cgdb[acid]['msg'])

      old_embed = msg.embeds[0]
		
      desc = old_embed.description
      embed = Embed(
        description=f'{desc.split("▬▬▬▬▬▬▬▬▬▬▬▬")[0]}<@{uid}> se conectou **<t:{int(datetime.now().timestamp())}:R>**\n▬▬▬▬▬▬▬▬▬▬▬▬\n:gem: **Bônus:** +0.0{len(cgdb[acid]) - 2} <:blank:1124439750208655500>/min',
        colour=0xffffff,
      )
      embed.set_thumbnail(url=old_embed.thumbnail.url)
		
      await msg.edit(embed=embed)
		
      with open('jsons/callgroups.json', 'w') as file: jdump(cgdb, file, indent=2)

      if '🎯' in desc: asyncio.create_task(detectModes(int(uid), 'focuschannel'))
      else: asyncio.create_task(detectModes(int(uid)))

      await simple_overwrite(user, cMusic)
		
      return 

    with open('jsons/calls.json', 'w') as file: jdump(cdb, file, indent=2)
  except Exception as e: print(f'callenter -> {error()}')
        
    
      
  
  with open('jsons/calls.json', 'w') as file: jdump(cdb, file, indent=2)

async def callUpdate(cCalls, bot):
  guild = cCalls.guild
  cCalls, cRoom, cGroup_category = getSv(['cCalls', 'cRoom', 'cGroup_category'])

  class vchannel:
    def __init__(self, channel):
        self.channel = channel

  vgids = [j for i in list(cgdb.values()) for j in i if j.isdigit()]

  with open('jsons/callspomo.json', 'r') as file: cpdb = jload(file)
	  
  okchannel = [] # Lista dos usuarios que já estavam on no canal de voz
  for channel in guild.voice_channels: # Se o membro tiver entrado no canal de voz durante o reset
    for member in channel.members:
      if str(member.id) not in cdb and not member.bot and str(member.id) not in cgdb and str(member.id) not in cpdb:
        await state(member, vchannel(None), vchannel(channel), [cCalls, cRoom, cGroup_category], bot)
        
      okchannel.append(member.id)
            

  try: # Se o membro tiver saído do canal de voz durante o reset
    cgdb2 = jloads(jdumps(cgdb)) 
    for vgid in cgdb2:
      for uid in cgdb2[vgid]:
        if uid.isdigit() and int(uid) not in okchannel:
          await callgrouptime(uid, bot.get_channel(int(vgid)), cCalls)

    cdbs = jloads(jdumps({**cdb, **cpdb})) # Mistura dos canais normais com os no modo pomodoro
    for uid in cdbs:
      if int(uid) not in okchannel:
        await calltime(uid, bot.get_channel(cdbs[uid][1]), cCalls, bot) 
        userobj = await guild.fetch_member(int(uid))
        await detectModes(userobj)

    cpdb2 = jloads(jdumps(cpdb)) 
    for uid in cpdb:
      if int(uid) in okchannel: # Recalibrar os timings dos pomodoros
        started_cycle = datetime.strptime(cpdb[uid][2], "%Y-%m-%d %H:%M:%S")

        time_elapsed = datetime.now() - started_cycle
        time_elapsed_minutes = time_elapsed.total_seconds() / 60

        task = asyncio.create_task(nextCycle(uid, cpdb[uid][3] - time_elapsed_minutes))
        pomo_tasks[uid] = task

		  
  except Exception as e: print(f"Ante reset -> {e} {error()}")
  
async def invGroup(user):
  invgroup = 0
  uid = str(user.id)
  for vgid in cgdb:
    for uid in cgdb[vgid]:
      if uid.isdigit() and int(uid) == user.id:
        return vgid
          
  return invgroup

async def camera_state(user, time, msg): # Tirar o usuario da call se não ativar a câmera
  try:
    await asleep(time)

    channel = msg.channel

    embed = Embed(
      description=':warning::camera: **Você foi desconectado desse canal porque não ativou a câmera nem compartilhou tela**',
      colour=0xFFBD00
    )

    try: 
      await user.move_to(None)
      await msg.delete()
 
    except: pass

    new_msg = await channel.send(f'{user.mention} **Esse aviso sumirá <t:{int((datetime.now() + timedelta(seconds=10)).timestamp())}:R>**', embed=embed)
    await new_msg.delete(delay=10)
  except: print(error())
  