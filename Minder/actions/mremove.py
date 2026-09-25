from datetime import datetime, timezone
from mongo import udb
import disnake

from json import load as jload, dump as jdump, dumps as jdumps
from traceback import format_exc as error

from copy import deepcopy

from functions.page1 import namedisplay, getSv

async def memberRemove(member, cLeave):
  if member.bot: return

  ulvl = udb.find_one({'uid': member.id})['level']
	
  ecolor = 0xff0000

  now = datetime.now().astimezone(timezone.utc)
  joined_at = member.joined_at.replace(tzinfo=timezone.utc)
	
  tdiff = now - joined_at
  mdays = tdiff.days

  mdays_disp = f'📜 Durou {mdays} dia'
  if mdays_disp != 1: mdays_disp += 's'

  levels = [
    1093543202105077792,
    1122230870460342412,
    1132163320179339344,
    1135629912770891816,
    1143937396027699352,
    1168640140395163728,
    1199039648828235857
  ]
	
  embed = disnake.Embed(
    description=f'### <:left:1219746952896577537> {member.mention} ({member.name})\n> <@&{levels[ulvl - 1]}>',
    color=ecolor,
  )       

  embed.set_footer(text=mdays_disp)

  try: embed.set_author(name=user.name.capitalize())
  except: pass

  await cLeave.send(embed=embed)

  cNotifys, cMembers = getSv(['cNotifys', 'cMembers'])

  inviter = udb.find_one({'uid': member.id})['invited_by']
  if inviter and inviter != 302050872383242240:
    try:
      udb.update_one({'uid': inviter}, {'$inc': {'blanks': -3.0}})

      try: await namedisplay(inviter)
      except: print(error())
    except: print(error())

  print(member.id)
  try:
    udb.delete_one(
      {'uid': member.id}
    )
  except: pass

  jsons = ['calls', 'callgroups', 'invites', 'marks']
  for json in jsons:
    try:
      with open(f'jsons/{json}.json', 'r') as file: db = jload(file)
      del db[str(member.id)]
      with open(f'jsons/{json}.json', 'w') as file: jdump(db, file, indent=2)
    except: pass

    with open('jsons/loan.json', 'r') as file: loan = jload(file)

  # Dívidas
  loan2 = deepcopy(loan)
  for user, value in loan2.items():
    if int(user) == member.id:
      udb.update_one({'uid': value['acordador']}, {'$inc': {'blanks': value['total_a_ser_pago'] - value['pago']}})

      del loan[user]

      await cNotifys.send(f'<:left:1219746952896577537> <@{user}>, saiu do server sem quitar sua dívida de **{value["total_a_ser_pago"]}** <:blank:1124439750208655500>.\n <@{value["acordador"]}> recuperou os blanks atrasados')

      try: await namedisplay(value['acordador'])
      except: pass

      break
	
  with open('jsons/loan.json', 'w') as file: jdump(loan, file, indent=2)
