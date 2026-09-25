import disnake
from json import load as jload, dump as jdump
from datetime import datetime, timedelta
from traceback import format_exc as error
from random import randint

from mongo import udb, readSet
from functions.page1 import newBlank, tempMsg, getSv, namedisplay
from functions.time import timeFormat
from commands.cronocards import newThinker

global subjects
subjects = {1137496076954370088: '📐 Matemática', 1137497287648628827: '🧪 Química', 1137497316694171768: '❓ Filosofia', 1137497303016542289: '🧬 Biologia', 1137497049022074920: '⚡ Física', 1137497605564276786: '🌍 Geografia', 1137497593929277582: '⏳ História'}


global msg_del_by_pale
msgdel_by_pale = []

async def newReaction(bot, reaction):
  rPaleShield, cPaleShield = getSv(['rPaleShield', 'cPaleShield'])

  try:
    user = reaction.member
    emoview = reaction.emoji.name
	  
    id = str(user.id)

    if not user.bot:
      with open('jsons/marks.json', 'r') as file: marks = jload(file)
		
      if emoview == '♻️': 
        chat = bot.get_channel(reaction.channel_id)
        msg = await chat.fetch_message(reaction.message_id)
        if int(msg.content.split(">")[0][2:]) == user.id: # Se o usuario for dono da interação original
          await newThinker(msg, 'edit')

          embed = msg.embeds[0]
          if 'Card adicionado à sua coleção' in embed.description:
            await msg.add_reaction('💼')
          await msg.remove_reaction("♻️", user)

      elif emoview == '💼':
        chat = bot.get_channel(reaction.channel_id)
        msg = await chat.fetch_message(reaction.message_id)
        embed = msg.embeds[0]
        if int(msg.content.split(">")[0][2:]) == user.id:
          if "nenhum card" in embed.description: 
            await msg.remove_reaction('💼', user)
            pass
          else:
            blanks = int(embed.description.split('💼 Para adicionar à coleção` | **')[1].split(" ")[0])
            udata = udb.find_one({'uid': user.id, 'blanks': {'$gte': blanks}})
  
            if not udata: 
              embed = disnake.Embed(
                description="Blanks insuficientes. Pobre.",
                colour=0xed3325
              )
              return await tempMsg(chat, embed, [str(user.id)])

            embdesc = embed.description
            card_id = int(embdesc.replace("~ Card ", "").split("~ ")[0].split("**")[1].replace(' ~', ''))
            await msg.clear_reaction('💼')
            await msg.add_reaction("♻️")

            if '<:C1:1142494346696982650>' in embdesc:
              cpower = 5
              
            elif '<:I1:1142495469717684236>' in embdesc:
              cpower = 15
              
            elif '<:R1:1142496422948786201>' in embdesc:
              cpower = 25
              
            elif '<:E1:1142498412391043076>' in embdesc:
              cpower = 50
              
            else: 
              cpower = 150
            
            udb.update_one({'uid': user.id}, {
              '$push': {'thinkers.cards': card_id},
              '$inc': {'thinkers.cardpower': cpower, 'blanks': -blanks}
            })  

            try: await namedisplay(user.id)
            except: print(error())

            embed.description = f'{embed.description.split("`♻️ Para um novo card`")[0]}### 💼 Card adicionado à sua coleção\n<a:cronocard:1142933723097084014> **Ganhou {cpower} de poder!**'
            embed.set_image(file=disnake.File('images/null.png', filename='null.png'))

            final_blanks = float(msg.content.split(' | <:no:1132703732543529000> **Gastou ')[1].split(' ')[0]) + blanks
            
            await msg.edit(f'<@{user.id}> | <:no:1132703732543529000> **Gastou {final_blanks} <:blank:1124439750208655500>**', embed=embed) 

		
      elif (emoview == "🟩" or emoview == "🟥") and id in marks["checklists"]:
        try:
          if reaction.message_id == marks["checklists"][id]:
            channel = bot.get_channel(reaction.channel_id)
            message = await channel.fetch_message(reaction.message_id)
            brtime = datetime.now() - timedelta(hours=3)
            
            embed = message.embeds[0]
            utcnow = datetime.utcnow()

            if utcnow.date() == message.created_at.date(): # Se for marcado no mesmo dia
              embed.description = embed.description.replace("` :white_large_square:", f"({timeFormat(brtime.hour)}:{timeFormat(brtime.minute)})` {emoview}", 1)
            
            else: # Se for de um dia diferente
              embed.description = embed.description.replace("` :white_large_square:", f"({timeFormat(brtime.day)}/{timeFormat(brtime.month)}, {timeFormat(brtime.hour)}:{timeFormat(brtime.minute)})` {emoview}", 1)

            await message.remove_reaction(f"{emoview}", user)

            topics = [topic for topic in embed.description.split("\n\n")[1:] if '▬▬▬▬▬▬' not in topic]

            check_types = ['<:check_fail:1221248877890637844>', ':white_check_mark:', '<:some_checks:1221263671360094279>']
            for i, topic in enumerate(topics):
              if topic.count(':white_large_square:') == 0 and not any(type for type in check_types if type in topic):
                if topic.count('🟥') == topic.count('\n'):
                  embed.description = embed.description.replace(topic, '<:check_fail:1221248877890637844> ' + topic)
                elif topic.count('🟩') == topic.count('\n'):
                  embed.description = embed.description.replace(topic, ':white_check_mark: ' + topic)
                else:
                  embed.description = embed.description.replace(topic, '<:some_checks:1221263671360094279> ' + topic) 
  
            if embed.description.count(":white_large_square:") <= 0:
              await message.clear_reactions()
  
              ch = embed.description.count("🟩")
              lc = ch + embed.description.count("🟥")
              if ch == lc:
                lmsg = "✨ **Concluiu tudo, parabéns!**"
              else:
                lmsg = f"✨ Concluiu **{ch}/{lc}** tarefas"
                
              embed.description = embed.description.split('- Reaja para marcar')[0] + lmsg
              embed.colour = 0x5865F2
				
              del marks["checklists"][id]
              with open('jsons/marks.json', 'w') as file: jdump(marks, file, indent=2)
            
            await message.edit(embed=embed)
        except Exception as e: print(e)
          
      elif emoview == '🔖': 
        thread = await bot.fetch_channel(reaction.channel_id)
        if thread.category.id == 1137495923170230374:
          try:
            uid = f'wiki {user.id}'

            subject = subjects[thread.parent_id]

            try:
              marks[uid][subject].append(thread.id)
            except: 
              if uid not in marks: marks[uid] = {}
              marks[uid][subject] = [thread.id]

            with open('jsons/marks.json', 'w') as file: jdump(marks, file, indent=2)
          except: print(error())		
    
        
      elif emoview == "✅": 
        bump = udb.find_one({'bumptime': {'$exists': True}})['bumptime']
        bumpcheck_id = bump[1]
        if reaction.message_id == bumpcheck_id:
          chat = bot.get_channel(reaction.channel_id)
          bumpcheck = await chat.fetch_message(bumpcheck_id)
          await bumpcheck.delete()

          bumplist = ["Gostei do bump", "Valeu pelo bump", "BUMP BUMP BUMP", "Divulgação braba", "Bumpado com sucesso", "Brabo d+", "Belo bump", "Bump perfeito", "Bem na hora", "Interessante esse bump hein", "Toma uns blanks pra você"]
          bumpcombo = ['BUMP', ':anger: DOUBLE BUMP', ':anger: TRIPLE BUMP', ':anger: QUADRA BUMP', ':anger: PENTA BUMP', ':anger: MASTER BUMP', ':anger: GODLIKE BUMP', ':anger: UNSTOPABBLE BUMP', ':boom: EXPLOSIBUMP', ':infinity: I N F I N I T Y BUMP!!!']
			
          rew = 1.5
          
          udata = udb.find_one({'uid': user.id})

          if bump[2] == user.id:	
            udb.update_one({'bumptime': {'$exists': True}}, {
              '$inc': {'bumptime.3': 1}
            })
            bump[3] += 1
			
          else:
            udb.update_one({'bumptime': {'$exists': True}}, {
              '$set': {'bumptime.2': user.id, 'bumptime.3': 0}
            })
            bump[3] = 0

          if bump[3] > len(bumpcombo): bump[3] = len(bumpcombo) - 1

          embed = disnake.Embed(
            title=f'({bump[3] + 1}x) {bumpcombo[bump[3]]}',
            color=0x24B7B7,
            description=f":sunglasses: {bumplist[randint(0,len(bumplist)-1)]}, {user.mention}\n**▃▃▃▃▃▃▃▃▃▃▃▃**\n\n{newBlank([udata['blanks'], rew])}",
          )
          readSet(user.id, 'bumps')
  
          udb.update_one({'uid': user.id}, {
            '$inc': {'blanks': rew, 'timed.week.blank': rew, 'bumps': 1}
          })

          await chat.send(embed=embed)

          try: await namedisplay(user.id)
          except: print(error())

      elif emoview == "✨" and str(reaction.channel_id) in marks['sketch_start']: 
        channel = bot.get_channel(reaction.channel_id)
        schannel = str(reaction.channel_id)
        if marks['sketch_start'][schannel] == 4:
          await channel.send('Seu Artigo será avaliado por <@663525286784139274>. Obrigado pelo empenho!')
          marks['sketch_start'][schannel] += 1


      elif emoview == '❌' and rPaleShield in user.roles:
		  
        suid = str(user.id)
        with open('jsons/updayte.json', 'r') as file: updayte = jload(file)

        if suid in updayte['punish_messages'] and updayte['punish_messages'][suid] >= 10:
          warn_embed = disnake.Embed(
            description='**Você alcançou o limite de remoção de mensagens de hoje (3)**\n> Tente amanhã.',
            colour=0xed3325
          )
          delay = 10
          msg = await cPaleShield.send(f'{user.mention} **Esse aviso sumirá <t:{int((datetime.now() + timedelta(seconds=delay)).timestamp())}:R>**', embed=warn_embed)
          await msg.delete(delay=delay)

        else:
          if suid not in updayte['punish_messages']: updayte['punish_messages'][suid] = 1
          else: updayte['punish_messages'][suid] += 1

          chat = bot.get_channel(reaction.channel_id)
          msg = await chat.fetch_message(reaction.message_id)

          if msg.author.bot:
            warn_embed = disnake.Embed(
              description='**Você não pode remover mensagens de bots.**',
              colour=0xed3325
            )
            delay = 10
            msg = await cPaleShield.send(f'{user.mention} **Esse aviso sumirá <t:{int((datetime.now() + timedelta(seconds=delay)).timestamp())}:R>**', embed=warn_embed)
            return await msg.delete(delay=delay)

          embed = disnake.Embed(
            description=f'# <:paleshield:1232749831886209035>:shushing_face: {user.mention} removeu uma mensagem inadequada\n> **De:** {msg.author.mention}\n> **Mensagem:** {msg.content.capitalize()}',
            colour=0xFFFFFF
          )
          await cPaleShield.send(embed=embed)

          msgdel_by_pale.append(msg)
			
          await msg.delete()
  
        with open('jsons/updayte.json', 'w') as file: jdump(updayte, file, indent=2)

  except: print(error())

async def remReaction(bot, reaction):
  emoview = reaction.emoji.name
  if emoview == '🔖': 
    thread = await bot.fetch_channel(reaction.channel_id)
    if thread.category.id == 1137495923170230374:
      with open('jsons/marks.json', 'r') as file: marks = jload(file)
      subject = subjects[thread.parent_id]
      uid = f'wiki {reaction.user_id}'

      try:
        umark = marks[uid][subject]
        umark.remove(thread.id)

        if len(umark) == 0:
          del marks[uid][subject]
        with open('jsons/marks.json', 'w') as file: jdump(marks, file, indent=2)
      except: pass