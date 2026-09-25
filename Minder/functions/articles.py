import disnake
import requests
import io
from json import load as jload, dump as jdump
from traceback import format_exc as error

from mongo import udb, readSet
from functions.page1 import getSv, newBlank


async def newArticle(msg, bot):
      await msg.delete()
      rew, enchannel = msg.content.split(' ')[1:]
      rew, enchannel = float(rew), int(enchannel)
      delchannel = msg.channel

      messages = await msg.channel.history(limit=None).flatten()
      messages = messages[::-1]
      
      sketch_uid = int(messages[0].content.split('<@')[1].split('>!')[0])
      """
      marks['sketch_uids'].remove(sketch_uid)
      del marks['sketch_start'][suid]

      with open('jsons/marks.json', 'w') as file: jdump(marks, file, indent=2)
      """
	
      initial = []
      sketch_content, sketch_images = [], {}

      for initial_message in messages: # Mensagens iniciais
        if initial_message.author.bot: pass
        elif initial_message.author.id == sketch_uid:
          if len(initial) < 3:
            if len(initial) == 0: initial.append(initial_message.attachments[0])
            else: initial.append(initial_message.content)

          else: break

      enciclopedia = bot.get_channel(enchannel)
      guild = enciclopedia.guild
      response = requests.get(initial[0])
	
      new_thread = await enciclopedia.create_thread(
        file = disnake.File(io.BytesIO(response.content), 'imagem.png'),
        name=initial[1].replace('# ', '').replace('*', '').capitalize(),
        content="**" + initial[2].replace('# ', '').replace('*', '').capitalize() + "**",
      )	
      thread = new_thread.message.channel

      summary = await thread.send(f'# :page_facing_up: Sumário\nSendo renderizado :hourglass:')
	
      sum_indexes = {}
      link_format = f'https://discord.com/channels/{guild.id}/{thread.id}'

      line_div = f"""
▬
▬▬
▬▬▬
▬▬▬▬
▬▬▬▬▬
▬▬▬▬▬▬
▬▬▬▬▬▬
▬▬▬▬▬
▬▬▬▬
▬▬▬
▬▬▬
▬▬
▬▬▬
▬▬▬▬
▬▬▬▬▬
▬▬▬▬▬▬
▬▬▬▬▬▬
▬▬▬▬▬
▬▬▬▬
▬▬▬
▬▬▬
▬▬
[▬]({link_format}/{summary.id})
"""

      start_article = next(pos for pos, message in enumerate(messages) if 'pode começar a escrever' in message.content)
      messages = messages[start_article:]
	
      for pos, message in enumerate(messages):
        if message.author.id == 744349038429733005: pass # Se for mensagem do VOID, ignore
        #elif message.author.id == 663525286784139274: break
        else:	
          try:  
            images = []
            try:
              msg3 = message.content[0].upper() + message.content[1:] + '\n'
              topics_inside = ['#' + topic.replace('SUBTITLE 1', '###').replace('SUBTITLE 2', '###') for topic in msg3.replace('###', 'SUBTITLE 1').replace('##', 'SUBTITLE 2').split('#')[1:]]

              if not topics_inside and message.author.id != 510789298321096704 and not message.content[0] == '$': await thread.send(message.content)
				
              for pos2, topic in enumerate(topics_inside):
                await thread.send(line_div)
					
                new_msg = await thread.send(topic)
				  
                sum_indexes[topic[1:].split('\n')[0]] = f'{link_format}/{new_msg.id}'     
	
            except: print(error())

            for attachment in message.attachments:
              try:
                response = requests.get(attachment.url)
                images.append(disnake.File(io.BytesIO(response.content), attachment.filename))        
              except: print(error())

            if images: 
               img_msg = await thread.send(files=images)
               pre_div = await img_msg.history(limit=2).flatten()[1]
               if '▬▬▬▬▬▬' in pre_div.content: await pre_div.delete()

          except: pass

      sum_new = ''
      for topic, link in sum_indexes.items(): # Listar os itens do sumário
        sum_new += f'- **[{topic.replace("**", "").replace("# ", "")[1:].capitalize()}](<{link}>)**\n'

      await summary.edit(f'# :page_facing_up: Sumário\n{sum_new}')
      await thread.send(line_div)
      await thread.send(f"**AUTORIA:** <@{sketch_uid}>")

      try:
        if sketch_uid == 663525286784139274: tag = enciclopedia.get_tag_by_name('Oficial')
        else: tag = enciclopedia.get_tag_by_name('Artigo')

        await thread.add_tags(tag)

        first_part, last_part = enciclopedia.name.split('〔')
        await enciclopedia.edit(name=f"{first_part}〔{int(last_part.replace('〕', '')) + 1}〕")

      except: print(error())

      channel = getSv('cRels')

      
      udata = udb.find_one({'uid': sketch_uid})
      val = udata['blanks']

      searches = readSet(sketch_uid, 'searches', 0)
		
      if rew == 0:
        bdisp = ''
      else:
        bdisp = f'\n{newBlank([val, rew])}'
      
      embed = disnake.Embed(
        title = '',
        description = f'## :bookmark: ARTIGO P/ BLANKPEDIA (#{searches + 1})\n### {link_format}\n▬▬▬▬▬▬▬▬▬▬▬▬\n\nSeu artigo foi aprovado. O tema em questão pertence à área de <#{enchannel}>\n### Tópicos\n{sum_new}\n▬▬▬▬▬▬▬▬▬▬▬▬{bdisp}',
        colour = 0xbeff70
      )

      udb.update_one({'uid': sketch_uid}, {
        '$inc': {
          'searches': 1, 'blanks': rew
		}
      })

      user = await bot.fetch_user(sketch_uid)

      try:
        if discord.utils.get(user.roles, id=1174146227961614467) is None:
          role = thread.guild.get_role(1174146227961614467)
          await user.add_roles(role)
      except: pass

      try: imgprof = user.avatar.url
      except: imgprof = 'https://assets.mofoprod.net/network/images/discord.width-250.jpg'

      embed.set_author(
            name = user.display_name,
            icon_url = imgprof
      )
      
      embed.set_thumbnail(url=imgprof)
      
      await channel.send(embed=embed)
	  
      #await delchannel.delete()