from disnake import ApplicationCommandInteraction as Dinter, Embed
import disnake
from disnake.ext import commands as com
from traceback import format_exc as error
import re
from unidecode import unidecode

from functions.page1 import getSv, agetSv, specChannel

from traceback import format_exc as error

def command(client):
  @client.slash_command(name="searchbuddy")
  async def search(
      inter = Dinter,
      filtros = com.Param(min_length=3, max_length=50)
  ):
    """
    🔎😎┃Encontre colegas de estudo por filtragem
    Parameters
    ----------
    filtros: Use vírgulas para especificar mais. Exemplo ➔ Idade: +18, faculdade
    """
    cIntros, guild = getSv(['cIntros', 'guild'])

    filters = unidecode(filtros.lower()).replace(", ", ",").split(',') 

    alt_ages = []
	  
    try: 
      age_great = next(i for i in filters if re.search(r'^idade: \+\d+$', i))
      filters.remove(age_great)
      age_great = int(age_great.split(': +')[1])
      alt_ages = [i for i in range(age_great, 40)]

    except: age_great = False

    try: 
      age_less = next(i for i in filters if re.search(r'^idade: -\d+$', i))
      filters.remove(age_less)
      age_less = int(age_less.split(': ')[1])
		
      alt_ages = [abs(i) for i in range(age_less, 8)]

    except: age_less = False

    messages = await agetSv('mIntros')

    if alt_ages:
      if filters:
        filtered_messages = [msg for msg in messages if any(re.search(r'\bidade: {}\b'.format(age), unidecode(msg.content.lower())) for age in alt_ages) and all(word in msg.content.lower() for word in filters)]

      else:
        filtered_messages = [msg for msg in messages if any(re.search(r'\bidade: {}\b'.format(age), unidecode(msg.content.lower())) for age in alt_ages)]
	
    else:
      filtered_messages = [msg for msg in messages if all(word in unidecode(msg.content.lower()) for word in filters)]


    gathered = [f'- **{msg.author.display_name.split(" ═ ")[0].capitalize()}** ═ https://discord.com/channels/1091742896098660372/1124455706309963817/{msg.id}\n' for msg in filtered_messages]
    try: gathered = gathered[:60]
    except: pass
	  
    if len(gathered) == 0:
      return await inter.response.send_message(f'## {filtros.capitalize()}\n> **Nenhuma pessoa encontrada. Tente ser menos específico..**', ephemeral=True)

    merged, merged_strings = '', []
    for pos, i in enumerate(gathered):
      merged += i
      if len(merged) + len(i) > 1024:
        merged_strings.append(merged)
        merged = ''

    if not merged_strings: merged_strings.append(merged)

    warn = ''

    embed = Embed(
      description=f'# 🔎 Estudantes filtrados:\n## {filtros.capitalize()}\n> (Do mais recente ao mais antigo)',
      colour=0xFFFFFF
    )
    """
    def dividir_texto(texto, tamanho_max):
      partes = []
      link_regex = r'https?://\S+'
      pos = 0
      while pos < len(texto):
        # Encontra o próximo link a partir da posição atual
        match = re.search(link_regex, texto[pos:])
        if match:
            link_pos = pos + match.start()
            # Verifica se o link está dentro do limite
            if link_pos + len(match.group()) <= pos + tamanho_max:
                # Divide o texto até o próximo link ou tamanho máximo
                partes.append(texto[pos:link_pos + len(match.group())])
                pos = link_pos + len(match.group())
            else:
                # Divide o texto no tamanho máximo
                partes.append(texto[pos:pos + tamanho_max])
                pos += tamanho_max
        else:
            # Não há mais links, divide o texto no tamanho máximo
            partes.append(texto[pos:pos + tamanho_max])
            pos += tamanho_max
      return partes

    partes_embed = dividir_texto(final, 1024)[:25]
    """
	
    [embed.add_field(name='', value=parte, inline=False) for parte in merged_strings]
    #[embed.add_field(name='', value=final[part:part+1024], inline=False) for part in range(0, len(final), 1024)]

    count = sum(field.value.count('https') for field in embed.fields)

    if count > 1: cdisp = f'{count} estudantes encontrados'
    else: cdisp = '1 estudante encontrado'

    print(f'{inter.author.id} pesquisou: {filtros}')

    delete = disnake.PartialEmoji(animated=False, id='1219965874442600508', name='delete')
    await inter.response.send_message(f'🔎 **{cdisp}**. Enviei a lista na sua DM')
    await inter.author.send(embed=embed, components=[disnake.ui.Button(label='Excluir', emoji=delete, style=disnake.ButtonStyle.danger, custom_id="custom_search")])
    
     


