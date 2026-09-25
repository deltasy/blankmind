import disnake
from datetime import datetime, timedelta
from functions.page1 import trueFocus, namedisplay, getSv
import asyncio

from mongo import udb, readSet

async def dropdown(inter):
	user = inter.author
	did = inter.component.custom_id

	if did == 'cavemode_select':
		rCave, cChat = getSv(['rCave', 'cChat'])
		days = int(inter.data.values[0].replace(' dias', ''))

		if days == 1: pl = ''
		else: pl = 's'

		udb.update_one({'uid': user.id}, {'$set': {'cavemode': days}})

		await inter.response.send_message(f"🗻 Você entrou no modo caverna por **{days} dia{pl}**. Você não poderá ver mensagens de ninguém e todos os chats comuns ficarão indisponíveis.", ephemeral=True)

		try: await user.move_to(None)
		except: pass

		await user.add_roles(rCave)
		asyncio.create_task(trueFocus(user))

		embed = disnake.Embed(
			colour=0x000000,
			description=f'🗻 {user.mention} Entrou no modo caverna até o dia **<t:{int((datetime.now() + timedelta(days=days)).timestamp())}:D>**. Nada pode pará-lo!\n\n> Ele ficará completamente invisível para todos durante esse tempo, focado em seus objetivos.',
		)

		try: await namedisplay(user)
		except: pass

		return await cChat.send(embed=embed)