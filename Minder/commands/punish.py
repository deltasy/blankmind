import disnake
from disnake.ext import commands as com
from traceback import format_exc as error
from datetime import timedelta
from json import load as jload, dump as jdump

from functions.page1 import getSv

global reasons, times, dreasons, dtimes, true_times
reasons = {"Mal comportamento": 0, "Mensagens / conversas inadequadas": 1, "Desrespeito": 2, "Spam / flood": 3, "Raid": 4}
times = {"30 minutos": 0, "3 horas": 1, "6 horas": 2, "12 horas": 3, "1 dia": 4}

dreasons = ['Mal comportamento', 'Mensagem / conversas inadequadas', 'Desrespeito', 'Spam / flood', 'Raid']
dtimes = ['30 minutos', '3 horas', '6 horas', '12 horas', '1 dia']
true_times = [0.5, 3, 6, 12]

def command(client):
  @client.slash_command(name="punish")
  async def spunish(
    inter = disnake.ApplicationCommandInteraction,
    usuário: str = com.Param(max_length=100),
    motivo: com.option_enum(reasons) = 0,
    tempo: com.option_enum(times) = 0,
  ):
    """
    🔰 Pale Shield┃Puna um usuário
    Parameters
    ----------
    usuário: @Fulano
    motivo: Seja justo em sua punição
    tempo: Seja justo em sua punição
    """
    user = inter.author

    with open('jsons/updayte.json', 'r') as file: updayte = jload(file)

    if user.id in updayte['punish']: return await inter.response.send_message("**Você já puniu alguém hoje. Você só tem direito a 1 punição por dia.**", ephemeral=True)

    try:
      punished = await inter.guild.fetch_member(int(usuário.replace('<@', '').replace('>', '')))
      if not punished: return await inter.response.send_message("**Escolha um usuário válido**", ephemeral=True)
    except: return await inter.response.send_message("**Escolha um usuário válido**", ephemeral=True)

    if tempo == 4: duration = timedelta(days=1)
    elif tempo == 0: duration = timedelta(minutes=30)
    else: duration = timedelta(hours=true_times[tempo])

    embed = disnake.Embed(
      description='# A Pale Shield está de olho..\n> **1 Membro foi punido**',
      colour=0xFFFFFF
    )
    embed.set_thumbnail(url='https://media.discordapp.net/attachments/1223022126198558734/1226904885702955058/paleshield.png')

    await inter.response.send_message(f"<:yes:1132703714256359584> **Usuário punido, bom trabalho.**", ephemeral=True)

    chat, paleshield = getSv(['cChat', 'cPaleShield'])
    await chat.send(embed=embed)

    updayte['punish'].append(user.id)
    with open('jsons/updayte.json', 'w') as file: jdump(updayte, file, indent=2)

    await punished.edit(timeout=duration)

    embed2 = disnake.Embed(
      description=f'# <:paleshield:1232749831886209035>:shaking_face: {user.mention} puniu {punished.mention}\n> **Motivo:** {dreasons[motivo]}\n> **Duração:** {dtimes[tempo]}',
      colour=0xFFFFFF
    )
    await paleshield.send(embed=embed2)

    try: return await punished.send(f'# <:paleshield:1232749831886209035> **Um membro da Pale Shield** te castigou\n> Motivo: **{dreasons[motivo]}**\n> Duração: **{dtimes[tempo]}**\n\nNão cometa erros novamente..')
    except: return