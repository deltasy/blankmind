from disnake import ApplicationCommandInteraction as Dinter, Embed
from json import load as jload, dump as jdump
from disnake.ext import commands as com
from traceback import format_exc as error

from mongo import udb, readSet

global ucycles
with open('jsons/usercycles.json', 'r') as file: ucycles = jload(file)

def command(client):
  remind_opts = {"Bumps": 0, "Relatório próximo": 1}
  @client.slash_command(name="pomodoro")
  async def spomodoro(
      inter: Dinter,
  ):
    pass

  @spomodoro.sub_command(name="set")
  async def spomodoro(
      inter: Dinter,
      estudo: com.Range[int, 25, 200],
      pausa: com.Range[int, 5, 100]
  ):
    """
    🍅┃Sete um ciclo pomodoro!
    Parameters
    ----------
    estudo: Tempo que você irá estudar (em minutos)
    pausa: Tempo que você terá pausas durante o estudo (em minutos)
    """
    user = inter.author
    
    pomodoro = readSet(user.id, 'cycles.pomodoro', [25, 5, 0])
      
    udb.update_one({'uid': user.id}, {
      '$set': {
        'cycles': {
          'pomodoro': [estudo, pausa]
        }
      }
    })

    ucycles['pomodoro'][str(user.id)] = {"📖 Estudo": estudo, "💤 Descanso": pausa}

    with open('jsons/usercycles.json', 'w') as file: jdump(ucycles, file, indent=2)

    await inter.response.send_message(f"🍅 Pomodoro setado! Divisão **{estudo}/{pausa}**")

