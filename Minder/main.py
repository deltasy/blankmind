import disnake
from disnake.ext import commands
from json import load as jload, dump as jdump
from os import listdir as dirs
from asyncio import sleep as asleep
from asyncio import get_event_loop as asynloop
from traceback import format_exc as error
from random import randint
import re
import asyncio
import unicodedata

from actions.buttons import buttonClick
from actions.mjoin import memberJoin
from actions.mremove import memberRemove
from actions.dropdown import dropdown
from actions.reactions import newReaction, remReaction, msgdel_by_pale

from functions.page1 import getSv, agetSv, newBlank, namedisplay, idealist_repo
from functions.articles import newArticle
from functions.userloop import loopState
from functions.topweek import topweek
from functions.initial import initial

import gc

from mongo import udb, readSet
import pymongo

from datetime import datetime, timedelta, timezone
import requests
import io

import time

from functions.time import timeString

import plotly.graph_objects as go

import numpy as np

import os
import sys

global nodelt
nodelt = ['delt', 'deut', 'atle']

global intros
intros = {'tribun': '⚖️', '🍔': 'culinaria', '⌛': 'historia', '🌎': 'geografi', 'juiz': '⚖️', 'medi': '💉', 'programa': '💻', 'matema': '📐', 'milit': '🪖', 'olimpi': '🏅', 'music': '🎵', 'nutric': '🍴', 'cozinh': '🍜', 'direito': '⚖️', 'advocac': '⚖️', 'empresa': '🏢', 'desenh': '🎨', 'quimic': '🔬', 'fotogr': '📷', 'arte': '🎨', 'artista': '🎨', 'medalh': '🥇', 'fisica': '⚛️', 'psicolo': '🗣️', 'calculo': '📐', 'livro': '📘', 'xadrez': '♟️', 'biol': '🌱'}

def readComs(mode='errors'):
	folder = 'commands'
	for filename in dirs(folder):
		if filename.endswith('.py'):
			module_name = filename[:-3]
			module_path = f'{folder}.{module_name}'
			
			try:
				comando_module = __import__(module_path, fromlist=[''])
				if hasattr(comando_module, 'command'):
					comando_module.command(bot)
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
  with open('bot_display.gif', 'rb') as avatar:
    await bot.user.edit(avatar=avatar.read()) 
  """
	
  print('Atualizado!!')
  readComs('no error')
  
  getSv(bot)
  await agetSv(bot)

  #await topweek(bot)
  #await initial(bot, 'roles')
  await initial(bot, 'chats')

  global cInvites, cWelcome, cLeave, cReqbook, cIdea
  cInvites, cWelcome, cLeave, cReqbook, cIdea = getSv(['cInvites', 'cWelcome', 'cLeave', 'cReqbook', 'cIdea'])
	
  # Adicionar emojis em pedidos de livros que não possuem emojis
  rmessages = await cReqbook.history(limit=None).flatten()
  rmessages = rmessages[::-1]
  add_reqs = [msgs for msgs in rmessages if not msgs.reactions]
  [await msg.add_reaction('⌛') for msg in add_reqs]

  # Caso alguém entre no server enquanto o bot está off! ------------------------------------
  now = datetime.utcnow().replace(tzinfo=timezone.utc)
  members = [user for user in cInvites.guild.members if now - user.joined_at <= timedelta(minutes=10)]

  for member in members:
    if udb.find_one({'uid': member.id}) is None:
      await memberJoin(member, cInvites, cWelcome)

  loop = asynloop()
  loop.create_task(loopState(bot))

  # Criar mensagem da lista de ideias (Se não existir)
  #asyncio.create_task(idealist_repo('spawn'))
	
  await bot.change_presence(activity=disnake.Activity(type=disnake.ActivityType.custom, name="Blank Mind", state="⭐ Bot principal"))

readComs()   

@bot.event
async def on_member_update(before, after):
  from functions.page1 import botnick_change

  if before in botnick_change:
    return botnick_change.remove(before)

  elif '═ ?' in after.display_name or '═' in after.display_name:
    return await namedisplay(after)

  # Extrai os displays do nick anterior e atual
  before_display = before.display_name[before.display_name.find('═'):]
  after_display = after.display_name[after.display_name.find('═'):]

  # Verifica se os números são diferentes
  if before_display != after_display:
      try: await namedisplay(before)
      except: print(error())



@bot.slash_command(name="restart")
async def Srestart(
  inter: disnake.ApplicationCommandInteraction
):
  script = os.path.abspath(__file__)

  # Substituir o processo atual com um novo processo, reiniciando o programa
  os.execv(sys.executable, [sys.executable, script])

@bot.event
async def on_member_join(member):
  await memberJoin(member, cInvites, cWelcome)

@bot.event
async def on_member_remove(member):
  await memberRemove(member, bot.get_channel(1100117223600816219))

with open('jsons/marks.json', 'r') as file: marks = jload(file)
	
@bot.listen("on_button_click")
async def btn(inter: disnake.MessageInteraction):
  global marks
  await buttonClick(inter, bot)
  with open('jsons/marks.json', 'r') as file: marks = jload(file)


from io import BytesIO


@bot.event
async def on_message(msg):
  global marks

  if not msg.guild: return

  #if msg.content == '<-V->': await initial(bot, 'cmds')
	
  if '.startest' in msg.content:
    ustats = readSet(663525286784139274, 'calls.stats', [[0, 0, 0, 0, 0, 0, 0], 0, [0, 0, 0, 0, 0, 0, 0]])
  
    try:
      meta = ustats[1]
    except:
      meta = 9999
  
    colors, usimbols = [], []
  
    xpos = np.arange(len(ustats[0]))
  
    maxval = max([max(ustats[0]), max(ustats[2])])

    utimes = [timeString(i, 'simple') for i in ustats[0]]
    ulasttimes = [timeString(i, 'simple') for i in ustats[2]]

    day_display = udb.find_one({'semday': {'$exists': True}})
    today = day_display['today']
    semday = day_display['semday']

    # Exibir tempo da semana passada
    days_past = (today - semday).days + 1
  
    for pos, valor in enumerate(ustats[0]):
      if valor == max(ustats[0]) and valor != 0:
        colors.append('gold')
        usimbols.append('★')
      elif valor < meta or valor == 0:
        colors.append('firebrick')
        usimbols.append('X')
      else:
        colors.append('limegreen')
        usimbols.append('OK')

    fig = go.Figure()
  
    # Adicionar barras para a semana atual e semana passada
    fig.add_trace(go.Bar(x=xpos, y=ustats[0], marker_color=colors, text=ustats[0], textposition='inside', name='Semana Atual'))
    fig.add_trace(go.Bar(x=xpos, y=ustats[2], marker_color='gray', text=ustats[2], textposition='inside', name='Semana Passada'))
  
    # Adicionar texto acima das barras
    for i, s in enumerate(utimes):
        fig.add_annotation(x=xpos[i], y=ustats[0][i], text=s, showarrow=False, font=dict(color='white', size=14), yshift=20)
  
    # Adicionar símbolos acima das barras
    for i, s in enumerate(usimbols):
        fig.add_annotation(x=xpos[i], y=ustats[0][i] - maxval * 0.05, text=s, showarrow=False, font=dict(color='white', size=14), yshift=20)
  
    # Atualizar layout
    fig.update_layout(
        xaxis=dict(tickvals=xpos, ticktext=[f'Dia {day}' for day in range(len(ustats[0]))]),
        yaxis=dict(title='TEMPO', titlefont=dict(color='white', size=14), color='white'),
        title='Estudo em calls (Semanal)',
        plot_bgcolor='black',
        paper_bgcolor='black',
        font=dict(color='white')
    )
  
    # Salvar figura
    buffer = BytesIO()
    fig.write_image(buffer, format='png', width=800, height=600)
    buffer.seek(0)
    fig = None
    del fig
    gc.collect()
  
    this_week, last_week = sum(ustats[0][0:days_past]), sum([val for pos, val in enumerate(ustats[2][0:days_past])])
  
    embed = disnake.Embed(
      description = f"> **Total:** {timeString(readSet(663525286784139274, 'calls.totaltime', 0))}\n> **Maior tempo seguido:** {timeString(readSet(663525286784139274, 'calls.record', 0))}\n\n> **Com câmera:** {timeString(readSet(663525286784139274, 'calls.camera', 0))}\n▬▬▬▬▬▬▬\n### :alarm_clock: SEMANAL\n\n> **Essa semana:** {timeString(this_week)}\n> **Semana passada:** {timeString(last_week)}\n\n> **Meta diária:** {timeString(ustats[1])}"
    )
  
    if this_week > last_week:
      percent = f'{int(((this_week - last_week) / this_week) * 100)}% '
      pemoji = 'https://i.imgur.com/PkqyzV6.png'
      pdisplay = 'melhor que'
  
    elif this_week < last_week:
      percent = f'{int(((last_week - this_week) / last_week) * 100)}% '
      pemoji = 'https://i.imgur.com/rEqvADU.png'
      pdisplay = 'pior que'
      
    else:
      pdisplay = 'Rendimento igual à'
      percent = ''
      pemoji = ''
    
  
    embed.set_image(file=disnake.File(buffer, filename="stats.png"))
  
    if sum(ustats[2]) != 0:
      embed.set_footer(text=f'Rendimento {percent}{pdisplay} semana passada', icon_url=pemoji)
  
    
    chat = bot.get_channel(1100117223600816219)
  
    await chat.send(embed=embed)
	  
  if msg.channel.id == 1197315979710046288:
    await msg.add_reaction('⌛')

  elif msg.channel.id == 1202369082251280404:
    await msg.add_reaction('🌟')

    await msg.create_thread(
      name=f'Conquista de {msg.author.display_name.split(" ═ ")[0]}'
    )

  elif msg.channel.id == 1124455706309963817:
    brute_text = msg.content.lower()

    nfkd = unicodedata.normalize('NFKD', brute_text)
    text = ''.join([c for c in nfkd if not unicodedata.combining(c)])

    emojis = list(set([intros[content] for content in intros if content in text.lower()]))[:5]

    [asyncio.create_task(msg.add_reaction(reaction)) for reaction in emojis]
    await msg.create_thread(
      name=f'Impressões'
    )

  elif not msg.author.bot and isinstance(msg.channel, disnake.Thread) and msg.channel.parent.id == 1197315654412419183 and msg.mentions:

    confirm2 = None
    embed = disnake.Embed(
      colour=0xed3325
    )

    async def error_msg(text, embed, msg, delay=10):
      embed.description = f':warning: **{text}**'
      error = await msg.channel.send(f'{msg.author.mention} **Esse aviso sumirá <t:{int((datetime.now() + timedelta(seconds=delay)).timestamp())}:R>**', embed=embed)
      await error.delete(delay=delay)
      
    
    first_msg = await msg.channel.fetch_message(msg.channel.id) 

    if first_msg.author.id != msg.author.id:
      await error_msg('Você não criou esse post, então não pode receber a recompensa.', embed, msg)
    
    elif '🤝' in [react.emoji for react in first_msg.reactions]:
      await error_msg('Você já recebeu a recompensa.', embed, msg)
    
    elif any(mention.id == msg.author.id for mention in msg.mentions):
      await error_msg('Você não pode mencionar você mesmo!', embed, msg)

    else:
      messages = await cReqbook.history(limit=None).flatten()
      messages = messages[::-1]

      confirm = [msg2 for msg2 in messages if msg2.author.id == msg.mentions[0].id]

      for msg3 in confirm: # Percorrer mensagens do usuario mencionado
        if '✅' not in [react.emoji for react in msg3.reactions]:
            confirm2 = msg3 # A primeira mensagem do usuario mencionado sem esse emoji
            break
  
      if not confirm2:
        await error_msg('Essa pessoa não pediu esse livro', embed, msg)
        
      else:
        try:
          udata = udb.find_one({'uid': msg.author.id})
          
          blanks = 2.5
          udb.update_one({'uid': msg.author.id}, {'$inc': {'blanks': blanks}})

          try: await namedisplay(msg.author.id)
          except: print(error())
	
          await confirm2.remove_reaction('⌛', bot.user)
          await confirm2.add_reaction('✅')

          await first_msg.add_reaction('🤝')

          embed = disnake.Embed(
            colour=0x33FF33,
            description=f'{msg.author.mention} atendeu o pedido de {msg.mentions[0].mention}\n> "{confirm2.content}"\n\n{newBlank([udata["blanks"], blanks])}',
          )

          await msg.reply(embed=embed)
        except: pass
	
  elif msg.author.bot and msg.author.id == 302050872383242240: # Enviada por bot
    if msg.embeds: # Contém embeds
      for embed in msg.embeds:
        try:
          if "Bump done" in embed.description:
            bumpcheck = await msg.channel.send(f"> Reaja a essa mensagem para adquirir **<:blank:1124439750208655500>**!")
            await bumpcheck.add_reaction("✅")

            udb.update_one({'bumptime': {'$exists': True}}, {
              '$set': {'bumptime.0': datetime.now(), 'bumptime.1': bumpcheck.id}
            })
            
        except: 
          print(error())
          pass
  elif msg.channel.id == 1119710450741940325:
    if msg.content == '-deletar':
      with open('jsons/marks.json', 'r') as file: marks = jload(file)
      author_id = str(msg.author.id)
      if author_id in marks['checklists']:
        checklist = await msg.channel.fetch_message(marks['checklists'][author_id])
        del marks['checklists'][author_id]
        await checklist.delete()
        await msg.delete()
        with open('jsons/marks.json', 'w') as file: jdump(marks, file, indent=2)

  elif msg.channel.category is not None and msg.channel.category.id == 1207834421273567254 and not msg.author.bot: # Comandos do modo caverna
    await msg.channel.purge(limit=1)

  elif msg.channel.id == 1123771863802335332 and not msg.author.bot: # Chat de ideias
    try:
      eyes = disnake.PartialEmoji(animated=False, id='1132703714256359584', name='yes')
      eno = disnake.PartialEmoji(animated=False, id='1132703732543529000', name='no')

      embed = disnake.Embed(
        description=f'{msg.content.capitalize()}\n\n▬▬▬▬▬▬▬▬▬▬▬▬▬\n# <:idea_chart:1217856573620097075> **0 Votos**\n> **O voto é secreto**. Não hesite em votar!\n\n<:waiting_votes:1217925376920129666><:waiting_votes:1217925376920129666><:waiting_votes:1217925376920129666><:waiting_votes:1217925376920129666><:waiting_votes:1217925376920129666><:waiting_votes:1217925376920129666><:waiting_votes:1217925376920129666><:waiting_votes:1217925376920129666><:waiting_votes:1217925376920129666><:waiting_votes:1217925376920129666>',
        colour=0xFFFFFF
      )
  
      try: imgprof = msg.author.avatar.url
      except: imgprof = 'https://assets.mofoprod.net/network/images/discord.width-250.jpg'
          
      embed.set_author(
        name=f'💡 Ideia de {msg.author.display_name.split("═")[0]}',
        icon_url=imgprof
      )

      if msg.attachments: 
        msg_img = msg.attachments[0].url
        embed.set_image(url=msg_img)
      
      new_msg = await msg.channel.send(embed=embed,components=[disnake.ui.Button(label='Sim', emoji=eyes, style=disnake.ButtonStyle.success, custom_id=f"idea-yes-{msg.id}"),disnake.ui.Button(label='Não', emoji=eno, style=disnake.ButtonStyle.danger, custom_id=f"idea-no-{msg.id}")])
      idealist = await msg.channel.history(limit=3).flatten()
      idealist = idealist[2]
		
      iembed = idealist.embeds[0]

      iembed.description += f'\n<:waiting_votes:1217925376920129666> https://discord.com/channels/1091742896098660372/1123771863802335332/{idealist.id} **(0 Votos)** {msg.author.mention}'

      await idealist.delete()
		
      await msg.channel.send(embed=iembed)
		
      with open('jsons/marks.json', 'r') as file: marks = jload(file)
  
      marks[f'idea {new_msg.id}'] = {
        "created_by": msg.author.id,
        "votes": {}
      }

      await new_msg.create_thread(
        name="Opiniões"
      )

      msgdel_by_pale.append(msg)
      await msg.delete()
        
      with open('jsons/marks.json', 'w') as file: jdump(marks, file, indent=2)
          
    except: print(error())

  elif '.startsend' in msg.content:
    chat = bot.get_channel(1093630384174006282)
    await chat.send(msg.content.replace('.startsend ', ''))
  elif isinstance(msg.channel, disnake.Thread) and str(msg.channel.id) in marks['sketch_start'] and not msg.author.bot:
    suid = str(msg.channel.id)

    # Caso for aprovado ----------------------------------------------------------------------------------
    if msg.author.id == 663525286784139274 and msg.content.startswith('aprovado'):
      await newArticle(msg, bot)

    # Customizar artigo ----------------------------------------------------------------------------------
    try:
	    if marks['sketch_start'][suid] == 1:
	      if len(msg.attachments) != 1 or msg.content:
	        await msg.reply('Inválido. Você deve enviar apenas uma imagem e mais nada.')
	        await msg.delete()
	        
	      else:
	        marks['sketch_start'][suid] += 1
	        await msg.channel.send("# Título do artigo:")
	        with open('jsons/marks.json', 'w') as file: jdump(marks, file, indent=2)
	
	    elif marks['sketch_start'][suid] == 2:
	      if 35 < len(msg.content) or len(msg.content) < 5:
	        await msg.reply("O título deve ter entre **5 e 35** caracteres.")
	        await msg.delete()
	        
	      elif len(msg.attachments) > 1:
	        await msg.reply("O título deve ser apenas texto.")
	        await msg.delete()
	      
	      else:
	        await msg.channel.edit(name=msg.content.capitalize().replace('#', '').replace('*', ''))
	        marks['sketch_start'][suid] += 1
	        await msg.channel.send("# Descrição do artigo:")
	        with open('jsons/marks.json', 'w') as file: jdump(marks, file, indent=2)
	          
	    elif marks['sketch_start'][suid] == 3:
	      if 55 < len(msg.content) or len(msg.content) < 10:
	        await msg.reply("Descrição deve ter entre **10 e 55** caracteres.")
	        await msg.delete()
	        
	      elif len(msg.attachments) > 1:
	        await msg.reply("A descrição deve ser apenas texto.")
	        await msg.delete()
	        
	      else:
	        msg = await msg.channel.send('## :pencil: Agora pode começar a escrever.\n> Não esqueça dos tópicos! Escreva como se estivesse escrevendo para alguém leigo; seja didático\n\n- Reaja se terminar seu artigo. Após a reação, seu texto será avaliado')
	        await msg.add_reaction('✨')
	        marks['sketch_start'][suid] += 1
	        with open('jsons/marks.json', 'w') as file: jdump(marks, file, indent=2)
    except: pass

global subjects
subjects = {1137496076954370088: '📐 Matemática', 1137497287648628827: '🧪 Química', 1137497316694171768: '❓ Filosofia', 1137497303016542289: '🧬 Biologia', 1137497049022074920: '⚡ Física', 1137497605564276786: '🌍 Geografia', 1137497593929277582: '⏳ História',}

@bot.event
async def on_dropdown(inter: disnake.Interaction):
  await dropdown(inter)

@bot.event
async def on_raw_reaction_add(reaction):
  await newReaction(bot, reaction)

@bot.event
async def on_raw_reaction_remove(reaction):
  await remReaction(bot, reaction)

bot.run('T')
