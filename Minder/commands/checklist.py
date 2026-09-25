import disnake
from json import load as jload, dump as jdump
from traceback import format_exc as error

from functions.page1 import specChannel
from mongo import udb, readSet

class checkModal(disnake.ui.Modal):
  def __init__(self):
    components = [
        disnake.ui.TextInput(
            label="Use um asterico antes para criar um tópico",
            placeholder="*Tópico\nTarefa 1\nTarefa 2...",
            custom_id="checklist",
            style=disnake.TextInputStyle.paragraph,
            min_length=10,
            max_length=1000,
        ),
    ]
    super().__init__(title="Criar checklist", components=components)
    
  async def callback(self, inter: disnake.ModalInteraction):
    try:
      items = list(inter.text_values.items())[0][1].split("\n") # Pegar tarefas da checklist  
      desc = ""

      cont = 0
      for i in range(len(items)):
        try:
          if items[i][0] != "*":
            cont += 1
            desc += f"`{cont}.` :white_large_square: {items[i].capitalize()}\n"
          else:
            cont = 0
            if i != 0: desc += '\n'
            desc += f'**{items[i].upper().replace("* ", "").replace("*", "")}**\n'
        except: continue

      if desc.count(':white_large_square:') == 0: return await inter.response.send_message('Você só criou tópicos, mas não tarefas. Siga o modelo.', ephemeral=True)

      if desc.count("**") == 0: desc = '**LISTA**\n' + desc

      checklist_count = readSet(inter.author.id, 'checklists', 0)
      udb.update_one({'uid': inter.author.id}, {'$inc': {'checklists': 1}})
		
      embed = disnake.Embed(
        description=f'## <:auto_checklist:1220507904961024080> AUTOLIST (#{checklist_count + 1})\n▬▬▬▬▬▬\n\n{desc}\n▬▬▬▬▬▬\n- Reaja para marcar os quadrados um por um\n- Digite **-deletar** para excluir a lista',
        colour=0xFFFFFF,
      )
      
      try: imgprof = inter.author.avatar.url
      except: imgprof = 'https://assets.mofoprod.net/network/images/discord.width-250.jpg'

      embed.set_author(
        name=inter.author.display_name.split(' ═ ')[0].capitalize(),
        icon_url=imgprof,
      )
      
      emsg = await inter.channel.send(embed=embed)
      await emsg.add_reaction("🟩")
      await emsg.add_reaction("🟥")
      
      with open('jsons/marks.json', 'r') as file: marks = jload(file)
      marks["checklists"][inter.author.id] = emsg.id
      with open('jsons/marks.json', 'w') as file: jdump(marks, file, indent=2)
        
      try:
        await inter.response.send_message()
      except: pass
        
    except: print(error())


def command(client):
  @client.slash_command(name="checklist")
  async def Schecklist(inter: disnake.ApplicationCommandInteraction):
    """
    ⬜┃Crie uma checklist automática do que precisa fazer hoje!
    """
    if await specChannel(inter, [1119710450741940325]): return
		
    with open('jsons/marks.json', 'r') as file: marks = jload(file)
    id = str(inter.author.id)
    if id in marks["checklists"]:
        await inter.response.send_message(f'Você já tem uma **[checklist automática ativa](<https://discord.com/channels/{inter.guild.id}/{inter.channel.id}/{marks["checklists"][id]}>)**! termine-a primeiro', ephemeral=True)
    else:
      await inter.response.send_modal(modal=checkModal())