from disnake import ApplicationCommandInteraction as Dinter
from json import load as jload, dump as jdump
import disnake
from traceback import format_exc as error
from unidecode import unidecode

from traceback import format_exc as error

from actions.calls import day_name

global ucycles
with open('jsons/usercycles.json', 'r') as file: ucycles = jload(file)

class checkModal(disnake.ui.Modal):
  def __init__(self, display: str):
    components = [
        disnake.ui.TextInput(
            label="Siga a formatação (Emojis são opcionais)",
            value=display,
            custom_id="studycycle",
            style=disnake.TextInputStyle.paragraph,
            min_length=10,
            max_length=1000,
        ),
    ]
    super().__init__(title="Criar ciclo de estudos", components=components)

  async def callback(self, inter: disnake.ModalInteraction):
    try:
      items = [item.strip().capitalize() for item in list(inter.text_values.items())[0][1].split("\n")]
  
      semday_detect = ['Segunda', 'Terca', 'Quarta', 'Quinta', 'Sexta', 'Sabado', 'Domingo']
      semday = []

      current_semday = 'Segunda'

      suid = str(inter.author.id)

      if suid in ucycles['custom_cycles']: # Se já existir, resete
        del ucycles['custom_cycles'][suid]
        with open('jsons/usercycles.json', 'w') as file: jdump(ucycles, file, indent=2)


      ucycles['custom_cycles'][suid] = {}
      for item in items:
        if unidecode(item) in semday_detect: 
          current_semday = item

          ucycles['custom_cycles'][suid][item] = {}
          semday.append(item)
          
        elif item:
          try:
            sub_divide = next(pos for pos, char in enumerate(item) if char.isdigit())
            subject, times = item[:sub_divide], item[sub_divide:]

            first_char = next(char for char in subject if char.isalpha())
            index_divide = subject.find(first_char)

            subject = subject[:index_divide] + subject[index_divide:].capitalize()

            ucycles['custom_cycles'][suid][current_semday][subject] = list(map(int, times.split('min')[0].split('h')))

          except:
            all_capitalized = '\n'.join(items)
            try: await inter.response.send_message(f'# :warning: Formatação incorreta. Faça assim:\n(DIA DA SEMANA)\n**(Matéria)** **(horas)**h**(minutos)**min\n▬▬▬▬▬▬▬▬▬▬▬▬▬\n- Sua tentativa anterior:\n\n{all_capitalized.replace(item, ":warning: **Mal formatado ➜ " + item + "**")}', ephemeral=True)
            except: pass


      with open('jsons/usercycles.json', 'w') as file: jdump(ucycles, file, indent=2)
  
      try:
        await inter.response.send_message(f'📀 **Ciclo de estudos alterado com sucesso**', ephemeral=True)
      except: pass
        
    except: pass

def command(client):
  remind_opts = {"Bumps": 0, "Relatório próximo": 1}
  @client.slash_command(name="cycle")
  async def scycle(
      inter: Dinter,
  ):
    pass
  
  @scycle.sub_command(name="set")
  async def sb_cycleset(
      inter: Dinter,
  ):
    """
    📀┃Sete um ciclo de estudos personalizado
    """
    user = inter.author
    with open('jsons/usercycles.json', 'r') as file: ucycles = jload(file)

    if str(user.id) in ucycles['custom_cycles']:
        display = ''
        for key, val in ucycles['custom_cycles'][str(user.id)].items():
          display += key.upper() + '\n'
          for subject in val.items():
              if "CHECKPOINTED" not in subject:
                display += f'{subject[0]}{subject[1][0]}h{subject[1][1]}min\n'
          display += '\n'

    else:
        display = "SEGUNDA\n📐 Matemática 3h25min\n🌐 Geografia 0h40min\n\nTERÇA\n🌵 Biologia 1h00min"

    await inter.response.send_modal(modal=checkModal(display))

  @scycle.sub_command(name="today")
  async def sb_cycleset(
      inter: Dinter,
  ):
    """
    📀👀┃Veja qual o seu ciclo de hoje
    """
    with open('jsons/usercycles.json', 'r') as file: ucycles = jload(file)

    user = inter.author
    uid = str(user.id)

    day = day_name()
    display = ''

    if uid in ucycles['custom_cycles']:
        display = f'**{day}**\n'
        checked_indexes = None

        try:
          checked_indexes = next(pos for pos, key in enumerate(list(ucycles['custom_cycles'][uid][day].keys())) if key == ucycles['custom_cycles'][uid][day]["CHECKPOINTED"])
        except: pass

        if not checked_indexes: checked_indexes = -1

        for i, (key, val) in enumerate(ucycles['custom_cycles'][uid][day].items()):
          if key != "CHECKPOINTED":

            if val[0] != 1: pl1 = 's'
            else: pl1 = ''

            if val[1] != 1: pl2 = 's'
            else: pl2 = ''
			
            if i > checked_indexes: display += f'- **{key}**/ {val[0]} hora{pl1} e {val[1]} minuto{pl2}\n'.replace(' e 0 minutos', '').replace('0 horas e ', '')
            elif i < checked_indexes: display += f'- :white_check_mark: **{key}**/ {val[0]} hora{pl1} e {val[1]} minuto{pl2}\n'.replace(' e 0 minutos', '').replace('0 horas e ', '')
            else: display += f'▬▬▬▬▬\n➜ **{key}/ {val[0]} hora{pl1} e {val[1]} minuto{pl2}**\n▬▬▬▬▬\n'.replace(' e 0 minutos', '').replace('0 horas e ', '')

    if not display: return await inter.response.send_message(f'Você não montou um ciclo de estudo para hoje **({day})**', ephemeral=True)
    else: return await inter.response.send_message(display)
