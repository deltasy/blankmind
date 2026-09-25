import disnake
from disnake import Embed, PermissionOverwrite as Dperms, ChannelType
from json import load as jload, dump as jdump

from mongo import udb, readSet
from functions.page1 import getSv

async def dropdown(inter):
	user = inter.author
	did = inter.component.custom_id


	if 'shelf' in did:
		bname = inter.data.values[0].split(' ➜ ')[1].strip()

		with open('jsons/bookshelf.json', 'r') as file: shelf = jload(file)

		souid = did.split('_')[1]

		valpos, val = next([i, array] for i, array in enumerate(shelf[souid]["data"]) if bname in array[0])

		name, categ, annot, pages, link, votes = val

		if link: link = '\n**Link do livro:** '+ link.replace('Https', 'https')
		if pages: pages = '\n**Páginas lidas:** '+ str(pages)

		embed=disnake.Embed(
			description=f'# {name}\n▬▬▬▬▬▬▬▬▬▬▬▬\n**Categoria:** {categ}{pages}{link}\n▬▬▬▬▬▬▬▬▬▬▬▬\n# 📃 Anotações:\n{annot}',
			colour=0x0CA4A9
		)

		oldembed = inter.message.embeds[0]

		embed.set_author(
			name = oldembed.author.name,
			icon_url = oldembed.author.icon_url
		)

		if souid == str(user.id): # Se o dono escolheu o livro
			delete = disnake.PartialEmoji(animated=False, id='1219965874442600508', name='delete')
			comps=[disnake.ui.Button(label='Editar', emoji='✏️', style=disnake.ButtonStyle.primary, custom_id=f"shelfedit_{valpos}"),disnake.ui.Button(label='Excluir livro', emoji=delete, style=disnake.ButtonStyle.danger, custom_id=f"shelfdelbook1_{valpos}")]

		else: comps = []
		
		return await inter.response.send_message(embed=embed, components=comps, ephemeral=True)




	
	elif did == 'report':
		with open('jsons/marks.json', 'r') as file: marks = jload(file)
			
		if str(user.id) in marks['tickets'].keys(): return await inter.response.send_message(f'# Você já possui um ticket ativo!\n> <#{marks["tickets"][str(user.id)]}>', ephemeral=True)
		
		option = inter.data['values'][0]
		cPale = getSv('cPalemain')

		embed = disnake.Embed(
			description='',
			colour=0xfc5600
		)
		
		if option == "🤖 Relatar bug":
			embed.description = '# 🤖 Qual bug você achou?\n- **Seja claro e específico**\n- **Se possível, mostre prints**\n- **Exemplo:**\n - <:no:1132703732543529000> **Jeito errado:** Minhas horas n contaram (muito geral)\n - <:yes:1132703714256359584> **Jeito certo:** Criei uma sala privada mas ela não foi destruída e meu tempo não estava sendo contado. Isso aconteceu quando eu fiz X, Y, etc..'
		
		else:
			if option == "🔰 Denunciar usuário": embed.description = '# 🔰 Informe:\n- **Nome do usuário**\n- **Motivo da denúncia com as respectivas provas**'
			else: embed.description = embed.description = '# ❔ Diga qual a sua dúvida\n- **Seja claro e direto**'
		
		thread = await inter.channel.create_thread(
			name=option,
			type=ChannelType.private_thread
			
		)
		
		delete = disnake.PartialEmoji(animated=False, id='1219965874442600508', name='delete')
		await thread.send(user.mention, embed=embed, components=[disnake.ui.Button(label="Excluir ticket", emoji=delete, style=disnake.ButtonStyle.danger, custom_id=f"delticket_{user.id}")])
		with open('jsons/marks.json', 'r') as file: marks = jload(file)
		marks['tickets'][str(user.id)] = thread.id
		with open('jsons/marks.json', 'w') as file: jdump(marks, file, indent=2)

		pembed = disnake.Embed(
			description=f'<@{user.id}> quer **{option}**',
			colour=0xfc5600
		)
		
		await cPale.send(embed=pembed,components=[disnake.ui.Button(label="Ver", emoji='👀', style=disnake.ButtonStyle.primary, custom_id=f"viewthread_{thread.id}")])
		
		
		return await inter.response.send_message('# Ticket criado', ephemeral=True)

	
	elif did == 'role_dropdown1':
		true_role = {"🚨 Updates": 1162917883777663037, "🚀 Bump": 1112017303580708936, "📝 Relatórios": 1138591176681869322, "💠 Guildas": 1230693176839245846, "🎬 Cinema": 1230632596334055465, "🎲 Minigames": 1230697271771922475}

	elif did == 'role_dropdown2':
		true_role = {"🎓 Faculdade": 1115751360344887316, "🎓 Vestibulando": 1143697792158666856, "🎓 3º ano": 1115751063610470581, "🎓 2º ano": 1115751059692986608, "🎓 1º ano": 1115751050041888931, "🎓 Fundamental": 1115750314679730207}
		for idd in true_role.values():
			try: await user.remove_roles(disnake.utils.get(inter.guild.roles, id=idd))
			except: pass
	elif did == 'role_dropdown3':
		true_role = {"🎯 ENEM": 1178025309589745665, "🎯 Vestibular": 1178026381586739211, "🎯 Concurso Público": 1207455384671883395, "🎯 Concurso Militar": 1207455386874150963, "🎯 Olimpíedas": 1238313392985608193}

	elif did == 'role_dropdown4':
		true_role = {"🌐 Norte": 1205909270030454835, "🌐 Nordeste": 1205908446231138396, "🌐 Sul": 1205909274207723530, "🌐 Sudeste": 1205909278607802479, "🌐 Centro-Oeste": 1205909753511804979}
	
	rids = [true_role[role] for role in inter.data['values']]
    
	final = ''
	for role_id in rids:
		role = disnake.utils.get(inter.guild.roles, id=role_id)
    
		if role:
			if role_id == 1138591176681869322:
				vRelator = udb.find_one({'uid': user.id, 'relat': {'$exists': True}})
				if not vRelator:
					final += f':warning: **Não pude te dar o cargo <@&{role_id}>\n> Você precisa ser um relator para ter esse cargo. Use o comando `/mission set`\n\n**'
				
				else:
					fields = {1138591176681869322: "rnearby"}
					field = fields[role_id]
					notifys_descs = []
					readSet(user.id, f'notifys.{field}', 0)

					udb.update_one({'uid': user.id}, {
						'$bit': {f'notifys.{field}': {'xor': 1}}
					})
            
		if role in user.roles:
			await user.remove_roles(role)
			final += f':x: **Removi o cargo** <@&{role_id}>\n\n'
		else:
			await user.add_roles(role)
			final += f':white_check_mark: **Te dei o cargo** <@&{role_id}>\n\n'
        
	try: await inter.response.send_message(final, ephemeral=True)
	except: return