from functions.page1 import notify
from json import load as jload, dump as jdump
from commands.stats import showStatus
from disnake import ChannelType, PermissionOverwrite
import disnake
from traceback import format_exc as error
import asyncio

from commands.cronocards import thinkerList
from functions.page1 import newBlank, namedisplay, getSv, idealist_repo
from commands.bookshelf import bookrew

from mongo import udb

async def buttonClick(inter, client):
	guild = inter.guild
	inter.component.disabled = True
	btn = inter.component.custom_id
	user = inter.author

	if 'displaychange' in btn:
		stat, display, cost  = btn.split('_')[1:]
		if stat.isdigit(): stat = int(stat) 

		cost = float(cost)

		udata = udb.find_one({'uid': user.id})

		try:
			if udata['linked_stat'] == stat: return await inter.response.send_message("**Você já tem esse display. Nada mudou.**", ephemeral=True)
		except: pass

		if udata['blanks'] < cost: return await inter.response.send_message(f'<:no:1132703732543529000> Você é muito pobre pra isso... Ainda falta-lhe **{round(cost - ublanks["blanks"], 1)}** <:blank:1124439750208655500>', ephemeral=True)
		else:
			udb.update_one({'uid': user.id}, {'$set': {'linked_stat': stat}, '$inc': {'blanks': -cost}})
			await namedisplay(inter.author)
			resp_embed = disnake.Embed(
				description=f'{user.mention} alterou seu display\n> :credit_card: **Gastou {cost}** <:blankbag:1124445117261037630>',
				colour=0xFF7F50
			)

			await inter.channel.send(embed=resp_embed)
			try: await inter.response.send_message()
			except: pass

	
	elif 'idea' in btn:
		idea_key = f'idea {inter.message.id}'
		this_vote = btn.split('ea-')[1].split('-')[0]

		embed = inter.message.embeds[0]
    
		with open('jsons/marks.json', 'r') as file: marks = jload(file)

		if user.id == 663525286784139274:
			decision = {'yes': 'Aceito', 'no': 'Negado'}

			nvotes = sum(1 for vote in marks[idea_key]["votes"].values() if vote == "no")
			yvotes = sum(1 for vote in marks[idea_key]["votes"].values() if vote == "yes")

			explain = ''
			if yvotes > nvotes and this_vote == 'no': explain = '\n> **Apesar da aprovação pública**, sua ideia se mostrou vaga e/ou não foi defendida corretamente.\n'

			if 'Votos' in embed.description: modifier = 'Votos'
			else: modifier = 'Voto'

			new_embed = disnake.Embed(
				description=embed.description.replace('<:idea_chart:1217856573620097075>', f'<:decision:1218252303212216360> ({decision[this_vote]})').replace(modifier, f'{modifier}{explain}')
			)
			new_embed.set_author(name=embed.author.name, icon_url=embed.author.icon_url)
			new_embed.set_image(url=embed.image.url)
			
			elock = disnake.PartialEmoji(animated=False, id='1217951908229287965', name='closed')

			try:
				mention = f"<@{marks[idea_key]['created_by']}>"
				await inter.message.thread.send(f'{mention}, sua ideia foi avaliada.')
			except: pass

			if this_vote == 'no': new_embed.colour = 0xed3325
			else:
				try:
					cChat = getSv('cChat')
					new_embed.colour = 0x33FF33
					geralEmbed = disnake.Embed(
						description=f'# 💡🎉 Ideia aprovada\n> **Autor:** {mention}\n> **Detalhes:** https://discord.com/channels/1091742896098660372/1123771863802335332/{inter.message.id}',
						colour=new_embed.colour
					)
					geralmsg = await cChat.send(embed=geralEmbed)
					await geralmsg.add_reaction('🎉')
				except: print(error())

			del marks[idea_key]
			with open('jsons/marks.json', 'w') as file: jdump(marks, file, indent=2)

			new_btn = disnake.ui.Button(label='Votações encerradas', style=disnake.ButtonStyle.secondary, emoji=elock, custom_id="closed", disabled=True)


			await idealist_repo()
			return await inter.response.edit_message(embed=new_embed, components=[new_btn])
      
      
		else:
			if marks[idea_key]['created_by'] == user.id: 
				return await inter.response.send_message('**Não é possível votar na própria ideia**', ephemeral=True)
  
			elif str(user.id) in marks[idea_key]['votes'].keys():
				return await inter.response.send_message('**Você já votou nessa ideia.**', ephemeral=True)
  
			marks[idea_key]["votes"][str(user.id)] = this_vote

		with open('jsons/marks.json', 'w') as file: jdump(marks, file, indent=2)

		nvotes = sum(1 for vote in marks[idea_key]["votes"].values() if vote == "no")
		yvotes = sum(1 for vote in marks[idea_key]["votes"].values() if vote == "yes")

		total_votes = yvotes + nvotes

		yes_per = round((yvotes / total_votes) * 100, 1)
		no_per = round((nvotes / total_votes) * 100, 1)

		npoint = (int(no_per // 10)) * '<:disapprove:1217860350943432785>'
		ypoint = (int(yes_per // 10)) * '<:approve:1217860414465904803>'

		total_votes_display = f'{total_votes} Voto'
		if total_votes > 1:
			total_votes_display += 's'
    
		display = ''
		if no_per > yes_per:
			display = f'# <:idea_chart:1217856573620097075> {total_votes_display}\n**__<:disapprove:1217860350943432785> Desaprovação ({no_per}%)__**\n<:approve:1217860414465904803> Aprovação ({yes_per}%)\n\n' + npoint + ypoint

		else:
			display = f'# <:idea_chart:1217856573620097075> {total_votes_display}\n<:approve:1217860414465904803> __**Aprovação ({yes_per}%)**__\n<:disapprove:1217860350943432785> Desaprovação ({no_per}%)\n\n' + ypoint + npoint

    
		embed.description = embed.description.split("\n▬▬▬▬▬▬▬▬▬▬▬▬▬\n")[0] + f'\n▬▬▬▬▬▬▬▬▬▬▬▬▬\n{display}'

		await idealist_repo()
		await inter.response.edit_message(embed=embed)

	  
	elif 'enterguild' in btn:
		invited_id = int(btn.split('enterguild.')[1].split('.')[0])

		if invited_id != user.id:
			return await inter.response.send_message('Não foi você que foi convidado. Vaza, seu intrometido :rage:', ephemeral=True)

		uguild_owner_id = int(btn.split('by.')[1].split('.')[0])
		embed = inter.message.embeds[0]

		uguild = udb.find_one({'ugid': uguild_owner_id})

		udb.update_one({'uid': user.id}, {'$set': {'guild': uguild_owner_id}})
    
		await inter.response.edit_message(embed=embed, components=[disnake.ui.Button(label='✅ Entrou na guilda', style=disnake.ButtonStyle.success, disabled=True)])
		await inter.followup.send(f'Você aceitou o convite. Recebeu o cargo personalizado <@&{uguild["guild_role"]}>', ephemeral=True)

		role = guild.get_role(uguild['guild_role'])  
		await user.add_roles(role)
	  
	elif 'loan' in btn:
		with open('jsons/loan.json', 'r') as file: loan = jload(file)

		uori_id = int(btn.split('.')[1])

		if str(uori_id) in loan.keys(): return await inter.response.send_message('Você já tem um empréstimo em vigor. Só é possível aceitar um contrato por vez.', ephemeral=True)
		
		if uori_id != user.id:
			return await inter.response.send_message('Só o mencionado pode assinar o contrato!', ephemeral=True)

		blanks = udb.find_one({'uid': uori_id})['blanks']
		embed = inter.message.embeds[0]
		rew = float(embed.description.split('receberá **')[1].split(' <:blank')[0])

		los = float(embed.description.split('cobrará **')[1].split(' <:blank')[0])
		dias = int(embed.description.split('durante ')[1].split(' dias')[0])

		user1 = int(embed.description.split(' quer firmar')[0][2:].replace('>', ''))

		loan[str(uori_id)] = {"diario": los, "total_a_ser_pago": dias * los, "pago": 0, "dias_restantes": dias, "acordador": user1}
		with open('jsons/loan.json', 'w') as file: jdump(loan, file, indent=2)

		udb.update_one({'uid': uori_id}, {'$inc': {'blanks': rew}})
		udb.update_one({'uid': user.id}, {'$inc': {'blanks': -rew}})
		
		try: await namedisplay(uori_id)
		except: print(error())

		try: await namedisplay(user.id)
		except: print(error())
		
		await inter.response.edit_message(embed=embed, components=[disnake.ui.Button(label='✅ Proposta aceita', style=disnake.ButtonStyle.success, disabled=True)])
		await inter.followup.send(newBlank([blanks, rew]), ephemeral=True)
	  
	elif btn == 'new_sketch':
		with open('jsons/marks.json', 'r') as file: marks = jload(file)
    
		suid = str(inter.author.id)
		if inter.author.id not in marks['sketch_uids']:
			thread = await inter.channel.create_thread(
				name="Artigo sem nome",
				type=ChannelType.private_thread,
			)
			
			await thread.send(f'Este é seu rascunho pessoal, <@{suid}>!\n▬▬▬▬▬▬▬▬▬▬▬▬▬\n# :printer: Formatação\n\nÉ de suma importância que você divida seu conteúdo em várias partes usando **# (nome do seu tópico)** para cada parte do conteúdo. A versão final do seu artigo será segmentada baseada nesses tópicos! não tente enrolar nem abordar os conteúdos de forma superficial.')
			await thread.send('https://media.discordapp.net/attachments/1221653197257572352/1222352281584795749/topic_tuto.png')
			await thread.send('\n▬▬▬▬▬▬▬▬▬▬\n- **Para começar, preencha os campos:**\n# Capa do artigo:\n> Use uma imagem de tamanho 225 x 225 ou superior, desde que seja centralizada.')


			latexbot_ping = await thread.send(f'<@{510789298321096704}>')
			await latexbot_ping.delete()
			
			marks['sketch_start'][str(thread.id)] = 1
			marks['sketch_uids'].append(inter.author.id)
			with open('jsons/marks.json', 'w') as file: jdump(marks, file, indent=2)

			await inter.response.send_message(f"Rascunho criado! https://discord.com/channels/1091742896098660372/{thread.id}", ephemeral=True)
			
		else:
			article_pos = next(pos for pos, uid in enumerate(marks['sketch_uids']) if uid == inter.author.id)
			article = list(marks['sketch_start'].keys())[article_pos]
			delete = disnake.PartialEmoji(animated=False, id='1219965874442600508', name='delete')
			
			embed= disnake.Embed(
				description=f"Você já tem um rascunho ativo: https://discord.com/channels/1091742896098660372/{article}.\nTermine ele primeiro!",
				colour=0xFFFFFF
			)
			await inter.response.send_message(embed=embed, components=[disnake.ui.Button(label='Excluir rascunho', emoji=delete, style=disnake.ButtonStyle.danger, custom_id=f"delarticle-{article}")], ephemeral=True)
		
	elif 'profile' in btn:
	    embed = inter.message.embeds[0]
	    cmdauthorname = embed.author.name.split(" - ")[0]
	  
	    if inter.author.name == cmdauthorname:
	      await showStatus(inter, client, 'edit', btn.split(".")[1])
	    else:
	      await inter.response.send_message("Calma aí! não foi você que usou esse comando!", ephemeral=True)
	
	elif btn == "dmrel_mode":
		await notify(user, "dmrel", "btn", inter)
		
	elif btn == 'post_list':
		with open('jsons/marks.json', 'r') as file: marks = jload(file)
		final = '# Suas marcações\n'
		uid = f'wiki {user.id}'
		try:
			for mark in marks[uid]:
				final += f'### {mark}\n'
				for submark in marks[uid][mark]:
					final += f'> <#{submark}>\n'
			if len(marks[uid][mark]) == 0: final += 'Ainda não tem nenhuma'
		except: final += 'Ainda não tem nenhuma'
		await inter.response.send_message(final, ephemeral=True)
	elif btn == 'lack_cards':
		await thinkerList(inter, True)

	elif btn == 'custom_search':
		await inter.message.delete()

	elif 'delarticle' in btn:
		article = int(btn.split('-')[1])
		cWrite = getSv('cWrite')

		thread = cWrite.get_thread(article)

		with open('jsons/marks.json', 'r') as file: marks = jload(file)
		try:
			marks['sketch_uids'].remove(user.id)
		except: return await inter.response.send_message('Esse rascunho não existe mais.', ephemeral=True)
		
		del marks['sketch_start'][str(article)]

		with open('jsons/marks.json', 'w') as file: jdump(marks, file, indent=2)

		await thread.delete()

		await inter.response.send_message('Rascunho excluído com sucesso.', ephemeral=True)
	elif 'delticket' in btn:
		with open('jsons/marks.json', 'r') as file: marks = jload(file)
		messages = await inter.message.channel.history(limit=None).flatten()
		first_msg = messages[::-1][0]
      
		uid = int(first_msg.content.split('<@')[1].split('>')[0])
		
		if user.id == 663525286784139274 or user.id == uid:
			if user.id != 663525286784139274: ticket = marks['tickets'][str(user.id)]
		
			del marks['tickets'][str(uid)]
			with open('jsons/marks.json', 'w') as file: jdump(marks, file, indent=2)

			return await inter.channel.delete()
				
		else: return await inter.response.send_message(":warning: Você não tem permissão para deletar esse ticket!", ephemeral=True)

	elif 'viewthread' in btn:
		thread = client.get_channel(int(btn.split('_')[1]))
		if not thread:
			await inter.response.send_message('**Esse ticket não existe mais**', ephemeral=True)
			embed = inter.message.embeds[0]
			embed.description = embed.description + '\n> <:yes:1132703714256359584> **Ticket finalizado**'
			embed.colour = 0x00FF42

			return await inter.message.edit(embed=embed, components=[])
			
		await thread.add_user(user)
		await inter.response.send_message(':ticket: **Você foi adicionado ao ticket**', ephemeral=True)

	elif 'palerequest' in btn:
		with open('jsons/marks.json', 'r') as file: marks = jload(file)

		if user.id in marks['ps_recruits']: return await inter.response.send_message("**Você já criou um pedido de candidatura..**", ephemeral=True)
		elif not any(lvlrole for lvlrole in getSv('palerequired') if lvlrole in user.roles): return await inter.response.send_message(":warning: **Você deve estar pelo menos no nível <@&1143937396027699352> para se candidatar, ou seja, precisa estudar 100 horas em calls**", ephemeral=True)

		thread = await inter.channel.create_thread(
			name='Candidatura - PS',
			type=ChannelType.private_thread	
		)

		embed = disnake.Embed(
			colour=0xFF0000,
			description='# <:paleshield:1232749831886209035> Candidatura Pale Shield\n> O que você tem a oferecer?',
		)

		await inter.response.send_message("🔰 **Pedido de candidatura criado**", ephemeral=True)

		await thread.send(f'<@{user.id}>', embed=embed)

		deltaping = await thread.send(f'<@{663525286784139274}>')
		await deltaping.delete()
		
		marks['ps_recruits'].append(user.id)
		with open('jsons/marks.json', 'w') as file: jdump(marks, file, indent=2)
    


	elif 'shelf' in btn:
		valpos = int(btn.split('_')[1])
		suid = str(user.id)
		with open('jsons/bookshelf.json', 'r') as file: shelf = jload(file)

		name, categ, annot, pages, link, votes = shelf[suid]["data"][valpos]

		if 'edit' in btn:
			await inter.response.send_modal(modal=sendBook('Editando livro da estante', name, categ, annot, pages, link, valpos, votes))
		
		elif 'delbook1' in btn:
			delete = disnake.PartialEmoji(animated=False, id='1219965874442600508', name='delete')
			await inter.response.send_message(f'Tirar o livro **"{name}"** da estante?', components=[disnake.ui.Button(label='Confirmar', emoji=delete, style=disnake.ButtonStyle.danger, custom_id=f"shelfdelbook2_{valpos}")], ephemeral=True)

		elif 'delbook2' in btn:
			cShelf = inter.channel

			past_msg = await cShelf.fetch_message(shelf[suid]["message"])

			shelf[suid]["data"].pop(valpos)

			asyncio.create_task(bookrew(user, '-'))

			newmsg = await shelfmessage(shelf, user, cShelf)
			await past_msg.delete()

			if len(shelf[suid]["data"]) > 0: 
				shelf[suid]["message"] = newmsg.id
				
				respond = f'**Livro removido da estante.**\n{newBlank([0, rew])}'

			else: 
				del shelf[suid]
			
				respond = '<:no:1132703732543529000> **Todos os livros foram removidos. Sua estante não existe mais.**'

			with open('jsons/bookshelf.json', 'w') as file: jdump(shelf, file, indent=2)

			try: await inter.response.send_message(respond, ephemeral=True)
			except: pass