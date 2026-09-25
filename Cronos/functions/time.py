from datetime import datetime, timedelta

from mongo import udb, readSet

def timeFormat(time, mode='hour'):
  ntime = f'0{time}'
  if ntime == '0-1': return "23"
  elif ntime == '024' and mode == 'hour': return "00"
  elif len(ntime) == 2: return ntime
  else: return int(ntime)

def timeString(time, mode=''):
  if mode == 'profile' and time == 0: return 'Nenhum'
  hora = int(time // 60)
  if mode == 'simple':
    minutos = f'{int(time % 60)}m' # % 1 = Pegar a parte decimal da hora
  
    if minutos == '0m': minutos = ''
  
    if time % 60 == 0:
      minutos = ''
    if hora < 1:
      hora2 = ''
    else:
      hora2 = f'{hora}h'
  elif mode == 'simple2':
    minutos = f' e {int(time % 60)}min' # % 1 = Pegar a parte decimal da hora
  
    if minutos == ' e 0min': minutos = ''
  
    if time % 60 == 0:
      minutos = ''
    if hora < 1:
      hora2 = ''
    else:
      hora2 = f'{hora}h'          
  else:
    minutos = f' e {int(time % 60)} minuto' # % 1 = Pegar a parte decimal da hora
  
    if minutos == ' e 0 minuto': minutos = ''
    
    if time == 0: 
      return 'Nenhum'
    elif time % 60 > 1: minutos += "s"
  
    if time % 60 == 0:
      minutos = ''
    if hora < 1:
      hora2 = ''
      minutos = minutos.replace(" e ", "")
    else:
      hora2 = f'{hora} hora'
      if hora > 1: hora2 += 's'
        
  return f'{hora2}{minutos}'


def userTime(uid, mode=""):
	now = datetime.now() - timedelta(hours=3)
	usertime = udb.find_one({'uid': uid})['relat']['time']
	
	ustart = usertime - timedelta(hours=1)
	uend = usertime + timedelta(hours=1)

	if ustart <= now <= uend: return True
	else: return False
