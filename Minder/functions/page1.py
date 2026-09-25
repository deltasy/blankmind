from disnake import utils as Dutils, ButtonStyle as Dbtn_color, ui as Dui
from disnake import PermissionOverwrite as Dperms
from json import load as jload

from asyncio import sleep as asleep
from traceback import format_exc as error

import disnake

import pymongo
from mongo import udb, readSet

def getSv(bot):
  global cCalls, cRoom, cGroup_category, cPen, cDisplays, cCommands, cInvites, cWelcome, cLeave, cBumps, cNotifys, cRels, cReqbook, guild, rCave, cCaveCalls, cChat, cMembers, rFocus, cEnem, cVest, cConp, cConm, rFun, r1, r2, r3, rVestibulando, rFac, c1, c2, c3, cFun, cFac, cVestibulando, rEnem, rVest, rConp, rConm, cBoosters, rBooster, cIntros, cWrite
  global rRelator, rSearcher, truefocus_roles, truefocus_chats, cPaleShield, rPaleShield, cRecruit
  global cIdea, cReport, cPalemain, palerequired, cShelf
	
  if isinstance(bot, str):
    return globals().get(bot, None)
  elif isinstance(bot, list):
    return [globals().get(var, None) for var in bot]
  else: 
    cShelf = bot.get_channel(1238934620163276861)
    cChat = bot.get_channel(1093630384174006282)
    cRoom = bot.get_channel(1126180695019102208)
    cCalls = bot.get_channel(1109998084718612530)
    cPen = bot.get_channel(1119383275320909896)
    cDisplays = 1126222142883766352 
    cCommands = bot.get_channel(1138573308837777568)
    cGroup_category = Dutils.get(cCalls.guild.categories, id=1207442864477577257)
    cInvites = bot.get_channel(1119719224160551063)
    cWelcome = bot.get_channel(1101311176597569657)
    cLeave = bot.get_channel(1100117223600816219)
    cBumps = bot.get_channel(1112018256564326480)
    cNotifys = bot.get_channel(1133474876003459112)
    cRels = bot.get_channel(1135738380555137084)
    cReqbook = bot.get_channel(1197315979710046288)
    cIdea = bot.get_channel(1123771863802335332)

    cMembers = bot.get_channel(1211478899435896832)

    guild = bot.get_guild(1091742896098660372)

    rCave = guild.get_role(1207830254870331412)
    rFocus = guild.get_role(1134644151883943937)

    cCaveCalls = bot.get_channel(1207835219755794432)
	
    rFun = guild.get_role(1115750314679730207)
    r1 = guild.get_role(1115751050041888931)
    r2 = guild.get_role(1115751059692986608)
    r3 = guild.get_role(1115751063610470581)
    rFac = guild.get_role(1115751360344887316)
    rVestibulando = guild.get_role(1143697792158666856)

    rVest = guild.get_role(1178026381586739211)
    rConp = guild.get_role(1207455384671883395)
    rConm = guild.get_role(1207455386874150963)
    rEnem = guild.get_role(1178025309589745665)

    cEnem = bot.get_channel(1178045729797837000)
    cVest = bot.get_channel(1178045822391291984)
    cConp = bot.get_channel(1178045915030880356)
    cConm = bot.get_channel(1144425598928826368)
	  
    c1 = bot.get_channel(1143699549035188376)
    c2 = bot.get_channel(1143699599576535212)
    c3 = bot.get_channel(1143699644275228793)
    cVestibulando = bot.get_channel(1143699775154311268)
    cFac = bot.get_channel(1143699722138300447)
    cFun = bot.get_channel(1143699345561100298)

    cBoosters = bot.get_channel(1219802539889787020)
    rBooster = guild.get_role(1160147235330330664)

    cIntros = bot.get_channel(1124455706309963817)
    cWrite = bot.get_channel(1174127784189239377)

    rRelator = guild.get_role(1092918220400369775)
    rSearcher = guild.get_role(1174146227961614467)

    cPaleShield = bot.get_channel(1230638850091782194)
    rPaleShield = guild.get_role(1226674268159610891)

    cChats = bot.get_channel(1138573291829858366)

    cReport = bot.get_channel(1238155003651166271)
    cPalemain = bot.get_channel(1226678712280420352)

    cRecruit = bot.get_channel(1226679492609704038)

    rInsano = guild.get_role(1143937396027699352)
    rMestre = guild.get_role(1168640140395163728)
    rLenda = guild.get_role(1199039648828235857)
    rSupremo = guild.get_role(1231649305362694216)

    palerequired = [rInsano, rMestre, rLenda, rSupremo]
	  
    truefocus_roles = [rFun, r1, r2, r3, rVestibulando, rFac, rEnem, rVest, rConm, rConp, rBooster]
    truefocus_chats = [cFun, c1, c2, c3, cVestibulando, cFac, cEnem, cVest, cConm, cConp, cBoosters]


async def idealist_repo(mode='edit'):
  with open('jsons/marks.json', 'r') as file: marks = jload(file)

  desc = {}
  activeid_ideas = [int(idea.split('idea ')[1]) for idea in marks.keys() if 'idea' in idea]
  for idea_key in activeid_ideas:
    skey = 'idea ' + str(idea_key)
		  
    nvotes = sum(1 for vote in marks[skey]["votes"].values() if vote == "no")
    yvotes = sum(1 for vote in marks[skey]["votes"].values() if vote == "yes")

    if nvotes < yvotes: emdisplay = '<:approve:1217860414465904803>'
    elif nvotes > yvotes: emdisplay = '<:disapprove:1217860350943432785>'
    else: emdisplay = '<:waiting_votes:1217925376920129666>'

    if nvotes + yvotes == 1: pl = ''
    else: pl = 's'

    desc[f'{emdisplay} https://discord.com/channels/1091742896098660372/1123771863802335332/{idea_key} **({nvotes + yvotes} Voto{pl})** <@{marks[skey]["created_by"]}>'] = nvotes + yvotes

  desc = sorted(desc, key=lambda key: desc[key])[::-1]
	  
  desc[0] = '# <:idea_chart:1217856573620097075> Votações abertas\n<a:top_ideas:1233112726377599128>' + desc[0]
  desc[1] = '<a:top_ideas:1233112726377599128>' + desc[1]
  desc[2] = '<a:top_ideas:1233112726377599128>' + desc[2] + '\n▬▬▬▬▬▬▬▬▬▬▬▬▬'

	  
  iembed = disnake.Embed(
    description='\n'.join(desc)
  )

  if mode == 'spawn': await cIdea.send(embed=iembed)
  else:
    idealist = await cIdea.history(limit=1).flatten()
    msg = idealist[0]
	  
    await msg.edit(embed=iembed)

async def agetSv(bot):
  global mIntros
  
  if isinstance(bot, str):
    return globals().get(bot, None)
  elif isinstance(bot, list):
    results = []
    for var in bot:
      results.append(globals().get(var, None))
    return results
  else: 
    mIntros = [msg async for msg in cIntros.history(limit=None) if guild.get_member(msg.author.id)]


async def trueFocus(user, mode='activate'):
  if mode == 'activate':
    for pos, role in enumerate(truefocus_roles):
      if role in user.roles:

        current_overwrite = truefocus_chats[pos].overwrites_for(user)
        current_overwrite.update(view_channel=False)

        # Define as novas permissões para o usuário
        await truefocus_chats[pos].set_permissions(user, overwrite=current_overwrite)

  else:
    for pos, role in enumerate(truefocus_roles):
      if role in user.roles: 
        await truefocus_chats[pos].set_permissions(user, overwrite=None)

botnick_change = []
async def namedisplay(user):
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
      roles = [1199075408759509062, 1, 1199075405731217539, 1199075398735114391]

      selected = False
      for num, id in enumerate(roles):
        try:
          role = guild.get_role(id)

          if role in user.roles:
            udb.update_one({'uid': user.id}, {'$set': {'linked_stat': num}})
            await user.remove_roles(role)
            ustat = num
            selected = True
			  
        except: print(error())

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
  
async def notify(user, opername, oper="btn", inter=0):
  try:
    simb = {
      "dmrel": ["🔔 Ativar", "🔕 Desativar"],
      "color": [Dbtn_color.success, Dbtn_color.danger]
    }


    if oper == "verify": # Se for só para verificar
      readSet(user.id, 'notifys.rsend', 1)
      search = udb.find_one({'uid': user.id})
      return search['notifys']['rsend']
      
    else:
      readSet(user.id, 'notifys.rsend', 1)
      udb.update_one(
        {'uid': user.id},
        {'$bit': {'notifys.rsend': {'xor': 1}}}
      )
      notify = udb.find_one({'uid': user.id})['notifys']['rsend']
  
      endi = notify
      if inter != 0:
        button = Dui.Button(
          label=simb[opername][endi], 
          style=simb["color"][endi], 
          custom_id="dmrel_mode"
        )
        await inter.message.edit(components=[button])
  
      try: await inter.response.send_message()
      except: await asleep(5)
        
  except Exception as e: print(f'Notify -> {error()}')

async def tempMsg(msg, content, user, mode=True):
  try:
    if len(user) > 1:
      user = ', '.join([f'<@{i}>' for i in user])
    elif '@' not in user[0]: 
      user = f'<@{user[0]}>'
    else:
      user = user[0]

    try: # Se message for realmente uma mensagem
      message = await msg.edit(user, embed=content)
    except: # Se message for um chat
      message = await msg.send(user, embed=content)
	  
    if mode == True:
      await message.delete(delay=15)
  except: 
    print(error())
    pass

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
      await inter.response.send_message(f"**Utilize esse comando só no canal <#{cid[0]}>**!", ephemeral=True)
		
    else:
      await inter.response.send_message(f"**Utilize esse comando só no canal <#{cid}>**!", ephemeral=True)
	  
    return True

  else:
    return False

async def pingUser(uid, chat='cCalls'):
	chat = getSv(chat)
	if type(uid) == list:
		if len(uid) > 1: msg = ', '.join([f'<@{i}>' for i in uid])
		else: msg = f'<@{uid[0]}>'
	else:
		msg = f'<@{uid}>'
	ping = await chat.send(msg)
	await ping.delete()