from disnake import ApplicationCommandInteraction as Dinter, Embed
import disnake
from disnake.ext import commands as com
from traceback import format_exc as error
import re
from unidecode import unidecode

from functions.page1 import getSv, agetSv, specChannel
from actions.buttons import modelist_prepare

from traceback import format_exc as error
from mongo import udb, readSet

def command(client):
  @client.slash_command(name="modelist")
  async def modelist(
      inter = Dinter,
  ):
    """
    🧰┃Abre seu painel de modos de estudo
    """
    if inter.author.voice: return await inter.response.send_message('Saia da sua call para alterar os modos.', ephemeral=True)

    uid = inter.author.id

    readSet(uid, 'modelist', {'focado': 100, 'pomodoro': 100, 'ciclodeestudos': 100})

    udata = udb.find_one({'uid': uid})

    cavemode = 0
    try:
      if udata['cavemode'] > 0: cavemode = 1
    except: pass


    new_components = modelist_prepare(udata['modelist'], uid)
    if cavemode: 
      new_components.pop(0)
      new_components.pop(2)

    embed = Embed(
      description='# Painel de modos de estudo\n> Os modos que estiverem verdes serão os que ativarão automaticamente quando você entrar em calls',
      colour=0xFFFFFF
    )
    
    await inter.response.send_message(embed=embed,components=new_components)
    




