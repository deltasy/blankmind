from datetime import datetime, timedelta
from random import randint
from disnake import Embed, File as Dfile
from asyncio import sleep as asleep
from traceback import format_exc as error
from zoneinfo import ZoneInfo
from copy import deepcopy
from json import load as jload, dump as jdump

from functions.page1 import getSv, newBlank, namedisplay, trueFocus
from functions.time import timeString
from functions.topweek import topweek

from mongo import udb, readSet
import pymongo

chatph = [
  "Vai la e FAZ!",
  "Sem desculpas.",
  "Tenha atitude",
  "Não espere. Faça",
  "O céu não é o limite!",
  "Estude e conquiste blanks",
  "A perfeição é um degrau",
  "Mantenha sua mente livre",
  "Concentre-se e relaxe",
  "Mantenha a consistência!",
  "Mente sã, corpo são",
  "Não há vitória sem luta",
  "Poucos realmente tentam",
  "Faça. Apenas faça.",
  "O importante é fazer",
  "Mais esforço, mais blanks",
  "Dome o futuro selvagem",
  "Faça e não lamente",
  "Se torne seu melhor",
  "Pare de procrastinar",
  "Estudou muito hoje?",
  "você é > você foi?",
  "Comemore suas vitórias",
  "Viva o progresso",
  "Estudar é uma arte",
  "Conquiste cards!",
  "Seja melhor",
  "Evolua",
  "Tempo é irrecuperável..",
  "Ninguém vai te esperar",
  "Nunca descanse demais",
  "Seja o que não são",
  "Colecione conhecimento",
  "Cuidado com o burnout"
]


def fhFilter(lvl):
  pipeline = [
        {"$match": {"level": lvl, "ugid": {"$exists": True}}},
        {"$addFields": {
            "total_contributors": {
                "$sum": {
                    "$map": {
                        "input": {"$objectToArray": "$bank.contributors"},
                        "in": "$$this.v"
                    }
                }
            }
        }},
        {"$sort": {"total_contributors": 1}} 
  ]

	
  return list(udb.aggregate(pipeline))



async def loopState(bot): 
  cPen, cDisplayID, cCommands, cBumps, cNotifys, rCave, guild = getSv(['cPen', 'cDisplays', 'cCommands', 'cBumps', 'cNotifys', 'rCave', 'guild'])
  while True:  
    try:
  
      cDisplays = bot.get_channel(cDisplayID)
      await cDisplays.edit(name=chatph[randint(0, len(chatph) - 1)])

      now = datetime.utcnow() - timedelta(hours=3)

      this_hour = now.hour
      day = now.weekday()

      newday = udb.find_one({'today': {'$exists': True}})['today']


	  # Notificações ----------------------------------------------------------
      users_notify = udb.find(
        {
          'relat.time': 
          {
          '$lte': now - timedelta(minutes=35),
          }, 
          'relat.status': ':pencil:',
          'notifys.rnearby': 1
        }
      )
		
      for user in users_notify:
        try:
          await cNotifys.send(f"🔔📄 <@{user['uid']}>, seu prazo para enviar seu relatório expirará <t:{int((user['relat']['time'] + timedelta(hours=4)).timestamp())}:R>")
        except: print(error())

      if users_notify:
        users = udb.update_many(
        {
          'relat.time': 
          {
          '$lte': now - timedelta(minutes=35),
          }, 
          'relat.status': ':pencil:',
          'notifys.rnearby': 1
        },
        {
          '$set': {'notifys.rnearby': 2}
        }
      )
      
      # Atualização de dia ----------------------------------------------------
      if newday.day != now.day: # Se for um novo dia, atualizar o dia do banco de dados
        try: # Verificar se é pra atualizar a semana
          semday_filter = {'semday': {'$lte': now - timedelta(days=6)}}
          udb.find_one(semday_filter)['semday']

          udb.update_many({'calls': {'$exists': True}}, {
            '$set': {
              'calls.stats.0': [0, 0, 0, 0, 0, 0, 0]
            }
          })
          udb.update_many({'timed.week.blank': {'$exists': True}}, {
            '$set': {
              'timed.week.blank': 0,
              'timed.week.calls': 0
            }
          })


          udb.update_one(semday_filter, {
            '$set': {
              'semday': now
            },
            '$inc': {
              'number': 1
            }
          })

          week = udb.find_one({'bumptime': {'$exists': True}})
          kings = week['kings']

          types = ['Rei das calls', 'Rei dos blanks']
          rew = 15.0

          display_top = ''
          mention_top = []

          try:
            for i in kings:
              udb.update_one({'uid': i}, {
                '$inc': {'blanks': rew}
              })

              display_top += f'<:king_crown:1157866006111342592> **`{types[i]}`** <@{i}>\n' 
              mention_top.append(f'<@{i}>')


            mention_top = ','.join(mention_top)

            topembed = Embed(
               description=f'Vocês foram os reis finais da SEMANA {week["number"]}!\n▬▬▬▬▬▬▬▬▬▬▬▬▬\n{display_top}▬▬▬▬▬▬▬▬▬▬▬▬▬\n**+15** <:blank:1124439750208655500> para cada um, parabéns!',
               colour=0xfff400
		    )
            await cNotifys.send(mention_top, embed=topembed)
          except: print(error())

        except: pass
 
        cHall = bot.get_channel(1233830022473711636) # RANK DE GUILDA DIARIO
		  
        svguild = cHall.guild
	
        by_level = [fhFilter(i + 1) for i in range(2)]

        grank = []

        best_guild = by_level[::-1][0][::-1][0]
	
        for guilds in by_level[::-1]:
          for guild in guilds[::-1]:
            grank.append(f"<@&{guild['guild_role']}> ➜ **{round(sum(guild['bank']['contributors'].values()), 1)}** <:blank:1124439750208655500>")

        grank[0] = '# :trophy: ' + grank[0]
        grank[1] = '## :second_place: ' + grank[1]
        grank[2] = '## :third_place: ' + grank[2] + '\n▬▬▬▬▬▬▬'

        gembed = Embed(
          description='\n'.join(grank),
          colour=svguild.get_role(best_guild['guild_role']).colour
	  
        )

        await cHall.purge(limit=None)
        await cHall.send(embed=gembed)
        await cHall.send(f'# <a:animated_fire:1216782884036280390> **{best_guild["guild_name"]} está dominando o hall!**')

        guild = cHall.guild
		  
        cavemode = udb.find({'cavemode': {'$gt': 0}})
		  
        for user in cavemode:
          if user['cavemode'] <= 1:
            try:
              uobj = guild.get_member(user['uid'])
		   
              await uobj.remove_roles(rCave)

              await cNotifys.send(f'🗻 {uobj.mention}, seu modo caverna acabou!')

              await trueFocus(uobj, 'disable')

              try: await namedisplay(uobj)
              except: print(error())

            except: print(error())

          else:
            try: await namedisplay(user.id)
            except: pass

        udb.update_many({'cavemode': {'$gt': 0}}, {'$inc': {'cavemode': -1}})
		  
        with open('jsons/updayte.json', 'r') as file: updayte = jload(file)
        updayte['punish'] = []
        updayte['punish_messages'] = {}
        with open('jsons/updayte.json', 'w') as file: jdump(updayte, file, indent=2)

        with open('jsons/loan.json', 'r') as file: loan = jload(file)
        loan2 = deepcopy(loan)
        for key, value in loan2.items(): 
          udb.update_one({"uid": int(key)}, {"$inc": {"blanks": -value['diario']}})
          blanks = udb.find_one({'uid': int(key)})['blanks']
    
          loan[key]['dias_restantes'] -= 1

          if blanks > 0:
            loan[key]['pago'] += value['diario']
      
          if value['dias_restantes'] - 1 == 0: 
            del loan[key]

            if blanks <= 0:
              await cNotifys.send(f'<:no:1132703732543529000> <@{key}>, não quitou sua dívida de **{value["total_a_ser_pago"]}** <:blank:1124439750208655500> e agora está devendo mais __**15**__ <:blank:1124439750208655500>.\n <@{value["acordador"]}> recuperou os blanks atrasados')
              udb.update_one({"uid": int(key)}, {"$inc": {"blanks": -15.0}})
              udb.update_one({'uid': value['acordador']}, {'$inc': {'blanks': value['total_a_ser_pago'] - value['pago']}})
            else:
              await cNotifys.send(f'<:yes:1132703714256359584> <@{key}>, você quitou sua dívida de **{value["total_a_ser_pago"]}** <:blank:1124439750208655500> acordada com <@{value["acordador"]}>')

            try: await namedisplay(int(key))
            except: pass

          with open('jsons/loan.json', 'w') as file: jdump(loan, file, indent=2)
		
        if day == 5 or day == 6:
          newstat = ":shield:"
        else:
          newstat = ":pencil:"

        users = udb.find({'relat.time': {'$exists': True}})

        updates = []
        for user in users: # Se o usuário tiver um dia diferente do dia de hoje, atualize o dia
          try:
            if now.day != user['relat']['time'].day:
              update = pymongo.UpdateOne(
                {'_id': user['_id']},
                {
                  '$set': {
                    'relat.status': newstat,
                    'relat.time': user["relat"]["time"] + timedelta(days=1)
                  },
                  '$inc': {'relat.days': 1}
                }
              )
              updates.append(update)
          except: print(f'{error()} --------> {user["uid"]}')

        if len(updates) > 0: 
          udb.bulk_write(updates)


        udb.update_many({'notifys.rnearby': 2}, {
		  '$set': {'notifys.rnearby': 1}
        })
        
        udb.update_one({'today': {'$exists': True}}, {'$set': {'today': now}}) # Atualizar o dia do banco de dados

        await topweek(bot)

		
      """
      #Tempos e penalidades de relatório -------------------------------------
      users = udb.find(
        {
          'relat.time': 
          {
          '$lt': now - timedelta(hours=1),
          }, 
          'relat.status': ':pencil:',
          'blanks': {'$gte': 0}
        }
      )
		
      updates = []
      for user in users:
        uid = user['uid']
        uobj = await bot.fetch_user(uid)
        blanks = user['blanks']
        rew = 1 + 0.025 * blanks

        try: imgprof = uobj.avatar.url
        except: imgprof = 'https://assets.mofoprod.net/network/images/discord.width-250.jpg'

        streak = user['relat']['streak']
        if streak > 1:
          msg_streak = f'\n> **Perdeu sua sequência de relatórios** ({streak} dias) <:blobsad:1132703835404652626>'
        else:
          msg_streak = ''

		  
        embed = Embed(
          title=f"**ATRASO DE RELATÓRIO┃Penalidade**",
          description=f"Você devia ter enviado um relatório no máximo até **<t:{int((user['relat']['time'] + timedelta(hours=4)).timestamp())}:t>**{msg_streak}\n▬▬▬▬▬▬▬▬▬▬▬▬",
          colour=0xed3325,
        )

        rew = 1 + 0.025 * blanks

        embed.set_thumbnail(url=imgprof)
        embed.add_field(name=newBlank([blanks, rew], '-'), value='', inline=False)
        embed.set_author(
          name=uobj.name,
          icon_url=imgprof,
        )

        await cPen.send(f'<@{user["uid"]}>', embed=embed)

        rew = rew * -1
        update = pymongo.UpdateOne({'uid': uid}, {
          '$set': {'relat.status': ':no_entry_sign:', 'relat.streak': 0},
          '$inc': {'blanks': rew}
        })

        try: await namedisplay(uid)
        except: print(error())

        updates.append(update)

      if len(updates) > 0: 
        udb.bulk_write(updates)


      """
		
      # Verificar se alguém upou seu cargo --------------------------------------------------------------
      levels = {    
        1122230870460342412: 300,
        1132163320179339344: 900,
        1135629912770891816: 2400,
	    1143937396027699352: 6000,
        1168640140395163728: 12000,
        1199039648828235857: 24000,
        1231649305362694216: 48000,
      }
  
      lvc = 1
      previus_role = 1093543202105077792

      for lvl in levels.items():
        time_required = lvl[1]
        users = udb.find({'level': lvc, 'calls.totaltime': {'$gte': time_required}})

        for user in users: # Para todos os usuários que cumprirem os requisitos, faça isso:
          udb.update_one({'_id': user['_id']},
            {
              '$inc': {'level': 1}
            }
          )

          uobj = guild.get_member(user['uid'])
          role = guild.get_role(lvl[0])

          embed = Embed(
            title="**PROMOVIDO**",
            description=f"Você ultrapassou seus limites e evoluiu seu cargo para <@&{lvl[0]}>\n\n:white_check_mark: **__{timeString(time_required)}__ estudando em calls**",
            colour=role.colour,
            timestamp = datetime.now(),
          )

          with open('images/promovido.gif', 'rb') as file:
            gif = Dfile(file, filename='promovido.gif')
            
          embed.set_image(url='https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMmpkdmttdXYzaXV0YTU5Y2J3MWF5aWZrb3I1aDNraWE0ZWphOWs1ZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/mKHqijgQPOWR19BN1r/giphy.gif')

          try: imgprof = uobj.avatar.url
          except: imgprof = 'https://assets.mofoprod.net/network/images/discord.width-250.jpg'
            
          embed.set_thumbnail(url=imgprof)
            
          await cNotifys.send(uobj.mention, embed=embed)
          await uobj.add_roles(role)

          await asleep(3)

          await uobj.remove_roles(guild.get_role(previus_role))

        previus_role = lvl[0]
        lvc += 1

      bumptime = udb.find_one({'bumptime': {'$exists': True}})['bumptime']

      if (now + timedelta(hours=3) - bumptime[0]) >= timedelta(hours=2) and bumptime[1] != 0:
        udb.update_one({'bumptime': {'$exists': True}}, {
          '$set': {'bumptime.1': 0}
        })

        await cBumps.send("Hey <@&1112017303580708936>, hora do Bump!")
    
    except: print(f'Checkusers -> {error()}')
    await asleep(600)  # Esperar 10 minutos antes de verificar novamente
