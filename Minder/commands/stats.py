import disnake
from disnake.ext import commands as com
from functions.page1 import specChannel
from traceback import format_exc as error
from datetime import datetime, timedelta
from typing import Optional
import asyncio
import gc

from functions.time import timeString, timeFormat
from functions.page1 import getSv

from mongo import udb, readSet



global mpbar
mpbar = ['<:MPS_L:1230951553825771520><:MP_N:1230949545265987656><:MP_N:1230949545265987656><:MPE_N:1230960976816242728>', 
		 '<:MPS_M:1230951569512464384><:MP_M:1230949600798703729><:MP_N:1230949545265987656><:MPE_N:1230960976816242728>',
		 '<:MPS_H:1230951582368268319><:MP_H:1230949617668067379><:MP_H:1230949617668067379><:MPE_N:1230960976816242728>',
		 '<:MPS_F:1230955228954890442><:MP_F:1230954943180050604><:MP_F:1230954943180050604><:MPE_F:1230954925387681823>'
		 ]



def command(client):  
  @client.slash_command(name="stats")
  async def sstats(
    inter: disnake.ApplicationCommandInteraction,
    meta = ''
  ):
    """
    ✨┃Mostra suas estatísticas
    Parameters
    ----------
    meta: 🕗 Formato ➜ horas:minutos
    """
    if await specChannel(inter): return
    if meta != '':
      try:
        horas, minutos = list(map(int, meta.replace(' ', '').split(':')))
        total = horas * 60 + minutos
        if total < 10:
          return await inter.response.send_message("**A meta deve ser de, no mínimo, 10 minutos**", ephemeral=True)
        elif total >= 1440:
          return await inter.response.send_message("**Que loucura é essa? como sua meta diária ultrapassa 24h? :face_with_raised_eyebrow:**", ephemeral=True)
          
        udb.update_one({'uid': inter.author.id}, {
          '$set': {'calls.stats.1': total}
        })
  
        return await inter.response.send_message(f'**Sua meta diária agora é:** {timeString(total)}', ephemeral=True)
      except:
        print(error())
        return await inter.response.send_message("**Formato inválido!** tente novamente", ephemeral=True)
        
    else:     
      await showStatus(inter)

    # Enviar o embed com o gráfico como imagem
    #await inter.edit_original_message(embed=embed, components=[disnake.ui.Button(label="🔕 Desativar", style=disnake.ButtonStyle.danger, custom_id="ta")])


  global top_opts
  top_opts = {"Poder de cronocard": 0, "Blanks": 1, "Calls": 2, "Calls com câmera": 3, "Produções": 4, "Bumps": 5, "Convites": 6}
  @client.slash_command(name="top")
  async def stop(
      inter: disnake.ApplicationCommandInteraction,
      categoria: com.option_enum(top_opts) = 0
  ):
    """
    🏆┃Mostra os estudantes mais dedicados
    """
    try:
      if await specChannel(inter): return
        
      await ranking(inter, client, ['GLOBAL', categoria], 'normal', top_opts)
    except: pass#print(error())







global levels
levels = [
  'nada',
  1093543202105077792,
  1122230870460342412,
  1132163320179339344,
  1135629912770891816,
  1143937396027699352,
  1168640140395163728,
  1199039648828235857,
  1231649305362694216
]
level_icons = [
  '',
  '',
  '<:Ambicioso:1231657391620358265> ',
  '<:Amador:1231657353242345542> ',
  '<:Experiente:1231657323429363722> ',
  '<:Insano:1231657289081946143> ',
  '<:Mestre:1231657249693372624> ',
  '<:Lendaviva:1231657160455360532> ',
  '<:SUPREMO:1231657119091134565> '
]


async def showStatus(inter, client='', mode='summon', stats='calls'):
  uobj = inter.author
  guild = uobj.guild

  embed = disnake.Embed(
    colour=disnake.Color.blue()
  )

  if stats != 'calls': embed.set_image(file=disnake.File('images/null.png', filename='null.png'))
  
  try: imgprof = uobj.avatar.url
  except: imgprof = 'https://assets.mofoprod.net/network/images/discord.width-250.jpg'
      
  embed.set_author(
    name=f'{uobj.name} - {stats.capitalize()}',
    icon_url=imgprof
  )

  user = udb.find_one({'uid': uobj.id})

  try:
    if stats == 'calls':
      udays = readSet(uobj.id, 'calls.stats', [[0, 0, 0, 0, 0, 0, 0], 0])
      
    
      if type(udays) == dict:
        udays = [val for val in udays.values()]

      await inter.response.defer()
      
      uhours = []
      
      uhours = [hour for hour in udays[0]]

      semday = udb.find_one({'semday': {'$exists': True}})['semday']
      days = [f'{timeFormat((semday + timedelta(days=day)).day, "date")}/{timeFormat(((semday + timedelta(days=day)).month))}' for day in range(len(udays[0]))]

      semday_display = []

      for i in range(len(days)):
        if uhours[i] == 0:
          semday_display.append(f'-')
          msimbol = ''
        else:
          try:
            if uhours[i] == max(uhours): 
              msimbol = ':star:'

            elif udays[1] > 0:
              if uhours[i] >= udays[1]: msimbol = '<:yes:1132703714256359584>'
              else: msimbol = '<:no:1132703732543529000>'

            else:
              msimbol = ''
				
	
          except:
            msimbol = ''
          semday_display.append(f'{msimbol} **({days[i]}) ➜** {timeString(uhours[i], "simple")}')
		  
      semday_display = '\n'.join(semday_display)

      """
      try:
          meta = udays[1]
      except:
          meta = 9999
  
      colors, usimbols = [], []
      for valor in udays[0]:
        if valor == max(udays[0]) and valor != 0:
          usimbols.append('★')
          colors.append('gold')
        elif valor < meta or valor == 0:
          if valor != 0:
            usimbols.append('○')
          else:
            usimbols.append('')
          colors.append('gray')
        else:
          usimbols.append('●')
          colors.append('royalblue')

      fig = figure.Figure()
      gr = fig.subplots(1)
		
      xpos = np.arange(len(udays[0]))
      fig.set_facecolor('black')
        
      gr.plot(xpos, [i - 5 for i in udays[0]], color='lightgray', label='Linhas')
      gr.bar(xpos, udays[0], width=0.85, color=colors, edgecolor='black', zorder=2)
      if max(udays[0]) != 0:
        gr.imshow(background, extent=[-0.95, 7, 0, max(udays[0]) + max(udays[0]) * 0.06], aspect='auto', alpha=0.5)

      # Adicione as strings acima de cada barra
      for i, s in enumerate(uhours): plt.text(xpos[i], udays[0][i], s, ha='center', va='bottom', fontweight='bold')
      for i, s in enumerate(usimbols): plt.text(xpos[i], udays[0][i] - max(udays[0]) * 0.06, s, ha='center', va='bottom', fontsize=14)
  
      semday = udb.find_one({'semday': {'$exists': True}})['semday']
      days = [(semday + timedelta(days=day)).day for day in range(len(udays[0]))]
      plt.xticks(xpos, days, color='white', fontweight='bold')
      plt.yticks([])
      plt.xlabel('Dia', color='white', fontweight='bold')
      plt.ylabel('Tempo', color='white', fontweight='bold')
      plt.title('Estudo em calls (Semanal)', color='white', fontweight='bold')
      """  

      try:
        if user.get('calls', {}).get('stats', [0])[1] != 0:
          metaday = f"**Meta diária:** {timeString(user['calls']['stats'][1])}"
        else:
          metaday = "`/stats meta` para definir uma meta diária!"
      except:
         metaday = "`/stats meta` para definir uma meta diária!"
  
      #embed.set_image(file=disnake.File('images/stats.png', filename='stats.png'))
      #plt.close('all')
  

      calls_field = user.get('calls', {})
      embed.description = f"> **Total:** {timeString(calls_field.get('totaltime', 0))}\n> **Maior tempo seguido:** {timeString(calls_field.get('record', 0))}\n\n> **Com câmera:** {timeString(calls_field.get('camera', 0), 'profile')}\n▬▬▬▬▬▬▬\n:alarm_clock: **SEMANAL:** \n\n> **Total:** {timeString(user.get('timed', {}).get('week', {}).get('calls', 0))}\n> {metaday}\n\n{semday_display}"
    elif stats=='principal':
      ldisp = f'{level_icons[user["level"]]}<@&{levels[user["level"]]}>'

      uranks = []
      uranks_ordened = ''
      medals = {1: '🥇', 2: '🥈', 3: '🥉'}
      for n in range(len(top_opts)):
        try:
          pos, rname = await ranking(inter, client, ['GLOBAL', n], 'self', top_opts)
          uranks.append((pos, rname))
        except: pass

      uranks_ordened = sorted(uranks, key=lambda x: x[0])
      uranks_final = ''

      for x in uranks_ordened: 
        if x[0] in medals: 
          uranks_final += f'> {medals[x[0]]} {x[1]}\n'
        else:
          uranks_final += f'> `#{x[0]}` {x[1]}\n'

      have_guild = user.get('guild', False)

      if have_guild: 
        uguild = udb.find_one({'ugid': have_guild})
        have_guild = f'<@&{uguild["guild_role"]}>'

        if uguild['ugid'] == user['uid']:
          gicon = '<:guild_owner:1217871403538321428> '
        else:
          gicon = '<:guild_member:1217871413617229914> '
			
      else:
        have_guild, gicon = 'Nenhuma', ''

      carlist = getSv(['rRelator', 'rSearcher'])

		
      career = [f'<@&{role.id}>' for role in carlist if role in uobj.roles]
		
      if not career: career = 'Nenhuma'
      else: career = ', '.join(career)

      thinkers_field = user.get('thinkers', {})
      embed.description = f"> **Nível:** {ldisp}\n> **Guilda:** {gicon}{have_guild}\n> **Carreira:** {career}\n\n> **{round(user['blanks'], 1)}** <:blank:1124439750208655500>\n\n## 🏆 Rankings\n{uranks_final}"
    
    elif stats=='Produções':
      try:
        urelat = user['relat']
        pl = [urelat["sends"]]
  
        rmode = urelat['status']
      
        if rmode == ":shield:": rmode = f"{rmode} Não precisa enviar um relatório hoje"
        elif rmode == ":pencil:": rmode = f"{rmode} Relatório diário ainda não enviado!"
        elif rmode == ":white_check_mark:": rmode = f"{rmode} Já enviou o relatório de hoje"
        elif rmode == ":no_entry_sign:": rmode = f"{rmode} Não enviou o relatório de hoje.."
  
        now = datetime.now() - timedelta(hours=3)

        articles = readSet(user['uid'], 'searches', 0)
          
        embed.description = f"> Virou relator **<t:{int((now - timedelta(days=urelat['days']) + timedelta(hours=3)).timestamp())}:R>**\n> **Relatórios enviados:** {urelat['sends']}\n\n> {rmode}\n> **Horário de envio: <t:{int((urelat['time'] - timedelta(hours=1) + timedelta(hours=3)).timestamp())}:t>** até **<t:{int((urelat['time'] + timedelta(hours=1) + timedelta(hours=3)).timestamp())}:t>**\n\n> **Artigos escritos:** {articles}"
      except: print(error())
	  
    elif stats == 'Guilda':
      uguild_id = user['guild']

      uguild = udb.find_one({'ugid': uguild_id})

      members = [f'> <:guild_member:1217871413617229914> <@{member}>' for member in uguild['guild_members']]
      members[0] = members[0].replace('> <:guild_member:1217871413617229914>', '> <:guild_owner:1217871403538321428>')
      members = '\n'.join(members)

      embed.description = f"# {uguild['guild_name']}\n> Fundada **<t:{int((uguild['was_born'] + timedelta(hours=3)).timestamp())}:R>**\n\n- <@&{uguild['guild_role']}>\n## Integrantes ({len(uguild['guild_members'])})\n{members}"
	
	  
  except: print(error())

  bfields = ['blanks', 'calls', 'relat', 'guild']
  bnames = {"🌀 Principal": "principal", "📢 Calls": "calls", "📄 Produções": 'Produções', '👥 Guilda': 'Guilda'}
  buttons = []
  count = 0
  if mode == 'edit': 
    for name in bnames:
      if user.get(bfields[count]) is not None: # Se o usuário tiver esse field
        if bnames[name] == stats:
          buttons.append(disnake.ui.Button(label=name, style=disnake.ButtonStyle.secondary, custom_id=f"profile.{bnames[name]}", disabled=True))
        else:
          buttons.append(disnake.ui.Button(label=name, style=disnake.ButtonStyle.primary, custom_id=f"profile.{bnames[name]}"))
      count += 1

    if stats == 'calls':
      await inter.edit_original_message(embed=embed, components=buttons, files=[])
    else:
      await inter.message.edit(embed=embed, components=buttons, files=[])

    try: await inter.response.send_message()
    except: pass
      
  else:  
    for name in bnames:
      if user.get(bfields[count]) is not None: # Se o usuário tiver esse field
        if bnames[name] == 'calls': # Parte padrão do perfil
          buttons.append(disnake.ui.Button(label=name, style=disnake.ButtonStyle.secondary, custom_id=f"profile.calls", disabled=True))
        else:
          buttons.append(disnake.ui.Button(label=name, style=disnake.ButtonStyle.primary, custom_id=f"profile.{bnames[name]}"))
      count += 1

    if stats == 'calls':
      await inter.edit_original_message(embed=embed, components=buttons)
    else:
      await inter.message.edit(embed=embed, components=buttons)
  



async def ranking(inter, client, mode, mode2, opts=''):	
  try:
    stat_fields = ['thinkers.cardpower', "blanks", "calls.totaltime", "calls.camera", "relat.sends", "bumps", "invites"]
    emoji = ['<a:cronocard:1142933723097084014>', '<:blank:1124439750208655500> ', ':loudspeaker:', ":camera:", ':pencil:', ':rocket:', ':envelope:'][mode[1]]
    field = stat_fields[mode[1]]
    mode[1] = list(opts.keys())[mode[1]]
	
    uid, desc = inter.author.id, ''
	
    users = list(udb.find({field: {"$exists": True}}).sort(field, -1))
	
    uid, pos = inter.author.id, 1
	
    for indice, user in enumerate(users, start=1):
      if user.get('uid') == uid:
        upos, udata = indice, user
        if mode2 == 'self':
          return [upos, mode[1]]
        break
	
    if mode2 == 'self': return
	    
    for pos, user in enumerate(users, start=1):
      if pos >= 11 and upos > 10:
        user = udb.find_one({'uid': uid})
	  
      if field == "calls.totaltime":
        value = timeString(user.get('calls', {}).get('totaltime', 0), 'simple2')
        
      elif field == 'calls.camera':
        value = timeString(user.get('calls', {}).get('camera', 0), 'simple2')
        
      elif field == 'thinkers.cardpower':
        val1 = user.get('thinkers', {})
        value = f'{val1.get("cardpower", 0)} ({len(val1.get("cards"))} cards)'

      elif field == "relat.sends":
        value = user.get('relat', {}).get('sends', 0) + user.get('searches', 0)

      elif field == "blanks":
        value = f'{round(user.get(field, 0), 1)} <:blank:1124439750208655500>'

      elif field == 'bumps':
        value = user.get('bumps', 0)

      elif field == 'invites':
        value = user.get('invites', 0)

      medals = {1: '🥇', 2: '🥈', 3: '🥉'}

      if pos >= 11:
        if upos > 10:          
          desc += f'▬▬▬▬▬▬▬▬▬▬▬▬▬\n**`#{upos} Você` <@{uid}> ➜ {value}**'
        break
      elif user.get('uid') == uid:
        if pos in medals: pos = medals[pos]
        else: pos = f'`#{pos}`'
        desc += f'▬▬▬▬▬\n**{pos} `Você` <@{uid}> ➜ {value}**\n▬▬▬▬▬\n'
      else:
        if pos in medals: pos = medals[pos]
        else: pos = f'`#{pos}`'
        desc += f'{pos} <@{user["uid"]}> ➜ {value}\n'
	
    embed = disnake.Embed(
      description=f'## {emoji} {mode[1]}\n\n{desc}',
      colour=0xf1de52,
    )
    embed.set_author(
      name=f'TOP 10 - {mode[0]}',
      icon_url=inter.author.guild.icon
    )
	  
    await inter.response.send_message(embed=embed)
  except: print(error())
