from functions.page1 import notify
import disnake
from traceback import format_exc as error
from json import load as jload


from mongo import udb
from functions.page1 import getSv

def modelist_prepare(umodelist, uid, cavemode=0):
  try:
    components=[disnake.ui.Button(label='Focused', emoji='🎯', style=disnake.ButtonStyle.secondary, custom_id=f"configmode-focado-{uid}"), disnake.ui.Button(label='Pomodoro', emoji='🍅', style=disnake.ButtonStyle.secondary, custom_id=f"configmode-pomodoro-{uid}"), disnake.ui.Button(label='Cycle', emoji='📀', style=disnake.ButtonStyle.secondary, custom_id=f"configmode-ciclodeestudos-{uid}")]

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

  components.append(disnake.ui.Button(label='Cave', emoji='🗻', style=disnake.ButtonStyle.primary, custom_id=f"configmode-caverna-{uid}"))
  return components

async def buttonClick(inter, client):
	guild = inter.guild
	inter.component.disabled = True
	btn = inter.component.custom_id
	user = inter.author

	if 'configmode' in btn:
		mode, truid = btn.split('-')[1:]
		modepos = {"focado": 0, "pomodoro": 1, "ciclodeestudos": 2, "caverna": 3}
		fchooses= {'focado': '🎯 Most chats will disappear as soon as you join a call', 'pomodoro': '🍅 Alternate between rest and study periods\n> Use the command </pomodoro set:1225204130730217544> to customize','ciclodeestudos': '📀 Works like a pomodoro, but is more complete. You can name each part of the cycle, increasing the level of organization\n> Use the command </cycle set:1225204130730217542> to customize', 'caverna': '⛰️ The absolute focus mode, perfect for lone wolves. Isolates you from all chats and all distractions for a set time **(It is not possible to cancel this mode while it is already active!)**\n# Once chosen, you will have to wait for the time to end'}

		if truid != str(user.id): return await inter.response.send_message('You were not the one who used this command!', ephemeral=True)
		elif user.voice: return await inter.response.send_message('Leave your call to change modes.', ephemeral=True)

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
					roles = ['3 days', '6 days', '9 days', '12 days', '15 days']
					cave_dropdown = disnake.ui.Select(
        				placeholder='Choose the time you will stay in the cave',
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

			try: # In case you are in cave mode(new_components gets smaller)
				if new_components[2].style == disnake.ButtonStyle.success and mode == 'pomodoro' and change_state == disnake.ButtonStyle.success: 
					new_components[2].style = disnake.ButtonStyle.secondary
					udb.update_one({'uid': user.id}, {'$set': {f'modelist.ciclodeestudos': 0}})

				elif new_components[1].style == disnake.ButtonStyle.success and  mode == 'ciclodeestudos' and change_state == disnake.ButtonStyle.success:
					new_components[1].style = disnake.ButtonStyle.secondary
					udb.update_one({'uid': user.id}, {'$set': {f'modelist.pomodoro': 0}})

				new_components[modepos[mode]].style = change_state
			except: pass
		
			if cavemode: 
				if cavemode == 2: # Already in cave mode
					new_components.pop(0)
					new_components.pop(2)
	
				elif cavemode: # Want to enter cave mode
					new_components[3].style = disnake.ButtonStyle.primary
					
				
			udb.update_one({'uid': user.id}, {'$set': {f'modelist.{mode}': active}})

			await inter.message.edit(components=new_components)
			
			try: await inter.response.send_message()
			except: pass

		except: print(error())
	
	elif btn == 'leave_focus':
		if user.voice: return await inter.response.send_message('Leave your call before clicking the button..', ephemeral=True)
		print(f'{user.nick} Manually exited focus.')
		try: 
			await user.remove_roles(getSv('rFocus'))
			return await inter.response.send_message('Focused mode disabled.', ephemeral=True)
		except: pass
			
    
