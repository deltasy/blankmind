from functions.page1 import notify
import disnake
from traceback import format_exc as error
from json import load as jload


from mongo import udb
from functions.page1 import getSv

def modelist_prepare(umodelist, uid, cavemode=0):
  try:
    components=[disnake.ui.Button(label='Focado', emoji='🎯', style=disnake.ButtonStyle.secondary, custom_id=f"configmode-focado-{uid}"), disnake.ui.Button(label='Pomodoro', emoji='🍅', style=disnake.ButtonStyle.secondary, custom_id=f"configmode-pomodoro-{uid}"), disnake.ui.Button(label='Ciclo', emoji='📀', style=disnake.ButtonStyle.secondary, custom_id=f"configmode-ciclodeestudos-{uid}")]

    for pos, (key, val) in enumerate(umodelist.items()):
      if val == 100: 
        
        components[pos].style = disnake.ButtonStyle.secondary

      elif val == 1: 
        components[pos].style = disnake.ButtonStyle.success
        if pos == 1 and components[2].style == disnake.ButtonStyle.success:
          components[2].style = disnake.ButtonStyle.secondary
        elif pos == 2 and components[1].style == disnake.ButtonStyle.success:
          components[1].style = disnake.ButtonStyle.secondary

      else: 
        components[pos].style = disnake.ButtonStyle.secondary
        
  except: pass

  components.append(disnake.ui.Button(label='Caverna', emoji='🗻', style=disnake.ButtonStyle.primary, custom_id=f"configmode-caverna-{uid}"))
  return components

async def buttonClick(inter, client):
	guild = inter.guild
	inter.component.disabled = True
	btn = inter.component.custom_id
	user = inter.author

	if 'configmode' in btn:
		mode, truid = btn.split('-')[1:]
		modepos = {"focado": 0, "pomodoro": 1, "ciclodeestudos": 2, "caverna": 3}
		fchooses= {'focado': '🎯 A maioria dos chats desaparecerão assim que você entrar em alguma call', 'pomodoro': '🍅 Alterne entre períodos de descanso e estudo\n> Use o comando </pomodoro set:1225204130730217544> para personalizar','ciclodeestudos': '📀 Funciona como um pomodoro, mas é mais completo. Você pode nomear cada parte do ciclo, aumentando o nível de organização\n> Use o comando </cycle set:1225204130730217542> para personalizar', 'caverna': '⛰️ O modo de foco absoluto, perfeito para lobos solitários. Isola você de todos os chats e de todas as distrações por um tempo determinado **(Não é possível cancelar esse modo enquanto ele já estiver ativo!)**\n# Uma vez escolhido, terá que esperar o tempo acabar'}

		if truid != str(user.id): return await inter.response.send_message('Não foi você que usou esse comando!', ephemeral=True)
		elif user.voice: return await inter.response.send_message('Saia da sua call para alterar os modos.', ephemeral=True)

		style = inter.component.style

		try:
			first_choose = None
			if style == disnake.ButtonStyle.success: 
				change_state, active = disnake.ButtonStyle.secondary, 0

			else: 
				first_choose = fchooses[mode]

				change_state, active = disnake.ButtonStyle.success, 1

			cave_dropdown, cavemode = None, 0
			if first_choose: 
				if not mode == 'caverna': await inter.response.send_message(first_choose, ephemeral=True)
				else:
					roles = ['3 dias', '6 dias', '9 dias', '12 dias', '15 dias']
					cave_dropdown = disnake.ui.Select(
        				placeholder='Escolha o tempo que ficará na caverna',
        				options=[disnake.SelectOption(label=role, value=role) for role in roles],
       					custom_id='cavemode_select',
        				min_values=1,
        				max_values=1
					)

					view = disnake.ui.View()
					view.add_item(cave_dropdown)

					try: await inter.response.send_message(first_choose, view=view, ephemeral=True)
					except: pass

					cavemode=1

			udata = udb.find_one({'uid': user.id})
			new_components = modelist_prepare(udata['modelist'], user.id)

			try:
				if udata['cavemode'] > 0: cavemode = 2
			except: pass

			try: # Caso esteja no modo caverna(new_components fica menor)
				if new_components[2].style == disnake.ButtonStyle.success and mode == 'pomodoro' and change_state == disnake.ButtonStyle.success: 
					new_components[2].style = disnake.ButtonStyle.secondary
					udb.update_one({'uid': user.id}, {'$set': {f'modelist.ciclodeestudos': 0}})

				elif new_components[1].style == disnake.ButtonStyle.success and  mode == 'ciclodeestudos' and change_state == disnake.ButtonStyle.success:
					new_components[1].style = disnake.ButtonStyle.secondary
					udb.update_one({'uid': user.id}, {'$set': {f'modelist.pomodoro': 0}})

				new_components[modepos[mode]].style = change_state
			except: pass
		
			if cavemode: 
				if cavemode == 2: # Já está no modo caverna
					new_components.pop(0)
					new_components.pop(2)
	
				elif cavemode: # Quer entrar no modo caverna
					new_components[3].style = disnake.ButtonStyle.primary
					
				
			udb.update_one({'uid': user.id}, {'$set': {f'modelist.{mode}': active}})

			await inter.message.edit(components=new_components)
			
			try: await inter.response.send_message()
			except: pass

		except: print(error())
	
	elif btn == 'leave_focus':
		if user.voice: return await inter.response.send_message('Saia da sua call antes de clicar no botão..', ephemeral=True)
		print(f'{user.nick} Saiu do foco manualmente.')
		try: 
			await user.remove_roles(getSv('rFocus'))
			return await inter.response.send_message('Modo focado desativado.', ephemeral=True)
		except: pass
			
    
