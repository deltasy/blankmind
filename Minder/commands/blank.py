import disnake
from disnake.ext import commands as com
from json import load as jload, dump as jdump
from traceback import format_exc as error

from functions.page1 import specChannel, newBlank, namedisplay
from mongo import udb

def command(client):
  @client.slash_command(name="blank")
  async def sblank(
    inter = disnake.ApplicationCommandInteraction,
    teste = ''
  ):
    pass

  @sblank.sub_command(name="pay")
  async def sbpay(
    inter = disnake.ApplicationCommandInteraction,
    usuário = com.Param(max_length=30),
    valor = com.Param(max_length=3)
  ): 
    """
    💰┃Pague um usuário
    Parameters
    ----------
    usuário: @fulano
    valor: 1 ~ 100 𝔅
    """

    if await specChannel(inter): return

    blanks = valor
    
    user = inter.author
    ublanks = udb.find_one({'uid': user.id})['blanks']
    try:
      blanks = float(blanks.replace(',', '.'))
    except:
      return await inter.response.send_message('Insira um valor válido.', ephemeral=True)

    if blanks > 100 or blanks <= 0:
      return await inter.response.send_message('Os valores devem estar **entre 1 e 100 blanks*', ephemeral=True)
      
    elif blanks > ublanks:
      await inter.response.send_message(f'Você é :point_right: __POBRE__ :point_left: demais para isso. Ainda faltam **{round(blanks - ublanks, 1)} <:blank:1124439750208655500>**', ephemeral=True)
      
    else:
      try:
        user2 = client.get_user(int(usuário.replace('>', '').replace('<@', '')))
        if user2.id == user.id:
          return await inter.response.send_message('Você doou blanks para você mesmo! parabéns, rei da matemática', ephemeral=True)
      except:
        await inter.response.send_message('Escolha um usuário válido', ephemeral=True)

      u2data = udb.find_one({'uid': user2.id})

      if not u2data:
        return await inter.response.send_message('Escolha um usuário válido', ephemeral=True)

      udb.update_one({'uid': user.id}, {'$set': {'blanks': ublanks - blanks}})
      udb.update_one({'uid': user2.id}, {'$inc': {'blanks': blanks}})

      if blanks <= 2: 
        displaym = 'te deu uma merreca.. que insulto'
      elif blanks <= 10:
        displaym = 'te fez uma doação'
      elif blanks <= 30:
        displaym = 'te fez uma grande doação'
      elif blanks <= 60:
        displaym = 'te deu uma pequena fortuna. Faça bom proveito'
      elif blanks >= 80:
        displaym = 'te deu uma grande fortuna 🤑'
        
      embed = disnake.Embed(
          colour=0x33FF33,
          description=f"{user.mention} {displaym}\n{newBlank([u2data['blanks'], blanks])}",
      )
      
      await inter.response.send_message(user2.mention, embed=embed)

      try: await namedisplay(user.id)
      except: pass

      try: await namedisplay(user2.id)
      except: pass


  @sblank.sub_command(name="loan")
  async def sbloan(
    inter = disnake.ApplicationCommandInteraction,
    usuário = com.Param(max_length=30),
    emprestado = com.Param(max_length=4),
    desejado = com.Param(max_length=4),
    dias = com.Param(max_length=2)
  ): 
    """
    💸┃Crie um contrato de empréstimo com um usuário
    Parameters
    ----------
    usuário: @fulano
    emprestado: 5 ~ 30 𝔅 | Quantidade de blanks que você emprestará ao usuário
    desejado: 5 ~ 30 𝔅 | Quantidade de blanks que você quer receber do usuário
    dias: 5 ~ 15 𝔅 | Duração do empréstimo em dias
    """

    if await specChannel(inter): return

    user = inter.author
    ublanks = udb.find_one({'uid': user.id})['blanks']
    
    try:
      emprestado = float(emprestado.replace(',', '.'))
      desejado = float(desejado.replace(',', '.'))
      dias = int(dias)
    except:
      return await inter.response.send_message('Insira valores válidos.', ephemeral=True)

    if emprestado > 50 or emprestado <= 4 or desejado > 50 or desejado <= 4:
      return await inter.response.send_message('Os valores devem estar **entre 5 e 30 blanks**', ephemeral=True)

    elif dias <= 4 or dias > 15:
      return await inter.response.send_message('Escolha um valor **entre 5 e 15** dias', ephemeral=True)

    elif emprestado > ublanks:
      await inter.response.send_message(f'Você é :point_right: __POBRE__ :point_left: demais para emprestar dinheiro. Ainda faltam **{round(emprestado - ublanks, 1)} <:blank:1124439750208655500>**', ephemeral=True)

    else:
      try:
        user2 = client.get_user(int(usuário.replace('>', '').replace('<@', '')))
        if user2.id == user.id:
          return await inter.response.send_message('Você não pode emprestar dinheiro a si mesmo, obviamente', ephemeral=True)
      except:
        await inter.response.send_message('Escolha um usuário válido', ephemeral=True)

      u2data = udb.find_one({'uid': user2.id})
      if not u2data:
        return await inter.response.send_message('Escolha um usuário válido', ephemeral=True)

      embed = disnake.Embed(
          colour=0x952df7,
          description=f"{user.mention} quer firmar um contrato de empréstimo com você.\n\n## :page_with_curl: Termos\n- Você receberá **{emprestado} <:blank:1124439750208655500> imediatamente**\n- Ele te cobrará **{round((emprestado + desejado)/dias, 1)} <:blank:1124439750208655500> por dia durante {dias} dias**\n\n:warning: Se você não pagar a dívida a tempo, ele recuperará os <:blank:1124439750208655500> atrasados e você deverá 15 <:blank:1124439750208655500>.",
      )

      msg = await inter.response.send_message(user2.mention, embed=embed, components=[disnake.ui.Button(label='✍️ Aceitar contrato', style=disnake.ButtonStyle.primary, custom_id=f"loan.{user2.id}")])