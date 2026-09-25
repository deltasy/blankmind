import disnake
from disnake.ext import commands as com
from datetime import datetime, timedelta
from re import sub as filterlen
from random import randint
from traceback import format_exc as error
from asyncio import sleep as asleep

from functions.page1 import newBlank, specChannel, notify, getSv, namedisplay
from functions.time import timeFormat, userTime, timeString

from mongo import udb, readSet
import pymongo

global mission_loading
mission_loading = []

class sendRel(disnake.ui.Modal):
    def __init__(self):
        # The details of the modal, and its components
        components = [
            disnake.ui.TextInput(
                label="Matérias / assuntos",
                placeholder="EX: Matemática - probabilidade, funções",
                custom_id="materia",
                min_length=1,
                max_length=50
            ),
            disnake.ui.TextInput(
                label="Relatório",
                custom_id="relatorio",
                placeholder="Quanto maior o relatório, mais pontos ganhos\nNÃO ENVIE VÁRIAS VEZES! ESPERE.",
                style=disnake.TextInputStyle.paragraph,
                min_length=10,
                max_length=3200,
            ),
        ]
        super().__init__(title="Enviar relatório diário", components=components)

    async def callback(self, inter: disnake.ModalInteraction):
      vars = []
      if inter.author.id in mission_loading:
        for key, value in inter.text_values.items(): vars.append(value)

        await inter.response.send_message("Seu relatório já foi enviado! ele é grande, então tenha calma", ephemeral=True)
        try: await inter.response.send_message(None)
        except: return
			
      mission_loading.append(inter.author.id)
		
      for key, value in inter.text_values.items(): vars.append(value)
      title, text = vars
      user = inter.author
      uid = user.id

      udata = udb.find_one({'uid': uid})
      
      try:
        reltam = len(filterlen(r'[^a-zA-Z0-9]', '', text))
        val = udata['blanks']

        streak = udata['relat']['streak']

        if reltam < 70:
          relniv = [f":page_facing_up: Relatório simples (#{udata['relat']['sends'] + 1})", 0]
        elif reltam < 200:
          relniv = [f":clipboard: Relatório razoável (#{udata['relat']['sends'] + 1})", 0.5]
        elif reltam < 400:
          relniv = [f":book: Relatório bom (#{udata['relat']['sends'] + 1})", 1.0]
        elif reltam <= 550:
          relniv = [f":blue_book: Relatório muito bom (#{udata['relat']['sends'] + 1})", 1.5]
        elif reltam <= 1900:
          relniv = [f":books: Relatório incrível (#{udata['relat']['sends'] + 1})", 2.0]
        else:
          relniv = [f":rosette: OBRA PRIMA! (#{udata['relat']['sends'] + 1})", 3.5]

        if streak > 14: streak_limit = 14
        else: streak_limit = streak
		  
        rew = round(1.5 + relniv[1] + streak_limit * 0.15, 1)
		  
        cRels = getSv('cRels')

        statusday = ((datetime.now() - timedelta(hours=3)) - udb.find_one({'semday': {'$exists': True}})['semday']).days
        try: calltime = udata['calls']['stats'][0][statusday]
        except: calltime = udata['calls']['stats']['0'][statusday]
        if calltime > 0:
          msg_calltime = f'\n> :timer: **Estudo em calls:** {timeString(calltime)}'
        else:
          msg_calltime = ''

        if streak > 1:
          msg_streak = f'\n> <a:animated_fire:1216782884036280390> **Sequência:** {streak} dias'
        else:
          msg_streak = ''
			

        title = ' ' + title
        title = title.upper().replace("PROGR", "💻 PROGR").replace(" MATEM", " 📐 MATEM").replace(" SIMULADO", " ✏️ SIMULADO").replace(" EXER", "✏️  EXER").replace(" QUEST", " ✏️ QUEST").replace(" SOCIO", " 👨‍👦 SOCIO").replace(" FÍS", " 🛸 FÍS").replace(" FISIC", " 🛸 FISIC").replace(" FILOS", " ❔ FILOS").replace(" FILÓS", " ❔ FILÓS").replace(" GEO", " 🌐 GEO").replace(" BIO", " 🌿 BIO").replace(" ING", " 🗣️ ING").replace(" HIST", " ⏳ HIST").replace(" LITE", " 📜 LITE").replace(" QUIM", " 🧪 QUIM").replace(" QUÍM", " 🧪 QUÍM").replace(" REDAÇ", " ✏️ REDAÇ").replace(" PORT", " 🗣️ PORT")

        if title[0] == ' ':
          title = title.replace(' ', '', 1)
		  
        subject = relniv[0].split(": ")
        embed = disnake.Embed(
            title='', 
            description=f'## {subject[0] + ": " + subject[1].upper()}\n### {title}\n▬▬▬▬▬▬▬▬▬▬▬▬\n\n{text}\n\n▬▬▬▬▬▬▬▬▬▬▬▬{msg_calltime}{msg_streak}\n> {newBlank([val, rew])}',
            colour=0x33FF33,     
        )

        if 'OBRA PRIMA' in relniv[0]:
          embed.colour = 0xf1de52
          readSet(user.id, 'relat.masterpiece', 0)
          udb.update_one({'uid': user.id}, {'$inc': {'relat.masterpiece': 1}})

        if udata['relat']['sends'] == 1:
          await user.send("**Mandarei cada relatório seu aqui, para você acompanhar seu progresso!**\n\n> Clique no botão abaixo para ativar/desativar essas mensagens", components=[disnake.ui.Button(label="🔕 Desativar", style=disnake.ButtonStyle.danger, custom_id="dmrel_mode")])
          await notify(user, "dmrel")
        
        if await notify(user, "dmrel", "verify") == 1:
          try:      
            await user.send(embed=embed)
          except Exception as e: print(f"DMrel -> {error()}")

        if udata["relat"]["last_id"] != 0:
          lastrel = f'\n\n**Relatório Anterior:** https://discord.com/channels/{cRels.guild.id}/{cRels.id}/{udata["relat"]["last_id"]}'
        else:
          lastrel = '\n> -'
			
        embed.description += lastrel

        try: imgprof = inter.author.avatar.url
        except: imgprof = 'https://assets.mofoprod.net/network/images/discord.width-250.jpg'

        if relniv[1] == 4.0: # Se for obra prima
          embed.set_author(
            name=f'{inter.author.display_name.split("═")[0]} criou uma obra-prima',
            icon_url=imgprof
		  )

        else:
          embed.set_author(
            name=inter.author.display_name.split("═")[0],
            icon_url=imgprof
          )

        embed.set_thumbnail(url=imgprof)
        
        newrel = await cRels.send(f'<@{uid}>', embed=embed)

        if user.id != 663525286784139274:
          udb.update_one(
            {'uid': uid},
            {
              '$inc': {'blanks': rew, 'timed.week.blank': rew, 'relat.sends': 1, 'relat.streak': 1},
              '$set': {'relat.status': ':white_check_mark:', 'relat.last_id': newrel.id}
           
            }
          )

        try: await namedisplay(uid)
        except: print(error())

        await inter.response.send_message(None) # Fechar modal

        await asleep(20)
        mission_loading.remove(user.id)
		
      except: pass#print(error())


def command(client):  
  @client.slash_command(name="mission")
  async def smission(
      inter: disnake.ApplicationCommandInteraction,
  ):
    pass
        
  @smission.sub_command(name="set")
  async def smset(
    inter: disnake.ApplicationCommandInteraction,
    hora: com.Range[int, 6, 22],
    minutos: com.Range[int, 0, 59]
  ):
    """
    🕗 (Ganhe 10 𝔅 pelo primeiro uso)┃Defina o horário que irá enviar o relatório diário
    Parameters
    ----------
    hora: 🕗 Entre 06h ~ 22h
    minutos: 🕗 Entre 0m ~ 59m
    """

    if await specChannel(inter): return
      
    user = inter.author
    uid = user.id
    relatime = readSet(user.id, 'relat', -1)
    newtime = datetime.now() - timedelta(hours=3)
    newtime = newtime.replace(hour=hora).replace(minute=minutos)

    if relatime == -1: # Primeira vez que usar o relatório
      udb.update_one(
        {'uid': uid},
        {
		  '$set': {
             'relat': {
               'status': ':shield:',
               'time': newtime,
               'days': 0,
               'sends': 0,
               'last_id': 0,
               'streak': 0
              }
           },
           '$inc': {
			   'blanks': 10,
			   'timed.week.blank': 10
		   }
		}
      )

      val = udb.find_one({'uid': uid})['blanks']

      try: await namedisplay(uid)
      except: print(error())

      timedisp = newtime + timedelta(hours=3)

      embed = disnake.Embed(
          title=":pencil: **NOVO RELATOR**",
          description=f"{user.mention} firmou o compromisso e se tornou um escritor de relatórios. **Você pode ganhar mais blanks, mas também pode perdê-los se falhar em sua missão**.\n▬▬▬▬▬▬▬▬▬▬▬▬\n● Todo dia de semana, no horário que você escolheu, use o comando `/mission send` para enviar seu relatório (ele deve conter tudo que você estudou/revisou no dia)\n\n● **Horário escolhido: <t:{int(timedisp.timestamp())}:t>**\n> Você pode enviar seu relatório das __**<t:{int((timedisp - timedelta(hours=1)).timestamp())}:t>**__ até as __**<t:{int((timedisp + timedelta(hours=1)).timestamp())}:t>**__. \n\n● Tome **10 <:blank:1124439750208655500> (blanks)** para iniciar. Boa sorte!\n\n",
          colour=0xf1de52,
          timestamp = datetime.now(),
      )
  
      embed.set_image(url='https://images.contentstack.io/v3/assets/blt312bfd9a3caf2bfc/blt46c0b3b4e87bee44/605422df2415931ccd447c65/5c925da56dea4.gif')
      embed.set_footer(
        text="Novo relator"
      )

      try: await user.add_roles(user.guild.get_role(1092918220400369775))
      except: pass
      
      await inter.response.send_message(embed=embed)
    else:  
      udata = udb.find_one({'uid': uid})
      tnow = datetime.now() - timedelta(hours=3)
        
      tutime = tnow.replace(hour=hora).replace(minute=minutos)
      tutime_utc = tutime + timedelta(hours=3)

      interval = tnow - tutime
      warn, nextday = '', timedelta(days=0)

      if interval >= timedelta(hours=1): # Se estiver mais tarde do que o horário atual        
        nextday = timedelta(days=1)
        warn = f'\n> :warning: Já está mais tarde que esse horário, então seu relatório foi adiado para **Amanhã**'

      prehour = tutime_utc - timedelta(hours=1) + nextday
      poshour = tutime_utc + timedelta(hours=1) + nextday
      
      await inter.response.send_message(f"**Horário de envio de relatório atualizado**\nVocê pode enviar seu relatório das __**<t:{int(prehour.timestamp())}:t>**__ até as __**<t:{int(poshour.timestamp())}:t>**__{warn}")
      udb.update_one(
          {'uid': uid},
          {'$set': {
            'relat.time': newtime + nextday
          }}
        )


  
  @smission.sub_command(name="send")
  async def smsend(
    inter: disnake.ApplicationCommandInteraction
):  
    """
    📄┃Envie seu relatório diário
    """
    if await specChannel(inter): return

    try:
      if inter.author.id in mission_loading:
        mission_loading.remove(inter.author.id)
        return await inter.response.send_message("Ocorreu um erro ao enviar seu relatório. Use `/mission send` novamente", ephemeral=True)
      user = udb.find_one({'uid': inter.author.id})['relat']
      if user['status'] == ":white_check_mark:":
        await inter.response.send_message("Você já enviou o relatório de hoje 😎👍 pode relaxar", ephemeral=True)
      elif user['status'] == ":no_entry_sign:":
        await inter.response.send_message("Já passou do seu horário. Você falhou, tente amanhã 😞", ephemeral=True)
      elif not userTime(inter.author.id):
        utime = user['time'] + timedelta(hours=3)

        await inter.response.send_message(f"Você só pode enviar seu relatório das <t:{int((utime - timedelta(hours=1)).timestamp())}:t> até as <t:{int((utime + timedelta(hours=1)).timestamp())}:t>", ephemeral=True)
      else:
        await inter.response.send_modal(modal=sendRel())
        
    except:
      print(error())
      return await inter.response.send_message("Você precisa ser um **relator** para enviar relatórios!\n> Para se tornar um, use `/mission set`", ephemeral=True)


  
  @smission.sub_command(name="giveup")
  async def smgiveup(
    inter: disnake.ApplicationCommandInteraction,
    confirmar = '',
  ):
    """
    ❌┃Desista de ser um relator
    Parameters
    ----------
    confirmar: Digite 'sim' para prosseguir. Você perderá todas suas estatísticas de relator, cuidado.
    """
    try: 
      urelat = udb.find_one({'uid': inter.author.id})['relat']
    except: 
      return await inter.response.send_message("Você nem é um relator ainda... como vai desistir??", ephemeral=True)
    
    if confirmar == 'sim':
      if urelat['days'] < 7:
        return await inter.response.send_message(f"Você precisa ter sido um relator por **pelo menos 7 dias**.\n> Para você, ainda faltam {7 - urelat['days']} dia{'s' if 7 - urelat['days'] != 1 else ''}", ephemeral=True)
      udb.update_one({'uid': inter.author.id}, {'$unset': {'relat': 1}})
      return await inter.response.send_message("**Você não é mais um relator!**", ephemeral=True)
    else:
      return await inter.response.send_message("Você deve digitar **sim** dentro do campo **confirmar**", ephemeral=True)
    
