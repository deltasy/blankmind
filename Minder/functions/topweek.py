import disnake
from asyncio import sleep as asleep

from functions.time import timeString
from functions.page1 import getSv

from mongo import udb, readSet
from traceback import format_exc as error

async def topweek(bot):	
  chat = bot.get_channel(1157769760642171023)

  try:
    calls = list(udb.find({'timed.week.calls': {'$gt': 0}}).sort('timed.week.calls', -1))[:6]
    blanks = list(udb.find({'timed.week.blank': {"$gt": 0}}).sort('timed.week.blank', -1))[:6]

    def included(categs):
      for catnum in range(len(categs)):
        try:
          for i in range(3):
            if categs[catnum][0]['uid'] == categs[catnum + 1][i]['uid']:
              categs[catnum + 1].pop(i)
        except: break

    # Verificar se um rei está em outro pódio e vise versa
    included([calls, blanks])
    included([blanks, calls])
	  
    blank_titles = ['### <:king_crown:1157866006111342592> `REI`', '<:prince_crown:1157865761495326792> **`Príncipe`**', '<:duque_crown:1157865784371064892>  **`Duque`**']
    call_titles = ['### <:king_crown:1157866006111342592> `REI`', '<:prince_crown:1157865761495326792> **`Príncipe`**', '<:duque_crown:1157865784371064892>  **`Duque`**']
    call_rank, blank_rank = '', ''

    guild = chat.guild
    role_id = guild.get_role(1148017066096463892)

    kings = udb.find_one({'semday': {'$exists': True}})['kings']



    rank_lists = [calls, blanks]
    for rlist in range(len(rank_lists)):
      try:
        if rank_lists[rlist][0]['uid'] != kings[rlist]:
          try:
            old_king = await guild.fetch_member(kings[rlist])
            await old_king.remove_roles(role_id)
          except: pass
          try:
            new_king = await guild.fetch_member(rank_lists[rlist][0]['uid'])
            await new_king.add_roles(role_id)
          except: pass
      except: pass

    try:
      udb.update_one({'semday': {'$exists': True}}, {
        '$set': {
          'kings.0': calls[0].get('uid'),
          'kings.1': blanks[0].get('uid')
        }
      }) 
    except: pass

    c = 0
    for users in calls:
      if users['timed']['week']['calls'] == 0: 
        blank_rank += "~ Vago"
        break

      call_rank += f"{call_titles[c]} <@{users['uid']}> ➜ **{timeString(users['timed']['week']['calls'], 'simple')}**\n"
      c += 1
      if c == 3: break

    c = 0
    for users in blanks:
      if users['timed']['week']['blank'] == 0: 
        blank_rank += "~ Vago"
        break
	
      blank_rank += f"{blank_titles[c]} <@{users['uid']}> ➜ **{round(users['timed']['week']['blank'], 1)}** <:blank:1124439750208655500>\n"
      c += 1
      if c == 3: break

    status = udb.find_one({'semday': {'$exists': True}})
    week = status['number']
    day = (status['today'] - status['semday']).days
    
    embed = disnake.Embed(
      description=f"# NOBRES DA SEMANA\n> **Semana {week} / Dia {day + 1}**\n▬▬▬▬▬▬▬▬▬▬▬▬▬\n# :loudspeaker:  Tempo em calls\n" + call_rank + "\n▬▬▬▬▬▬▬▬▬▬▬▬▬\n# <:blank:1124439750208655500> Blanks ganhos\n" + blank_rank,
      colour=0xfff400
    )
    await chat.purge(limit=1)
    await chat.send(embed=embed)
    
  except: print(error())
