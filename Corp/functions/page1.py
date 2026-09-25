from disnake import utils as Dutils, ButtonStyle as Dbtn_color, ui as Dui
from disnake import PermissionOverwrite as Dperms

from asyncio import sleep as asleep
from traceback import format_exc as error

import disnake

import pymongo
from mongo import udb, readSet

def getSv(bot):
  global cGuilds, guild, cCommands_MPnull, cCommands_MPlow, cCommands_MPmed, cCommands, cChat, rFocus
  
  if isinstance(bot, str):
    return globals().get(bot, None)
  elif isinstance(bot, list):
    results = []
    for var in bot:
      results.append(globals().get(var, None))
    return results
  else: 
    cGuilds = bot.get_channel(1126331167084388372)
    guild = cGuilds.guild
    cChat = bot.get_channel(1093630384174006282)


    cCommands = bot.get_channel(1138573308837777568)
    cCommands_MPnull = bot.get_channel(1230908463865921546)
    cCommands_MPlow = bot.get_channel(1230908448430882866)
    cCommands_MPmed = bot.get_channel(1230908501858058362)

    rFocus = guild.get_role(1134644151883943937)

botnick_change = []
async def namedisplay(user):
  global guild

  field_stat = {0: 'Nenhum', 1: 'CUSTOMIZADO', 2: 'blanks', 3: 'calls.totaltime', 4: 'bumps'}

  if not isinstance(user, disnake.Member):
    user = await guild.fetch_member(int(user))

  udata = udb.find_one({'uid': user.id})
  ustat = udata['linked_stat']

  cavemode = None
  try: cavemode = udata['cavemode']
  except: pass
	
  if ustat == 0 and not cavemode: 
    if '═' in user.display_name:
      botnick_change.append(user)
      await user.edit(nick=user.display_name.split(' ═ ')[0].replace(' ?', '').replace('═', ''))
     
    return

  elif ustat != 100:
    if type(ustat) != str: value = readSet(user.id, field_stat[ustat], 0)
    else: # Se for um status customizado
      botnick_change.append(user)
      uprevious = ' '.join(user.display_name[:32 - 3 - len(ustat)].split('═')[0].split())
      return await user.edit(nick=uprevious + ' ═ ' + ustat)

  try:
    if not isinstance(user, disnake.Member):
      user = await guild.fetch_member(int(user))

    if ustat == 100:
      roles = [1199075408759509062, 1199075405731217539, 1199075398735114391]

      selected = False
      for num, id in enumerate(roles):
        role = guild.get_role(id)

        if role in user.roles:
          udb.update_one({'uid': user.id}, {'$set': {'linked_stat': num}})
          await user.remove_roles(role)
          ustat = num
          selected = True

      if not selected: 
        botnick_change.append(user)
        return await user.edit(nick=user.display_name[:32 - 6] + ' ═ ?')
      elif ustat == 0:
        botnick_change.append(user)
        return await user.edit(nick=user.display_name.replace(' ═ ?', ''))

    if cavemode:
      bstring = f' ═ {cavemode}' 

    elif ustat == 2:   
      bstring = f' ═ {round(value, 1)}'
	  
    else:
      if ustat == 3:
        try: 
          value = int(value) // 60
        except: 
          value = readSet(user.id, 'calls.totaltime', 0)
          value = int(value) // 60
          print(f'Namedisplay -> Erro no valor de {user.id} (ustat 2)')

      bstring = f' ═ {int(value)}'

    if cavemode: 
      bstring += ' dia'
      if cavemode> 1: bstring += 's'

    elif ustat == 2: bstring += ' 𝔅'
    elif ustat == 3: bstring += 'h'
    elif ustat == 4: bstring += ' Bumps'

    if ' ═ ' in user.display_name: div = ' ═ '
    else: div = '═ '
      
    uname = user.display_name[:32 - len(bstring) - 2].split(div)[0] + bstring

    botnick_change.append(user)
    try: await user.edit(nick=uname)
    except: pass
  except: print(error())
  
def newBlank(vals, mode="+"):
  total, reward = vals
  reward = round(reward, 1)
  
  if reward < 3:
      emoji = '<:blank:1124439750208655500>'
  elif reward < 8:
      emoji = '<:blanks:1124438972144295936>'
  else:
      emoji = '<:blankbag:1124445117261037630>'
  
  if mode == "-":
    return f'<:no:1132703732543529000> **Perdeu {reward}** {emoji}' #|  Total: __{round(total - reward, 1)}__** <:blank:1124439750208655500>'
  elif mode == 'g':
    return f':credit_card: **Gastou {reward}** {emoji}' #|  Total: __{round(total - reward, 1)}__** <:blank:1124439750208655500>'
  else:
    return f'<:yes:1132703714256359584> **Ganhou {reward}** {emoji}'# | #Total: __{round(total + reward, 1)}__** <:blank:1124439750208655500>'



async def specChannel(inter, cid=[1107757022503510147, 1207833725786787860, 1100117223600816219]):
  if inter.channel.id not in cid:   
    if type(cid) == list:
      await inter.response.send_message(f"**Utilize esse comando só no canal <#{1107757022503510147}>**!", ephemeral=True)
		
    else:
      await inter.response.send_message(f"**Utilize esse comando só no canal <#{cid}>**!", ephemeral=True)
	  
    return True

  else:
    return False