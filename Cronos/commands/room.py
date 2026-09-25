from disnake import ApplicationCommandInteraction as Dinter, utils as Dutils, Embed
import json

from disnake.ext import commands as com
from traceback import format_exc as error

from actions.calls import invGroup
from functions.page1 import specChannel, getSv

with open('jsons/callgroups.json', 'r') as file: cgdb = json.load(file)

def command(client):
  @client.slash_command(name="room")
  async def Sroom(
    inter: Dinter,
    usuários: str = com.Param(max_length=100),
  ):
    """
    🔒┃Convide pessoas para sua sala privada!
    Parameters
    ----------
    usuários: EX: @fulano @cicrano @beltrano
    """
    if await specChannel(inter): return
    uids = usuários.replace(">", "").replace("<", "").replace("@", "")
    uids = ' '.join(uids.split()).split(' ')

    if inter.author.voice and '💠' in inter.author.voice.channel.name:
      return await inter.response.send_message('**Não é possível convidar usuários externos se sua sala for uma sala de guilda!**', ephemeral=True)

    try: 
      users = [Dutils.get(client.users, id=int(i)) for i in uids if not Dutils.get(client.users, id=int(i)).bot]
    except: users = '0'

    for uid in uids:
      if len(uid) != 18 and len(uid) != 19:
        return await inter.response.send_message('**Insira usuários válidos!**', ephemeral=True)
      elif int(uid) == inter.author.id:
        return await inter.response.send_message('**Ué, você quer convidar você mesmo? que triste.** :pensive:', ephemeral=True)
    
    if len(users) == len(uids):
      invgroup = await(invGroup(inter.author))
      cRoom = getSv('cRoom')
      if invgroup == 0:
        return await inter.response.send_message(f"**Você não está numa sala privada para usar esse comando.**\n> Seja convidado ou Conecte-se a <#{cRoom.id}> para criar sua sala", ephemeral=True)
      
      else:
        with open('jsons/callgroups.json', 'r') as file: cgdb = json.load(file)
        channel = invgroup

        uquant = len(cgdb[str(invgroup)]) - 1
        
        if uquant > 1:
          uquant = f" **(Com {uquant} pessoas)**"
        else:
          uquant = ""

        channelobj = client.get_channel(int(channel))

        for user in users:
          try: await channelobj.set_permissions(user, connect=True)
          except: print(error())#pass

        if len(users) == 1:
          desc = f":envelope: {inter.author.mention} o convidou para um **estudo comprometido** na <#{channel}>! {uquant}\n\n> :warning: Você pode ganhar mais **blanks** nesse canal, mas lembre-se: **Se alguém sair dessa sala, ela será destruída**"
        else:
          desc = f"{inter.author.mention} os convidou para um **estudo comprometido** na <#{channel}>! {uquant}\n\n> :warning: Vocês podem ganhar mais **blanks**, mas lembre-se: **Se alguém sair dessa sala, ela será destruída**"
        embed = Embed(
          title="Convite para sala privada",
          description=desc,
          colour=0x5865F2,
        )
        return await inter.response.send_message(', '.join([f'<@{i}>' for i in uids]), embed=embed)
    else:
      return await inter.response.send_message('**Parâmetro inválido!** Mencione usuários **válidos**', ephemeral=True)
