import disnake
from disnake import PermissionOverwrite as Dperms
from traceback import format_exc as error

from mongo import udb
from functions.page1 import getSv

async def buttonClick(inter, client):
	guild = inter.guild
	inter.component.disabled = True
	btn = inter.component.custom_id
	user = inter.author

	if 'enterguild' in btn:
		invited_id = int(btn.split('enterguild.')[1].split('.')[0])

		if invited_id != user.id:
			return await inter.response.send_message('Não foi você que foi convidado. Vaza, seu intrometido :rage:', ephemeral=True)

		uguild_owner_id = int(btn.split('by.')[1].split('.')[0])
		embed = inter.message.embeds[0]

		uguild = udb.find_one({'ugid': uguild_owner_id})

		udb.update_one({'uid': user.id}, {'$set': {'guild': uguild_owner_id}})
		udb.update_one({'ugid': uguild_owner_id}, {'$push': {'guild_members': user.id}, '$set': {f'bank.contributors.{user.id}': 0}})
    
		await inter.response.edit_message(embed=embed, components=[disnake.ui.Button(label='✅ Entrou na guilda', style=disnake.ButtonStyle.success, disabled=True)])
		await inter.followup.send(f'Você aceitou o convite. Recebeu o cargo personalizado <@&{uguild["guild_role"]}>', ephemeral=True)

		role = guild.get_role(uguild['guild_role'])  
		await user.add_roles(role)

	elif 'upgradeguild' in btn:
		btnowner_id = int(btn.split('.')[1])
		
		if btnowner_id != user.id:
			return await inter.response.send_message('⏫ Apenas o dono da guilda pode dar upgrade', ephemeral=True)

		lvlup_cost = float(btn.split('.')[2])
		
		uguild = udb.find_one({'ugid': btnowner_id})
		if uguild["bank"]["blanks"] < lvlup_cost:
			return await inter.response.send_message(f':warning: O Cofre da guilda ainda não tem blanks o suficiente para isso\n> **Ainda falta {lvlup_cost - uguild["bank"]["blanks"]}** <:blank:1124439750208655500>', ephemeral=True)

		svguild = getSv('guild')
		
		grole = svguild.get_role(uguild['guild_role'])

		
		embed = disnake.Embed(
			description=f'# O nível da guilda <@&{uguild["guild_role"]}> subiu!\n> Agora está no Nível **{uguild["level"] + 1}**',
			colour=grole.colour
		)
		embedprogress = disnake.Embed(
			description=f'# A guilda <@&{grole.id}> conquistou seu próprio chat exclusivo.',
			colour=grole.colour
		)

		rFocus, cChat = getSv(['rFocus', 'cChat'])

		if uguild["level"] == 1:
			category = disnake.utils.get(svguild.categories, id=1233161089177358398)
		
			overwrites = {
				guild.default_role: Dperms(view_channel=False),
				rFocus: Dperms(view_channel=False),
				grole: Dperms(view_channel=True),
				user: Dperms(manage_messages=True, mention_everyone=True)
			}
		
			newchannel = await svguild.create_text_channel(f'║{grole.name.lower().replace(" ","・")}', category=category, overwrites=overwrites, topic=f':cyclone: **Chat da guilda {uguild["guild_name"].capitalize()}**')
			await newchannel.edit(position=1)
			await newchannel.send(f'**Parabéns, guilda** <@&{grole.id}>! Vocês conquistaram seu próprio chat')
			await cChat.send(embed=embedprogress)
			await grole.edit(name=grole.name.replace(grole.name.split(' (')[::-1][0], f'Nv{uguild["level"] + 1})'))
		

		udb.update_one({'ugid': btnowner_id}, {'$inc': {'level': 1, 'bank.blanks': -lvlup_cost}})
		
		return await inter.response.send_message(embed=embed)
			
    
