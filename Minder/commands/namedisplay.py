import disnake
from disnake.ext import commands as com
from traceback import format_exc as error

from mongo import udb, readSet

from functions.page1 import namedisplay

class customDisplay(disnake.ui.Modal):
    def __init__(self):
        # The details of the modal, and its components
        components = [
            disnake.ui.TextInput(
                label="O texto escolhido ficará ao lado do seu nome",
                placeholder="EX: Seu curso / emoji / título, etc.\nNão use nenhum número.",
                custom_id="materia",
                min_length=1,
                max_length=25
            )
        ]
        super().__init__(title="Crie seu próprio display", components=components)

    async def callback(self, inter: disnake.ModalInteraction):
      vars = []
      display = list(inter.text_values.values())[0]
      user = inter.author
      uid = user.id

      uprevious = ' '.join(user.display_name[:32 - 3 - len(display)].split('═')[0].split())

      preview = uprevious + f' ═ {display}'

      false_chars = ['𝔅', '∞h', '═', 'bump']

      compact_display = display.replace(' ', '')
      
      if any([char for char in compact_display if char.isdigit()]): 
        return await inter.response.send_message(f'# :warning: Erro\n> **Números não são permitidos.**', ephemeral=True)
      
      elif any([char for char in false_chars if char in compact_display]):
        return await inter.response.send_message(f'# :warning: Erro\n> **Não é permitido simular estatísticas existentes.**', ephemeral=True)

      eyes = disnake.PartialEmoji(animated=False, id='1132703714256359584', name='yes')
      try: await inter.response.send_message(f'# {preview}\n> Seu nome ficará dessa forma. Você ainda poderá alterar toda a parte que vem antes de "═" **({preview.split(" ═ ")[0]})** á vontade.\n\n> :warning: Essa ação custará **250** <:blank:1124439750208655500>, então pense com cuidado.\n▬▬▬▬▬', components=[disnake.ui.Button(label="Confirmar alteração", emoji=eyes, style=disnake.ButtonStyle.primary, custom_id=f"displaychange_custom_{display}_250")], ephemeral=True) # Fechar modal
      except: pass

def command(client):
  global display_opts, display_list
  display_opts = {"❌ Nenhuma": 0, '🌟 Personalizada': 1, "Blanks": 2, "Tempo em calls": 3, "Bumps": 4}
  display_list = ['', '', 'blanks', 'calls.totaltime', 'bumps']
  
  @client.slash_command(name="namedisplay")
  async def sdisplay(
    inter = disnake.ApplicationCommandInteraction,
    estatística: com.option_enum(display_opts) = 0
  ):
    """
    🎩┃ Vincule/desvincule uma estatística ao seu nome
    """
    
    uid = inter.author.id

    try:
      actual_stat = udb.find_one({'uid': uid})['linked_stat']
      if actual_stat == estatística: return await inter.response.send_message('**Você já tem essa estatística vinculada ao seu nome. Nenhuma alteração foi feita.**', ephemeral=True)
    except: pass

    if estatística == 1: # Status personalizado
      await inter.response.send_modal(modal=customDisplay())

    else: 
      dicon = ['', '', ' 𝔅', 'h', ' bumps']
      udata = udb.find_one({'uid': uid})

      if estatística == 0: # Desvincular estatísticas
        display, preview = 0, inter.author.display_name.split('═')[0].strip()

      else: 
        display = readSet(uid, display_list[estatística])

        if estatística == 2: display = round(display, 1) # Blanks
        elif estatística == 3: display = int(display // 60) # Horas

        uprevious = ' '.join(inter.author.display_name[:32 - 3 - len(str(display)) - len(dicon[estatística])].split('═')[0].split())
        preview = uprevious + f' ═ {display}{dicon[estatística]}'

      eyes = disnake.PartialEmoji(animated=False, id='1132703714256359584', name='yes')

      if estatística == 0:
        return await inter.response.send_message(f'# {preview}\n> Seu nome ficará dessa forma, sem nenhuma estatística.\n\n> :warning: **Essa ação custará __5__ <:blank:1124439750208655500>, então pense com cuidado.**\n▬▬▬▬▬', components=[disnake.ui.Button(label="Confirmar alteração", emoji=eyes, style=disnake.ButtonStyle.primary, custom_id=f"displaychange_{estatística}_{display}{dicon[estatística]}_5")], ephemeral=True) # Fechar modal
		
      await inter.response.send_message(f'# {preview}\n> Seu nome ficará dessa forma. Você ainda poderá alterar toda a parte que vem antes de "═" **({preview.split(" ═ ")[0]})** á vontade.\n\n> :warning: **Essa ação custará __5__ <:blank:1124439750208655500>, então pense com cuidado.**\n▬▬▬▬▬', components=[disnake.ui.Button(label="Confirmar alteração", emoji=eyes, style=disnake.ButtonStyle.primary, custom_id=f"displaychange_{estatística}_{display}{dicon[estatística]}_5")], ephemeral=True) # Fechar modal
      