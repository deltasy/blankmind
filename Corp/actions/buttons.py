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
			return await inter.response.send_message('You were not invited. Leave, you intruder :rage:', ephemeral=True)

		uguild_owner_id = int(btn.split('by.')[1].split('.')[0])
		embed = inter.message.embeds[0]

		uguild = udb.find_one({'ugid': uguild_owner_id})

		udb.update_one({'uid': user.id}, {'$set': {'guild': uguild_owner_id}})
		udb.update_one({'ugid': uguild_owner_id}, {'$push': {'guild_members': user.id}, '$set': {f'bank.contributors.{user.id}': 0}})
    
		await inter.response.edit_message(embed=embed, components=[disnake.ui.Button(label='✅ Joined the guild', style=disnake.ButtonStyle.success, disabled=True)])
		await inter.followup.send(f'You accepted the invitation. Received the custom role <@&{uguild["guild_role"]}>', ephemeral=True)

		role = guild.get_role(uguild['guild_role'])  
		await user.add_roles(role)

	elif 'upgradeguild' in btn:
		btnowner_id = int(btn.split('.')[1])
		
		if btnowner_id != user.id:
			return await inter.response.send_message('⏫ Only the guild owner can upgrade', ephemeral=True)

		lvlup_cost = float(btn.split('.')[2])
		
		uguild = udb.find_one({'ugid': btnowner_id})
		if uguild["bank"]["blanks"] < lvlup_cost:
			return await inter.response.send_message(f':warning: The guild Vault does not have enough blanks for this yet\n> **Still need {lvlup_cost - uguild["bank"]["blanks"]}** <:blank:1124439750208655500>', ephemeral=True)

		svguild = getSv('guild')
		
		grole = svguild.get_role(uguild['guild_role'])

		
		embed = disnake.Embed(
			description=f'# The guild <@&{uguild["guild_role"]}> leveled up!\n> Now at Level **{uguild["level"] + 1}**',
			colour=grole.colour
		)
		embedprogress = disnake.Embed(
			description=f'# The guild <@&{grole.id}> earned its own exclusive chat.',
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
		
			newchannel = await svguild.create_text_channel(f'║{grole.name.lower().replace(" ","・")}', category=category, overwrites=overwrites, topic=f':cyclone: **Guild {uguild["guild_name"].capitalize()} chat**')
			await newchannel.edit(position=1)
			await newchannel.send(f'**Congratulations, guild** <@&{grole.id}>! You earned your own chat')
			await cChat.send(embed=embedprogress)
			await grole.edit(name=grole.name.replace(grole.name.split(' (')[::-1][0], f'Lv{uguild["level"] + 1})'))
		

		udb.update_one({'ugid': btnowner_id}, {'$inc': {'level': 1, 'bank.blanks': -lvlup_cost}})
		
		return await inter.response.send_message(embed=embed)
			
    
